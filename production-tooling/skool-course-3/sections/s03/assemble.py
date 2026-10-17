"""Assemble Skool Course 3, Section 3: slides + Aria narration -> 1920x1080 MP4s.

Lessons L09-L12. Recipe per PRODUCTION-SPEC.md (Course 2 pipeline):
Aria avocado_v2:MAI_01 speed 77; loudnorm I=-16:TP=-1.5:LRA=11;
title hold 4.0s / gaps 0.5s / closing hold 3.0s standard; slide 1 (title card)
is the visual for beat 1: its duration = title_hold + seg1; each later slide
starts with its preceding gap (gap + seg_i), last slide adds closing hold,
so slide durations sum exactly to the narration total.
Duration gate +-10%: only presentation holds may change (title <=12s,
gaps <=2.5s, closing <=10s).
Usage: python3 assemble.py [l09|l10|l11|l12|all]
"""
import os
import re
import subprocess
import sys

COURSE = os.path.expanduser(
    '~/workspace/udemy-skool/skool-course-3-mcp-architecture')
D = os.path.join(COURSE, 'sections', 's03')
S = os.path.join(D, 'slides')
VIDEOS = os.path.join(COURSE, 'videos')
VOICE = 'avocado_v2:MAI_01'
SPEED = '77'
FPS = 30
GAP = 0.5
TITLE_HOLD = 4.0
CLOSING_HOLD = 3.0

