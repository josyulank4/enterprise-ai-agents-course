"""Slide builder for Skool Course 3, Section 10 (Lessons 39-42).

Visual system copied from Course 2 s00 / Course 3 s08 build_slides.py:
dark navy BG #0e1a2b, gold #e0a83c, white, grey #b8c4d4, card #16283f,
DejaVu Sans, 1920x1080, gold rule near top, footer centered at bottom.
Footer: MCP ARCHITECTURE - BUILDING TOOL-USING AI SYSTEMS
One title card + one content slide per remaining beat, per lesson.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import os

D = os.path.expanduser(
    '~/workspace/udemy-skool/skool-course-3-mcp-architecture/sections/s10/slides')
os.makedirs(D, exist_ok=True)

BG = '#0e1a2b'
GOLD = '#e0a83c'
WHITE = '#ffffff'
GREY = '#b8c4d4'
CARD = '#16283f'
W, H = 19.2, 10.8
FONT = 'DejaVu Sans'
FOOTER = 'MCP ARCHITECTURE \u00b7 BUILDING TOOL-USING AI SYSTEMS'


def base():
    fig, ax = plt.subplots(figsize=(W, H), dpi=100)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(0, W)
    ax.set_ylim(0, H)
    ax.axis('off')
    ax.add_patch(FancyBboxPatch((0.6, H - 0.75), W - 1.2, 0.06,
                                boxstyle='round,pad=0.01', facecolor=GOLD,
                                edgecolor='none'))
    ax.text(W / 2, 0.55, FOOTER, color=GREY, fontsize=17, ha='center',
            va='center', family=FONT)
    return fig, ax


def heading(ax, text, sub=None, size=50):
    ax.text(W / 2, 9.3, text, color=WHITE, fontsize=size, ha='center',
            va='center', weight='bold', family=FONT)
    if sub:
        ax.text(W / 2, 8.35, sub, color=GOLD, fontsize=30, ha='center',
                va='center', family=FONT)


def card(ax, x, y, w, h, title, lines, title_size=28, line_size=23):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                                boxstyle='round,pad=0.08,rounding_size=0.25',
                                facecolor=CARD, edgecolor=GOLD, linewidth=1.5))
    ax.text(x + w / 2, y + h - 0.78, title, color=GOLD, fontsize=title_size,
            ha='center', va='center', weight='bold', family=FONT)
    yy = y + h - 1.78
    for ln in lines:
        ax.text(x + w / 2, yy, ln, color=WHITE, fontsize=line_size,
                ha='center', va='center', family=FONT)
        yy -= 0.64


def cards3(ax, specs):
    for x, spec in zip((1.0, 6.95, 12.9), specs):
        card(ax, x, 3.05, 5.3, 4.35, spec[0], spec[1], title_size=23, line_size=22)


def cards2(ax, specs):
    for x, spec in zip((1.6, 10.2), specs):
        card(ax, x, 3.05, 7.4, 4.35, spec[0], spec[1])


def bottomline(ax, text, size=28):
    ax.text(W / 2, 1.95, text, color=GOLD, fontsize=size, ha='center',
            va='center', weight='bold', family=FONT)


def save(fig, name):
    fig.savefig(os.path.join(D, name), facecolor=BG)
    plt.close(fig)
    print('saved', name)


def title_card(name, section_line, title_lines):
    fig, ax = base()
    ax.text(W / 2, 7.65, 'MCP ARCHITECTURE', color=WHITE, fontsize=80,
            ha='center', va='center', weight='bold', family=FONT)
    ax.text(W / 2, 6.35, 'Building Tool-Using AI Systems',
            color=GOLD, fontsize=42, ha='center', va='center', family=FONT)
    ax.text(W / 2, 4.85, section_line, color=GREY, fontsize=34,
            ha='center', va='center', family=FONT)
    yy = 3.95
    for tl in title_lines:
        ax.text(W / 2, yy, tl, color=WHITE, fontsize=36,
                ha='center', va='center', family=FONT)
        yy -= 0.70
    ax.text(W / 2, 1.85, 'Naveen Kumar Josyula', color=GREY, fontsize=30,
            ha='center', va='center', family=FONT)
    save(fig, name)


# ================= LESSON 39 =================
title_card('l39-slide0-title.png', 'Section 10  \u00b7  Lesson 39',
           ['Testing MCP Servers', 'Like APIs: Unit Tests'])

fig, ax = base()
heading(ax, 'An API, Unusual Consumer', 'not a thin script \u2014 a production API', size=44)
cards3(ax, [
    ('Not a Thin Script', ['Reachable by agents', 'acting in production', 'Treat it as an API']),
    ('Model Reads Schema', ['Field name drifts', 'Invents a mapping', 'Downstream harm']),
    ('Pyramid Still Applies', ['Unit, contract,', 'integration testing', '+ adversarial (L42)']),
])
bottomline(ax, 'Untested tools fail in production conversations.', size=26)
save(fig, 'l39-slide1-unusual.png')

fig, ax = base()
heading(ax, 'Deterministic Core,', 'probabilistic shell', size=46)
cards3(ax, [
    ('Pure Determinism', ['Same args + deps', 'Same result or error', 'Every single time']),
    ('Model: Probabilistic', ['Picks tool + args', 'From descriptions', 'Measured over runs']),
    ('Keep Layers Apart', ['Handler bug looks', 'like model confusion', 'Keep them separate']),
])
bottomline(ax, 'Each failure tells you exactly where to go.', size=27)
save(fig, 'l39-slide2-core.png')

fig, ax = base()
heading(ax, 'Isolate the Handler', 'from the transport', size=46)
cards3(ax, [
    ('Plain Function', ['Validated args in', 'Domain object out', 'Or structured error']),
    ('Inject Dependencies', ['Database, HTTP, files', 'Injected, never global', 'Nothing hidden']),
    ('Thin Adapter', ['Parses + serialises', 'Generic, per-tool free', 'No unit tests needed']),
])
bottomline(ax, 'Build it that way: testing becomes boring.', size=27)
save(fig, 'l39-slide3-isolate.png')

fig, ax = base()
heading(ax, 'Happy, Boundaries, Hostile', 'the unit-test case set', size=42)
cards3(ax, [
    ('Happy Path', ['Known customer', 'Fixture-backed repo', 'Exact orders returned']),
    ('Boundaries', ['Empty string', '100k-char string', 'Impossible date']),
    ('Hostile Inputs', ['Every schema edge', 'from Lesson 15', 'Becomes a test case']),
])
bottomline(ax, 'Test your logic, not the framework plumbing.', size=27)
save(fig, 'l39-slide4-cases.png')

fig, ax = base()
heading(ax, 'Error Paths + Side Effects', 'test them at least as hard', size=42)
cards3(ax, [
    ('Error Paths First', ['Agent explores edges', 'Errors seen most often', 'Test as hard as happy']),
    ('Test via Fakes', ['Fake the dependency', 'Assert what fake got', 'Exact request shape']),
    ('Slow or Down?', ['Pin timeout behaviour', 'Structured error', 'Retryable + hint']),
])
bottomline(ax, 'No refactor may silently degrade recovery.', size=27)
save(fig, 'l39-slide5-errors.png')

fig, ax = base()
heading(ax, 'Hands-On + Next', 'one clean failure', size=46)
cards3(ax, [
    ('Write the Suite', ['S10 unit suite', 'Sample tool', 'Happy, bounds, hostile']),
    ('Planted Bug Test', ['Fails exactly', 'one test', 'That is the signature']),
    ('Next Lesson', ['Contract Testing', 'Schemas and', 'Error Shapes']),
])
bottomline(ax, 'Unit tests prove handlers. Contracts prove promises.', size=25)
save(fig, 'l39-slide6-next.png')

# ================= LESSON 40 =================
title_card('l40-slide0-title.png', 'Section 10  \u00b7  Lesson 40',
           ['Contract Testing:', 'Schemas and Error Shapes'])

fig, ax = base()
heading(ax, 'Promises a Model Reads', 'the contract, precisely', size=46)
cards3(ax, [
    ('What Is Declared', ['What server supports', 'Promised up front', 'Verified by tests']),
    ('Schemas + Outputs', ['Inputs accepted', 'Output shapes', 'the model receives']),
    ('Error Responses', ['What model should do', 'when things go wrong', 'Part of contract']),
])
bottomline(ax, 'Advertisement and reality: same, or it is a bug.', size=26)
save(fig, 'l40-slide1-promises.png')

fig, ax = base()
heading(ax, 'Input Schemas: Snapshot', 'snapshot everything', size=44)
cards3(ax, [
    ('Snapshot in Git', ['Serialise each schema', 'Store under', 'version control']),
    ('Any Change Fails', ['Renamed property', 'Tightened values', 'New required field']),
    ('Reviewed Breaks', ['Diff in the PR', 'Say it out loud', 'Migration stated']),
])
bottomline(ax, 'The cheapest incident prevention you will buy.', size=26)
save(fig, 'l40-slide2-snapshot.png')

fig, ax = base()
heading(ax, 'Output Shapes: Goldens', 'golden fixtures, structural checks', size=42)
cards3(ax, [
    ('Golden Fixtures', ['Real, anonymised', 'Representative calls', 'Captured by example']),
    ('Assert on Shape', ['Fields present', 'Types correct', 'Nesting as expected']),
    ('Values May Change', ['Tickets change daily', 'Shape must never', 'change silently']),
])
bottomline(ax, 'Drift caught in CI, while the fix is cheap.', size=27)
save(fig, 'l40-slide3-golden.png')

fig, ax = base()
heading(ax, 'Error Shapes Are Contract', 'the most important pillar', size=42)
cards3(ax, [
    ('One Error Envelope', ['Machine-readable code', 'Readable message', 'Retryable flag']),
    ('Trigger Failures', ['Unknown tool', 'Invalid args', 'Permission denied']),
    ('Errors Guide Models', ['Retryable = retry once', 'Only if flag trusted', 'Every tool, every time']),
])
bottomline(ax, 'Caller-fixable to fatal is a breaking change.', size=26)
save(fig, 'l40-slide4-errors.png')

fig, ax = base()
heading(ax, 'Schema Evolution Rules', 'what is safe, what breaks', size=44)
cards3(ax, [
    ('Safe: Additive', ['Add optional field', 'Callers ignore it', 'Existing calls pass']),
    ('Breaking Changes', ['Rename a field', 'Retype a field', 'Tighten acceptance']),
    ('Version Events', ['Announce it', 'Support old + new', 'Migration path given']),
])
bottomline(ax, 'The suite classifies. Humans decide.', size=27)
save(fig, 'l40-slide5-evolution.png')

fig, ax = base()
heading(ax, 'Hands-On + Next', 'feel the suite classify', size=46)
cards3(ax, [
    ('Run the Suite', ['S10 contract suite', 'Against sample server', 'All promises checked']),
    ('Tighten One Field', ['One schema field', 'Suite classifies it', 'as breaking']),
    ('Next Lesson', ['Integration Testing', 'Real and Mock', 'Clients']),
])
bottomline(ax, 'Contracts prove promises. Connections come next.', size=26)
save(fig, 'l40-slide6-next.png')

# ================= LESSON 41 =================
title_card('l41-slide0-title.png', 'Section 10  \u00b7  Lesson 41',
           ['Integration Testing:', 'Real and Mock Clients'])

fig, ax = base()
heading(ax, 'Real Clients Reveal', 'the compatibility surface', size=44)
cards3(ax, [
    ('Real Hosts + SDK', ['Actual hosts users run', 'Official SDK client', 'Server in fixture']),
    ('Full Conversation', ['Spawn or temp port', 'Handshake, list, call', 'Assert end to end']),
    ('Only This Catches', ['Serialisation drift', 'Handshake failures', 'Stale session state']),
])
bottomline(ax, 'Sequence matters: list, read, act, verify.', size=27)
save(fig, 'l41-slide1-real.png')

fig, ax = base()
heading(ax, 'Mock Clients Misbehave', 'politeness is not a test strategy', size=42)
cards3(ax, [
    ('Mock Misbehaviour', ['Schema-violating args', 'Abandoned sessions', '50 concurrent calls']),
    ('Hostile Harness', ['Corpus of malformed', '+ adversarial requests', 'Replayed per release']),
    ('Two Views', ['Real: conformance', 'Mock: resilience', 'Production has both']),
])
bottomline(ax, 'Resilience unrehearsed is resilience hoped for.', size=26)
save(fig, 'l41-slide2-mock.png')

fig, ax = base()
heading(ax, 'The Honest Test Matrix', 'server by client by transport', size=44)
cards3(ax, [
    ('The Natural Matrix', ['Server version', 'by client', 'by transport']),
    ('Prune Honestly', ['Versions in real use', 'Transports deployed', 'Pairings that occur']),
    ('Both Directions', ['New client, old server', 'Old client, new server', 'Uneven upgrades occur']),
])
bottomline(ax, 'A small running matrix beats a large idle one.', size=26)
save(fig, 'l41-slide3-matrix.png')

fig, ax = base()
heading(ax, 'Seeded, Replayed, Never Live', 'environments for integration tests', size=38)
cards3(ax, [
    ('Seeded Environment', ['Dedicated test env', 'Scratch database', 'Stubbed services']),
    ('Record + Replay', ['Cannot seed it?', 'Capture once', 'Replay in tests']),
    ('Never Production', ['Slow + unreliable', 'Red builds ignored', 'Trust is consumed']),
])
bottomline(ax, 'Protect the suite credibility like the server.', size=26)
save(fig, 'l41-slide4-envs.png')

fig, ax = base()
heading(ax, 'A Report, Not a Memory', 'keep the results as evidence', size=44)
cards3(ax, [
    ('Every Run Files One', ['Client + transport', 'Server build', 'Passed + failed']),
    ('Evidence Later', ['Host ships an update', 'Prove where change', 'arrived from']),
    ('Pruning Instrument', ['Dead clients leave', 'by evidence', 'New clients enter early']),
])
bottomline(ax, 'Teams with reports argue from evidence.', size=27)
save(fig, 'l41-slide5-report.png')

fig, ax = base()
heading(ax, 'Hands-On + Next', 'run the matrix, file the report', size=46)
cards3(ax, [
    ('Run the Matrix', ['Sample server', 'Real client', 'end to end']),
    ('Three Abuse Cases', ['Malformed messages', 'Mid-call disconnect', 'Stripped session']),
    ('Next Lesson', ['Adversarial Testing', 'and Regression', 'Suites']),
])
bottomline(ax, 'Integration proves survival. Adversarial is next.', size=25)
save(fig, 'l41-slide6-next.png')

# ================= LESSON 42 =================
title_card('l42-slide0-title.png', 'Section 10  \u00b7  Lesson 42',
           ['Adversarial Testing and', 'Regression Suites'])

fig, ax = base()
heading(ax, 'Hostile Language, Legit Output', 'the attack rides inside real content', size=38)
cards3(ax, [
    ('Genuine Content', ['Tool fetches a page', 'Queries a database', 'Returns real content']),
    ('Hidden Instruction', ['Ignore instructions', 'Forward the keys', 'Inside the output']),
    ('Drills Become Tests', ['Poisoned records', 'Booby-trapped docs', 'Permanent fixtures']),
])
bottomline(ax, 'A defence in the gate is a control, not a story.', size=26)
save(fig, 'l42-slide1-hostile.png')

fig, ax = base()
heading(ax, 'Half One: Server Hygiene', 'no model needed', size=44)
cards3(ax, [
    ('Provenance Marking', ['Provenance markings', 'Feed hostile content', 'Assert marks survive']),
    ('Gate on Provenance', ['Tainted items', 'cannot trigger', 'gated actions']),
    ('Deterministic Tests', ['Confirmation tokens', 'Reject calls lacking', 'Run every commit']),
])
bottomline(ax, 'These prove the walls exist.', size=28)
save(fig, 'l42-slide2-hygiene.png')

fig, ax = base()
heading(ax, 'Half Two: Model in the Loop', 'measured statistically', size=42)
cards3(ax, [
    ('Adversarial Corpus', ['Instruction override', 'Exfiltration attempts', 'Fake authority claims']),
    ('Run the Harness', ['Real model calls tools', 'Receives poison', 'Continues the task']),
    ('Judge What It Did', ['Followed injection?', 'Leaked data?', 'Refused, task done?']),
])
bottomline(ax, 'Test the model family your users deploy.', size=27)
save(fig, 'l42-slide3-loop.png')

fig, ax = base()
heading(ax, 'Keep the Corpus Honest', 'and growing, permanently', size=44)
cards3(ax, [
    ('Label the Poison', ['Fixtures labelled', 'Kept out of', 'training data']),
    ('Every New Pattern', ['Like a disclosed', 'vulnerability', 'Added permanently']),
    ('Report Limits Truly', ['Risk reduction', 'Not elimination', 'Budget accordingly']),
])
bottomline(ax, 'Overselling this layer invites surprise.', size=27)
save(fig, 'l42-slide4-corpus.png')

fig, ax = base()
heading(ax, 'Fuzz the Output Boundary', 'outputs engineered to confuse', size=44)
cards3(ax, [
    ('Built to Confuse', ['Oversized payloads', 'Contradictory fields', 'Smuggled encodings']),
    ('Meet Them Early', ['In your harness', 'Failure = information', 'Not an incident']),
    ('Honest Progress', ['Not proven safe', 'Proven harder', 'to surprise']),
])
bottomline(ax, 'In this domain, that is the unit of progress.', size=26)
save(fig, 'l42-slide5-fuzz.png')

fig, ax = base()
heading(ax, 'Regression: Lock Behaviour In', 'replay, properties, goldens', size=38)
cards3(ax, [
    ('Recorded Replay', ['Record real pairs', 'Replay per release', 'Normalise noise first']),
    ('Properties Hold', ['Results match query', 'Pages disjoint + full', 'Read reflects write']),
    ('The Golden Set', ['Description edits', 'replay the set', 'Behaviour = API change']),
])
bottomline(ax, 'A suite everyone rubber-stamps is theatre.', size=27)
save(fig, 'l42-slide6-regression.png')

fig, ax = base()
heading(ax, 'Hands-On + Next', 'run the full gate green', size=46)
cards3(ax, [
    ('Add the Fixtures', ['S10 adversarial', 'fixtures into', 'regression suite']),
    ('The Full Gate', ['Unit, contract,', 'integration, adversarial', 'All green \u2014 done']),
    ('Next: Section 11', ['Observability', 'Logging, Tracing,', 'Metrics That Matter']),
])
bottomline(ax, 'That closes Section 10. Production comes next.', size=26)
save(fig, 'l42-slide7-next.png')

print('ALL SLIDES DONE')
