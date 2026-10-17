"""Assemble Skool Course 3, Section 5: slides + Aria narration -> 1920x1080 MP4s.

Lessons l18-l21. Pattern replicated from Course 3 s04 assemble.py
(Course 2 s00 pattern), per PRODUCTION-SPEC.md. Includes Authorized
adaptation A1: if a segment deterministically fails segment QC after
3 attempts, split its text VERBATIM at sentence boundaries into 2-3
sub-segments, QC each identically, concat with 0.3s silence.
Usage: python3 assemble.py [l18|l19|l20|l21]
"""
import json
import os
import re
import subprocess
import sys

COURSE = os.path.expanduser(
    '~/workspace/udemy-skool/skool-course-3-mcp-architecture')
D = os.path.join(COURSE, 'sections', 's05')
S = os.path.join(D, 'slides')
VIDEOS = os.path.join(COURSE, 'videos')
VOICE = 'avocado_v2:MAI_01'
SPEED = '77'
FPS = 30
GAP = 0.5
TITLE_HOLD = 4.0
CLOSING_HOLD = 3.0
MAX_TITLE, MAX_GAP, MAX_CLOSE = 12.0, 2.5, 10.0

LESSONS = {
    'l18': {
        'script': 's05-l18.md', 'target': 12.0,
        'slides': ['l18-slide0-title.png', 'l18-slide1-control.png',
                   'l18-slide2-error.png', 'l18-slide3-uris.png',
                   'l18-slide4-templates.png', 'l18-slide5-subscriptions.png',
                   'l18-slide6-never-act.png', 'l18-slide7-first-pass.png',
                   'l18-slide8-handson.png', 'l18-slide9-next.png'],
        'out': 's05-l18-three-control-models-and-resources-in-depth-2026-10.mp4',
    },
    'l19': {
        'script': 's05-l19.md', 'target': 11.0,
        'slides': ['l19-slide0-title.png', 'l19-slide1-granularity.png',
                   'l19-slide2-schemas.png', 'l19-slide3-output.png',
                   'l19-slide4-errors.png', 'l19-slide5-annotations.png',
                   'l19-slide6-naming.png', 'l19-slide7-handson.png',
                   'l19-slide8-next.png'],
        'out': 's05-l19-tools-in-depth-2026-10.mp4',
    },
    'l20': {
        'script': 's05-l20.md', 'target': 11.0,
        'slides': ['l20-slide0-title.png', 'l20-slide1-rituals.png',
                   'l20-slide2-template.png', 'l20-slide3-opinionated.png',
                   'l20-slide4-versus.png', 'l20-slide5-warning.png',
                   'l20-slide6-versioning.png', 'l20-slide7-handson.png',
                   'l20-slide8-next.png'],
        'out': 's05-l20-prompts-in-depth-2026-10.mp4',
    },
    'l21': {
        'script': 's05-l21.md', 'target': 12.0,
        'slides': ['l21-slide0-title.png', 'l21-slide1-roots.png',
                   'l21-slide2-sampling.png', 'l21-slide3-risks.png',
                   'l21-slide4-pagination.png', 'l21-slide5-completion.png',
                   'l21-slide6-boundaries12.png', 'l21-slide7-boundaries34.png',
                   'l21-slide8-handson.png', 'l21-slide9-next.png'],
        'out': 's05-l21-roots-sampling-pagination-and-clean-boundaries-2026-10.mp4',
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


def qc_ok(words, d):
    expected = words / 135.0 * 60.0
    wpm = words / d * 60 if d > 0 else 0
    return d >= expected * 0.5 and 75 <= wpm <= 210, wpm


def synth_qc(text, mp3, tag, regen):
    """Synthesize with up to 3 attempts under segment QC. Returns dur or None."""
    words = len(text.split())
    if os.path.exists(mp3) and os.path.getsize(mp3) > 0:
        sidecar = mp3 + '.txt'
        if os.path.exists(sidecar) and open(sidecar).read() == text:
            d0 = dur(mp3)
            ok, wpm0 = qc_ok(words, d0)
            if ok:
                print(f'  {tag}: reuse existing {d0:.1f}s ({wpm0:.0f} wpm)', flush=True)
                return d0
    for attempt in range(1, 4):
        tts(text, mp3)
        d = dur(mp3)
        ok, wpm = qc_ok(words, d)
        print(f'  {tag}: {words}w -> {d:.1f}s ({wpm:.0f} wpm), '
              f'attempt {attempt}, {"OK" if ok else "BAD"}', flush=True)
        if ok:
            if attempt > 1:
                regen.append(f'{tag} regenerated on attempt {attempt}')
            return d
        if attempt < 3:
            regen.append(f'{tag} bad take discarded (attempt {attempt}: {d:.1f}s, {wpm:.0f} wpm)')
    return None


def split_sentences(text, nchunks):
    sents = re.split(r'(?<=[.!?])\s+', text)
    sents = [s for s in sents if s.strip()]
    if len(sents) <= 1:
        return [text]
    # group sentences into nchunks balanced by word count
    total = sum(len(s.split()) for s in sents)
    target = total / nchunks
    chunks, cur, curw = [], [], 0
    for s in sents:
        w = len(s.split())
        if cur and curw + w > target and len(chunks) < nchunks - 1:
            chunks.append(' '.join(cur))
            cur, curw = [s], w
        else:
            cur.append(s)
            curw += w
    if cur:
        chunks.append(' '.join(cur))
    return chunks


def apply_a1(key, i, seg, mp3, regen):
    """Authorized adaptation A1. Returns (combined_dur, a1_record) or (None, record)."""
    words = len(seg.split())
    nchunks = 2 if words <= 130 else 3
    chunks = split_sentences(seg, nchunks)
    if len(chunks) < 2:
        return None, {'seg': i, 'error': 'no sentence boundary to split'}
    assert ' '.join(chunks) == seg, 'A1 split must be verbatim'
    sub_stats = []
    sub_mp3s = []
    for k, chunk in enumerate(chunks, 1):
        sub_mp3 = os.path.join(D, f'{key}-seg{i}sub{k}.mp3')
        txt_path = os.path.join(D, f'{key}-seg{i}sub{k}.txt')
        with open(txt_path, 'w') as f:
            f.write(chunk)
        d = synth_qc(chunk, sub_mp3, f'seg{i}sub{k}', regen)
        if d is None and len(chunk.split()) > 65:
            # recursive split of this sub-segment in 2
            parts = split_sentences(chunk, 2)
            if len(parts) >= 2 and ' '.join(parts) == chunk:
                part_mp3s, part_stats, okflag = [], [], True
                for m, part in enumerate(parts, 1):
                    pm = os.path.join(D, f'{key}-seg{i}sub{k}p{m}.mp3')
                    with open(os.path.join(D, f'{key}-seg{i}sub{k}p{m}.txt'), 'w') as f:
                        f.write(part)
                    pd_ = synth_qc(part, pm, f'seg{i}sub{k}p{m}', regen)
                    if pd_ is None:
                        okflag = False
                        break
                    part_mp3s.append(pm)
                    part_stats.append({'words': len(part.split()), 'dur': round(pd_, 2),
                                       'wpm': round(len(part.split()) / pd_ * 60)})
                if okflag:
                    d = concat_with_silence(part_mp3s, sub_mp3, f'{key}-seg{i}sub{k}')
                    sub_stats.append({'sub': k, 'words': len(chunk.split()),
                                      'dur': round(d, 2), 'recursive_split': part_stats})
                    sub_mp3s.append(sub_mp3)
                    continue
            return None, {'seg': i, 'error': f'sub{k} failed QC'}
        if d is None:
            return None, {'seg': i, 'error': f'sub{k} failed QC'}
        sub_stats.append({'sub': k, 'words': len(chunk.split()), 'dur': round(d, 2),
                          'wpm': round(len(chunk.split()) / d * 60)})
        sub_mp3s.append(sub_mp3)
    combined = concat_with_silence(sub_mp3s, mp3, f'{key}-seg{i}')
    # sidecar for the combined segment must hold the full verbatim text
    with open(mp3 + '.txt', 'w') as f:
        f.write(seg)
    rec = {'seg': i, 'words': words, 'combined_dur': round(combined, 2),
           'combined_wpm': round(words / combined * 60), 'subs': sub_stats,
           'note': 'VERBATIM text split at sentence boundaries; 0.3s silence joins'}
    print(f'  A1 seg{i}: combined {combined:.1f}s ({words / combined * 60:.0f} wpm)', flush=True)
    return combined, rec


def concat_with_silence(mp3s, out_mp3, tag):
    sil = os.path.join(D, f'{tag}-sil03.mp3')
    run(['ffmpeg', '-y', '-threads', '2', '-f', 'lavfi', '-i',
         'anullsrc=r=44100:cl=stereo:d=0.3',
         '-c:a', 'libmp3lame', '-b:a', '128k', sil], 'a1 silence')
    lst = os.path.join(D, f'{tag}-a1concat.txt')
    with open(lst, 'w') as f:
        for j, m in enumerate(mp3s):
            f.write(f"file '{m}'\n")
            if j < len(mp3s) - 1:
                f.write(f"file '{sil}'\n")
    run(['ffmpeg', '-y', '-threads', '2', '-f', 'concat', '-safe', '0',
         '-i', lst, '-c:a', 'libmp3lame', '-b:a', '128k', out_mp3], 'a1 concat')
    return dur(out_mp3)


def parse_script(path):
    raw = open(path).read()
    parts = re.split(r'\*\*\[Slide (\d+) \u2014 (.*?)\]\*\*', raw)
    segs, labels = [], []
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
    seg_mp3s, regen, seg_stats, a1_records = [], [], [], []
    for i, seg in enumerate(segs, 1):
        txt_path = os.path.join(D, f'{key}-seg{i}.txt')
        mp3 = os.path.join(D, f'{key}-seg{i}.mp3')
        with open(txt_path, 'w') as f:
            f.write(seg)
        words = len(seg.split())
        chosen = synth_qc(seg, mp3, f'seg{i}', regen)
        a1 = None
        if chosen is None:
            print(f'  seg{i}: 3 attempts failed -> applying A1 split', flush=True)
            chosen, a1 = apply_a1(key, i, seg, mp3, regen)
            if a1:
                a1_records.append(a1)
            if chosen is None:
                print(f'seg{i}: FAILED even after A1')
                raise SystemExit(1)
            regen.append(f'seg{i} built via A1 split (see manifest)')
        seg_mp3s.append((mp3, chosen))
        st = {'seg': i, 'label': labels[i - 1], 'words': words,
              'dur': round(chosen, 2), 'wpm': round(words / chosen * 60)}
        if a1:
            st['a1'] = a1
        seg_stats.append(st)

    n = len(seg_mp3s)
    narr_sum = sum(d for _, d in seg_mp3s)
    target_s = cfg['target'] * 60
    lo, hi = target_s * 0.9, target_s * 1.1
    t_hold, gap, c_hold = TITLE_HOLD, GAP, CLOSING_HOLD
    total_std = t_hold + narr_sum + gap * (n - 1) + c_hold
    hold_note = 'standard holds (title 4.0 / gap 0.5 / closing 3.0)'
    blocked = None
    if narr_sum > hi:
        blocked = (f'narration alone {narr_sum:.1f}s exceeds target x1.10 ({hi:.0f}s)')
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
    total_planned = t_hold + narr_sum + gap * (n - 1) + c_hold
    print(f'narration sum {narr_sum:.1f}s; planned total {total_planned:.1f}s '
          f'(window {lo:.0f}-{hi:.0f})', flush=True)
    print('holds:', hold_note, flush=True)
    if blocked:
        print('BLOCKER:', blocked, flush=True)

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
            'regen': regen, 'a1': a1_records, 'blocker': blocked,
            'slide_durations': [round(x, 2) for x in durations],
            'intervals': intervals, 'norm_duration': round(norm_d, 2)}
    with open(os.path.join(D, f'{key}-build.json'), 'w') as f:
        json.dump(meta, f, indent=1)
    print('META saved', flush=True)
    return final


if __name__ == '__main__':
    build(sys.argv[1])
