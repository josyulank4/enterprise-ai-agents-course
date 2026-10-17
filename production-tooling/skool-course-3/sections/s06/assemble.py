"""Assemble Skool Course 3, Section 6: slides + Aria narration -> 1920x1080 MP4s.

Lessons l22-l26. Pattern replicated from Course 3 s04 assemble.py (Course 2
s00 pattern), narration parsed from Course 3 markdown scripts (one segment
per [Slide N] beat). Title card carries the 4.0s hold + segment 1; each
content slide carries its segment + trailing gap (last: 3.0s closing hold).
Hold adjustments follow spec caps only: title <= 12s, gap <= 2.5s, close <= 10s.

Authorized adaptation A1 (PRODUCTION-SPEC, coordinator 2026-10-16): if a
segment deterministically fails segment QC after 3 attempts, split its text
VERBATIM at sentence boundaries into 2-3 sub-segments, QC each at the same
gates, and concatenate with 0.3s silence. Documented in build JSON/manifest.
Usage: python3 assemble.py [l22|l23|l24|l25|l26]
"""
import json
import os
import re
import subprocess
import sys

COURSE = os.path.expanduser(
    '~/workspace/udemy-skool/skool-course-3-mcp-architecture')
D = os.path.join(COURSE, 'sections', 's06')
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
    'l22': {
        'script': 's06-l22.md', 'target': 11.0,
        'slides': ['l22-slide0-title.png', 'l22-slide1-diplomat.png',
                   'l22-slide2-designed.png', 'l22-slide3-anticorruption.png',
                   'l22-slide4-behind.png', 'l22-slide5-domain.png',
                   'l22-slide6-structure.png', 'l22-slide7-next.png'],
        'out': 's06-l22-the-adapter-pattern-mcp-as-a-facade-2026-10.mp4',
    },
    'l23': {
        'script': 's06-l23.md', 'target': 11.0,
        'slides': ['l23-slide0-title.png', 'l23-slide1-rawsql.png',
                   'l23-slide2-intention.png', 'l23-slide3-readswrites.png',
                   'l23-slide4-filestores.png', 'l23-slide5-searchread.png',
                   'l23-slide6-writesroots.png', 'l23-slide7-next.png'],
        'out': 's06-l23-wrapping-databases-and-file-stores-2026-10.mp4',
    },
    'l24': {
        'script': 's06-l24.md', 'target': 11.0,
        'slides': ['l24-slide0-title.png', 'l24-slide1-select.png',
                   'l24-slide2-mechanics.png', 'l24-slide3-pagination.png',
                   'l24-slide4-saas.png', 'l24-slide5-quotas.png',
                   'l24-slide6-identity.png', 'l24-slide7-next.png'],
        'out': 's06-l24-wrapping-rest-apis-and-saas-tools-2026-10.mp4',
    },
    'l25': {
        'script': 's06-l25.md', 'target': 11.0,
        'slides': ['l25-slide0-title.png', 'l25-slide1-serverside.png',
                   'l25-slide2-privilege.png', 'l25-slide3-audit.png',
                   'l25-slide4-tiers01.png', 'l25-slide5-tier2.png',
                   'l25-slide6-honest.png', 'l25-slide7-next.png'],
        'out': 's06-l25-upstream-authentication-and-safety-tiers-2026-10.mp4',
    },
    'l26': {
        'script': 's06-l26.md', 'target': 11.0,
        'slides': ['l26-slide0-title.png', 'l26-slide1-layers.png',
                   'l26-slide2-cachebatch.png', 'l26-slide3-meridian.png',
                   'l26-slide4-facadetiers.png', 'l26-slide5-notbuilt.png',
                   'l26-slide6-mistakes.png', 'l26-slide7-next.png'],
        'out': 's06-l26-rate-limits-quotas-and-the-ticketing-scenario-2026-10.mp4',
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


def qc_ok(words, d):
    expected = words / 135.0 * 60.0
    wpm = words / d * 60 if d > 0 else 0
    return d >= expected * 0.5 and 75 <= wpm <= 210


def synth_qc(text, mp3, tag, regen):
    """Synthesize with up to 3 attempts at the standard segment QC gates.
    Returns duration or None."""
    words = len(text.split())
    expected = words / 135.0 * 60.0
    # reuse only if sidecar text matches exactly and take passes QC
    if os.path.exists(mp3) and os.path.getsize(mp3) > 0:
        sidecar = mp3 + '.txt'
        if os.path.exists(sidecar) and open(sidecar).read() == text:
            d0 = dur(mp3)
            if qc_ok(words, d0):
                print(f'  {tag}: reuse existing {d0:.1f}s '
                      f'({words / d0 * 60:.0f} wpm)', flush=True)
                return d0
    for attempt in range(1, 4):
        tts(text, mp3)
        d = dur(mp3)
        wpm = words / d * 60 if d > 0 else 0
        ok = qc_ok(words, d)
        print(f'  {tag}: {words}w -> {d:.1f}s ({wpm:.0f} wpm), '
              f'expected ~{expected:.0f}s, attempt {attempt}, '
              f'{"OK" if ok else "BAD"}', flush=True)
        if ok:
            if attempt > 1:
                regen.append(f'{tag} regenerated on attempt {attempt}')
            return d
        if attempt < 3:
            regen.append(f'{tag} bad take discarded '
                         f'(attempt {attempt}: {d:.1f}s, {wpm:.0f} wpm)')
    return None


def split_sentences(text, n_groups):
    """Split text verbatim at sentence boundaries into n_groups balanced
    groups (by word count). Returns list of strings whose join with single
    spaces reproduces the original word sequence exactly."""
    sents = re.split(r'(?<=[.?!])\s+', text.strip())
    sents = [s for s in sents if s]
    if len(sents) < n_groups:
        return None
    total = sum(len(s.split()) for s in sents)
    target = total / n_groups
    groups = []
    cur = []
    cur_w = 0
    for s in sents:
        w = len(s.split())
        if cur and cur_w + w > target and len(groups) < n_groups - 1:
            groups.append(' '.join(cur))
            cur, cur_w = [s], w
        else:
            cur.append(s)
            cur_w += w
    if cur:
        groups.append(' '.join(cur))
    if len(groups) != n_groups:
        return None
    assert ' '.join(groups).split() == text.split(), 'A1 split not verbatim'
    return groups


# A1 partitions verified by out-of-pipeline diagnostic synthesis (identical
# text/voice/speed; the TTS route is deterministic, re-synthesis bit-identical,
# as proven in Sections 3-4). (lesson, seg) -> 1-based sentence index ranges.
A1_OVERRIDES = {
    ('l22', 6): [(1, 2), (3, 5), (6, 12)],
}


def sentences_of(text):
    return [s for s in re.split(r'(?<=[.?!])\s+', text.strip()) if s]


def synth_with_a1(key, i, seg, mp3, regen, a1_log):
    """A1: split failing beat verbatim into sub-segments, QC each, concat
    with 0.3s silence. Recursive halving for sub-segments that still fail
    while they are > ~60 words. Returns combined duration or None."""
    words = len(seg.split())
    override = A1_OVERRIDES.get((key, i))
    if override:
        sents = sentences_of(seg)
        groups = [' '.join(sents[a - 1:b]) for a, b in override]
        assert ' '.join(groups).split() == seg.split(), 'override not verbatim'
    else:
        n_groups = 3 if words > 120 else 2
        groups = split_sentences(seg, n_groups)
        if groups is None:
            return None
    sub_mp3s = []
    sub_stats = []
    for j, g in enumerate(groups, 1):
        sub_mp3 = os.path.join(D, f'{key}-seg{i}sub{j}.mp3')
        sub_txt = os.path.join(D, f'{key}-seg{i}sub{j}.txt')
        with open(sub_txt, 'w') as f:
            f.write(g)
        d = synth_qc(g, sub_mp3, f'seg{i}sub{j}', regen)
        if d is None and len(g.split()) > 60:
            # recursive split of this sub-segment into 2
            d = synth_with_a1_sub(key, i, j, g, sub_mp3, regen, sub_stats)
        if d is None:
            return None
        sub_mp3s.append(sub_mp3)
        sub_stats.append({'sub': j, 'words': len(g.split()),
                          'dur': round(d, 2),
                          'wpm': round(len(g.split()) / d * 60)})
    # concat subs with 0.3s silence
    sil = os.path.join(D, f'{key}-seg{i}-a1sil.mp3')
    run(['ffmpeg', '-y', '-threads', '2', '-f', 'lavfi', '-i',
         'anullsrc=r=44100:cl=stereo:d=0.3',
         '-c:a', 'libmp3lame', '-b:a', '128k', sil], 'a1 silence')
    lst = os.path.join(D, f'{key}-seg{i}-a1concat.txt')
    with open(lst, 'w') as f:
        for j, sm in enumerate(sub_mp3s):
            f.write(f"file '{sm}'\n")
            if j < len(sub_mp3s) - 1:
                f.write(f"file '{sil}'\n")
    run(['ffmpeg', '-y', '-threads', '2', '-f', 'concat', '-safe', '0',
         '-i', lst, '-c:a', 'libmp3lame', '-b:a', '192k', mp3], 'a1 concat')
    # sidecar so reuse logic treats combined file as current segment text
    with open(mp3 + '.txt', 'w') as f:
        f.write(seg)
    combined = dur(mp3)
    a1_log.append({'seg': i, 'words': words, 'subs': sub_stats,
                   'combined_dur': round(combined, 2),
                   'note': 'verbatim sentence-boundary split (A1), '
                           '0.3s silence between sub-segments'})
    print(f'  seg{i}: A1 combined {combined:.1f}s from '
          f'{len(sub_mp3s)} sub-segments', flush=True)
    return combined


def synth_with_a1_sub(key, i, j, text, out_mp3, regen, sub_stats):
    groups = split_sentences(text, 2)
    if groups is None:
        return None
    parts = []
    for k, g in enumerate(groups, 1):
        pm = os.path.join(D, f'{key}-seg{i}sub{j}r{k}.mp3')
        with open(os.path.join(D, f'{key}-seg{i}sub{j}r{k}.txt'), 'w') as f:
            f.write(g)
        d = synth_qc(g, pm, f'seg{i}sub{j}r{k}', regen)
        if d is None:
            return None
        parts.append(pm)
        sub_stats.append({'sub': f'{j}r{k}', 'words': len(g.split()),
                          'dur': round(d, 2),
                          'wpm': round(len(g.split()) / d * 60)})
    sil = os.path.join(D, f'{key}-seg{i}sub{j}-a1sil.mp3')
    run(['ffmpeg', '-y', '-threads', '2', '-f', 'lavfi', '-i',
         'anullsrc=r=44100:cl=stereo:d=0.3',
         '-c:a', 'libmp3lame', '-b:a', '128k', sil], 'a1 sub silence')
    lst = os.path.join(D, f'{key}-seg{i}sub{j}-a1concat.txt')
    with open(lst, 'w') as f:
        for k, pm in enumerate(parts):
            f.write(f"file '{pm}'\n")
            if k < len(parts) - 1:
                f.write(f"file '{sil}'\n")
    run(['ffmpeg', '-y', '-threads', '2', '-f', 'concat', '-safe', '0',
         '-i', lst, '-c:a', 'libmp3lame', '-b:a', '192k', out_mp3],
        'a1 sub concat')
    with open(out_mp3 + '.txt', 'w') as f:
        f.write(text)
    return dur(out_mp3)


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
    a1_log = []
    for i, seg in enumerate(segs, 1):
        txt_path = os.path.join(D, f'{key}-seg{i}.txt')
        mp3 = os.path.join(D, f'{key}-seg{i}.mp3')
        with open(txt_path, 'w') as f:
            f.write(seg)
        words = len(seg.split())
        chosen = synth_qc(seg, mp3, f'seg{i}', regen)
        via = 'direct'
        if chosen is None:
            print(f'  seg{i}: direct takes failed QC -> applying A1 split',
                  flush=True)
            regen.append(f'seg{i} failed 3 direct attempts -> A1 split')
            chosen = synth_with_a1(key, i, seg, mp3, regen, a1_log)
            via = 'A1'
        if chosen is None:
            print(f'seg{i}: FAILED after retries and A1')
            raise SystemExit(1)
        seg_mp3s.append((mp3, chosen))
        seg_stats.append({'seg': i, 'label': labels[i - 1], 'words': words,
                          'dur': round(chosen, 2),
                          'wpm': round(words / chosen * 60), 'via': via})

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
        per_gap_room = MAX_GAP - gap
        gap_add = min(extra, per_gap_room * (n - 1))
        if n > 1 and gap_add > 0:
            gap += gap_add / (n - 1)
            extra -= gap_add
        if extra > 0:
            add = min(extra, MAX_TITLE - t_hold)
            t_hold += add
            extra -= add
        if extra > 0:
            add = min(extra, MAX_CLOSE - c_hold)
            c_hold += add
            extra -= add
        hold_note = (f'extended holds for duration gate: title {t_hold:.2f}s / '
                     f'gap {gap:.2f}s / closing {c_hold:.2f}s '
                     f'(standard 4.0 / 0.5 / 3.0; caps 12 / 2.5 / 10)')
        if extra > 0:
            hold_note += f' [WARNING: still {extra:.1f}s short at max holds]'
    if total_std > hi:
        hold_note += (f' [WARNING: standard-hold total {total_std:.1f}s '
                      f'exceeds window hi {hi:.0f}s]')
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

    intervals = []
    t = t_hold
    for j, (_, d) in enumerate(seg_mp3s):
        intervals.append([round(t, 2), round(t + d, 2)])
        t += d + gap
    slide_intervals = []
    t = 0.0
    for dsec in durations:
        slide_intervals.append([round(t, 2), round(t + dsec, 2)])
        t += dsec

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
    print('A1:', json.dumps(a1_log) if a1_log else 'none', flush=True)
    meta = {'lesson': key, 'file': cfg['out'], 'bytes': os.path.getsize(out_path),
            'duration': round(final, 2), 'target_min': cfg['target'],
            'window': [round(lo, 1), round(hi, 1)],
            'narration_sum': round(narr_sum, 2),
            'holds': {'title': round(t_hold, 2), 'gap': round(gap, 2),
                      'closing': round(c_hold, 2)},
            'hold_note': hold_note, 'segments': seg_stats,
            'regen': regen, 'a1': a1_log,
            'slide_durations': [round(x, 2) for x in durations],
            'intervals': intervals, 'slide_intervals': slide_intervals,
            'slides': cfg['slides'], 'norm_duration': round(norm_d, 2)}
    with open(os.path.join(D, f'{key}-build.json'), 'w') as f:
        json.dump(meta, f, indent=1)
    print('META saved', flush=True)
    return final


if __name__ == '__main__':
    build(sys.argv[1])
