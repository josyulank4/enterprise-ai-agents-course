"""Slide deck builder for Skool Course 3, Section 3 (Architecture): Lessons 9-12.

Visual system copied from Course 2 s00: dark navy BG, gold accents, cards,
DejaVu Sans, 1920x1080, gold rule near top, centered footer.
Footer: MCP ARCHITECTURE · BUILDING TOOL-USING AI SYSTEMS
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import os

D = os.path.expanduser(
    '~/workspace/udemy-skool/skool-course-3-mcp-architecture/sections/s03/slides')
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


def heading(ax, text, sub=None, size=58):
    ax.text(W / 2, 9.3, text, color=WHITE, fontsize=size, ha='center',
            va='center', weight='bold', family=FONT)
    if sub:
        ax.text(W / 2, 8.35, sub, color=GOLD, fontsize=32, ha='center',
                va='center', family=FONT)


def card(ax, x, y, w, h, title, lines, title_size=29, line_size=24):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                                boxstyle='round,pad=0.08,rounding_size=0.25',
                                facecolor=CARD, edgecolor=GOLD, linewidth=1.5))
    ax.text(x + w / 2, y + h - 0.78, title, color=GOLD, fontsize=title_size,
            ha='center', va='center', weight='bold', family=FONT)
    n = len(lines)
    spacing = 0.64 if n <= 3 else 0.52
    start = y + h - 1.78 if n <= 3 else y + h - 1.62
    yy = start
    for ln in lines:
        ax.text(x + w / 2, yy, ln, color=WHITE, fontsize=line_size,
                ha='center', va='center', family=FONT)
        yy -= spacing


def cards3(ax, specs):
    xs = [1.0, 6.95, 12.9]
    for x, (t, lines) in zip(xs, specs):
        ml = max(len(l) for l in lines)
        ls = 24 if ml <= 21 else 21 if ml <= 25 else 19 if ml <= 29 else 17
        tl = len(t)
        ts = 29 if tl <= 15 else 25 if tl <= 19 else 22 if tl <= 23 else 20
        card(ax, x, 3.05, 5.3, 4.35, t, lines, title_size=ts, line_size=ls)


def cards2(ax, specs):
    xs = [1.6, 10.2]
    for x, (t, lines) in zip(xs, specs):
        ls = 24 if max(len(l) for l in lines) <= 34 else 22
        card(ax, x, 3.05, 7.4, 4.35, t, lines, line_size=ls)


def bottomline(ax, text, size=31):
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


# ================= LESSON 9 =================
title_card('l09-slide0-title.png', 'Section 3  \u00b7  Lesson 9',
           ['Separation of Concerns', 'and Server Anatomy'])

fig, ax = base()
heading(ax, 'If Servers Ran Inside the Host', 'Tools as plugins inside the host process.', size=52)
cards3(ax, [
    ('Crash and Trust', ['One bug crashes the host', 'A compromised tool holds', "the host's privileges"]),
    ('Coupled Delivery', ["The host's language only", "The host's release cycle", 'One host, not every host']),
    ('The Failure', ['Never the first tool', 'It is the twentieth tool', "Someone else's code"]),
])
bottomline(ax, 'Process separation turns tools into a marketplace.')
save(fig, 'l09-slide1-inside-host.png')

fig, ax = base()
heading(ax, 'If the Host Spoke Every Native API', 'No client in between.', size=48)
cards3(ax, [
    ('Bespoke Again', ['Every integration by hand', 'Every quirk, in every app', 'N times M, forever']),
    ("The Client's Job", ['Absorb complexity once', 'One protocol on the wire', 'One uniform interface']),
    ('Policy: The Host', ['Servers are least trusted', 'Host requires confirmation', 'Allow-lists and audit']),
])
bottomline(ax, 'The layering is the trust model.')
save(fig, 'l09-slide2-native-api.png')

fig, ax = base()
heading(ax, 'The Responsibility Checklist', 'When anything goes wrong, debug by layer.')
cards3(ax, [
    ('Host', ['User interface', 'Model interaction', 'Approval policy', 'Audit logging', 'Client lifecycles']),
    ('Client', ['Establish transport', 'Capability negotiation', 'Frame and route messages', 'Match responses', 'Deliver notifications']),
    ('Server', ['Declare honestly', 'Validate inputs', 'Execute safely', 'Well-formed results', 'Notify of changes']),
])
bottomline(ax, 'Find the violated responsibility \u2014 find the failed layer.', size=29)
save(fig, 'l09-slide3-checklist.png')

fig, ax = base()
heading(ax, 'Server Anatomy', 'The declared surface.')
cards3(ax, [
    ('Tools', ['list: the definitions', 'call: invoke by name', 'Name, description, schema']),
    ('Resources', ['list: enumerate them', 'read: fetch by URI', 'Templates: families']),
    ('Prompts + Support', ['list / get: templates', 'Change notifications', 'Logging and completion']),
])
bottomline(ax, 'That surface is all the outside world may see.')
save(fig, 'l09-slide4-anatomy.png')

fig, ax = base()
heading(ax, 'What Stays Hidden', 'And the two reverse methods.')
cards3(ax, [
    ('Behind the Facade', ['Credentials', 'Connection pools', 'Internal clients', 'Retry logic']),
    ('Reverse Methods', ['Sampling: ask the model', 'to generate text', 'Roots: scoped locations', 'Both client-declared']),
    ('Three Layers', ['Protocol layer \u2014 the SDK', 'Capability layer', 'System layer', 'Guard the boundary']),
])
bottomline(ax, 'Bugs live at the capability\u2013system boundary.')
save(fig, 'l09-slide5-hidden.png')

fig, ax = base()
heading(ax, 'A Server Is a Product', 'With a contract, not a script with a port.')
cards3(ax, [
    ('Its Consumers', ['Models reading descriptions', 'Hosts presenting them', 'as truth']),
    ('Product Defects', ['Vague tool descriptions', 'Dishonest declarations', 'Leaked internals']),
    ('Replaceable', ['Swap the model', 'Swap the host', 'Swap the server']),
])
bottomline(ax, 'Clarity of the surface is the feature.')
save(fig, 'l09-slide6-product.png')

fig, ax = base()
heading(ax, 'Try It: The Anatomy Inspector', 'Inspection before construction.')
cards2(ax, [
    ('Run the Inspector', ['Section 3 anatomy inspector', 'Against the sample server', 'Full exposed-surface report']),
    ('Ask the Harder Question', ['Every capability declared?', 'Every tool, resource, prompt?', 'What is this server hiding?', 'Is it hiding enough?']),
])
bottomline(ax, 'Next: Lesson 10 \u2014 The stdio Transport.', size=29)
save(fig, 'l09-slide7-try-it.png')

# ================= LESSON 10 =================
title_card('l10-slide0-title.png', 'Section 3  \u00b7  Lesson 10',
           ['The stdio Transport: Local,', 'Simple, Process-Bound'])

fig, ax = base()
heading(ax, 'Mechanics', 'A subprocess and two streams.')
cards3(ax, [
    ('Launch', ['Client spawns the server', 'As a subprocess', 'It lives with the session']),
    ('Streams', ["Write to the server's stdin", "Read from its stdout", 'One JSON message per line']),
    ('No Network', ['No port, no socket', 'No network handshake', 'Fresh process each time']),
])
bottomline(ax, 'The transport is the process boundary.')
save(fig, 'l10-slide1-mechanics.png')

fig, ax = base()
heading(ax, 'The Discipline', 'Standard output belongs to the protocol.', size=52)
cards3(ax, [
    ('What Corrupts It', ['One stray print statement', 'One debug line', 'One friendly banner']),
    ('How It Looks', ['The client starts failing', 'Looks like protocol bugs', 'Actually plumbing bugs']),
    ('The Absolute Rule', ['Log to standard error', 'Or log to files', 'Never to standard output']),
])
bottomline(ax, 'For a human? It does not go to standard output. Ever.', size=29)
save(fig, 'l10-slide2-discipline.png')

fig, ax = base()
heading(ax, 'Strengths', 'Isolation and zero network surface.')
cards3(ax, [
    ('OS Isolation', ['Its own process', 'A limited user', 'Filesystem confinement', 'Resource caps']),
    ('Trivial Deployment', ['A server is an executable', 'Command from config', 'No ports or certificates']),
    ('The Right Trade', ['Personal tools', 'Developer assistants', 'Desktop hosts']),
])
bottomline(ax, 'Maximum simplicity, zero network attack surface.')
save(fig, 'l10-slide3-strengths.png')

fig, ax = base()
heading(ax, 'Limitations', 'Local by definition.')
cards3(ax, [
    ('Not Shared', ['No shared team servers', 'No SaaS hosting', 'No multi-machine use']),
    ('Coupled Lifecycle', ['Born and dies with client', 'Two hosts cannot share it', '100 hosts, 100 processes']),
    ('Ad Hoc Observability', ['Logs via stderr capture', 'No standard health checks', 'Unlike a network service']),
])
bottomline(ax, 'The honest price of simplicity \u2014 pay it knowingly.', size=29)
save(fig, 'l10-slide4-limitations.png')

fig, ax = base()
heading(ax, 'Where It Fits', 'One machine, one trust domain.')
cards3(ax, [
    ('The Default For', ['Local developer tools', 'Desktop hosts', 'Single-user automation']),
    ('Reach Heavier When', ['The server must be shared', 'Reached over a network', 'Scaled independently', 'Operated as a service']),
    ('Configuration', ['A name for the server', 'The launch command + args', 'The environment it needs', 'Host launches on demand']),
])
bottomline(ax, 'Keep the capability layer transport-independent.', size=29)
save(fig, 'l10-slide5-where-it-fits.png')

fig, ax = base()
heading(ax, 'Try It: Break It Once, On Purpose', 'In the demo, where failure is cheap.', size=50)
cards2(ax, [
    ('Watch a Clean Session', ['Run the Section 3 stdio demo', 'Subprocess spawned', 'Messages line by line', 'Session closed']),
    ('Then Break It', ['Print to standard output', 'Inside the server', 'Watch the client fail', 'Learn it here, not in production']),
])
bottomline(ax, 'Next: Lesson 11 \u2014 Streamable HTTP.', size=29)
save(fig, 'l10-slide6-try-it.png')

# ================= LESSON 11 =================
title_card('l11-slide0-title.png', 'Section 3  \u00b7  Lesson 11',
           ['Streamable HTTP: Remote,', 'Stateless, Scalable'])

fig, ax = base()
heading(ax, 'Mechanics', 'One endpoint, one POST per message.')
cards3(ax, [
    ('One Endpoint', ['A single MCP endpoint', 'Conventionally at /mcp', 'One POST per message']),
    ('The Reply', ['Plain JSON for one response', 'Or an SSE stream', 'For progress while it works']),
    ('Details That Matter', ['Protocol-version header', 'Origin header validated', 'Localhost by default', 'The web toolkit applies']),
])
bottomline(ax, 'Same protocol semantics \u2014 only the framing differs.', size=29)
save(fig, 'l11-slide1-mechanics.png')

fig, ax = base()
heading(ax, 'Stateless by Design', 'No protocol-level sessions.')
cards3(ax, [
    ('Each Request Carries', ['Its protocol version', 'Its capability context', 'Its identity']),
    ('Any Instance', ['No state inside one instance', 'Instances come and go', 'Failure loses no state']),
    ('State, Explicitly', ['In the request', 'In a shared store', 'In the authenticated identity']),
])
bottomline(ax, 'The old session model is superseded \u2014 recognize it.', size=29)
save(fig, 'l11-slide2-stateless.png')

fig, ax = base()
heading(ax, 'Why Statelessness Scales', 'What makes it scalable.', size=52)
cards3(ax, [
    ('Scaling', ['Add instances', 'Behind a load balancer', 'Any request, any instance']),
    ('Failover + Deployment', ['Route around a dead instance', 'Drain and replace', 'No live sessions to negotiate']),
    ('Amortized Cost', ['One server, many hosts', 'Its own deployment', 'Its own release cycle']),
])
bottomline(ax, 'The deployment model shared things require.')
save(fig, 'l11-slide3-scales.png')

fig, ax = base()
heading(ax, 'The Operational Bill', 'Price remote reach before you buy it.')
cards3(ax, [
    ('Run It, Forever', ['Authenticated callers', 'Encrypted in transit', 'Load-balanced, rate-limited', 'Someone, on a rota']),
    ('Observe It', ['Health checks', 'Metrics and tracing', 'Incident response', 'Latency is real']),
    ('The Assumptions Trap', ['Local-trust code', 'Placed on the network', 'unchanged', 'Verbose errors leak internals']),
])
bottomline(ax, 'Changing the transport changes the threat model.', size=29)
save(fig, 'l11-slide4-bill.png')

fig, ax = base()
heading(ax, 'Choosing Between the Two Transports', 'The selection heuristic.', size=48)
cards3(ax, [
    ('Local: stdio', ['Personal files', 'Local repositories', 'Host on the same machine']),
    ('Shared: HTTP', ['A team database', 'A company SaaS product', 'Shared, scaled, operated']),
    ('Keep It Reversible', ['Capability layer agnostic', 'Bind transport at the edge', 'Prototype locally first']),
])
bottomline(ax, 'Old session-based docs are superseded \u2014 check the revision.', size=27)
save(fig, 'l11-slide5-choosing.png')

fig, ax = base()
heading(ax, 'Try It: Same Server, Two Transports', 'Compare the traces line by line.')
cards2(ax, [
    ('Run the HTTP Demo', ['Section 3 HTTP demo', 'The same server as before', 'Now behind Streamable HTTP']),
    ('Compare the Traces', ['Find one message in each', 'The message is identical', 'Only the framing changed']),
])
bottomline(ax, 'Next: Lesson 12 \u2014 Sessions and a Full Round-Trip.', size=27)
save(fig, 'l11-slide6-try-it.png')

# ================= LESSON 12 =================
title_card('l12-slide0-title.png', 'Section 3  \u00b7  Lesson 12',
           ['Sessions, Concurrency,', 'and a Full Round-Trip'])

fig, ax = base()
heading(ax, 'Connection Lifecycle', 'Establish, operate, terminate.')
cards3(ax, [
    ('Establish', ['stdio: spawn the subprocess', 'HTTP: post to the endpoint', 'The pipes / endpoint connect']),
    ('Initialize', ['Discover identity first', 'Versions and capabilities', 'Negotiate, then operate']),
    ('Operate + Terminate', ['List, call, read resources', 'Notifications both ways', 'Either side may close']),
])
bottomline(ax, 'A dropped connection is a normal event, not a crisis.', size=29)
save(fig, 'l12-slide1-lifecycle.png')

fig, ax = base()
heading(ax, 'Sessions in the Stateless Era', 'And cleanup.')
cards3(ax, [
    ('No Protocol Sessions', ['Nothing to create', 'Nothing to replicate', 'Correlate by identity']),
    ('Recovery', ['Reconnect with backoff', 'Re-run discovery', 'And resume']),
    ('Cleanup', ['stdio: terminate subprocess', 'HTTP: drain instances', 'No state stranded']),
])
bottomline(ax, 'Make establishment cheap and idempotent.')
save(fig, 'l12-slide2-sessions.png')

fig, ax = base()
heading(ax, 'Concurrency Across Servers', 'One client each.')
cards3(ax, [
    ('The Host Multiplexes', ['One client per server', 'Its own transport each', 'Union: a single tool belt']),
    ('Fan-Out, Fan-In', ['Route each call out', 'Route the results back', 'Slow must not block others']),
    ('The Teaching Case', ['Database, orders, knowledge', 'Three requests at once', 'Latency = the slowest']),
])
bottomline(ax, 'Timeouts and circuit breaking belong in the host.', size=29)
save(fig, 'l12-slide3-across.png')

fig, ax = base()
heading(ax, 'Concurrency Within a Connection', 'IDs correlate everything.', size=50)
cards3(ax, [
    ('In Flight Together', ['Many requests at once', 'Matched by request ID', 'Responses in any order']),
    ('Never Assume', ['No ordering is promised', 'Response 2 may land first', 'Never block the connection']),
    ('Server Duties', ['Synchronize shared state', 'Slow calls must not starve', 'Bound calls, memory, time']),
])
bottomline(ax, 'Isolate. Parallelize. Bound.')
save(fig, 'l12-slide4-within.png')

fig, ax = base()
heading(ax, 'The Full Round-Trip', 'Discovery to decision \u2014 steps 1 to 4.')
cards3(ax, [
    ('Steps 1\u20132: Discover', ['Learn what the server offers', 'Identity, versions, tools', 'Cache the definitions']),
    ('Step 3: Model Decides', ['Host sends the conversation', 'Plus the tool definitions', 'Model emits a tool call']),
    ('Step 4: Policy Check', ['Allowed? Confirmed?', 'Within limits? Logged?', 'Model proposes, host disposes']),
])
bottomline(ax, 'MCP standardizes everything around the decision.', size=29)
save(fig, 'l12-slide5-roundtrip-a.png')

fig, ax = base()
heading(ax, 'The Full Round-Trip', 'Invocation to answer \u2014 steps 5 to 8.')
cards3(ax, [
    ('Step 5: Invocation', ['A tools/call request', 'One line on stdin, or', 'One POST to the endpoint']),
    ('Step 6: Execution', ['Validate against the schema', 'Invoke the real system', 'Progress while it works']),
    ('Steps 7\u20138: Answer', ['Result carries the ID', 'Client matches the request', 'Result back to the model']),
])
bottomline(ax, "No layer did another layer's job.")
save(fig, 'l12-slide6-roundtrip-b.png')

fig, ax = base()
heading(ax, 'Try It: The Round-Trip Tracer', 'Reconstruction from message IDs alone.')
cards2(ax, [
    ('Run the Tracer', ['Section 3 round-trip tracer', 'Three concurrent calls', 'An interleaved timeline']),
    ('Rebuild the Timeline', ['Pair every response', 'With its request, by ID', 'In completion order']),
])
bottomline(ax, 'Next: Lesson 13 \u2014 The Minimal Server and Project Setup.', size=26)
save(fig, 'l12-slide7-try-it.png')

print('ALL SLIDES DONE')
