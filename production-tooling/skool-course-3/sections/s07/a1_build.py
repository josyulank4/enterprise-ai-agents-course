"""A1 adaptation builder (PRODUCTION-SPEC Authorized adaptation A1).

Splits a deterministically slow segment's narration at sentence boundaries
into sub-segments (VERBATIM text), synthesizes each via the identical route
(Aria avocado_v2:MAI_01, speed 77, /opt/hatch/bin/tts), QCs each with the
same gates (>=50% expected, 75-210 wpm), concatenates with 0.3s silence
between sub-segments, and writes the result as the segment's mp3 plus the
sidecar .txt (full original text) so assemble.py reuses it.

Usage: python3 a1_build.py l27 5 [max_words_per_sub]
"""
import os
import re
import subprocess
import sys

D = os.path.dirname(os.path.abspath(__file__))
VOICE = 'avocado_v2:MAI_01'
SPEED = '77'


def dur(p):
    out = subprocess.run(
        ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
         '-of', 'csv=p=0', p], capture_output=True, text=True).stdout.strip()
    return float(out)


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
        print((r.stderr or r.stdout)[-2000:])
        raise SystemExit(1)


def split_sentences(text):
    # split after '. ' (period + space); decimals like 2.1 are safe
    parts = re.split(r'(?<=\.)\s+', text.strip())
    return [p for p in parts if p]


def main():
    key, segn = sys.argv[1], int(sys.argv[2])
    maxw = int(sys.argv[3]) if len(sys.argv) > 3 else 60
    seg_txt = os.path.join(D, f'{key}-seg{segn}.txt')
    text = open(seg_txt).read()
    words_total = len(text.split())
    sents = split_sentences(text)
    print(f'{key} seg{segn}: {words_total} words, {len(sents)} sentences')
    # greedy grouping
    groups, cur, curw = [], [], 0
    for s in sents:
        w = len(s.split())
        if cur and curw + w > maxw:
            groups.append(cur)
            cur, curw = [], 0
        cur.append(s)
        curw += w
    if cur:
        groups.append(cur)
    sub_texts = [' '.join(g) for g in groups]
    joined = ' '.join(sub_texts)
    assert joined == text, 'VERBATIM CHECK FAILED: split/join != original'
    print(f'{len(sub_texts)} sub-segments, verbatim join verified')

    # preserve failed full take
    seg_mp3 = os.path.join(D, f'{key}-seg{segn}.mp3')
    failed = os.path.join(D, f'{key}-seg{segn}-fulltake-failed.mp3')
    if os.path.exists(seg_mp3) and not os.path.exists(failed):
        os.rename(seg_mp3, failed)
        print('failed full take preserved:', os.path.basename(failed),
              f'{dur(failed):.1f}s')

    subsil = os.path.join(D, f'{key}-seg{segn}-subsil.mp3')
    run(['ffmpeg', '-y', '-threads', '2', '-f', 'lavfi', '-i',
         'anullsrc=r=44100:cl=stereo:d=0.3',
         '-c:a', 'libmp3lame', '-b:a', '128k', subsil], 'subsil')

    stats = []
    sub_mp3s = []
    for i, st in enumerate(sub_texts, 1):
        out = os.path.join(D, f'{key}-seg{segn}-sub{i}.mp3')
        w = len(st.split())
        expected = w / 135.0 * 60.0
        chosen = None
        if os.path.exists(out) and os.path.getsize(out) > 0 \
                and os.path.exists(out + '.txt') \
                and open(out + '.txt').read() == st:
            d0 = dur(out)
            wpm0 = w / d0 * 60 if d0 > 0 else 0
            if d0 >= expected * 0.5 and 75 <= wpm0 <= 210:
                print(f'  sub{i}: reuse {d0:.1f}s ({wpm0:.0f} wpm)')
                chosen = d0
        for attempt in range(1, 4):
            if chosen is not None:
                break
            tts(st, out)
            d = dur(out)
            wpm = w / d * 60 if d > 0 else 0
            ok = d >= expected * 0.5 and 75 <= wpm <= 210
            print(f'  sub{i}: {w}w -> {d:.1f}s ({wpm:.0f} wpm), attempt '
                  f'{attempt}, {"OK" if ok else "BAD"}', flush=True)
            if ok:
                chosen = d
                break
        if chosen is None:
            print(f'sub{i} FAILED QC after 3 attempts — A1 needs deeper split')
            raise SystemExit(2)
        sub_mp3s.append(out)
        stats.append((i, w, round(chosen, 2), round(w / chosen * 60)))

    concat = os.path.join(D, f'{key}-seg{segn}-subconcat.txt')
    with open(concat, 'w') as f:
        for j, mp3 in enumerate(sub_mp3s):
            f.write(f"file '{mp3}'\n")
            if j < len(sub_mp3s) - 1:
                f.write(f"file '{subsil}'\n")
    tmp_mp3 = os.path.join(D, f'{key}-seg{segn}-joined.mp3')
    run(['ffmpeg', '-y', '-threads', '2', '-f', 'concat', '-safe', '0',
         '-i', concat, '-c:a', 'libmp3lame', '-b:a', '128k', tmp_mp3],
        'sub concat')
    os.replace(tmp_mp3, seg_mp3)
    with open(seg_mp3 + '.txt', 'w') as f:
        f.write(text)
    d = dur(seg_mp3)
    wpm = words_total / d * 60
    print(f'COMBINED seg{segn}: {d:.1f}s, {wpm:.0f} wpm '
          f'(words {words_total}) -> {"OK" if 75 <= wpm <= 210 else "BAD"}')
    for i, w, dd, ww in stats:
        print(f'  sub{i}: {w}w / {dd}s / {ww} wpm')
    print('A1_DONE')


if __name__ == '__main__':
    main()
