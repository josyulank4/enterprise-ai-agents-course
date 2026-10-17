"""Slide builder for Skool Course 3, Section 8 (Lessons 32-35).

Visual system copied from Course 2 s00 / Course 3 s01 build_slides.py:
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
    '~/workspace/udemy-skool/skool-course-3-mcp-architecture/sections/s08/slides')
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


# ================= LESSON 32 =================
title_card('l32-slide0-title.png', 'Section 8  \u00b7  Lesson 32',
           ['Why One Agent Needs', 'Many Servers: Discovery'])

fig, ax = base()
heading(ax, 'Small Servers, Owned Locally', 'one system, one server, one team', size=46)
cards3(ax, [
    ('Customer Server', ['Built by the team', 'that owns customers', 'Customer tools only']),
    ('Knowledge Base', ['Built by the docs team', 'Search + retrieval', 'Its own cadence']),
    ('Ticketing Server', ['Built by support', 'Case management', 'Its own policies']),
])
bottomline(ax, 'Ownership, change, and failure in one small box.', size=27)
save(fig, 'l32-slide1-small.png')

fig, ax = base()
heading(ax, 'One Conversation, One Catalog', 'tools from every connected server', size=46)
cards3(ax, [
    ('The Host View', ['One conversation', 'One tool catalog', 'Assembled live']),
    ('The Model Chooses', ['Sees tools from', 'all servers', 'Picks what fits']),
    ('The N+M World', ['Each new system', 'adds one server', 'No multiplied work']),
])
bottomline(ax, 'A new system simply shows up as another server.', size=27)
save(fig, 'l32-slide2-catalog.png')

fig, ax = base()
heading(ax, 'Composition Creates Problems', 'that one server never has', size=46)
cards3(ax, [
    ('Collisions', ['Two tools called', 'search, or get status', 'Tell them apart']),
    ('Dependencies', ['One call needs', "another server's data", 'Ordering + errors']),
    ('Partial Failure', ['One server down', 'Others healthy', 'Degrade, never collapse']),
])
bottomline(ax, 'Orchestration is the set of answers.', size=28)
save(fig, 'l32-slide3-problems.png')

fig, ax = base()
heading(ax, 'Discovery 1: Static Config', 'the production foundation', size=46)
cards3(ax, [
    ('What It Lists', ['Server name', 'Command or URL', 'Credentials + tools']),
    ('Its Strengths', ['Explicit + auditable', 'Version controlled', 'Ops knows exactly']),
    ('Its Weakness', ['Adding a server', 'means editing config', 'and redeploying']),
])
bottomline(ax, 'Most common approach in production today.', size=27)
save(fig, 'l32-slide4-static.png')

fig, ax = base()
heading(ax, 'Discovery 2: The Registry', 'the official public catalog', size=46)
cards3(ax, [
    ('What It Holds', ['Names + namespaces', 'Repository pointers', 'Package references']),
    ('Verified Ownership', ['Manifest published', 'Namespace proven', 'Identity checked']),
    ('What It Is Not', ['Not a code host', 'Not an app store', 'Metadata only']),
])
bottomline(ax, 'Discovery never grants trust. That stays yours.', size=27)
save(fig, 'l32-slide5-registry.png')

fig, ax = base()
heading(ax, 'Discovery 3: Internal Catalog', 'and runtime discovery', size=44)
cards3(ax, [
    ('Internal Catalog', ['Private registry', 'Approved servers', 'Owners + health']),
    ('Runtime Discovery', ['Client queries', 'a directory service', 'Connects at startup']),
    ('Trust Controls', ['Approval first', 'Definition pinning', 'Scope review']),
])
bottomline(ax, 'Convenience raises the bar. It never lowers it.', size=27)
save(fig, 'l32-slide6-internal.png')

fig, ax = base()
heading(ax, 'The Practical Rule', 'and the selection problem', size=46)
cards3(ax, [
    ('By Setting', ['Production: static', 'Development: registry', 'Between: internal']),
    ('Always Log', ['Resolved server list', 'Part of the', 'session audit trail']),
    ('Selection Problem', ['50 servers, 500 tools', 'Context cannot', 'hold them all']),
])
bottomline(ax, 'Finding servers is step one. Selecting is harder.', size=26)
save(fig, 'l32-slide7-rule.png')

fig, ax = base()
heading(ax, 'Hands-On + Next', 'inspect what the host knows', size=46)
cards3(ax, [
    ('Run the Demo', ['Section 8 discovery', 'Register 3 servers', 'Connect a host']),
    ('Inspect First', ['Names + endpoints', 'Advertised tools', 'Nothing assumed']),
    ('Next Lesson', ['Namespacing', 'Collisions', 'and Routing']),
])
bottomline(ax, 'Make the assembled catalog unambiguous.', size=27)
save(fig, 'l32-slide8-next.png')

# ================= LESSON 33 =================
title_card('l33-slide0-title.png', 'Section 8  \u00b7  Lesson 33',
           ['Namespacing, Collisions,', 'and Routing'])

fig, ax = base()
heading(ax, 'Three Tools Called Search', 'the collision problem, concretely', size=46)
cards3(ax, [
    ('Three Servers', ['Customer server', 'Knowledge base', 'Web search']),
    ('Same Name', ['All expose search', 'Different schemas', 'Different collections']),
    ('Silent Failure', ['Model calls wrong one', 'Plausible results', 'Wrong answer buried']),
])
bottomline(ax, 'Ambiguity here becomes wrong answers there.', size=27)
save(fig, 'l33-slide1-collision.png')

fig, ax = base()
heading(ax, 'The Fix: Prefix Every Tool', 'client-side namespacing', size=46)
cards3(ax, [
    ('Prefixed Names', ['crm search', 'kb search', 'web search']),
    ('Now Distinct', ['Model sees', 'distinct names', 'Origin in the name']),
    ('A Convention', ['Not protocol-required', 'Near-universal', 'in multi-server clients']),
])
bottomline(ax, 'Provenance stays visible everywhere the name travels.', size=25)
save(fig, 'l33-slide2-prefix.png')

fig, ax = base()
heading(ax, 'Namespacing Is a Policy', 'not an improvisation', size=46)
cards3(ax, [
    ('Define Aliases', ['In configuration', 'Short + stable', 'Documented once']),
    ('Never Rebrand', ['No semantic renames', 'at the client layer', 'Logs must match']),
    ("The Client's Job", ['Disambiguate', 'Never rebrand', 'Keep boundary clean']),
])
bottomline(ax, 'Your future debugging sessions will thank you.', size=27)
save(fig, 'l33-slide3-policy.png')

fig, ax = base()
heading(ax, 'Collisions Below the Name', 'parameters, and collisions as signal', size=42)
cards3(ax, [
    ('Parameter Level', ['id with', 'different formats', 'query languages differ']),
    ('The Discipline', ['Narrow tools', 'Precise schemas', 'Explicit descriptions']),
    ('As a Signal', ['Overlapping surface?', 'Maybe consolidate', 'One server owns it']),
])
bottomline(ax, 'Review new servers against the catalog first.', size=27)
save(fig, 'l33-slide4-params.png')

fig, ax = base()
heading(ax, 'Routing: Trivial on Purpose', 'the standard case is a lookup', size=44)
cards3(ax, [
    ('Standard Case', ['Namespaced name', 'maps to one server', 'Client forwards call']),
    ('Three Exceptions', ['Overlapping tools', 'Connection-time choice', 'Failover']),
    ('The Principle', ['Routing is mechanical', 'Never model-chosen', 'where a rule decides']),
])
bottomline(ax, 'Blame a config line, not a model mood.', size=27)
save(fig, 'l33-slide5-routing.png')

fig, ax = base()
heading(ax, 'Overlapping Capabilities', 'descriptions and catalog filtering', size=44)
cards3(ax, [
    ('When It Arises', ['Two servers could', 'handle the task', 'Different collections']),
    ('Descriptions Decide', ['Say what it does', 'and when to prefer it', 'Quality = routing']),
    ('Catalog Filtering', ['Show only relevant', 'servers per task', 'Less confusion + context']),
])
bottomline(ax, 'Often the highest-value routing move you can make.', size=25)
save(fig, 'l33-slide6-overlap.png')

fig, ax = base()
heading(ax, 'Selection + Explicit Failover', 'decided in configuration', size=44)
cards3(ax, [
    ('Per-Role Server Sets', ['Support: CRM + tickets', 'Analysis: warehouse', 'Minimal set first']),
    ('Why Not Everything', ['Wastes context', 'Widens attack surface', 'No benefit']),
    ('Explicit Failover', ['Replica in config', 'Never improvised', 'Log every event']),
])
bottomline(ax, 'Silently changing a data source changes the answers.', size=25)
save(fig, 'l33-slide7-failover.png')

fig, ax = base()
heading(ax, 'Hands-On + Next', 'fix the colliding demo', size=46)
cards3(ax, [
    ('The Rule', ['Every deterministic', 'routing decision', 'the model cannot miss']),
    ('Run the Demo', ['Colliding servers', 'Same tool name', 'Fix with namespacing']),
    ('Next Lesson', ['Composing', 'Multi-Server', 'Workflows']),
])
bottomline(ax, 'Then we chain tools across servers into workflows.', size=26)
save(fig, 'l33-slide8-next.png')

# ================= LESSON 34 =================
title_card('l34-slide0-title.png', 'Section 8  \u00b7  Lesson 34',
           ['Composing Multi-Server', 'Workflows'])

fig, ax = base()
heading(ax, 'The Refund Workflow', 'four steps, four servers', size=46)
cards3(ax, [
    ('Steps 1-2', ['Read the order', 'Commerce server', 'Check policy: KB']),
    ('Steps 3-4', ['Issue the refund', 'Billing server', 'Log case: ticketing']),
    ('The Risk', ['Every call succeeds', 'Workflow still wrong', 'Wrong order', 'Wrong account']),
])
bottomline(ax, 'Correctness lives in the composition.', size=27)
save(fig, 'l34-slide1-refund.png')

fig, ax = base()
heading(ax, 'Why Composition Is Possible', 'agreed shapes across servers', size=44)
cards3(ax, [
    ('Standard Outputs', ['Structured results', 'Carry identifiers', 'Not prose to parse']),
    ('Safety Tiers', ['Every tool tiered', 'Guards survive', 'composition intact']),
    ('The Forgotten Point', ['Approval-required write', 'still requires it', 'as workflow step 3']),
])
bottomline(ax, 'Composing tools never composes away their guards.', size=26)
save(fig, 'l34-slide2-shapes.png')

fig, ax = base()
heading(ax, 'Two Composition Engines', 'the toolbox and the assembly line', size=42)
cards3(ax, [
    ('The Model', ['Most flexible', 'Sequences + adapts', 'Exploratory work']),
    ('Orchestrated', ['Sequence in code', 'or configuration', 'Model works inside']),
    ('Match the Stakes', ['Low stakes: model', 'High stakes: defined', 'Toolbox vs line']),
])
bottomline(ax, 'The assembly line is more reliable.', size=28)
save(fig, 'l34-slide3-engines.png')

fig, ax = base()
heading(ax, 'Patterns 1-2: Pipeline, Fan-Out', 'chain it, or parallelize it', size=42)
cards3(ax, [
    ('Sequential Pipeline', ['Each step feeds', 'the next step', 'Validate handoffs']),
    ('Fan-Out + Gather', ['Parallel calls', 'across servers', 'Combine results']),
    ('Partial Failure', ['Policy decided', 'in advance', 'Proceed or fail whole?']),
])
bottomline(ax, 'Three servers answer in the time of the slowest.', size=26)
save(fig, 'l34-slide4-patterns12.png')

fig, ax = base()
heading(ax, 'Patterns 3-4: Branch, Compensate', 'design both paths', size=42)
cards3(ax, [
    ('Branching', ['Route on a result', 'Inside window: refund', 'Outside: escalate']),
    ('Compensation', ['Fails at step 4?', 'Undo or flag', 'steps 1 to 3']),
    ('Honest Status', ['Which steps done', 'Which failed', 'What was done']),
])
bottomline(ax, 'Partial completion is a normal outcome.', size=27)
save(fig, 'l34-slide5-patterns34.png')

fig, ax = base()
heading(ax, 'State Lives Outside Context', 'in the orchestration layer', size=44)
cards3(ax, [
    ('Context Is Lossy', ['Identifiers scroll out', 'Summarized away', 'Confused with others']),
    ('Persist State', ['Workflow-scoped store', 'References, not payloads', 'Steps re-runnable']),
    ('Recovery', ['Resume from state', 'Not from model memory', 'Retry = a lookup']),
])
bottomline(ax, 'A workflow on memory alone is fragile by design.', size=26)
save(fig, 'l34-slide6-state.png')

fig, ax = base()
heading(ax, 'The Support-Agent Shape', 'reads, reasoning, tiered writes', size=44)
cards3(ax, [
    ('Reads First', ['Fan out in parallel', 'Ticketing, account', 'billing — no changes']),
    ('Then Reasoning', ['On the composed picture', 'no single server', 'could provide']),
    ('Writes Last', ['Low-risk: pre-approved', 'Affecting: human decides', 'Validate between steps']),
])
bottomline(ax, 'Sequence planned. State persisted. Tiers intact.', size=26)
save(fig, 'l34-slide7-support.png')

fig, ax = base()
heading(ax, 'Hands-On + Next', 'kill step four on purpose', size=46)
cards3(ax, [
    ('Run the Workflow', ['Three-server support', 'ticket, end to end', 'Ticketing, account, billing']),
    ('The Instructive Part', ['Kill step four', 'Run compensation', 'Watch steps unwind']),
    ('Next Lesson', ['Failure Isolation', 'and Configuration', 'Across Environments']),
])
bottomline(ax, 'One dead server must never kill the agent.', size=27)
save(fig, 'l34-slide8-next.png')

# ================= LESSON 35 =================
title_card('l35-slide0-title.png', 'Section 8  \u00b7  Lesson 35',
           ['Failure Isolation and', 'Configuration Across Environments'])

fig, ax = base()
heading(ax, 'Servers Will Fail', 'design for the day, not the exception', size=42)
cards3(ax, [
    ('How They Fail', ['Processes crash', 'Networks partition', 'Credentials expire']),
    ('Also Normal', ['Rate limits bite', 'Upstream APIs down', 'It is a Tuesday']),
    ("The Agent's Job", ['Keep working with', 'whatever remains', 'Isolation makes it so']),
])
bottomline(ax, 'Depending on every server is building a chain.', size=26)
save(fig, 'l35-slide1-fail.png')

fig, ax = base()
heading(ax, 'Principle 1: Bulkheading', 'per-server circuit breakers', size=46)
cards3(ax, [
    ('Own Lifecycle', ['Per-server timeouts', 'Retries + breakers', 'No global setup']),
    ('Circuit Breaker', ['Trips for ticketing', 'Stops the hammering', 'Others keep flowing']),
    ('Tune Timeouts', ['Local: milliseconds', 'Remote: seconds', 'From observed behavior']),
])
bottomline(ax, 'One failure cannot cascade into the others.', size=27)
save(fig, 'l35-slide2-bulkhead.png')

fig, ax = base()
heading(ax, 'Principle 2: Degrade Plainly', 'gracefully, and say so', size=46)
cards3(ax, [
    ('Say It Plainly', ['Cannot reach ticketing', 'Account + articles', 'still available']),
    ('Never Substitute', ['No stale cache as live', 'No guessed status', 'Confident wrong = worst']),
    ('Policy in Config', ['Critical: fail session', 'Optional: continue', 'Fallback: replica']),
])
bottomline(ax, 'An honest partial answer beats a confident wrong one.', size=24)
save(fig, 'l35-slide3-degrade.png')

fig, ax = base()
heading(ax, 'Principle 3: Health Per Server', 'measured, never averaged', size=44)
cards3(ax, [
    ('Per-Server Signals', ['Success rate', 'Call latency', 'Error rate']),
    ('Never Averaged', ['Aggregate hides', 'one outage inside', "another's success"]),
    ('Drill It', ['Take each server down', 'in staging, in turn', 'Observe + learn']),
])
bottomline(ax, 'Isolation: architecture, or aspiration?', size=27)
save(fig, 'l35-slide4-health.png')

fig, ax = base()
heading(ax, 'Configuration Is a System', 'separate code, config, secrets', size=42)
cards3(ax, [
    ('Config From Code', ['Definitions in', 'version-controlled files', 'Reviewed like code']),
    ('Secrets Separate', ['In a secrets manager', 'Referenced by name', 'Never embedded']),
    ('Environments', ['Overlays + variables', 'Not forked copies', 'Injected at deploy']),
])
bottomline(ax, 'Same host build, any environment, by config alone.', size=25)
save(fig, 'l35-slide5-config.png')

fig, ax = base()
heading(ax, 'Review Changes, Honest Envs', 'capability changes get reviewed', size=42)
cards3(ax, [
    ('Review as Change', ['New server or tool', 'Security checklist', 'Staging first']),
    ('Keep Envs Honest', ['Inventory per env', 'Servers, versions', 'tools — diffed often']),
    ('Observable Live', ['Startup log records', 'resolved server list', 'Trace any session']),
])
bottomline(ax, 'Drift you diff for is drift you control.', size=27)
save(fig, 'l35-slide6-review.png')

fig, ax = base()
heading(ax, 'The Integrated Scenario', 'three servers, one fails mid-shift', size=44)
cards3(ax, [
    ('The Setup', ['Customer, KB, ticketing', 'Namespaced prefixes', 'Writes need confirmation']),
    ('Mid-Shift Failure', ['Ticketing goes down', 'Breaker trips', 'Agent says so plainly']),
    ('Clean Recovery', ['Ticket step queued', 'Inputs persisted', 'Retried on recovery']),
])
bottomline(ax, 'Degraded behavior was policy, not improvisation.', size=26)
save(fig, 'l35-slide7-scenario.png')

fig, ax = base()
heading(ax, 'Hands-On + Next', 'run the failure drill', size=46)
cards3(ax, [
    ('Run the Drill', ['Take one server down', 'mid-workflow', 'Verify degradation']),
    ('Do Not Skip', ['The recovery half', 'Degrade + report', 'Recover cleanly']),
    ('Next: Section 9', ['Three Ways to Give', 'a Model Tools', 'Honest comparison']),
])
bottomline(ax, 'That closes Section 8: orchestration, end to end.', size=26)
save(fig, 'l35-slide8-next.png')

print('ALL SLIDES DONE')
