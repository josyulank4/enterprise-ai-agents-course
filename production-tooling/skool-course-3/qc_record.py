"""Full-QC record writer for Skool Course 3 sections whose qc_check.py only
prints gates (s09-s13 variant): re-measures every gate from the lesson final
(streams, duration vs the section TARGETS window, full decode, blackdetect,
loudnorm) and computes the 7-frame slide/narration sync from the lesson's
build-meta (slide_durations + per-segment durations + holds — the same
method as sections/s04/qc_check.py), then writes sections/<s>/<l>-qc.json
in the variant-A schema production-chain4.sh passed() reads.

The record states the MEASURED truth: failing gates are written as failing.
Usage: python3 qc_record.py <section> <lesson>   e.g. python3 qc_record.py s09 l37
"""
import json
import os
import re
import subprocess
import sys

COURSE = os.path.expanduser(
    '~/workspace/udemy-skool/skool-course-3-mcp-architecture')
PCTS = [0.08, 0.22, 0.36, 0.50, 0.64, 0.78, 0.92]


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def dur(p):
    return float(run(['ffprobe', '-v', 'error', '-show_entries',
                      'format=duration', '-of', 'csv=p=0',
                      p]).stdout.strip())


def main():
    sec, key = sys.argv[1], sys.argv[2]
    D = os.path.join(COURSE, 'sections', sec)
    qc_src = open(os.path.join(D, 'qc_check.py')).read()
    m = re.search(r"'%s':\s*\('([^']+)',\s*([\d.]+)\)" % key, qc_src)
    if not m:
        print(f'qc_record: {key} not in {sec} TARGETS')
        return 1
    fname, target_min = m.group(1), float(m.group(2))
    meta = json.load(open(os.path.join(D, f'{key}-build-meta.json')))
    path = meta.get('out') or os.path.join(COURSE, 'videos', fname)
    if not os.path.exists(path):
        print(f'qc_record: MISSING final {path}')
        return 1
    res = {'lesson': key, 'file': os.path.basename(path),
           'bytes': os.path.getsize(path)}
    d = dur(path)
    res['duration'] = round(d, 2)
    lo, hi = target_min * 0.9 * 60, target_min * 1.1 * 60
    res['duration_ok'] = bool(lo <= d <= hi)
    print(f"duration {d:.1f}s window {lo:.0f}-{hi:.0f} -> "
          f"{'OK' if res['duration_ok'] else 'FAIL'}", flush=True)

    res['video_stream'] = run(
        ['ffprobe', '-v', 'error', '-select_streams', 'v:0',
         '-show_entries', 'stream=codec_name,width,height,avg_frame_rate',
         '-of', 'csv=p=0', path]).stdout.strip()
    res['audio_stream'] = run(
        ['ffprobe', '-v', 'error', '-select_streams', 'a:0',
         '-show_entries', 'stream=codec_name,sample_rate,channels',
         '-of', 'csv=p=0', path]).stdout.strip()

    r = run(['ffmpeg', '-v', 'error', '-threads', '2', '-i', path,
             '-f', 'null', '-'])
    res['decode_ok'] = not r.stderr.strip()
    print('decode:', 'ZERO ERRORS' if res['decode_ok'] else 'FAIL',
          flush=True)

    r = run(['ffmpeg', '-hide_banner', '-threads', '2', '-i', path, '-vf',
             'blackdetect=d=0.5:pix_th=0.10', '-an', '-f', 'null', '-'])
    blacks = [l for l in r.stderr.splitlines() if 'black_start' in l]
    res['blackdetect_clean'] = not blacks
    print('blackdetect:', 'CLEAN' if not blacks else 'FAIL', flush=True)

    r = run(['ffmpeg', '-hide_banner', '-threads', '2', '-i', path, '-vn',
             '-af', 'loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json',
             '-f', 'null', '-'])
    mi = re.search(r'"input_i"\s*:\s*"([-\d.]+)"', r.stderr)
    mt = re.search(r'"input_tp"\s*:\s*"([-\d.]+)"', r.stderr)
    if mi and mt:
        res['loudness_i'] = float(mi.group(1))
        res['loudness_tp'] = float(mt.group(1))
    print(f"loudness: I={res.get('loudness_i')} TP={res.get('loudness_tp')}",
          flush=True)

    # frames + sync from build-meta (s04 method): slide k spans
    # slide_durations[k]; segment k+1 narrates inside slide k, starting after
    # the title hold on slide 0; slide k carries segment k+1 + trailing gap.
    sdurs = meta['slide_durations']
    stats = meta['stats']
    title_hold = float(meta['holds'][0])
    bounds, acc = [], 0.0
    for sd in sdurs:
        bounds.append((acc, acc + sd))
        acc += sd
    frames = []
    countable = len(stats) == len(sdurs)
    for i, pc in enumerate(PCTS):
        t = d * pc
        slide_idx = next(j for j, (a, b) in enumerate(bounds) if a <= t < b)
        seg_idx, where, sync = None, 'silence/gap', False
        if countable:
            for j, (a, b) in enumerate(bounds):
                s0 = a + (title_hold if j == 0 else 0.0)
                if s0 <= t < s0 + float(stats[j]['duration']):
                    seg_idx, where = j, f'seg{j + 1}'
                    break
            sync = seg_idx is not None and seg_idx == slide_idx
        frames.append({'n': i + 1, 't': round(t, 1),
                       'file': f'{key}-qcframe{i + 1}-t{int(t)}s.png',
                       'slide_idx': slide_idx + 1,
                       'narrating': where, 'sync': bool(sync)})
        print(f"  frame {i + 1} @ {t:.1f}s slide{slide_idx + 1} "
              f"narrating {where} -> {'SYNC' if sync else 'CHECK'}",
              flush=True)
    res['frames'] = frames
    res['record_basis'] = ('qc_record.py full re-measurement 2026-10-17; '
                           'sync computed from build-meta slide_durations/'
                           'stats/holds (s04 method)')
    out = os.path.join(D, f'{key}-qc.json')
    with open(out, 'w') as f:
        json.dump(res, f, indent=1)
    print(f'QC json saved: {out}', flush=True)
    return 0


if __name__ == '__main__':
    sys.exit(main())
