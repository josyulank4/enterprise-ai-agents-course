"""Assemble Skool Course 3, Section 2: slides + Aria narration -> 1920x1080 MP4s.

Lessons l05-l08. Recipe per PRODUCTION-SPEC.md (Course 2 pattern):
Aria avocado_v2:MAI_01 speed 77; title card = beat 1 (title hold 4.0 + seg1);
content slide i = seg_i + 0.5 gap (last = seg_last + 3.0 closing hold);
loudnorm I=-16:TP=-1.5:LRA=11; H.264 30fps + AAC 44.1k stereo.
Holds are per-lesson configurable ONLY within spec limits (title<=12, gap<=2.5,
close<=10) for the duration gate. Usage: python3 assemble.py l05 [l06 ...]
"""
import os
import re
import subprocess
import sys

COURSE = os.path.expanduser('~/workspace/udemy-skool/skool-course-3-mcp-architecture')
D = os.path.join(COURSE, 'sections', 's02')
S = os.path.join(D, 'slides')
VIDEOS = os.path.join(COURSE, 'videos')
VOICE = 'avocado_v2:MAI_01'
SPEED = '77'
FPS = 30

LESSONS = {
    'l05': {
        'script': 's02-l05.md', 'target': 11.0,
        'slides': ['l05-slide0-title.png', 'l05-slide1-protocol.png',
                   'l05-slide2-usb.png', 'l05-slide3-interface.png',
                   'l05-slide4-not.png', 'l05-slide5-waist.png',
                   'l05-slide6-history.png', 'l05-slide7-tryit.png'],
        'out': 's02-l05-what-mcp-is-and-is-not-2026-10.mp4',
        'holds': (4.0, 0.5, 3.0),
    },
    'l06': {
        'script': 's02-l06.md', 'target': 11.0,
        'slides': ['l06-slide0-title.png', 'l06-slide1-composability.png',
                   'l06-slide2-simplicity.png', 'l06-slide3-security.png',
                   'l06-slide4-host.png', 'l06-slide5-client.png',
                   'l06-slide6-server.png', 'l06-slide7-tryit.png'],
        'out': 's02-l06-design-philosophy-and-the-three-roles-2026-10.mp4',
        'holds': (4.0, 0.5, 3.0),
    },
    'l07': {
        'script': 's02-l07.md', 'target': 10.0,
        'slides': ['l07-slide0-title.png', 'l07-slide1-tools.png',
                   'l07-slide2-resources.png', 'l07-slide3-prompts.png',
                   'l07-slide4-whythree.png', 'l07-slide5-mistake.png',
                   'l07-slide6-tryit.png'],
        'out': 's02-l07-the-three-primitives-tools-resources-and-2026-10.mp4',
        # Extended holds (spec duration gate): raw narration 511.0s + standard
        # holds = 521s < 540s floor; max-allowed holds give 548s. See MANIFEST.
        'holds': (12.0, 2.5, 10.0),
    },
    'l08': {
        'script': 's02-l08.md', 'target': 12.0,
        'slides': ['l08-slide0-title.png', 'l08-slide1-init.png',
                   'l08-slide2-negotiation.png', 'l08-slide3-requests.png',
                   'l08-slide4-errors.png', 'l08-slide5-versioning.png',
                   'l08-slide6-revisions.png', 'l08-slide7-tryit.png'],
        'out': 's02-l08-lifecycle-messages-and-versioning-2026-10.mp4',
        'holds': (4.0, 0.5, 3.0),
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
    parts = re.split(r'\*\*\[Slide \d+ \u2014 .*?\]\*\*', raw)
    segs = [p.strip() for p in parts[1:] if p.strip()]
    # strip any markdown bold markers inside narration
    segs = [s.replace('**', '') for s in segs]
    return segs


def build(key):
    cfg = LESSONS[key]
    title_hold, gap, closing = cfg['holds']
    print('====', key, 'holds', cfg['holds'], '====', flush=True)
    os.makedirs(S, exist_ok=True)
    os.makedirs(VIDEOS, exist_ok=True)
    missing = [f for f in cfg['slides'] if not os.path.exists(os.path.join(S, f))]
    if missing:
        print('missing slides, run build_slides.py first:', missing)
        raise SystemExit(1)

    segs = split_script(os.path.join(COURSE, 'scripts', cfg['script']))
    assert len(segs) == len(cfg['slides']), (len(segs), len(cfg['slides']))
    print(f'{len(segs)} narration segments', flush=True)
    seg_mp3s = []
    regen = []
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
                regen.append(f'seg{i} bad take discarded '
                             f'(attempt {attempt}: {d:.1f}s, {wpm:.0f} wpm)')
        if chosen is None:
            print(f'seg{i}: FAILED after retries')
            raise SystemExit(1)
        seg_mp3s.append((mp3, chosen))

    def silence(name, secs):
        p = os.path.join(D, name)
        run(['ffmpeg', '-y', '-threads', '2', '-f', 'lavfi', '-i',
             f'anullsrc=r=44100:cl=stereo:d={secs}',
             '-c:a', 'libmp3lame', '-b:a', '128k', p], 'silence')
        return p

    sil = silence(f'{key}-sil.mp3', gap)
    sil_title = silence(f'{key}-sil-title.mp3', title_hold)
    sil_close = silence(f'{key}-sil-close.mp3', closing)
    concat = os.path.join(D, f'{key}-concat.txt')
    with open(concat, 'w') as f:
        f.write(f"file '{sil_title}'\n")
        for j, (mp3, _) in enumerate(seg_mp3s):
            f.write(f"file '{mp3}'\n")
            if j < len(seg_mp3s) - 1:
                f.write(f"file '{sil}'\n")
        f.write(f"file '{sil_close}'\n")
    narr = os.path.join(D, f'{key}-narration.m4a')
    norm = os.path.join(D, f'{key}-narration-norm.m4a')
    expected_total = (title_hold + closing + gap * (len(seg_mp3s) - 1)
                      + sum(d for _, d in seg_mp3s))
    if (os.path.exists(norm) and os.path.getsize(norm) > 0
            and abs(dur(norm) - expected_total) < 1.5):
        print('reuse verified narration-norm:', round(dur(norm), 2), flush=True)
    else:
        run(['ffmpeg', '-y', '-threads', '2', '-f', 'concat', '-safe', '0',
             '-i', concat, '-c:a', 'aac', '-b:a', '192k', '-ar', '44100',
             '-ac', '2', narr], 'concat narration')
        run(['ffmpeg', '-y', '-threads', '2', '-i', narr, '-af',
             'loudnorm=I=-16:TP=-1.5:LRA=11',
             '-c:a', 'aac', '-b:a', '192k', '-ar', '44100', '-ac', '2', norm],
            'loudnorm')
    print('normalized narration:', round(dur(norm), 2), flush=True)

    durations = []
    for j, (_, d) in enumerate(seg_mp3s):
        if j == 0:
            extra = title_hold
        elif j == len(seg_mp3s) - 1:
            extra = closing
        else:
            extra = gap
        durations.append(d + extra)
    print('slide durations:', [round(x, 2) for x in durations], flush=True)
    print('video total:', round(sum(durations), 2), flush=True)

    clips = []
    for k, (img, dsec) in enumerate(zip(cfg['slides'], durations)):
        frames = max(2, round(dsec * FPS))
        out = os.path.join(D, f'{key}-vclip{k:02d}.mp4')
        if (os.path.exists(out) and os.path.getsize(out) > 0
                and abs(dur(out) - frames / FPS) < 0.06):
            print(f'  clip {k}: reuse verified {dur(out):.2f}s', flush=True)
            clips.append(out)
            continue
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

    out_path = os.path.join(VIDEOS, cfg['out'])
    run(['ffmpeg', '-y', '-threads', '2', '-i', vonly, '-i', norm, '-c:v', 'copy',
         '-c:a', 'aac', '-b:a', '192k', '-ar', '44100', '-ac', '2',
         '-shortest', '-movflags', '+faststart', out_path], 'mux')

    final = dur(out_path)
    print('FINAL:', round(final, 2), 's =', round(final / 60, 2), 'min', flush=True)
    print('REGENERATED:', '; '.join(regen) if regen else 'none', flush=True)
    return final


if __name__ == '__main__':
    keys = sys.argv[1:] or list(LESSONS)
    for k in keys:
        build(k)