LESSONS = {
    'l09': {
        'script': os.path.join(COURSE, 'scripts', 's03-l09.md'),
        'target_min': 11.0,
        'slides': ['l09-slide0-title.png', 'l09-slide1-inside-host.png',
                   'l09-slide2-native-api.png', 'l09-slide3-checklist.png',
                   'l09-slide4-anatomy.png', 'l09-slide5-hidden.png',
                   'l09-slide6-product.png', 'l09-slide7-try-it.png'],
        'out': os.path.join(VIDEOS, 's03-l09-separation-of-concerns-and-server-anatomy-2026-10.mp4'),
    },
    'l10': {
        'script': os.path.join(COURSE, 'scripts', 's03-l10.md'),
        'target_min': 11.0,
        'slides': ['l10-slide0-title.png', 'l10-slide1-mechanics.png',
                   'l10-slide2-discipline.png', 'l10-slide3-strengths.png',
                   'l10-slide4-limitations.png', 'l10-slide5-where-it-fits.png',
                   'l10-slide6-try-it.png'],
        'out': os.path.join(VIDEOS, 's03-l10-the-stdio-transport-local-simple-process-bound-2026-10.mp4'),
    },
    'l11': {
        'script': os.path.join(COURSE, 'scripts', 's03-l11.md'),
        'target_min': 12.0,
        'slides': ['l11-slide0-title.png', 'l11-slide1-mechanics.png',
                   'l11-slide2-stateless.png', 'l11-slide3-scales.png',
                   'l11-slide4-bill.png', 'l11-slide5-choosing.png',
                   'l11-slide6-try-it.png'],
        'out': os.path.join(VIDEOS, 's03-l11-streamable-http-remote-stateless-scalable-2026-10.mp4'),
    },
    'l12': {
        'script': os.path.join(COURSE, 'scripts', 's03-l12.md'),
        'target_min': 11.0,
        'slides': ['l12-slide0-title.png', 'l12-slide1-lifecycle.png',
                   'l12-slide2-sessions.png', 'l12-slide3-across.png',
                   'l12-slide4-within.png', 'l12-slide5-roundtrip-a.png',
                   'l12-slide6-roundtrip-b.png', 'l12-slide7-try-it.png'],
        'out': os.path.join(VIDEOS, 's03-l12-sessions-concurrency-and-a-full-round-trip-2026-10.mp4'),
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
    parts = re.split(r'\*\*\[Slide \d+ \u2014 [^\]]+\]\*\*', raw)
    segs = [p.strip().replace('**', '') for p in parts[1:] if p.strip()]
    return segs


def plan_holds(seg_durs, target_min):
    """Return (title_hold, gap, closing_hold, note). Standard holds unless the
    standard total falls below the +-10% window; then raise holds within the
    spec caps (gap 2.5, closing 10, title 12), aiming at the target."""
    n = len(seg_durs)
    narr = sum(seg_durs)
    target = target_min * 60.0
    lo, hi = target * 0.9, target * 1.1
    std_total = TITLE_HOLD + narr + GAP * (n - 1) + CLOSING_HOLD
    if lo <= std_total <= hi:
        return TITLE_HOLD, GAP, CLOSING_HOLD, f'standard holds; total {std_total:.1f}s in window'
    if std_total > hi:
        return TITLE_HOLD, GAP, CLOSING_HOLD, f'BLOCKER-CANDIDATE: standard total {std_total:.1f}s above window hi {hi:.1f}s'
    # Authorized adaptation A2 (PRODUCTION-SPEC.md, 2026-10-16): if even the
    # standard caps (gap 2.5 / closing 10 / title 12) cannot reach the window
    # floor, extend holds to the A2 caps (gap 5 / title 16 / closing 20) and
    # aim at floor + 9s. Distribution order gaps -> title -> closing (the
    # s04 order); for L10 this reproduces the banked A2 plan 16 / 5 / 18.
    max_std_total = 12.0 + narr + 2.5 * (n - 1) + 10.0
    a2 = max_std_total < lo
    if a2:
        aim = lo + 9.0
        cap_gap, cap_title, cap_close = 5.0, 16.0, 20.0
    else:
        aim = target
        cap_gap, cap_title, cap_close = 2.5, 12.0, 10.0
    extra = aim - std_total
    gap, title, closing = GAP, TITLE_HOLD, CLOSING_HOLD
    # 1) gaps up to cap
    add = min(extra, (cap_gap - GAP) * (n - 1))
    if n > 1 and add > 0:
        gap += add / (n - 1)
        extra -= add
    # 2) title up to cap
    add = min(extra, cap_title - TITLE_HOLD)
    if add > 0:
        title += add
        extra -= add
    # 3) closing up to cap
    add = min(extra, cap_close - CLOSING_HOLD)
    if add > 0:
        closing += add
        extra -= add
    total = title + narr + gap * (n - 1) + closing
    note = (f'extended holds to reach window: title {title:.2f}s, gap {gap:.2f}s, '
            f'closing {closing:.2f}s -> planned total {total:.1f}s '
            f'(target {target:.0f}s, window {lo:.0f}-{hi:.0f}s)')
    if a2:
        note += ' [A2 extended holds: caps title 16 / gap 5 / closing 20]'
    if total < lo:
        note += f' BLOCKER-CANDIDATE: even max holds give {total:.1f}s < window low {lo:.1f}s'
    return title, gap, closing, note


def build(key):
    cfg = LESSONS[key]
    print('====', key, '====', flush=True)
    os.makedirs(S, exist_ok=True)
    os.makedirs(VIDEOS, exist_ok=True)
    if not all(os.path.exists(os.path.join(S, f)) for f in cfg['slides']):
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
        attempts_used = 0
        for attempt in range(1, 4):
            if chosen is not None:
                break
            attempts_used = attempt
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
        stats.append((i, words, chosen, words / chosen * 60))

    seg_durs = [d for _, d in seg_mp3s]
    title_hold, gap, closing_hold, hold_note = plan_holds(seg_durs, cfg['target_min'])
    print('HOLDS:', hold_note, flush=True)
    print('SEGSTATS:', '; '.join(f'seg{i} {w}w/{d:.1f}s/{wpm:.0f}wpm' for i, w, d, wpm in stats), flush=True)

    def silence(name, secs):
        p = os.path.join(D, name)
        run(['ffmpeg', '-y', '-threads', '2', '-f', 'lavfi', '-i',
             f'anullsrc=r=44100:cl=stereo:d={secs}',
             '-c:a', 'libmp3lame', '-b:a', '128k', p], f'silence {name}')
        return p

    sil_gap = silence(f'{key}-sil.mp3', gap)
    sil_title = silence(f'{key}-sil-title.mp3', title_hold)
    sil_close = silence(f'{key}-sil-close.mp3', closing_hold)
    concat = os.path.join(D, f'{key}-concat.txt')
    with open(concat, 'w') as f:
        f.write(f"file '{sil_title}'\n")
        for j, (mp3, _) in enumerate(seg_mp3s):
            f.write(f"file '{mp3}'\n")
            if j < len(seg_mp3s) - 1:
                f.write(f"file '{sil_gap}'\n")
        f.write(f"file '{sil_close}'\n")
    narr = os.path.join(D, f'{key}-narration.m4a')
    run(['ffmpeg', '-y', '-threads', '2', '-f', 'concat', '-safe', '0', '-i', concat,
         '-c:a', 'aac', '-b:a', '192k', '-ar', '44100', '-ac', '2', narr],
        'concat narration')
    norm = os.path.join(D, f'{key}-narration-norm.m4a')
    run(['ffmpeg', '-y', '-threads', '2', '-i', narr, '-af', 'loudnorm=I=-16:TP=-1.5:LRA=11',
         '-c:a', 'aac', '-b:a', '192k', '-ar', '44100', '-ac', '2', norm],
        'loudnorm')
    print('normalized narration:', round(dur(norm), 2), flush=True)

    durations = []
    for j, d in enumerate(seg_durs):
        if j == 0:
            durations.append(title_hold + d)
        elif j == len(seg_durs) - 1:
            durations.append(gap + d + closing_hold)
        else:
            durations.append(gap + d)
    print('slide durations:', [round(x, 2) for x in durations], flush=True)
    print('video total:', round(sum(durations), 2), flush=True)

    clips = []
    for k, (img, dsec) in enumerate(zip(cfg['slides'], durations)):
        frames = max(2, round(dsec * FPS))
        out = os.path.join(D, f'{key}-vclip{k:02d}.mp4')
        if os.path.exists(out) and os.path.getsize(out) > 10000:
            try:
                cd = dur(out)
            except Exception:
                cd = -1
            if abs(cd - frames / FPS) <= 0.2:
                print(f'  clip {k}: reuse existing {cd:.2f}s', flush=True)
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

    run(['ffmpeg', '-y', '-threads', '2', '-i', vonly, '-i', norm, '-c:v', 'copy',
         '-c:a', 'aac', '-b:a', '192k', '-ar', '44100', '-ac', '2',
         '-shortest', '-movflags', '+faststart', cfg['out']], 'mux')

    final = dur(cfg['out'])
    print('FINAL:', round(final, 2), 's =', round(final / 60, 2), 'min', flush=True)
    print('REGENERATED:', '; '.join(regen) if regen else 'none', flush=True)
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
    return final


if __name__ == '__main__':
    which = sys.argv[1] if len(sys.argv) > 1 else 'all'
    keys = [which] if which in LESSONS else list(LESSONS)
    for k in keys:
        build(k)
