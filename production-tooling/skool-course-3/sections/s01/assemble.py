"""Assemble Skool Course 3, Section 1: slides + Aria narration -> 1920x1080 MP4s.

Replicates Course 2 s00 assemble.py exactly, with Course 3 spec slide timing:
title card = title hold + seg1; content slide i = seg_i + gap (last + closing).
Usage: python3 assemble.py l01 [title_hold gap closing_hold]
Holds default to standard 4.0 / 0.5 / 3.0 and may be overridden per lesson
for the documented duration gate (holds only, never voice/speed/text).
"""
import json
import os
import re
import subprocess
import sys

COURSE = os.path.expanduser('~/workspace/udemy-skool/skool-course-3-mcp-architecture')
D = os.path.join(COURSE, 'sections', 's01')
S = os.path.join(D, 'slides')
VIDEOS = os.path.join(COURSE, 'videos')
VOICE = 'avocado_v2:MAI_01'
SPEED = '77'
FPS = 30

LESSONS = {
    'l01': {
        'script': os.path.join(COURSE, 'scripts', 's01-l01.md'),
        'target': 7.0,
        'slides': ['l01-slide0-title.png', 'l01-slide1-priya.png',
                   'l01-slide2-paralyzed.png', 'l01-slide3-standard.png',
                   'l01-slide4-mcp.png', 'l01-slide5-course-map.png',
                   'l01-slide6-honest-bar.png', 'l01-slide7-audience.png',
                   'l01-slide8-next.png'],
        'out': os.path.join(VIDEOS, 's01-l01-welcome-the-protocol-that-gives-agents-hands-2026-10.mp4'),
    },
    'l02': {
        'script': os.path.join(COURSE, 'scripts', 's01-l02.md'),
        'target': 7.0,
        'slides': ['l02-slide0-title.png', 'l02-slide1-sections.png',
                   'l02-slide2-journey.png', 'l02-slide3-runnable.png',
                   'l02-slide4-repository.png', 'l02-slide5-plain-python.png',
                   'l02-slide6-study.png', 'l02-slide7-lasts.png',
                   'l02-slide8-voice.png'],
        'out': os.path.join(VIDEOS, 's01-l02-how-to-use-this-course-and-the-code-repository-2026-10.mp4'),
    },
    'l03': {
        'script': os.path.join(COURSE, 'scripts', 's01-l03.md'),
        'target': 11.0,
        'slides': ['l03-slide0-title.png', 'l03-slide1-model.png',
                   'l03-slide2-performance.png', 'l03-slide3-boundary.png',
                   'l03-slide4-zero.png', 'l03-slide5-agentic.png',
                   'l03-slide6-request.png', 'l03-slide7-capability.png',
                   'l03-slide8-trust.png', 'l03-slide9-audit.png'],
        'out': os.path.join(VIDEOS, 's01-l03-the-brilliant-prisoner-what-models-can-and-2026-10.mp4'),
    },
    'l04': {
        'script': os.path.join(COURSE, 'scripts', 's01-l04.md'),
        'target': 11.0,
        'slides': ['l04-slide0-title.png', 'l04-slide1-patchwork.png',
                   'l04-slide2-fragmentation.png', 'l04-slide3-mirror.png',
                   'l04-slide4-arithmetic.png', 'l04-slide5-exploding.png',
                   'l04-slide6-collapse.png', 'l04-slide7-case.png',
                   'l04-slide8-unlocks.png', 'l04-slide9-ecosystem.png'],
        'out': os.path.join(VIDEOS, 's01-l04-the-nxm-problem-why-a-standard-had-to-exist-2026-10.mp4'),
    },
}


def run(cmd, label=''):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print('FAILED', label or ' '.join(cmd[:8]))
        print(r.stderr[-3000:])
        raise SystemExit(1)
    return r


def dur(p):
    out = subprocess.run(
        ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
         '-of', 'csv=p=0', p], capture_output=True, text=True).stdout.strip()
    return float(out)


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


def split_script(path):
    raw = open(path).read()
    parts = re.split(r'\*\*\[Slide \d+ [^\]]*\]\*\*', raw)
    # parts[0] is header metadata before Slide 1 (not narration)
    segs = []
    for p in parts[1:]:
        seg = p.strip()
        seg = seg.replace('**', '')
        # collapse internal newlines within/between paragraphs to spaces? Keep
        # paragraph breaks as blank lines like Course 2 txt scripts.
        seg = re.sub(r'\n{3,}', '\n\n', seg)
        segs.append(seg)
    return segs


