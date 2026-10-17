"""Finish L32 after two interrupted full builds (VM reboot + dead resume).

Resume precedent: Course 2 s00 MANIFEST (verified vclips reused, video-only
rebuilt) + Course 3 s04 L13 (clips verified frame-duration-exact, reused).
Verifies every existing vclip (duration vs plan, full decode); re-renders
only clips that fail, with the identical ffmpeg command from assemble.py;
then concat + mux with the identical commands and the existing verified
narration-norm. No recipe parameter changes.
"""
import json
import os
import subprocess
import sys

COURSE = os.path.expanduser('~/workspace/udemy-skool/skool-course-3-mcp-architecture')
D = os.path.join(COURSE, 'sections', 's08')
S = os.path.join(D, 'slides')
VIDEOS = os.path.join(COURSE, 'videos')
FPS = 30
TITLE_HOLD, GAP, CLOSING = 4.0, 0.5, 3.0
SLIDES = ['l32-slide0-title.png', 'l32-slide1-small.png', 'l32-slide2-catalog.png',
          'l32-slide3-problems.png', 'l32-slide4-static.png', 'l32-slide5-registry.png',
          'l32-slide6-internal.png', 'l32-slide7-rule.png', 'l32-slide8-next.png']
OUT = os.path.join(VIDEOS, 's08-l32-why-one-agent-needs-many-servers-discovery-2026-10.mp4')


def run(cmd, label=''):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print('FAILED', label or ' '.join(cmd[:8]), flush=True)
        print(r.stderr[-3000:], flush=True)
        raise SystemExit(1)
    return r


def dur(p):
    out = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                          '-of', 'csv=p=0', p], capture_output=True, text=True).stdout.strip()
    return float(out) if out else -1


def decode_ok(p):
    r = subprocess.run(['ffmpeg', '-v', 'error', '-threads', '2', '-i', p, '-f', 'null', '-'],
                       capture_output=True, text=True)
    return r.returncode == 0 and not r.stderr.strip()


segs = []
for i in range(1, 10):
    segs.append(dur(os.path.join(D, f'l32-seg{i}.mp3')))
print('seg durations:', [round(x, 2) for x in segs], flush=True)

durations = []
for j, d in enumerate(segs):
    if j == 0:
        durations.append(TITLE_HOLD + d + GAP)
    elif j < len(segs) - 1:
        durations.append(d + GAP)
    else:
        durations.append(d + CLOSING)
print('slide durations:', [round(x, 2) for x in durations], flush=True)

norm = os.path.join(D, 'l32-narration-norm.m4a')
print('narration-norm:', round(dur(norm), 2), flush=True)

clips = []
for k, (img, dsec) in enumerate(zip(SLIDES, durations)):
    frames = max(2, round(dsec * FPS))
    out = os.path.join(D, f'l32-vclip{k:02d}.mp4')
    ok = False
    if os.path.exists(out) and os.path.getsize(out) > 0:
        cd = dur(out)
        if abs(cd - frames / FPS) <= 0.05 and decode_ok(out):
            print(f'clip {k}: REUSE {cd:.2f}s (plan {frames / FPS:.2f}s)', flush=True)
            ok = True
        else:
            print(f'clip {k}: BAD existing ({cd:.2f}s vs plan {frames / FPS:.2f}s) -> re-render', flush=True)
    if not ok:
        run(['ffmpeg', '-y', '-threads', '2', '-loop', '1', '-framerate', str(FPS),
             '-i', os.path.join(S, img), '-vf', 'scale=1920:1080,format=yuv420p',
             '-frames:v', str(frames), '-c:v', 'libx264', '-preset', 'veryfast',
             '-crf', '19', out], f'clip {k}')
        print(f'clip {k}: rendered {dur(out):.2f}s', flush=True)
    clips.append(out)

vconcat = os.path.join(D, 'l32-vconcat.txt')
with open(vconcat, 'w') as f:
    for c in clips:
        f.write(f"file '{c}'\n")
vonly = os.path.join(D, 'l32-video-only.mp4')
if os.path.exists(vonly):
    os.remove(vonly)
run(['ffmpeg', '-y', '-threads', '2', '-f', 'concat', '-safe', '0', '-i', vconcat,
     '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '19', '-pix_fmt', 'yuv420p', vonly],
    'concat video')
print('video-only:', round(dur(vonly), 2), flush=True)

run(['ffmpeg', '-y', '-threads', '2', '-i', vonly, '-i', norm, '-c:v', 'copy',
     '-c:a', 'aac', '-b:a', '192k', '-ar', '44100', '-ac', '2', '-shortest',
     '-movflags', '+faststart', OUT], 'mux')
final = dur(OUT)
print('FINAL:', round(final, 2), 's =', round(final / 60, 2), 'min', flush=True)
print('bytes:', os.path.getsize(OUT), flush=True)
meta = {'final': round(final, 3), 'slide_durations': [round(x, 2) for x in durations],
        'holds': [TITLE_HOLD, GAP, CLOSING], 'out': OUT, 'bytes': os.path.getsize(OUT),
        'resume': 'verified clips reused; bad clips re-rendered; video-only + mux rebuilt'}
with open(os.path.join(D, 'l32-finish-meta.json'), 'w') as f:
    json.dump(meta, f, indent=1)
print('DONE', flush=True)
