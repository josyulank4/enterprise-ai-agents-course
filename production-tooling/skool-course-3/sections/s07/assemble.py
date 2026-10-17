"""Assemble Skool Course 3, Section 7: slides + Aria narration -> 1920x1080 MP4s.

Lessons l27-l31. Pattern replicated from Skool Course 2 s00 assemble.py,
with narration parsed from Course 3 markdown scripts (one segment per
[Slide N] beat) and the PRODUCTION-SPEC slide scheme: title card carries
the 4.0s hold + segment 1; each content slide carries its segment + the
trailing gap (last slide carries the 3.0s closing hold).
Hold adjustments (duration gate) follow the spec caps only:
title <= 12s, gap <= 2.5s, closing <= 10s.
Usage: python3 assemble.py [l27|l28|l29|l30|l31]
"""
import json
import os
import re
import subprocess
import sys

COURSE = os.path.expanduser(
    '~/workspace/udemy-skool/skool-course-3-mcp-architecture')
D = os.path.join(COURSE, 'sections', 's07')
S = os.path.join(D, 'slides')
VIDEOS = os.path.join(COURSE, 'videos')
VOICE = 'avocado_v2:MAI_01'  # Aria
SPEED = '77'
FPS = 30
GAP = 0.5
TITLE_HOLD = 4.0
CLOSING_HOLD = 3.0
MAX_TITLE, MAX_GAP, MAX_CLOSE = 12.0, 2.5, 10.0

