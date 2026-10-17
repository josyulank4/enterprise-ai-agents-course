"""Slide builder for Skool Course 3, Section 11 (Lessons 43-46).

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
    '~/workspace/udemy-skool/skool-course-3-mcp-architecture/sections/s11/slides')
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


# ================= LESSON 43 =================
title_card('l43-slide0-title.png', 'Section 11  \u00b7  Lesson 43',
           ['Observability: Logging, Tracing,', 'and Metrics That Matter'])

fig, ax = base()
heading(ax, 'Structured Logging', 'a database of operational facts', size=46)
cards3(ax, [
    ('Every Call Logged', ['Timestamp + request ID', 'Server, tool, caller', 'Outcome + duration']),
    ('Arguments, Redacted', ['Summary only', 'Sensitive values', 'removed always']),
    ('Two Non-Negotiables', ['Never log secrets', 'or raw user data', 'Version log schemas']),
])
bottomline(ax, 'Log for the incident, not for the demo.', size=27)
save(fig, 'l43-slide1-logging.png')

fig, ax = base()
heading(ax, 'Tracing the Round-Trip', 'made permanent and searchable', size=46)
cards3(ax, [
    ('One Trace Shows', ['Model decides to call', 'Server executes', 'Dependencies inside']),
    ('Server-Side Spans', ['Parse, validate', 'Execute, serialise', 'Where time went']),
    ('One Correlation ID', ['Across the protocol', 'Every span + log line', 'One search: whole story']),
])
bottomline(ax, 'The difference between guessing and knowing.', size=27)
save(fig, 'l43-slide2-tracing.png')

fig, ax = base()
heading(ax, 'Metrics That Matter', 'few, per tool, reviewed weekly', size=46)
cards3(ax, [
    ('Volume + Errors', ['Calls per tool', 'Error rate by code', 'Bug, misuse, outage']),
    ('Latency + Quota', ['Percentiles, not', 'averages \u2014 per tool', 'Quota vs ceiling']),
    ('Refusals + Gates', ['Approvals stopping', 'calls, per tool', 'Safety working?']),
])
bottomline(ax, 'Five families. Weekly rhythm. Not 500 charts.', size=26)
save(fig, 'l43-slide3-metrics.png')

fig, ax = base()
heading(ax, 'Tool-Selection Accuracy', 'the metric no chart gives you', size=44)
cards3(ax, [
    ('Sample Sessions', ['On a schedule', 'Review qualitatively', 'Right tool chosen?']),
    ('Right in Three Ways', ['Right tool', 'Right arguments', 'Right reason']),
    ('Catches Regressions', ['Schema change', 'Description reworded', 'Use gets worse']),
])
bottomline(ax, 'This one measures the product, not the machine.', size=26)
save(fig, 'l43-slide4-selection.png')

fig, ax = base()
heading(ax, 'Close the Loop', 'observation becomes tests', size=46)
cards3(ax, [
    ('Top Error Codes', ['Become new', 'contract tests', 'From production']),
    ('Slowest Real Calls', ['Become load-test', 'scenarios', 'Real, not imagined']),
    ('Wrong Sessions', ['Become regression', 'fixtures, poison kept', 'Reality writes them']),
])
bottomline(ax, 'Test, observe, test what you observed.', size=27)
save(fig, 'l43-slide5-loop.png')

fig, ax = base()
heading(ax, 'Hands-On + Next', 'reconstruct the incident', size=46)
cards3(ax, [
    ('Run the Demo', ['S11 observability', 'Inject slow upstream', 'Rebuild timeline']),
    ('Only the ID', ['Correlation ID', 'Logs and traces', 'No dashboards']),
    ('Next Lesson', ['Packaging', 'Versioning', 'Deployment Topologies']),
])
bottomline(ax, 'Tell the whole story from one thread.', size=27)
save(fig, 'l43-slide6-next.png')

# ================= LESSON 44 =================
title_card('l44-slide0-title.png', 'Section 11  \u00b7  Lesson 44',
           ['Packaging, Versioning,', 'and Deployment Topologies'])

fig, ax = base()
heading(ax, 'Reproducible Packaging', 'and the release manifest', size=46)
cards3(ax, [
    ('Tested = Deployed', ['Artifact you tested', 'is artifact deployed', 'Nothing re-resolved']),
    ('Build Clean', ['Clean pipeline', 'Never a workstation', 'Exact SDK recorded']),
    ('Release Manifest', ['Server + contract', 'Source revision', 'Schema fingerprints']),
])
bottomline(ax, 'Diff Tuesday vs Monday in a minute, not a day.', size=26)
save(fig, 'l44-slide1-packaging.png')

fig, ax = base()
heading(ax, 'Two Surfaces, Two Versions', 'version them as what they are', size=44)
cards3(ax, [
    ('Server Software', ['Disciplined scheme', 'Bug fix, no schema', '= small release']),
    ('Tool Contract', ['Names, schemas', 'Output shapes', 'First-class surface']),
    ('Breaking = Major', ['Renamed / removed', 'Announce + window', 'Migration path']),
])
bottomline(ax, 'Contract suite decides if the story is honest.', size=26)
save(fig, 'l44-slide2-versions.png')

fig, ax = base()
heading(ax, 'Topology One: Stdio', 'distributed with the host', size=46)
cards3(ax, [
    ('How It Ships', ['Host spawns server', 'Local subprocess', 'Standard streams']),
    ('Its Virtues', ['No network to run', 'Data stays local', 'Dev + desktop fit']),
    ('Its Costs', ['Runtime on each host', 'Upgrades everywhere', 'Fragmented observing']),
])
bottomline(ax, 'Each host runs its own copy.', size=27)
save(fig, 'l44-slide3-stdio.png')

fig, ax = base()
heading(ax, 'Topology Two: Remote HTTP', 'run as a service', size=44)
cards3(ax, [
    ('Shared Infra', ['One fleet serves', 'many agents', 'Central observing']),
    ('One-Place Upgrades', ['Fleet updated once', 'Resources beyond', "the host's limits"]),
    ('The Price', ['Auth + encryption', 'Load balancing', 'Distributed failures']),
])
bottomline(ax, 'Most estates run both \u2014 same handlers, both targets.', size=24)
save(fig, 'l44-slide4-remote.png')

fig, ax = base()
heading(ax, 'The Decision', 'three questions, not a benchmark', size=46)
cards3(ax, [
    ('Who Operates It?', ['Platform team?', 'Network service', 'Developer? With host']),
    ('Who Updates It?', ['Must land tonight?', 'Remote wins', 'Pinned pace? Local']),
    ('Whose Credentials?', ['Shared + powerful:', 'behind a service', 'Local only: in process']),
])
bottomline(ax, 'Answer in writing, per server.', size=27)
save(fig, 'l44-slide5-decision.png')

fig, ax = base()
heading(ax, 'Hands-On + Next', 'package it both ways', size=46)
cards3(ax, [
    ('Package Both Ways', ['Stdio distribution', 'Containerised HTTP', 'One codebase']),
    ('Write Topology Note', ['Who operates it', 'Who updates it', 'Whose credentials']),
    ('Next Lesson', ['Scaling: Containers,', 'Pooling, and', 'Secrets']),
])
bottomline(ax, 'Two packages. Two honest notes.', size=27)
save(fig, 'l44-slide6-next.png')

# ================= LESSON 45 =================
title_card('l45-slide0-title.png', 'Section 11  \u00b7  Lesson 45',
           ['Scaling: Containers,', 'Pooling, and Secrets'])

fig, ax = base()
heading(ax, 'Containers', 'minimal, immutable, honest about state', size=46)
cards3(ax, [
    ('Immutable Artifact', ['Server + runtime', 'Pinned dependencies', 'Same in every env']),
    ('Minimal Images', ['No shells', 'No package managers', 'No build toolchains']),
    ('Honest Health', ['Non-privileged user', 'Limits declared', 'Health = tool health']),
])
bottomline(ax, 'Minimal image: faster, smaller attack surface.', size=26)
save(fig, 'l45-slide1-containers.png')

fig, ax = base()
heading(ax, 'Orchestration', 'declare it, let the platform enforce it', size=46)
cards3(ax, [
    ('Desired State', ['Describe what runs', 'Platform reconciles', 'reality to it']),
    ('Self-Healing Fleet', ['Health checks', 'Failed out, replaced', 'No laptop needed']),
    ('Rolling + Discovery', ['Rolling updates', 'default motion', 'Clients find healthy']),
])
bottomline(ax, 'Scale foundations too, or the queue just moves.', size=26)
save(fig, 'l45-slide2-orchestration.png')

fig, ax = base()
heading(ax, 'Statelessness', 'the rule that makes it arithmetic', size=46)
cards3(ax, [
    ('State Lives Outside', ['Shared cache or DB', 'Or in call arguments', 'Never process memory']),
    ('Any Instance Works', ['On which instance', 'served last call', 'Sessions: transport']),
    ('Scale on Signals', ['Queue depth', 'Slow-tail latency', 'Pools by workload']),
])
bottomline(ax, 'Add instances, shed load \u2014 arithmetic.', size=27)
save(fig, 'l45-slide3-stateless.png')

fig, ax = base()
heading(ax, 'Pooling and Keep-Alive', 'connections are the scarce resource', size=44)
cards3(ax, [
    ('Pool + Bound Them', ['Reuse connections', 'Fixed, bounded set', 'Exhaustion = metric']),
    ('Size From Reality', ['Observed concurrency', 'Verified under burst', 'Not under averages']),
    ('Clean Up Sessions', ['Idle timeouts', 'Graceful draining', 'Abandoned reclaimed']),
])
bottomline(ax, 'Production is made of abandoned sessions.', size=27)
save(fig, 'l45-slide4-pooling.png')

fig, ax = base()
heading(ax, 'Configuration and Secrets', 'injected, scoped, rotated', size=42)
cards3(ax, [
    ('Config Separate', ['Never hardcoded', 'Via environment', 'Fail fast if missing']),
    ('Secrets in Vault', ['Injected at runtime', 'Referenced by name', 'Scoped least privilege']),
    ('Never in Arguments', ['Args reach logs', 'traces + context', 'Rotation rehearsed']),
])
bottomline(ax, 'Arguments carry the task, nothing more.', size=27)
save(fig, 'l45-slide5-secrets.png')

fig, ax = base()
heading(ax, 'Hands-On + Next', 'prove the stateless design', size=46)
cards3(ax, [
    ('Run the Lab', ['Three replicas', 'Behind a balancer', 'Kill one mid-traffic']),
    ('Verify Survival', ['Sessions survive', 'If work dies, state', 'was hiding inside']),
    ('Next Lesson', ['Safe Rollouts', 'Monitoring', 'Incident Response']),
])
bottomline(ax, 'Find hidden state today, cheaply.', size=27)
save(fig, 'l45-slide6-next.png')

# ================= LESSON 46 =================
title_card('l46-slide0-title.png', 'Section 11  \u00b7  Lesson 46',
           ['Safe Rollouts, Monitoring,', 'and Incident Response'])

fig, ax = base()
heading(ax, 'Blue-Green', 'total rollback for infrastructure change', size=46)
cards3(ax, [
    ('Two Environments', ['Identical pair', 'One serves live', 'Other gets new version']),
    ('Validate + Switch', ['Smoke + contract', 'Replay prod calls', 'Switch traffic']),
    ('Rollback in Seconds', ['Old stays warm', 'Switch back, no', 'redeploy needed']),
])
bottomline(ax, 'Keep them identical, or do not claim the pattern.', size=25)
save(fig, 'l46-slide1-bluegreen.png')

fig, ax = base()
heading(ax, 'Canary', 'the pattern tool changes deserve', size=46)
cards3(ax, [
    ('Small Fraction First', ['Route few calls', 'to new version', 'Watch + compare']),
    ('What to Measure', ['Errors + latency', 'Selection accuracy', 'Refusal rates']),
    ('Promote on Evidence', ['Stages + criteria', 'written in advance', 'Auto-rollback']),
])
bottomline(ax, 'Promote on evidence. Never on a timer.', size=27)
save(fig, 'l46-slide2-canary.png')

fig, ax = base()
heading(ax, 'Monitoring the Fleet', 'symptoms, baselines, runbooks', size=46)
cards3(ax, [
    ('Watch Two Systems', ['Servers as infra', 'Agent experience', 'as the product']),
    ('Alert on Symptoms', ['Slow tail doubles', 'Errors cross baseline', 'Per tool, always']),
    ('One Dashboard', ['Fleet healthy?', 'Which tool is not?', 'What changed?']),
])
bottomline(ax, 'Every alert links a runbook.', size=27)
save(fig, 'l46-slide3-monitoring.png')

fig, ax = base()
heading(ax, 'Incident Response', 'the audit log is step one', size=46)
cards3(ax, [
    ('Standard Shape', ['Detect, triage', 'Mitigate, resolve', 'Learn \u2014 blamelessly']),
    ('Triage the Cause', ['Server failure?', 'Description failure?', 'Model failure?']),
    ('Mitigate Fast', ['Roll back canary', 'Shift to known-good', 'Shed sick tool load']),
])
bottomline(ax, 'Speed from rehearsed machinery, not heroics.', size=27)
save(fig, 'l46-slide4-incident.png')

fig, ax = base()
heading(ax, 'Cost', 'a million cheap calls is not cheap', size=50)
cards3(ax, [
    ('Traffic Multiplies', ['Human: one request', 'Agent: dozens', 'Budget per task']),
    ('Overheads Compound', ['Idle connections', 'Abandoned sessions', 'Large payloads']),
    ('Judge Per Task', ['Cost per success', 'not cost per call', 'Outliers = design']),
])
bottomline(ax, 'Review outliers as design problems first.', size=27)
save(fig, 'l46-slide5-cost.png')

fig, ax = base()
heading(ax, 'Hands-On + Next', 'rehearse the rollback', size=46)
cards3(ax, [
    ('Canary Drill', ['Promote description', 'Watch budget burn', 'Execute rollback']),
    ('Practise Slowly', ['First time out loud', 'Against the runbook', 'Drill = survival']),
    ('Next: Section 12', ['A2A and MCP', 'Two Protocols', 'Two Directions']),
])
bottomline(ax, 'Observed, packaged, scaled, defended.', size=27)
save(fig, 'l46-slide6-next.png')

print('ALL SLIDES DONE')