def build(key, title_hold=4.0, gap=0.5, closing_hold=3.0):
    cfg = LESSONS[key]
    print(f'==== {key} holds title={title_hold} gap={gap} closing={closing_hold} ====', flush=True)
    os.makedirs(S, exist_ok=True)
    os.makedirs(VIDEOS, exist_ok=True)
    missing = [f for f in cfg['slides'] if not os.path.exists(os.path.join(S, f))]
    if missing:
        print('missing slides, building:', missing)
        run([sys.executable, os.path.join(D, 'build_slides.py')], 'build slides')

    segs = split_script(cfg['script'])
    assert len(segs) == len(cfg['slides']), f'{len(segs)} segs vs {len(cfg["slides"])} slides'
    print(f'{len(segs)} narration segments', flush=True)
    seg_mp3s = []
    regen = []
    stats = []
    for i, seg in enumerate(segs, 1):
        txt_path = os.path.join(D, f'{key}-seg{i}.txt')
        mp3 = os.path.join(D, f'{key}-seg{i}.mp3')
        with open(txt_path, 'w') as f:
            f.write(seg)
        words = len(seg.split())
        expected = words / 135.0 * 60.0
        chosen = None
        if os.path.exists(mp3) and os.path.getsize(mp3) > 0:
            d0 = dur(mp3)
            wpm0 = words / d0 * 60 if d0 > 0 else 0
            if d0 >= expected * 0.5 and 75 <= wpm0 <= 210:
                print(f'  seg{i}: reuse existing {d0:.1f}s ({wpm0:.0f} wpm)', flush=True)
                chosen = d0
        for attempt in range(1, 4):
            if chosen is not None:
                break
            tts(seg, mp3)
            d = dur(mp3)
            wpm = words / d * 60 if d > 0 else 0
            ok = d >= expected * 0.5 and 75 <= wpm <= 210
            print(f'  seg{i}: {words}w -> {d:.1f}s ({wpm:.0f} wpm), '
                  f'expected ~{expected:.0f}s, attempt {attempt}, '
                  f'{"OK" if ok else "BAD"}', flush=True)
            if ok:
                chosen = d
                if attempt > 1:
                    regen.append(f'seg{i} regenerated on attempt {attempt}')
                break
            if attempt < 3:
                regen.append(f'seg{i} bad take discarded (attempt {attempt}: {d:.1f}s, {wpm:.0f} wpm)')
        if chosen is None:
            print(f'seg{i}: FAILED after retries')
            raise SystemExit(1)
        seg_mp3s.append((mp3, chosen))
        stats.append({'seg': i, 'words': words, 'duration': round(chosen, 2),
                      'wpm': round(words / chosen * 60, 1)})

    def silence(name, secs):
        p = os.path.join(D, name)
        run(['ffmpeg', '-y', '-threads', '2', '-f', 'lavfi', '-i',
             f'anullsrc=r=44100:cl=stereo:d={secs}',
             '-c:a', 'libmp3lame', '-b:a', '128k', p], f'silence {name}')
        return p

    sil = silence(f'{key}-sil.mp3', gap)
    sil_title = silence(f'{key}-sil-title.mp3', title_hold)
    sil_close = silence(f'{key}-sil-close.mp3', closing_hold)
    concat = os.path.join(D, f'{key}-concat.txt')
    with open(concat, 'w') as f:
        f.write(f"file '{sil_title}'\n")
        for j, (mp3, _) in enumerate(seg_mp3s):
            f.write(f"file '{mp3}'\n")
            if j < len(seg_mp3s) - 1:
                f.write(f"file '{sil}'\n")
        f.write(f"file '{sil_close}'\n")
    narr = os.path.join(D, f'{key}-narration.m4a')
    run(['ffmpeg', '-y', '-threads', '2', '-f', 'concat', '-safe', '0', '-i', concat,
         '-c:a', 'aac', '-b:a', '192k', '-ar', '44100', '-ac', '2', narr],
        'concat narration')
    norm = os.path.join(D, f'{key}-narration-norm.m4a')
    run(['ffmpeg', '-y', '-threads', '2', '-i', narr, '-af',
         'loudnorm=I=-16:TP=-1.5:LRA=11',
         '-c:a', 'aac', '-b:a', '192k', '-ar', '44100', '-ac', '2', norm],
        'loudnorm')
    print('normalized narration:', round(dur(norm), 2), flush=True)

    # Course 3 spec: title card = title_hold + seg1; slide i = seg_i + gap
    # (last slide = seg_last + closing hold)
    durations = []
    for j, (_, d) in enumerate(seg_mp3s):
        if j == 0:
            durations.append(title_hold + d)
        elif j < len(seg_mp3s) - 1:
            durations.append(gap + d)
        else:
            durations.append(closing_hold + d)
    # Note ordering of audio: gap comes AFTER seg j (before next), closing
    # after last. Slide i (i>=2) starts when seg i starts, so its duration is
    # seg_i + following gap; last slide seg_last + closing. Title slide spans
    # title hold + seg1 + following gap? Audio: title sil, seg1, gap, seg2...
    # So strictly: title = title_hold + seg1 + gap; middle slide i = seg_i +
    # gap; last = seg_last + closing. Total is identical either way; the
    # assignment above shifts each gap to the preceding slide except it
    # attaches the first gap to slide2 instead of title. Fix to audio truth:
    durations = []
    for j, (_, d) in enumerate(seg_mp3s):
        if j == 0:
            durations.append(title_hold + d + gap)
        elif j < len(seg_mp3s) - 1:
            durations.append(d + gap)
        else:
            durations.append(d + closing_hold)
    print('slide durations:', [round(x, 2) for x in durations])
    print('video total:', round(sum(durations), 2))

    clips = []
    for k, (img, dsec) in enumerate(zip(cfg['slides'], durations)):
        frames = max(2, round(dsec * FPS))
        out = os.path.join(D, f'{key}-vclip{k:02d}.mp4')
        run(['ffmpeg', '-y', '-threads', '2', '-loop', '1', '-framerate', str(FPS),
             '-i', os.path.join(S, img),
             '-vf', 'scale=1920:1080,format=yuv420p',
             '-frames:v', str(frames),
             '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '19', out],
            f'clip {k}')
        clips.append(out)

    vconcat = os.path.join(D, f'{key}-vconcat.txt')
    with open(vconcat, 'w') as f:
        for c in clips:
            f.write(f"file '{c}'\n")
    vonly = os.path.join(D, f'{key}-video-only.mp4')
    run(['ffmpeg', '-y', '-threads', '2', '-f', 'concat', '-safe', '0', '-i', vconcat,
         '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '19',
         '-pix_fmt', 'yuv420p', vonly], 'concat video')

    run(['ffmpeg', '-y', '-threads', '2', '-i', vonly, '-i', norm, '-c:v', 'copy',
         '-c:a', 'aac', '-b:a', '192k', '-ar', '44100', '-ac', '2',
         '-shortest', '-movflags', '+faststart', cfg['out']], 'mux')

    final = dur(cfg['out'])
    print('FINAL:', round(final, 2), 's =', round(final / 60, 2), 'min')
    print('REGENERATED:', '; '.join(regen) if regen else 'none')
    print('SEG_STATS:', json.dumps(stats))
    print('SLIDE_DURATIONS:', json.dumps([round(x, 2) for x in durations]))
    vr = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0',
                         '-show_entries', 'stream=width,height,codec_name,r_frame_rate',
                         '-of', 'csv=p=0', cfg['out']],
                        capture_output=True, text=True).stdout.strip()
    ar = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'a:0',
                         '-show_entries', 'stream=codec_name,sample_rate,channels',
                         '-of', 'csv=p=0', cfg['out']],
                        capture_output=True, text=True).stdout.strip()
    print('video stream:', vr)
    print('audio stream:', ar)
    meta = {'final': round(final, 3), 'stats': stats, 'regen': regen,
            'slide_durations': [round(x, 2) for x in durations],
            'holds': [title_hold, gap, closing_hold],
            'out': cfg['out'], 'bytes': os.path.getsize(cfg['out'])}
    with open(os.path.join(D, f'{key}-build-meta.json'), 'w') as f:
        json.dump(meta, f, indent=1)
    return final


if __name__ == '__main__':
    key = sys.argv[1]
    holds = [float(x) for x in sys.argv[2:5]] or [4.0, 0.5, 3.0]
    while len(holds) < 3:
        holds.append([4.0, 0.5, 3.0][len(holds)])
    build(key, *holds)