LESSONS = {
    'l27': {
        'script': 's07-l27.md', 'target': 12.0,
        'slides': ['l27-slide0-title.png', 'l27-slide1-why.png',
                   'l27-slide2-injection.png', 'l27-slide3-layers.png',
                   'l27-slide4-defense1.png', 'l27-slide5-defense2.png',
                   'l27-slide6-prompt.png', 'l27-slide7-next.png'],
        'out': 's07-l27-the-new-attack-surface-injection-through-tool-2026-10.mp4',
    },
    'l28': {
        'script': 's07-l28.md', 'target': 11.0,
        'slides': ['l28-slide0-title.png', 'l28-slide1-poisoning.png',
                   'l28-slide2-rugpull.png', 'l28-slide3-counter.png',
                   'l28-slide4-deputy.png', 'l28-slide5-audience.png',
                   'l28-slide6-exfil.png', 'l28-slide7-next.png'],
        'out': 's07-l28-tool-poisoning-rug-pulls-and-the-confused-deputy-2026-10.mp4',
    },
    'l29': {
        'script': 's07-l29.md', 'target': 11.0,
        'slides': ['l29-slide0-title.png', 'l29-slide1-flow.png',
                   'l29-slide2-details.png', 'l29-slide3-local.png',
                   'l29-slide4-bearer.png', 'l29-slide5-leaks.png',
                   'l29-slide6-pattern.png', 'l29-slide7-next.png'],
        'out': 's07-l29-authentication-oauth-2-1-keys-and-tokens-2026-10.mp4',
    },
    'l30': {
        'script': 's07-l30.md', 'target': 11.0,
        'slides': ['l30-slide0-title.png', 'l30-slide1-servercode.png',
                   'l30-slide2-narrow.png', 'l30-slide3-ladder.png',
                   'l30-slide4-approval.png', 'l30-slide5-real.png',
                   'l30-slide6-policy.png', 'l30-slide7-next.png'],
        'out': 's07-l30-least-privilege-authorization-and-human-approval-2026-10.mp4',
    },
    'l31': {
        'script': 's07-l31.md', 'target': 11.0,
        'slides': ['l31-slide0-title.png', 'l31-slide1-isolation.png',
                   'l31-slide2-rings.png', 'l31-slide3-audit.png',
                   'l31-slide4-tamper.png', 'l31-slide5-checklist.png',
                   'l31-slide6-gaps.png', 'l31-slide7-next.png'],
        'out': 's07-l31-sandboxing-audit-logging-and-the-security-2026-10.mp4',
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


def parse_script(path):
    raw = open(path).read()
    parts = re.split(r'\*\*\[Slide (\d+) \u2014 (.*?)\]\*\*', raw)
    segs = []
    labels = []
    for i in range(1, len(parts), 3):
        text = parts[i + 2].strip()
        text = re.sub(r'\n---\s*$', '', text).strip()
        text = text.replace('**', '')
        text = re.sub(r'\s+', ' ', text.replace('\n', ' ')).strip()
        segs.append(text)
        labels.append(parts[i + 1])
    return labels, segs


def build(key):
    cfg = LESSONS[key]
    print('====', key, '====', flush=True)
    os.makedirs(S, exist_ok=True)
    os.makedirs(VIDEOS, exist_ok=True)
    missing = [f for f in cfg['slides'] if not os.path.exists(os.path.join(S, f))]
    if missing:
        print('missing slides:', missing)
        raise SystemExit(1)

    labels, segs = parse_script(os.path.join(COURSE, 'scripts', cfg['script']))
    assert len(segs) == len(cfg['slides']), (len(segs), len(cfg['slides']))
    print(f'{len(segs)} narration segments', flush=True)
    seg_mp3s = []
    regen = []
    seg_stats = []
    for i, seg in enumerate(segs, 1):
        txt_path = os.path.join(D, f'{key}-seg{i}.txt')
        mp3 = os.path.join(D, f'{key}-seg{i}.mp3')
        with open(txt_path, 'w') as f:
            f.write(seg)
        words = len(seg.split())
        expected = words / 135.0 * 60.0
        chosen = None
        if os.path.exists(mp3) and os.path.getsize(mp3) > 0:
            # reuse only if the .txt sidecar matches current text
            sidecar = mp3 + '.txt'
            same = os.path.exists(sidecar) and open(sidecar).read() == seg
            if same:
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
        seg_stats.append({'seg': i, 'label': labels[i - 1], 'words': words,
                          'dur': round(chosen, 2),
                          'wpm': round(words / chosen * 60)})

    # ---- duration gate: choose holds within spec caps ----
    n = len(seg_mp3s)
    narr_sum = sum(d for _, d in seg_mp3s)
    target_s = cfg['target'] * 60
    lo, hi = target_s * 0.9, target_s * 1.1
    t_hold, gap, c_hold = TITLE_HOLD, GAP, CLOSING_HOLD
    total_std = t_hold + narr_sum + gap * (n - 1) + c_hold
    hold_note = 'standard holds (title 4.0 / gap 0.5 / closing 3.0)'
    if total_std < lo:
        aim = min(lo + 12.0, hi - 5.0)
        extra = aim - total_std
        # 1) widen gaps
        per_gap_room = MAX_GAP - gap
        gap_add = min(extra, per_gap_room * (n - 1))
        if n > 1 and gap_add > 0:
            gap += gap_add / (n - 1)
            extra -= gap_add
        # 2) widen title hold
        if extra > 0:
            add = min(extra, MAX_TITLE - t_hold)
            t_hold += add
            extra -= add
        # 3) widen closing hold
        if extra > 0:
            add = min(extra, MAX_CLOSE - c_hold)
            c_hold += add
            extra -= add
        hold_note = (f'extended holds for duration gate: title {t_hold:.2f}s / '
                     f'gap {gap:.2f}s / closing {c_hold:.2f}s '
                     f'(standard 4.0 / 0.5 / 3.0; caps 12 / 2.5 / 10)')
        if extra > 0:
            hold_note += f' [WARNING: still {extra:.1f}s short at max holds]'
    elif total_std > hi:
        # Over-length: narration alone fits the window but standard holds push
        # past the ceiling. Spec: adjust ONLY presentation holds — shrink them
        # toward minimums (title 2.0 / gap 0.3 / closing 1.5). Narration, voice
        # and text stay frozen; if still over at minimums, that is a BLOCKER.
        aim = hi - 3.0
        extra = total_std - aim
        if n > 1 and extra > 0:
            cut = min(extra, (gap - 0.3) * (n - 1))
            gap -= cut / (n - 1)
            extra -= cut
        if extra > 0:
            cut = min(extra, c_hold - 1.5)
            c_hold -= cut
            extra -= cut
        if extra > 0:
            cut = min(extra, t_hold - 2.0)
            t_hold -= cut
            extra -= cut
        hold_note = (f'reduced holds for duration gate: title {t_hold:.2f}s / '
                     f'gap {gap:.2f}s / closing {c_hold:.2f}s '
                     f'(standard 4.0 / 0.5 / 3.0)')
        if t_hold + narr_sum + gap * (n - 1) + c_hold > hi:
            hold_note += (' [WARNING: still over window at minimum holds — '
                          'spec BLOCKER]')
    total_planned = t_hold + narr_sum + gap * (n - 1) + c_hold
    print(f'narration sum {narr_sum:.1f}s; planned total {total_planned:.1f}s '
          f'(window {lo:.0f}-{hi:.0f})', flush=True)
    print('holds:', hold_note, flush=True)

    def silence(dsec, name):
        p = os.path.join(D, name)
        run(['ffmpeg', '-y', '-threads', '2', '-f', 'lavfi', '-i',
             f'anullsrc=r=44100:cl=stereo:d={dsec}',
             '-c:a', 'libmp3lame', '-b:a', '128k', p], 'silence')
        return p

    sil_gap = silence(gap, f'{key}-sil.mp3')
    sil_title = silence(t_hold, f'{key}-sil-title.mp3')
    sil_close = silence(c_hold, f'{key}-sil-close.mp3')
    concat = os.path.join(D, f'{key}-concat.txt')
    with open(concat, 'w') as f:
        f.write(f"file '{sil_title}'\n")
        for j, (mp3, _) in enumerate(seg_mp3s):
            f.write(f"file '{mp3}'\n")
            if j < len(seg_mp3s) - 1:
                f.write(f"file '{sil_gap}'\n")
        f.write(f"file '{sil_close}'\n")
    narr = os.path.join(D, f'{key}-narration.m4a')
    run(['ffmpeg', '-y', '-threads', '2', '-f', 'concat', '-safe', '0',
         '-i', concat, '-c:a', 'aac', '-b:a', '192k', '-ar', '44100',
         '-ac', '2', narr], 'concat narration')
    norm = os.path.join(D, f'{key}-narration-norm.m4a')
    run(['ffmpeg', '-y', '-threads', '2', '-i', narr,
         '-af', 'loudnorm=I=-16:TP=-1.5:LRA=11',
         '-c:a', 'aac', '-b:a', '192k', '-ar', '44100', '-ac', '2', norm],
        'loudnorm')
    norm_d = dur(norm)
    print('normalized narration:', round(norm_d, 2), flush=True)

    # slide durations: title = hold + seg1 + gap; middle = seg + gap; last = seg + close
    durations = []
    for j, (_, d) in enumerate(seg_mp3s):
        if j == 0:
            durations.append(t_hold + d + (gap if n > 1 else c_hold))
        elif j < n - 1:
            durations.append(d + gap)
        else:
            durations.append(d + c_hold)
    print('slide durations:', [round(x, 2) for x in durations], flush=True)
    print('video total:', round(sum(durations), 2), flush=True)

    # segment narration intervals [start, end) on the final timeline
    intervals = []
    t = t_hold
    for j, (_, d) in enumerate(seg_mp3s):
        intervals.append([round(t, 2), round(t + d, 2)])
        t += d + gap

    clips = []
    for k, (img, dsec) in enumerate(zip(cfg['slides'], durations)):
        frames = max(2, round(dsec * FPS))
        out = os.path.join(D, f'{key}-vclip{k:02d}.mp4')
        reused = False
        if os.path.exists(out) and os.path.getsize(out) > 10000:
            try:
                cd = dur(out)
                if abs(cd - frames / FPS) <= 0.06:
                    print(f'  clip {k}: reuse verified {cd:.2f}s', flush=True)
                    reused = True
            except Exception:
                reused = False
        if not reused:
            run(['ffmpeg', '-y', '-threads', '2', '-loop', '1', '-framerate',
                 str(FPS), '-i', os.path.join(S, img),
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
    run(['ffmpeg', '-y', '-threads', '2', '-f', 'concat', '-safe', '0',
         '-i', vconcat, '-c:v', 'libx264', '-preset', 'veryfast',
         '-crf', '19', '-pix_fmt', 'yuv420p', vonly], 'concat video')

    out_path = os.path.join(VIDEOS, cfg['out'])
    run(['ffmpeg', '-y', '-threads', '2', '-i', vonly, '-i', norm,
         '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-ar', '44100',
         '-ac', '2', '-shortest', '-movflags', '+faststart', out_path], 'mux')

    final = dur(out_path)
    print('FINAL:', round(final, 2), 's =', round(final / 60, 2), 'min', flush=True)
    print('REGENERATED:', '; '.join(regen) if regen else 'none', flush=True)
    meta = {'lesson': key, 'file': cfg['out'], 'bytes': os.path.getsize(out_path),
            'duration': round(final, 2), 'target_min': cfg['target'],
            'window': [round(lo, 1), round(hi, 1)],
            'narration_sum': round(narr_sum, 2),
            'holds': {'title': round(t_hold, 2), 'gap': round(gap, 2),
                      'closing': round(c_hold, 2)},
            'hold_note': hold_note, 'segments': seg_stats,
            'regen': regen, 'slide_durations': [round(x, 2) for x in durations],
            'intervals': intervals, 'norm_duration': round(norm_d, 2)}
    with open(os.path.join(D, f'{key}-build.json'), 'w') as f:
        json.dump(meta, f, indent=1)
    print('META saved', flush=True)
    return final


if __name__ == '__main__':
    which = sys.argv[1]
    build(which)
