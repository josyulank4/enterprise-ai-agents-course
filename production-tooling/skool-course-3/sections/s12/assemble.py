"""Assemble Skool Course 3, Section 12: slides + Aria narration -> 1920x1080 MP4s.

Replicates Course 2 s00 / Course 3 s01 assemble.py exactly, per
PRODUCTION-SPEC.md: title card = title hold + seg1 (+ trailing gap);
content slide i = seg_i + gap (last = seg_last + closing hold).
Authorized adaptation A1: if a segment deterministically fails segment QC
after 3 attempts, split its text VERBATIM at sentence boundaries into 2-3
sub-segments (recursively), synthesize each via the identical route, QC
each at the same gates, and concatenate with 0.3s silence.
Usage: python3 assemble.py l47 [title_hold gap closing_hold]
"""
import json
import os
import re
import subprocess
import sys

COURSE = os.path.expanduser('~/workspace/udemy-skool/skool-course-3-mcp-architecture')
D = os.path.join(COURSE, 'sections', 's12')
S = os.path.join(D, 'slides')
VIDEOS = os.path.join(COURSE, 'videos')
VOICE = 'avocado_v2:MAI_01'
SPEED = '77'
FPS = 30

LESSONS = {
    'l47': {
        'script': os.path.join(COURSE, 'scripts', 's12-l47.md'),
        'target': 11.0,
        'slides': ['l47-slide0-title.png', 'l47-slide1-directions.png',
                   'l47-slide2-hands.png', 'l47-slide3-verified.png',
                   'l47-slide4-boundary.png', 'l47-slide5-registry.png',
                   'l47-slide6-publishing.png', 'l47-slide7-patterns.png',
                   'l47-slide8-next.png'],
        'out': os.path.join(VIDEOS, 's12-l47-a2a-and-mcp-two-protocols-two-directions-2026-10.mp4'),
    },
    'l48': {
        'script': os.path.join(COURSE, 'scripts', 's12-l48.md'),
        'target': 11.0,
        'slides': ['l48-slide0-title.png', 'l48-slide1-consolidation.png',
                   'l48-slide2-trust.png', 'l48-slide3-identity.png',
                   'l48-slide4-roadmap.png', 'l48-slide5-contracts.png',
                   'l48-slide6-composition.png', 'l48-slide7-endures.png',
                   'l48-slide8-next.png'],
        'out': os.path.join(VIDEOS, 's12-l48-governance-trust-and-future-proofing-2026-10.mp4'),
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
    return d >= expected * 0.5 and 75 <= wpm <= 210, wpm, expected


def synth_qc(text, mp3, label, regen):
    """Synthesize one (sub-)segment with up to 3 attempts. Returns duration or None."""
    words = len(text.split())
    if os.path.exists(mp3) and os.path.getsize(mp3) > 0:
        d0 = dur(mp3)
        ok, wpm0, _ = qc_ok(words, d0)
        if ok:
            print(f'  {label}: reuse existing {d0:.1f}s ({wpm0:.0f} wpm)', flush=True)
            return d0
    for attempt in range(1, 4):
        tts(text, mp3)
        d = dur(mp3)
        ok, wpm, expected = qc_ok(words, d)
        print(f'  {label}: {words}w -> {d:.1f}s ({wpm:.0f} wpm), '
              f'expected ~{expected:.0f}s, attempt {attempt}, '
              f'{"OK" if ok else "BAD"}', flush=True)
        if ok:
            if attempt > 1:
                regen.append(f'{label} regenerated on attempt {attempt}')
            return d
        if attempt < 3:
            regen.append(f'{label} bad take discarded (attempt {attempt}: {d:.1f}s, {wpm:.0f} wpm)')
    return None


def split_sentences(text):
    """Split verbatim text into sentence units (split points only)."""
    flat = re.sub(r'\s+', ' ', text.strip())
    parts = re.split(r'(?<=[.!?])\s+', flat)
    return [p for p in parts if p.strip()]


def group_sentences(sents, n_groups):
    groups = [[] for _ in range(n_groups)]
    counts = [0] * n_groups
    for s in sents:
        i = counts.index(min(counts))
        groups[i].append(s)
        counts[i] += len(s.split())
    # preserve order: groups were filled greedily; instead do sequential chunking
    total = sum(len(s.split()) for s in sents)
    groups = []
    cur, cur_w, target = [], 0, total / n_groups
    for s in sents:
        w = len(s.split())
        if cur and cur_w + w > target and len(groups) < n_groups - 1:
            groups.append(cur)
            cur, cur_w = [], 0
        cur.append(s)
        cur_w += w
    if cur:
        groups.append(cur)
    return [' '.join(g) for g in groups]


def a1_build(key, i, seg, regen, a1_log):
    """A1: split failing beat verbatim into sub-segments, QC each, concat w/ 0.3s silence."""
    sents = split_sentences(seg)
    for n_groups in (2, 3):
        subs = group_sentences(sents, n_groups)
        # recursive guard: if a sub is still long, it gets its own QC + retry below
        sub_mp3s = []
        ok_all = True
        sub_stats = []
        for m, sub in enumerate(subs, 1):
            mp3 = os.path.join(D, f'{key}-seg{i}-part{m}.mp3')
            txt_path = os.path.join(D, f'{key}-seg{i}-part{m}.txt')
            with open(txt_path, 'w') as f:
                f.write(sub)
            d = synth_qc(sub, mp3, f'seg{i}.part{m} (A1)', regen)
            if d is None:
                # recursive split of this sub-segment into 2
                ss = split_sentences(sub)
                if len(ss) < 2:
                    ok_all = False
                    break
                deep = group_sentences(ss, 2)
                deep_mp3s = []
                for q, dsub in enumerate(deep, 1):
                    dmp3 = os.path.join(D, f'{key}-seg{i}-part{m}-{q}.mp3')
                    with open(dmp3 + '.txt', 'w') as f:
                        f.write(dsub)
                    dd = synth_qc(dsub, dmp3, f'seg{i}.part{m}.{q} (A1-deep)', regen)
                    if dd is None:
                        ok_all = False
                        break
                    deep_mp3s.append((dmp3, dd))
                if not ok_all:
                    break
                # concat deep parts with 0.3s silence
                sil03 = os.path.join(D, f'{key}-sil03.mp3')
                if not os.path.exists(sil03):
                    run(['ffmpeg', '-y', '-threads', '2', '-f', 'lavfi', '-i',
                         'anullsrc=r=44100:cl=stereo:d=0.3',
                         '-c:a', 'libmp3lame', '-b:a', '128k', sil03], 'sil 0.3')
                lst = os.path.join(D, f'{key}-seg{i}-part{m}-concat.txt')
                with open(lst, 'w') as f:
                    for j, (p, _) in enumerate(deep_mp3s):
                        f.write(f"file '{p}'\n")
                        if j < len(deep_mp3s) - 1:
                            f.write(f"file '{sil03}'\n")
                run(['ffmpeg', '-y', '-threads', '2', '-f', 'concat', '-safe', '0',
                     '-i', lst, '-c:a', 'libmp3lame', '-b:a', '128k', mp3], 'A1 deep concat')
                d = dur(mp3)
                sub_stats.append({'part': f'{m} (deep x2)', 'words': len(sub.split()),
                                  'duration': round(d, 2)})
            else:
                sub_stats.append({'part': m, 'words': len(sub.split()),
                                  'duration': round(d, 2),
                                  'wpm': round(len(sub.split()) / d * 60, 1)})
            sub_mp3s.append(mp3)
        if not ok_all:
            continue
        sil03 = os.path.join(D, f'{key}-sil03.mp3')
        if not os.path.exists(sil03):
            run(['ffmpeg', '-y', '-threads', '2', '-f', 'lavfi', '-i',
                 'anullsrc=r=44100:cl=stereo:d=0.3',
                 '-c:a', 'libmp3lame', '-b:a', '128k', sil03], 'sil 0.3')
        lst = os.path.join(D, f'{key}-seg{i}-a1concat.txt')
        with open(lst, 'w') as f:
            for j, p in enumerate(sub_mp3s):
                f.write(f"file '{p}'\n")
                if j < len(sub_mp3s) - 1:
                    f.write(f"file '{sil03}'\n")
        combined = os.path.join(D, f'{key}-seg{i}.mp3')
        run(['ffmpeg', '-y', '-threads', '2', '-f', 'concat', '-safe', '0',
             '-i', lst, '-c:a', 'libmp3lame', '-b:a', '128k', combined], 'A1 concat')
        d = dur(combined)
        a1_log.append({'seg': i, 'groups': n_groups, 'sub_stats': sub_stats,
                       'combined_duration': round(d, 2)})
        print(f'  seg{i}: A1 combined {d:.1f}s from {n_groups} sub-segments', flush=True)
        return d
    return None


def split_script(path):
    raw = open(path).read()
    parts = re.split(r'\*\*\[Slide \d+ [^\]]*\]\*\*', raw)
    segs = []
    for p in parts[1:]:
        seg = p.strip().replace('**', '')
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
    a1_log = []
    for i, seg in enumerate(segs, 1):
        txt_path = os.path.join(D, f'{key}-seg{i}.txt')
        mp3 = os.path.join(D, f'{key}-seg{i}.mp3')
        with open(txt_path, 'w') as f:
            f.write(seg)
        words = len(seg.split())
        chosen = synth_qc(seg, mp3, f'seg{i}', regen)
        if chosen is None:
            print(f'  seg{i}: standard route failed 3 attempts -> applying A1', flush=True)
            chosen = a1_build(key, i, seg, regen, a1_log)
            if chosen is None:
                print(f'seg{i}: FAILED after retries and A1')
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
    print('A1:', json.dumps(a1_log) if a1_log else 'none')
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
    meta = {'final': round(final, 3), 'stats': stats, 'regen': regen, 'a1': a1_log,
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
