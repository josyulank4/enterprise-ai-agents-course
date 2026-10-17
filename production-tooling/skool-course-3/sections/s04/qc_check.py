"""QC per Course 3 s04 lesson video: streams, decode, blackdetect,
loudness, duration gate, 7 QC frames + slide/narration sync from build.json.
Usage: python3 qc_check.py l13 [l14 ...]
"""
import json
import os
import re
import subprocess
import sys

COURSE = os.path.expanduser(
    '~/workspace/udemy-skool/skool-course-3-mcp-architecture')
D = os.path.join(COURSE, 'sections', 's04')
VIDEOS = os.path.join(COURSE, 'videos')
QC = os.path.join(D, 'qc')
os.makedirs(QC, exist_ok=True)
PCTS = [0.08, 0.22, 0.36, 0.50, 0.64, 0.78, 0.92]
SLIDES = {
    'l13': ['Title: Building Your First MCP Server',
            'Four Responsibilities', 'Identity Is Not Decoration',
            'Project Setup', 'Learn the Steps', 'Transport Binding',
            'Request Handling', 'Hands-On: Scaffold and Ping',
            'Next: Metadata and Capability Declaration'],
    'l14': ['Title: The First Thing Every Client Judges',
            'A Name a Tired Engineer Can Use', 'Written for Two Audiences',
            'The Instructions Field', 'Capability Declaration',
            'The Phantom Capability', 'Two Versions, Two Jobs',
            'Logging and Completions', 'Hands-On: Declare, Then Verify',
            'Next: Your First Tool'],
    'l15': ['Title: A Tool Is the Unit of Action',
            'The Name Reads Like a Command', 'The Description',
            'The Schema, Line by Line', 'Schema as User Interface',
            'Validation: Two Error Paths', 'Annotations',
            'Keep the Handler Boring', 'Hands-On: The Word-Count Tool',
            'Next: The Initialization Handshake, Live'],
    'l16': ['Title: Two Strangers Agreeing on a Language',
            'Message One: The Client Opens', 'Message Two: The Server Answers',
            'Message Three: Initialized', 'Version Negotiation',
            'Capability Negotiation', 'Reading Real Traces',
            'What the Wire Looks Like', 'Hands-On: Negotiate Twice',
            'Next: Testing with the Inspector'],
    'l17': ['Title: Test It the Way Its Consumers Will',
            'The Inspector', 'The Testing Loop, Step by Step',
            'Logging Without Breaking the Wire', 'Mistakes One and Two',
            'Mistakes Three and Four', 'Mistakes Five and Six',
            'Debug the Conversation', 'Hands-On: The Mistake Hunt',
            'Next: Three Control Models and Resources in Depth'],
}


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def dur(p):
    return float(run(['ffprobe', '-v', 'error', '-show_entries',
                      'format=duration', '-of', 'csv=p=0', p]).stdout.strip())


for key in sys.argv[1:]:
    meta = json.load(open(os.path.join(D, f'{key}-build.json')))
    path = os.path.join(VIDEOS, meta['file'])
    print('====', meta['file'], '====', flush=True)
    res = {'lesson': key, 'file': meta['file']}
    if not os.path.exists(path):
        print('MISSING')
        continue
    res['bytes'] = os.path.getsize(path)
    d = dur(path)
    res['duration'] = round(d, 2)
    lo, hi = meta['window']
    ok = lo <= d <= hi
    res['duration_ok'] = ok
    print(f'duration {d:.1f}s = {d/60:.2f} min (target {meta["target_min"]} '
          f'min, window {lo/60:.2f}-{hi/60:.2f}) -> {"OK" if ok else "FAIL"}')

    sv = run(['ffprobe', '-v', 'error', '-select_streams', 'v:0',
              '-show_entries', 'stream=codec_name,width,height,avg_frame_rate',
              '-of', 'csv=p=0', path]).stdout.strip()
    sa = run(['ffprobe', '-v', 'error', '-select_streams', 'a:0',
              '-show_entries', 'stream=codec_name,sample_rate,channels',
              '-of', 'csv=p=0', path]).stdout.strip()
    res['video_stream'] = sv
    res['audio_stream'] = sa
    print('video stream:', sv)
    print('audio stream:', sa)

    r = run(['ffmpeg', '-v', 'error', '-threads', '2', '-i', path,
             '-f', 'null', '-'])
    dec = r.stderr.strip()
    res['decode_ok'] = not dec
    print('decode:', 'ZERO ERRORS' if not dec else f'FAIL: {dec[:400]}',
          flush=True)

    r = run(['ffmpeg', '-hide_banner', '-threads', '2', '-i', path, '-vf',
             'blackdetect=d=0.5:pix_th=0.10', '-an', '-f', 'null', '-'])
    blacks = [l for l in r.stderr.splitlines() if 'black_start' in l]
    res['blackdetect_clean'] = not blacks
    print('blackdetect:', 'CLEAN' if not blacks else f'FAIL: {blacks}',
          flush=True)

    r = run(['ffmpeg', '-hide_banner', '-threads', '2', '-i', path, '-vn',
             '-af', 'loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json',
             '-f', 'null', '-'])
    mi = re.search(r'"input_i"\s*:\s*"([-\d.]+)"', r.stderr)
    mt = re.search(r'"input_tp"\s*:\s*"([-\d.]+)"', r.stderr)
    if mi and mt:
        res['loudness_i'] = float(mi.group(1))
        res['loudness_tp'] = float(mt.group(1))
        print(f"loudness: I={mi.group(1)} LUFS TP={mt.group(1)}", flush=True)
    else:
        print('loudness parse failed', flush=True)

    # frames + sync
    sdurs = meta['slide_durations']
    bounds = []
    acc = 0.0
    for sd in sdurs:
        bounds.append((acc, acc + sd))
        acc += sd
    frames = []
    for i, pc in enumerate(PCTS):
        t = d * pc
        out = os.path.join(QC, f'{key}-qcframe{i+1}-t{int(t)}s.png')
        run(['ffmpeg', '-y', '-v', 'error', '-threads', '2', '-ss', str(t),
             '-i', path, '-frames:v', '1', out])
        slide_idx = next(j for j, (a, b) in enumerate(bounds) if a <= t < b)
        seg_idx = None
        where = 'silence/gap'
        for j, (a, b) in enumerate(meta['intervals']):
            if a <= t < b:
                seg_idx = j
                where = f'seg{j+1}'
                break
        sync = (seg_idx is not None and slide_idx == seg_idx)
        frames.append({'n': i + 1, 't': round(t, 1),
                       'file': os.path.basename(out),
                       'slide': SLIDES[key][slide_idx],
                       'slide_idx': slide_idx + 1,
                       'narrating': where, 'sync': sync})
        print(f'  frame {i+1} @ {t:.1f}s slide{slide_idx+1} '
              f'"{SLIDES[key][slide_idx]}" narrating {where} '
              f'-> {"SYNC" if sync else "CHECK"}', flush=True)
    res['frames'] = frames
    with open(os.path.join(D, f'{key}-qc.json'), 'w') as f:
        json.dump(res, f, indent=1)
    print('QC json saved', flush=True)
