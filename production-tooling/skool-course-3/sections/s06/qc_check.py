"""QC per lesson video (Course 3 s06): streams, decode, blackdetect,
loudness, duration, 7 QC frames at 8/22/36/50/64/78/92%."""
import json
import os
import re
import subprocess
import sys

COURSE = os.path.expanduser('~/workspace/udemy-skool/skool-course-3-mcp-architecture')
D = os.path.join(COURSE, 'sections', 's06')
VIDEOS = os.path.join(COURSE, 'videos')
QC = os.path.join(D, 'qc')
os.makedirs(QC, exist_ok=True)

TARGETS = {
    'l22': ('s06-l22-the-adapter-pattern-mcp-as-a-facade-2026-10.mp4', 11.0),
    'l23': ('s06-l23-wrapping-databases-and-file-stores-2026-10.mp4', 11.0),
    'l24': ('s06-l24-wrapping-rest-apis-and-saas-tools-2026-10.mp4', 11.0),
    'l25': ('s06-l25-upstream-authentication-and-safety-tiers-2026-10.mp4', 11.0),
    'l26': ('s06-l26-rate-limits-quotas-and-the-ticketing-scenario-2026-10.mp4', 11.0),
}
FRACS = [0.08, 0.22, 0.36, 0.50, 0.64, 0.78, 0.92]


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def dur(p):
    return float(run(['ffprobe', '-v', 'error', '-show_entries',
                      'format=duration', '-of', 'csv=p=0', p]).stdout.strip())


def loudness(p):
    r = run(['ffmpeg', '-hide_banner', '-i', p, '-af',
             'loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json',
             '-f', 'null', '-'])
    m = re.search(r'\{\s*"input_i".*?\}', r.stderr, re.S)
    if not m:
        return None
    j = json.loads(m.group(0))
    return float(j['input_i']), float(j['input_tp']), float(j['input_lra'])


for key in (sys.argv[1:] or list(TARGETS)):
    fname, target_min = TARGETS[key]
    path = os.path.join(VIDEOS, fname)
    print('====', fname, '====', flush=True)
    if not os.path.exists(path):
        print('MISSING')
        continue
    d = dur(path)
    lo, hi = target_min * 0.9 * 60, target_min * 1.1 * 60
    ok_dur = lo <= d <= hi
    print(f'duration {d:.1f}s = {d/60:.2f} min (target {target_min} min, '
          f'window {lo/60:.2f}-{hi/60:.2f}) -> {"OK" if ok_dur else "FAIL"}')
    print(f'bytes {os.path.getsize(path)}')

    r = run(['ffmpeg', '-v', 'error', '-threads', '2', '-i', path,
             '-f', 'null', '-'])
    dec = r.stderr.strip()
    print('decode:', 'ZERO ERRORS' if not dec else f'FAIL: {dec[:500]}')

    r = run(['ffmpeg', '-hide_banner', '-threads', '2', '-i', path, '-vf',
             'blackdetect=d=0.5:pix_th=0.10', '-an', '-f', 'null', '-'])
    blacks = [l for l in r.stderr.splitlines() if 'black_start' in l]
    print('blackdetect:', 'CLEAN' if not blacks else f'FAIL: {blacks}')

    sv = run(['ffprobe', '-v', 'error', '-select_streams', 'v:0',
              '-show_entries', 'stream=codec_name,width,height,avg_frame_rate',
              '-of', 'csv=p=0', path]).stdout.strip()
    sa = run(['ffprobe', '-v', 'error', '-select_streams', 'a:0',
              '-show_entries', 'stream=codec_name,sample_rate,channels',
              '-of', 'csv=p=0', path]).stdout.strip()
    print('video stream:', sv)
    print('audio stream:', sa)

    ln = loudness(path)
    if ln:
        print(f'loudness: {ln[0]:.2f} LUFS integrated, TP {ln[1]:.2f}, '
              f'LRA {ln[2]:.2f} -> '
              f'{"OK" if -17.5 <= ln[0] <= -14.5 and ln[1] <= -1.0 else "FAIL"}')
    else:
        print('loudness: MEASURE FAILED')

    meta = {}
    bj = os.path.join(D, f'{key}-build.json')
    if os.path.exists(bj):
        meta = json.load(open(bj))
    frames = []
    for i, fr in enumerate(FRACS):
        t = d * fr
        out = os.path.join(QC, f'{key}-qcframe{i+1}-t{int(t)}s.png')
        run(['ffmpeg', '-y', '-v', 'error', '-ss', str(t), '-i', path,
             '-frames:v', '1', out])
        slide_idx = None
        if meta.get('slide_intervals'):
            for si, (a, b) in enumerate(meta['slide_intervals']):
                if a <= t < b:
                    slide_idx = si
                    break
        seg_idx = None
        if meta.get('intervals'):
            for si, (a, b) in enumerate(meta['intervals']):
                if a <= t < b:
                    seg_idx = si + 1
                    break
            if seg_idx is None:
                # in a gap/hold: nearest preceding segment
                for si, (a, b) in enumerate(meta['intervals']):
                    if t >= b:
                        seg_idx = si + 1
        sname = meta['slides'][slide_idx] if slide_idx is not None and meta.get('slides') else '?'
        frames.append({'frame': i + 1, 't': round(t, 1), 'file': os.path.basename(out),
                       'slide_idx': slide_idx, 'slide': sname, 'seg': seg_idx})
        print(f'  frame {i+1} @ {t:.1f}s -> {os.path.basename(out)} '
              f'slide={sname} narr-seg={seg_idx}')
    result = {'lesson': key, 'file': fname, 'bytes': os.path.getsize(path),
              'duration': round(d, 2), 'duration_ok': ok_dur,
              'decode': 'ZERO ERRORS' if not dec else dec[:500],
              'blackdetect': 'CLEAN' if not blacks else str(blacks),
              'video_stream': sv, 'audio_stream': sa,
              'loudness': ln, 'frames': frames}
    with open(os.path.join(D, f'{key}-qc.json'), 'w') as f:
        json.dump(result, f, indent=1)
    print('QC json saved', flush=True)
