"""QC per lesson video (Course 3 s09): streams, decode, blackdetect,
loudness, duration vs target, 7 QC frames at ~8/22/36/50/64/78/92%.

Slide titles per lesson (verbatim from the script [Slide N] beats;
slide 1 is the title card, slides 2-9 are the content slides):
  l36: Title: Three ways to give a model tools |
       The shared question, three layers of answer |
       Way one: native function calling, inside the provider's A P I |
       Way two: M C P, the contract moved into an open protocol |
       Way three: bespoke A P I integration, no tool protocol at all |
       The spectrum, stated plainly |
       Why this section refuses to declare a winner |
       What to watch for in the comparison |
       Hands-on and next: the honest comparison
  l37: Title: Head-to-head — the honest comparison |
       Axis one and two: portability and maintenance |
       Axis three and four: ecosystem and latency |
       Axis five: control — and what nobody gives you for free |
       The decision framework, questions one to three |
       The decision framework, questions four to six |
       The worked example: one product, three answers |
       Two observations before we build hybrids |
       Hands-on and next: hybrids and migrating to M C P
  l38: Title: Hybrids and migrating to M C P |
       Hybrid pattern one: M C P for the platform, native at the edges |
       Hybrid pattern two: M C P servers wrapping bespoke cores |
       Hybrid pattern three: bespoke orchestration over M C P tools |
       Migration phase one and two: inventory, then wrap — don't rewrite |
       Migration phase three and four: cut over per tool, then govern |
       Order, and the two pitfalls that ruin migrations |
       Section close: choose per integration, record the reasoning |
       Hands-on and next: testing M C P servers like A P Is
"""
import json
import os
import re
import subprocess
import sys

COURSE = os.path.expanduser('~/workspace/udemy-skool/skool-course-3-mcp-architecture')
D = os.path.join(COURSE, 'sections', 's09')
VIDEOS = os.path.join(COURSE, 'videos')
QC = os.path.join(D, 'qc')
os.makedirs(QC, exist_ok=True)

TARGETS = {
    'l36': ('s09-l36-three-ways-to-give-a-model-tools-2026-10.mp4', 11.0),
    'l37': ('s09-l37-head-to-head-the-honest-comparison-2026-10.mp4', 12.0),
    'l38': ('s09-l38-hybrids-and-migrating-to-mcp-2026-10.mp4', 11.0),
}


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def dur(p):
    return float(run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                      '-of', 'csv=p=0', p]).stdout.strip())


def check(key):
    fname, target_min = TARGETS[key]
    path = os.path.join(VIDEOS, fname)
    print('====', fname, '====', flush=True)
    if not os.path.exists(path):
        print('MISSING')
        return
    print('bytes:', os.path.getsize(path))
    d = dur(path)
    lo, hi = target_min * 0.9 * 60, target_min * 1.1 * 60
    print(f'duration {d:.1f}s = {d/60:.2f} min (target {target_min} min, '
          f'window {lo:.0f}-{hi:.0f}s) -> {"OK" if lo <= d <= hi else "FAIL"}')

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

    r = run(['ffmpeg', '-hide_banner', '-threads', '2', '-i', path, '-af',
             'loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json', '-vn', '-f', 'null', '-'])
    m = re.search(r'\{\s*"input_i".*?\}', r.stderr, re.S)
    if m:
        j = json.loads(m.group(0))
        print(f"loudness: integrated {j['input_i']} LUFS, true peak {j['input_tp']} dBTP")
    else:
        print('loudness: MEASURE FAILED')

    for i in range(7):
        t = d * [0.08, 0.22, 0.36, 0.50, 0.64, 0.78, 0.92][i]
        out = os.path.join(QC, f'{key}-qcframe{i+1}-t{int(t)}s.png')
        run(['ffmpeg', '-y', '-v', 'error', '-ss', str(t), '-i', path,
             '-frames:v', '1', out])
        print(f'  frame {i+1} @ {t:.1f}s -> {os.path.basename(out)}')


if __name__ == '__main__':
    keys = [sys.argv[1]] if len(sys.argv) > 1 else list(TARGETS)
    for k in keys:
        check(k)
