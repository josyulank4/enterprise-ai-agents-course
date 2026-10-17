"""QC per lesson video (Course 3 s10): streams, decode, blackdetect,
loudness, duration vs target, 7 QC frames at ~8/22/36/50/64/78/92%."""
import json
import os
import re
import subprocess
import sys

COURSE = os.path.expanduser('~/workspace/udemy-skool/skool-course-3-mcp-architecture')
D = os.path.join(COURSE, 'sections', 's10')
VIDEOS = os.path.join(COURSE, 'videos')
QC = os.path.join(D, 'qc')
os.makedirs(QC, exist_ok=True)

TARGETS = {
    'l39': ('s10-l39-testing-mcp-servers-like-apis-unit-tests-2026-10.mp4', 10.0),
    'l40': ('s10-l40-contract-testing-schemas-and-error-shapes-2026-10.mp4', 11.0),
    'l41': ('s10-l41-integration-testing-real-and-mock-clients-2026-10.mp4', 11.0),
    'l42': ('s10-l42-adversarial-testing-and-regression-suites-2026-10.mp4', 12.0),
}

SLIDES = {
    'l39': ['Title: Testing MCP Servers Like APIs',
            'An API with an unusual consumer',
            'Deterministic core, probabilistic shell',
            'Isolate the handler from the transport',
            'Happy path, boundaries, and hostile inputs',
            'Error paths, side effects, and slow dependencies',
            'Hands-on and next: contract testing'],
    'l40': ['Title: The Contract Is the Advertisement',
            'Promises a model actually reads',
            'Input schemas: snapshot everything',
            'Output shapes: golden fixtures, structural checks',
            'Error shapes are contract, too',
            'Schema evolution: what is safe, what is a version event',
            'Hands-on and next: real and mock clients'],
    'l41': ['Title: Prove the Whole Assembly Works',
            'Real clients reveal the compatibility surface',
            'Mock clients: politeness is not a test strategy',
            'The honest test matrix',
            'Environments: seeded, replayed, never production',
            'Keep the results as a report, not a memory',
            'Hands-on and next: adversarial testing'],
    'l42': ['Title: Test the Defences, Then Lock Behaviour In',
            'Hostile language inside legitimate output',
            "Half one: test your server's hygiene, no model needed",
            'Half two: model-in-the-loop, measured statistically',
            'Keep the corpus honest, and growing',
            'Fuzz the outputs the model will meet',
            'Regression: replay, properties, and golden conversations',
            'Hands-on and next: observability in production'],
}


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def dur(p):
    return float(run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                      '-of', 'csv=p=0', p]).stdout.strip())


def check(key):
    fname, target_min = TARGETS[key]
    path = os.path.join(VIDEOS, fname)
    print('====', fname, '====', flush=True)
    if not os.path.exists(path):
        print('MISSING')
        return
    print('bytes:', os.path.getsize(path))
    d = dur(path)
    lo, hi = target_min * 0.9 * 60, target_min * 1.1 * 60
    print(f'duration {d:.1f}s = {d/60:.2f} min (target {target_min} min, '
          f'window {lo:.0f}-{hi:.0f}s) -> {"OK" if lo <= d <= hi else "FAIL"}')

    r = run(['ffmpeg', '-v', 'error', '-threads', '2', '-i', path, '-f', 'null', '-'])
    dec = r.stderr.strip()
    print('decode:', 'ZERO ERRORS' if not dec else f'FAIL: {dec[:500]}')

    r = run(['ffmpeg', '-hide_banner', '-threads', '2', '-i', path, '-vf',
             'blackdetect=d=0.5:pix_th=0.10', '-an', '-f', 'null', '-'])
    blacks = [l for l in r.stderr.splitlines() if 'black_start' in l]
    print('blackdetect:', 'CLEAN' if not blacks else f'FAIL: {blacks}')

    sv = run(['ffprobe', '-v', 'error', '-select_streams', 'v:0',
              '-show_entries', 'stream=codec_name,width,height,avg_frame_rate',
              '-of', 'csv=p=0', path]).stdout.strip()
    sa = run(['ffprobe', '-v', 'error', '-select_streams', 'a:0',
              '-show_entries', 'stream=codec_name,sample_rate,channels',
              '-of', 'csv=p=0', path]).stdout.strip()
    print('video stream:', sv)
    print('audio stream:', sa)

    r = run(['ffmpeg', '-hide_banner', '-threads', '2', '-i', path, '-af',
             'loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json', '-vn', '-f', 'null', '-'])
    m = re.search(r'\{\s*"input_i".*?\}', r.stderr, re.S)
    if m:
        j = json.loads(m.group(0))
        print(f"loudness: integrated {j['input_i']} LUFS, true peak {j['input_tp']} dBTP")
    else:
        print('loudness: MEASURE FAILED')

    for i in range(7):
        t = d * [0.08, 0.22, 0.36, 0.50, 0.64, 0.78, 0.92][i]
        out = os.path.join(QC, f'{key}-qcframe{i+1}-t{int(t)}s.png')
        run(['ffmpeg', '-y', '-v', 'error', '-ss', str(t), '-i', path,
             '-frames:v', '1', out])
        print(f'  frame {i+1} @ {t:.1f}s -> {os.path.basename(out)}')


if __name__ == '__main__':
    keys = [sys.argv[1]] if len(sys.argv) > 1 else list(TARGETS)
    for k in keys:
        check(k)
