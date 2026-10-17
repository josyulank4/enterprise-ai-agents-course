"""QC per Course 3 s05 lesson video: streams, decode, blackdetect,
loudness, duration gate, 7 QC frames + slide/narration sync from build.json.
Usage: python3 qc_check.py l18 [l19 ...]
Frames at ~8/22/36/50/64/78/92% per PRODUCTION-SPEC.
"""
import json
import os
import re
import subprocess
import sys

COURSE = os.path.expanduser(
    '~/workspace/udemy-skool/skool-course-3-mcp-architecture')
D = os.path.join(COURSE, 'sections', 's05')
VIDEOS = os.path.join(COURSE, 'videos')
QC = os.path.join(D, 'qc')
os.makedirs(QC, exist_ok=True)
PCTS = [0.08, 0.22, 0.36, 0.50, 0.64, 0.78, 0.92]
SLIDES = {
    'l18': ['Title: Three Control Models and Resources in Depth',
            'Who Decides?', 'The Category Error', 'Resources: Stable URIs',
            'Direct vs Templates', 'Subscriptions',
            'Resources Never Act', 'Resource or Tool?',
            'Hands-On: Five Resources', 'Next: Tools in Depth'],
    'l19': ['Title: Tools in Depth',
            'Granularity: One Job', 'Schemas at Scale', 'Output Design',
            'Errors Are Interface', 'Annotations and Honesty',
            'Naming Decides Calls', 'Hands-On: Refactor It',
            'Next: Prompts in Depth'],
    'l20': ['Title: Prompts in Depth',
            "The Domain's Rituals", 'Template Design',
            'Opinionated by Design', 'Prompts vs Tool Text',
            'A Prompt That Is a Tool', 'Versioning and Care',
            'Hands-On: Triage Prompt', 'Next: Roots, Sampling, Pagination'],
    'l21': ['Title: Roots, Sampling, Pagination and Clean Boundaries',
            'Roots: Sense of Place', "Sampling: Borrowed Brain",
            "Sampling's Risks", 'Pagination', 'Completion',
            'Boundaries One and Two', 'Boundaries Three and Four',
            'Hands-On: Boundary Review', 'Next: The Adapter Pattern'],
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
