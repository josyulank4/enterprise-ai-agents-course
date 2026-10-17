"""Finish L33: verify existing vclips vs plan (duration + full decode),
re-render only missing/bad clips with the identical assemble.py ffmpeg
command, then concat + mux (identical commands) using the existing
verified l33-narration-norm.m4a. Resume precedent: Course 2 s00 / s04 L13.
"""
import json
import os
import subprocess

COURSE = os.path.expanduser('~/workspace/udemy-skool/skool-course-3-mcp-architecture')
D = os.path.join(COURSE, 'sections', 's08')
S = os.path.join(D, 'slides')
VIDEOS = os.path.join(COURSE, 'videos')
FPS = 30
TITLE_HOLD, GAP, CLOSING = 4.0, 0.5, 3.0
SLIDES = ['l33-slide0-title.png', 'l33-slide1-collision.png', 'l33-slide2-prefix.png',
          'l33-slide3-policy.png', 'l33-slide4-params.png', 'l33-slide5-routing.png',
          'l33-slide6-overlap.png', 'l33-slide7-failover.png', 'l33-slide8-next.png']
OUT = os.path.join(VIDEOS, 's08-l33-namespacing-collisions-and-routing-2026-10.mp4')
KEY = 'l33'


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


segs = [dur(os.path.join(D, f'{KEY}-seg{i}.mp3')) for i in range(1, 10)]
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
norm = os.path.join(D, f'{KEY}-narration-norm.m4a')
print('narration-norm:', round(dur(norm), 2), flush=True)

clips = []
reused, rendered = [], []
for k, (img, dsec) in enumerate(zip(SLIDES, durations)):
    frames = max(2, round(dsec * FPS))
    out = os.path.join(D, f'{KEY}-vclip{k:02d}.mp4')
    ok = False
    if os.path.exists(out) and os.path.getsize(out) > 0:
        cd = dur(out)
        if abs(cd - frames / FPS) <= 0.05 and decode_ok(out):
            print(f'clip {k}: REUSE {cd:.2f}s (plan {frames / FPS:.2f}s)', flush=True)
            ok = True
            reused.append(k)
        else:
            print(f'clip {k}: BAD existing ({cd:.2f}s vs plan {frames / FPS:.2f}s) -> re-render', flush=True)
    if not ok:
        run(['ffmpeg', '-y', '-threads', '2', '-loop', '1', '-framerate', str(FPS),
             '-i', os.path.join(S, img), '-vf', 'scale=1920:1080,format=yuv420p',
             '-frames:v', str(frames), '-c:v', 'libx264', '-preset', 'veryfast',
             '-crf', '19', out], f'clip {k}')
        print(f'clip {k}: rendered {dur(out):.2f}s', flush=True)
        rendered.append(k)
    clips.append(out)

vconcat = os.path.join(D, f'{KEY}-vconcat.txt')
with open(vconcat, 'w') as f:
    for c in clips:
        f.write(f"file '{c}'\n")
vonly = os.path.join(D, f'{KEY}-video-only.mp4')
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
stats = []
for i, d in enumerate(segs, 1):
    txt = open(os.path.join(D, f'{KEY}-seg{i}.txt')).read()
    w = len(txt.split())
    stats.append({'seg': i, 'words': w, 'duration': round(d, 2), 'wpm': round(w / d * 60, 1)})
meta = {'final': round(final, 3), 'stats': stats, 'regen': [],
        'slide_durations': [round(x, 2) for x in durations],
        'holds': [TITLE_HOLD, GAP, CLOSING], 'out': OUT,
        'bytes': os.path.getsize(OUT), 'clips_reused': reused, 'clips_rendered': rendered}
with open(os.path.join(D, f'{KEY}-build-meta.json'), 'w') as f:
    json.dump(meta, f, indent=1)
print('DONE', flush=True)
