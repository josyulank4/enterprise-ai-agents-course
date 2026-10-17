"""A1 recursive step: split one failing sub-segment at sentence boundaries
into per-sentence parts (VERBATIM), synth + QC each, concat with 0.3s
silence, and replace the sub-segment mp3 (sidecar = original sub text).

Usage: python3 a1_fix_sub.py l27 5 3
"""
import os
import re
import subprocess
import sys

D = os.path.dirname(os.path.abspath(__file__))
VOICE = 'avocado_v2:MAI_01'
SPEED = '77'


def dur(p):
    return float(subprocess.run(
        ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
         '-of', 'csv=p=0', p], capture_output=True, text=True).stdout.strip())


def run(cmd, label=''):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print('FAILED', label)
        print(r.stderr[-2000:])
        raise SystemExit(1)
    return r


def tts(text, out):
    tmp = out + '.txt'
    with open(tmp, 'w') as f:
        f.write(text)
    with open(tmp) as fin:
        r = subprocess.run(
            ['/opt/hatch/bin/tts', 'speak', '--voice', VOICE, '--speed', SPEED,
             '--output', out, '--text-stdin'],
            stdin=fin, capture_output=True, text=True)
    if r.returncode != 0 or not os.path.exists(out) or os.path.getsize(out) == 0:
        print('TTS FAILED for', out)
        raise SystemExit(1)


key, segn, subn = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
sub_mp3 = os.path.join(D, f'{key}-seg{segn}-sub{subn}.mp3')
text = open(sub_mp3 + '.txt').read()
sents = [p for p in re.split(r'(?<=\.)\s+', text.strip()) if p]
assert ' '.join(sents) == text, 'verbatim join failed'
print(f'sub{subn}: {len(text.split())}w -> {len(sents)} sentence parts')
failed = os.path.join(D, f'{key}-seg{segn}-sub{subn}-fulltake-failed.mp3')
if os.path.exists(sub_mp3) and not os.path.exists(failed):
    os.rename(sub_mp3, failed)
    print('failed sub take preserved:', os.path.basename(failed),
          f'{dur(failed):.1f}s')
subsil = os.path.join(D, f'{key}-seg{segn}-subsil.mp3')
parts = []
for i, st in enumerate(sents, 1):
    out = os.path.join(D, f'{key}-seg{segn}-sub{subn}-part{i}.mp3')
    w = len(st.split())
    expected = w / 135.0 * 60.0
    chosen = None
    for attempt in range(1, 4):
        tts(st, out)
        d = dur(out)
        wpm = w / d * 60 if d > 0 else 0
        ok = d >= expected * 0.5 and 75 <= wpm <= 210
        print(f'  part{i}: {w}w -> {d:.1f}s ({wpm:.0f} wpm) attempt '
              f'{attempt} {"OK" if ok else "BAD"}', flush=True)
        if ok:
            chosen = d
            break
    if chosen is None:
        print(f'part{i} FAILED — cannot split below sentence level')
        raise SystemExit(2)
    parts.append(out)
concat = os.path.join(D, f'{key}-seg{segn}-sub{subn}-partconcat.txt')
with open(concat, 'w') as f:
    for j, mp3 in enumerate(parts):
        f.write(f"file '{mp3}'\n")
        if j < len(parts) - 1:
            f.write(f"file '{subsil}'\n")
tmp = os.path.join(D, f'{key}-seg{segn}-sub{subn}-joined.mp3')
run(['ffmpeg', '-y', '-threads', '2', '-f', 'concat', '-safe', '0', '-i',
     concat, '-c:a', 'libmp3lame', '-b:a', '128k', tmp], 'part concat')
os.replace(tmp, sub_mp3)
with open(sub_mp3 + '.txt', 'w') as f:
    f.write(text)
d = dur(sub_mp3)
w = len(text.split())
print(f'sub{subn} rebuilt: {d:.1f}s, {w/d*60:.0f} wpm -> '
      f'{"OK" if 75 <= w/d*60 <= 210 else "BAD"}')
print('A1_SUB_DONE')
