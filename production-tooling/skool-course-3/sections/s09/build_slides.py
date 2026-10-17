"""Slide builder for Skool Course 3, Section 9 (Lessons 36-38).

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
    '~/workspace/udemy-skool/skool-course-3-mcp-architecture/sections/s09/slides')
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


# ================= LESSON 36 =================
title_card('l36-slide0-title.png', 'Section 9  \u00b7  Lesson 36',
           ['Three Ways to Give', 'a Model Tools'])

fig, ax = base()
heading(ax, 'The Shared Question', 'three layers of answer', size=46)
cards3(ax, [
    ('The Shared Question', ['Model decides to act', 'How does it become', 'an executed call?']),
    ('Three Positions', ['Provider-coupled', 'Open standard', 'Fully custom']),
    ('Not Generations', ['Newest does not kill', 'the oldest', 'A spectrum, not eras']),
])
bottomline(ax, 'Ask what each optimizes for, not which is best.', size=27)
save(fig, 'l36-slide1-shared.png')

fig, ax = base()
heading(ax, 'Way One: Native Calling', "inside the provider's API", size=44)
cards3(ax, [
    ('How It Works', ['JSON schemas in', 'provider format', 'Your code executes']),
    ('Its Shape', ['No protocol beyond', 'the provider API', 'Coupling is total']),
    ('Why It Came First', ['Asked the least', 'of everyone', 'Built on existing API']),
])
bottomline(ax, 'Declared in the API call, in one relationship only.', size=26)
save(fig, 'l36-slide2-native.png')

fig, ax = base()
heading(ax, 'Way Two: MCP', 'contract moved into an open protocol', size=46)
cards3(ax, [
    ('How It Works', ['Servers expose tools', 'resources + prompts', 'Clients connect to them']),
    ('Who Owns It', ['Contract owned by', 'the open standard', 'Not by any vendor']),
    ('The Trade', ['Overhead paid once', 'Reuse collected', 'forever']),
])
bottomline(ax, 'Built once as servers. Reusable everywhere compatible.', size=25)
save(fig, 'l36-slide3-mcp.png')

fig, ax = base()
heading(ax, 'Way Three: Bespoke APIs', 'no tool protocol at all', size=44)
cards3(ax, [
    ('How It Works', ['Ordinary code calls', 'APIs, SDKs, queues', 'Results as context']),
    ('Its Shape', ['Maximum control', 'Maximum maintenance', 'One consumer only']),
    ('The Catch', ['No other consumer', 'can share the surface', 'By design']),
])
bottomline(ax, 'Hand-built for one purpose, for exactly one consumer.', size=26)
save(fig, 'l36-slide4-bespoke.png')

fig, ax = base()
heading(ax, 'The Spectrum', "stated plainly, side by side", size=46)
cards3(ax, [
    ('Native Calling', ['Provider format', 'Fits models best', 'Travels worst']),
    ('MCP', ['Open standard', 'Travels best', 'Run a protocol layer']),
    ('Bespoke', ['Controls everything', 'Maintenance scales', 'with every system']),
])
bottomline(ax, 'No free approach. Only trade-offs, priced differently.', size=26)
save(fig, 'l36-slide5-spectrum.png')

fig, ax = base()
heading(ax, 'Why No Winner', 'this section refuses to declare one', size=46)
cards3(ax, [
    ('MCP Everywhere', ['Servers built for', '50 lines of code', 'Overhead for nothing']),
    ('MCP Nowhere', ['Same tool kept in', 'four dialects', 'NxM bill, with interest']),
    ('The Root Failure', ['One choice made', 'for everything', 'Not per integration']),
])
bottomline(ax, 'One choice per integration, reasoning written down.', size=26)
save(fig, 'l36-slide6-winner.png')

fig, ax = base()
heading(ax, 'What to Watch For', 'in the comparison ahead', size=46)
cards3(ax, [
    ('Cost of Change', ['Switch models?', 'Add a team?', 'Double the tools?']),
    ('Given for Free', ['Fit, ecosystem,', 'and control —', 'or build your own']),
    ('Exit Cost', ['Cheap to enter,', 'expensive to leave?', 'Price it up front']),
])
bottomline(ax, 'Answer per integration, with evidence, not preference.', size=26)
save(fig, 'l36-slide7-watch.png')

fig, ax = base()
heading(ax, 'Hands-On + Next', 'build it all three ways', size=46)
cards3(ax, [
    ('Build the Triptych', ['Same capability,', 'three ways', 'Native, MCP, bespoke']),
    ('Keep the Diffs', ['Feel the coupling', 'Protocol layer', 'Hand-built control']),
    ('Next Lesson', ['Head-to-Head:', 'The Honest', 'Comparison']),
])
bottomline(ax, 'Your hands will feel what no table can give you.', size=27)
save(fig, 'l36-slide8-next.png')

# ================= LESSON 37 =================
title_card('l37-slide0-title.png', 'Section 9  \u00b7  Lesson 37',
           ['Head-to-Head:', 'The Honest Comparison'])

fig, ax = base()
heading(ax, 'Axis One and Two', 'portability and maintenance', size=46)
cards3(ax, [
    ('Portability: Native', ['Definitions in one', 'provider format', 'Rewrite to switch']),
    ('Portability: MCP', ['Tools defined once', 'against the protocol', 'Swap models freely']),
    ('Maintenance', ['MCP: once per server', 'Native: one dialect', 'Bespoke: NxM growth']),
])
bottomline(ax, 'Maintenance follows portability, almost mechanically.', size=25)
save(fig, 'l37-slide1-axes12.png')

fig, ax = base()
heading(ax, 'Axis Three and Four', 'ecosystem and latency', size=46)
cards3(ax, [
    ('Ecosystem: Native', ['No shared catalog', 'Every tool defined', 'and kept by you']),
    ('Ecosystem: MCP', ['Servers are shareable', 'Community + vendor', 'Registry discovery']),
    ('Latency', ['Native + bespoke win', 'No protocol hop', 'Model time dominates']),
])
bottomline(ax, 'Design remote tools coarse-grained, not chatty.', size=26)
save(fig, 'l37-slide2-axes34.png')

fig, ax = base()
heading(ax, 'Axis Five: Control', 'what nobody gives you for free', size=46)
cards3(ax, [
    ('Bespoke Control', ['No abstraction', 'Exploit every', 'API feature']),
    ('Native Control', ['You run execution', 'You build discovery', 'audit + approvals']),
    ('MCP Separation', ['Server: domain + auth', 'Client: orchestration', 'Layers evolve apart']),
])
bottomline(ax, 'MCP gives governance a layer. It does not govern.', size=26)
save(fig, 'l37-slide3-control.png')

fig, ax = base()
heading(ax, 'The Decision Framework', 'questions one to three', size=44)
cards3(ax, [
    ('Q1: Unusual Shape?', ['Not request-response?', 'Streaming, long jobs', 'Build it bespoke']),
    ('Q2: Model Choice?', ['Must switch models?', 'Avoid lock-in?', 'MCP is the answer']),
    ('Q3: Shared Tool?', ['Many agents or teams?', 'Make it an MCP server', 'One agent? Anywhere']),
])
bottomline(ax, 'Sharing via MCP is a config change, not a project.', size=26)
save(fig, 'l37-slide4-framework123.png')

fig, ax = base()
heading(ax, 'The Decision Framework', 'questions four to six', size=44)
cards3(ax, [
    ('Q4: How Many Tools?', ['A handful, stable:', 'native simplicity', 'Dozens: MCP pays off']),
    ('Q5: Latency?', ['Every 100 ms counts?', 'Native or bespoke', 'Else weigh honestly']),
    ('Q6: Who Owns It?', ["Yours: bespoke or MCP", "Theirs: use their", 'MCP server']),
])
bottomline(ax, "Past a handful of tools, MCP's reuse compounds.", size=26)
save(fig, 'l37-slide5-framework456.png')

fig, ax = base()
heading(ax, 'The Worked Example', 'one product, three answers', size=46)
cards3(ax, [
    ('MCP Servers', ['Customer lookup', 'Knowledge search', 'Meeting scheduler']),
    ('Bespoke Core', ['Pricing engine', 'Runs under a second', 'Thin MCP wrapper']),
    ('Stays Native', ['Draft follow-up email', 'Provider-coupled fit', 'Native, for now']),
])
bottomline(ax, 'Three integrations, three answers, each defensible.', size=26)
save(fig, 'l37-slide6-example.png')

fig, ax = base()
heading(ax, 'Two Observations', 'before we build hybrids', size=46)
cards3(ax, [
    ('Complementary', ['Where one is weak,', 'another is strong', 'Platforms go hybrid']),
    ('Rarely Permanent', ['Prototype in native', 'Shared tools to MCP', 'Core stays bespoke']),
    ('Common Mistake', ['One choice made', 'for everything', 'Never per integration']),
])
bottomline(ax, 'A position, not a life sentence. Record the why.', size=26)
save(fig, 'l37-slide7-observations.png')

fig, ax = base()
heading(ax, 'Hands-On + Next', 'hybrids and migrating to MCP', size=46)
cards3(ax, [
    ('Run the Worksheet', ['Two real integrations', 'One stays bespoke', 'One standardizes']),
    ('Write the Reasoning', ['Which question', 'decided it?', 'What would flip it?']),
    ('Next Lesson', ['Hybrids and', 'Migrating', 'to MCP']),
])
bottomline(ax, 'No reasoning? A preference, not a decision.', size=27)
save(fig, 'l37-slide8-next.png')

# ================= LESSON 38 =================
title_card('l38-slide0-title.png', 'Section 9  \u00b7  Lesson 38',
           ['Hybrids and', 'Migrating to MCP'])

fig, ax = base()
heading(ax, 'Hybrid Pattern One', 'MCP for the platform, native edges', size=46)
cards3(ax, [
    ('MCP Platform', ['Shared tool catalog', 'Customer, KB,', 'ticketing, search']),
    ('Native Edges', ['Product-specific', 'Tight model fit', 'Not yet migrated']),
    ('One Catalog', ['Client presents both', 'Model does not care', 'Boundary documented']),
])
bottomline(ax, 'Documented boundary: architecture, not accumulation.', size=25)
save(fig, 'l38-slide1-platform.png')

fig, ax = base()
heading(ax, 'Hybrid Pattern Two', 'MCP servers wrapping bespoke cores', size=46)
cards3(ax, [
    ('Bespoke Core Stays', ['Hand-tuned code', 'Control + latency', 'Properties intact']),
    ('Thin MCP Wrapper', ['Clean tool interface', 'Facade pattern', 'Standard front door']),
    ('What It Buys', ['Portability', 'Discovery', 'Governance']),
])
bottomline(ax, 'Custom code stays. It gains a standard front door.', size=26)
save(fig, 'l38-slide2-wrapping.png')

fig, ax = base()
heading(ax, 'Hybrid Pattern Three', 'bespoke orchestration over MCP tools', size=44)
cards3(ax, [
    ('Engine Is Code', ['Sequencing, state,', 'compensation, retries', 'Full control in code']),
    ('Steps Call MCP', ['Each step calls', 'an MCP tool', 'Governed + portable']),
    ('Boundaries Explicit', ['Document which lives', 'where, and why', 'Never collapse them']),
])
bottomline(ax, 'Deliberate hybrid: architecture. Accidental: debt.', size=26)
save(fig, 'l38-slide3-orchestration.png')

fig, ax = base()
heading(ax, 'Phases One and Two', 'inventory, then wrap, never rewrite', size=46)
cards3(ax, [
    ('Phase 1: Inventory', ['Catalog every tool', 'Owner + format', 'Who depends on it']),
    ('Prioritize Sharing', ['Shared tools first', 'Most gain from', 'standardizing']),
    ('Phase 2: Wrap', ['Thin MCP server', 'Around existing code', 'Logic untouched']),
])
bottomline(ax, 'Only the interface changes. Blast radius stays small.', size=25)
save(fig, 'l38-slide4-migrate12.png')

fig, ax = base()
heading(ax, 'Phases Three and Four', 'cut over per tool, then govern', size=44)
cards3(ax, [
    ('Phase 3: Cut Over', ['One tool at a time', 'Original as fallback', 'Rollback stays open']),
    ('Watch the Logs', ['Argument shapes', 'Error rates, latency', 'Under real load']),
    ('Phase 4: Govern', ['Standard auth', 'Approvals + pinning', 'Catalog discovery']),
])
bottomline(ax, 'Retire bespoke only after MCP carries real traffic.', size=26)
save(fig, 'l38-slide5-migrate34.png')

fig, ax = base()
heading(ax, 'The Two Pitfalls', 'order, and what ruins migrations', size=46)
cards3(ax, [
    ('The Order', ['Highest reuse,', 'lowest risk first', 'Early wins fund it']),
    ('Pitfall 1: Leakage', ["Provider-isms don't", 'translate to MCP', 'Scrub at wrap time']),
    ('Pitfall 2: Gov Gap', ['Ad hoc auth must', 'not be inherited', 'Apply Section 7']),
])
bottomline(ax, 'Standard interface, old insecurity: half done.', size=26)
save(fig, 'l38-slide6-pitfalls.png')

fig, ax = base()
heading(ax, 'Section Close', 'choose per integration, record reasoning', size=46)
cards3(ax, [
    ('Native Optimizes', ['Speed', 'Provider fit', 'Simplicity']),
    ('MCP Optimizes', ['Portability', 'Ecosystem', 'Governance']),
    ('Bespoke Optimizes', ['Control', 'Unusual shapes', 'Latency']),
])
bottomline(ax, 'Deliberate assignment, not a compromise.', size=27)
save(fig, 'l38-slide7-close.png')

fig, ax = base()
heading(ax, 'Hands-On + Next', 'testing MCP servers like APIs', size=46)
cards3(ax, [
    ('Draft the Plan', ['Facade design', 'Cut-over order', 'Retirement criteria']),
    ('Define the Cycle', ['Full operational', 'cycle, written down', 'For this integration']),
    ('Next: Section 10', ['Testing MCP Servers', 'Like APIs:', 'Unit Tests']),
])
bottomline(ax, 'An API whose caller is a probabilistic model.', size=27)
save(fig, 'l38-slide8-next.png')

print('ALL SLIDES DONE')
