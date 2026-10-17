"""QC per lesson video: streams, duration vs target, decode errors,
blackdetect, loudness (integrated/TP via loudnorm analysis), 7 QC frames
at ~8/22/36/50/64/78/92% of duration.
Usage: python3 qc_check.py [l09|l10|l11|l12|all]
"""
import json
import os
import re
import subprocess
import sys

COURSE = os.path.expanduser('~/workspace/udemy-skool/skool-course-3-mcp-architecture')
D = os.path.join(COURSE, 'sections', 's03')
VIDEOS = os.path.join(COURSE, 'videos')
QC = os.path.join(D, 'qc')
os.makedirs(QC, exist_ok=True)

TARGETS = {
    'l09': ('s03-l09-separation-of-concerns-and-server-anatomy-2026-10.mp4', 11.0),
    'l10': ('s03-l10-the-stdio-transport-local-simple-process-bound-2026-10.mp4', 11.0),
    'l11': ('s03-l11-streamable-http-remote-stateless-scalable-2026-10.mp4', 12.0),
    'l12': ('s03-l12-sessions-concurrency-and-a-full-round-trip-2026-10.mp4', 11.0),
}
PCTS = [0.08, 0.22, 0.36, 0.50, 0.64, 0.78, 0.92]


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def dur(p):
    return float(run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                      '-of', 'csv=p=0', p]).stdout.strip())


def check(key):
    fname, target_min = TARGETS[key]
    path = os.path.join(VIDEOS, fname)
    print('====', key, fname, '====')
    if not os.path.exists(path):
        print('MISSING')
        return
    size = os.path.getsize(path)
    d = dur(path)
    lo, hi = target_min * 0.9 * 60, target_min * 1.1 * 60
    ok = lo <= d <= hi
    print(f'bytes {size}')
    print(f'duration {d:.1f}s = {d/60:.2f} min (target {target_min} min, '
          f'window {lo/60:.2f}-{hi/60:.2f}) -> {"OK" if ok else "FAIL"} '
          f'(delta {(d - target_min*60)/(target_min*60)*100:+.1f}%)')

    r = run(['ffmpeg', '-v', 'error', '-threads', '2', '-i', path, '-f', 'null', '-'])
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

    r = run(['ffmpeg', '-hide_banner', '-threads', '2', '-i', path, '-vn', '-af',
             'loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json', '-f', 'null', '-'])
    m = re.search(r'\{\s*"input_i".*?\}', r.stderr, re.S)
    if m:
        j = json.loads(m.group(0))
        print(f'loudness: integrated {j["input_i"]} LUFS, true peak {j["input_tp"]} dBTP, LRA {j["input_lra"]}')
    else:
        print('loudness: MEASURE FAILED')

    for i, pct in enumerate(PCTS):
        t = d * pct
        out = os.path.join(QC, f'{key}-qcframe{i+1}-t{int(t)}s.png')
        run(['ffmpeg', '-y', '-v', 'error', '-ss', str(t), '-i', path,
             '-frames:v', '1', out])
        print(f'  frame {i+1} @ {t:.1f}s ({int(pct*100)}%) -> {os.path.basename(out)}')


if __name__ == '__main__':
    which = sys.argv[1] if len(sys.argv) > 1 else 'all'
    keys = [which] if which in TARGETS else list(TARGETS)
    for k in keys:
        check(k)
