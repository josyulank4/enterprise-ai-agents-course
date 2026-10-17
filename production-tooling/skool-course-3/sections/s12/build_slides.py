"""Slide builder for Skool Course 3, Section 12 (Lessons 47-48).

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
    '~/workspace/udemy-skool/skool-course-3-mcp-architecture/sections/s12/slides')
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


# ================= LESSON 47 =================
title_card('l47-slide0-title.png', 'Section 12  \u00b7  Lesson 47',
           ['A2A and MCP: Two Protocols,', 'Two Directions'])

fig, ax = base()
heading(ax, 'Two Directions', 'down to tools, sideways to agents', size=50)
cards3(ax, [
    ('MCP: Downward', ['Agent reaches down', 'to tools and data', 'DB, APIs, files, search']),
    ('The Vertical Call', ['Model calls a', 'function; function', 'returns a result']),
    ('A2A: Sideways', ['Agent reaches across', 'to peer agents', 'Delegate + exchange']),
])
bottomline(ax, 'Different directions. Different design problems.', size=26)
save(fig, 'l47-slide1-directions.png')

fig, ax = base()
heading(ax, 'Hands and Colleagues', 'the mental model', size=50)
cards3(ax, [
    ('MCP Gives Hands', ['Tools to act with', 'Query, check, pay', 'Direct capabilities']),
    ('A2A Gives Colleagues', ['Delegate to peers', 'Specialist agents', 'Across teams']),
    ('Worked Example', ['Orchestrator delegates', 'Finance specialist', 'then uses MCP tools']),
])
bottomline(ax, "Neither protocol could do the other's job well.", size=26)
save(fig, 'l47-slide2-hands.png')

fig, ax = base()
heading(ax, 'A2A, Verified', 'cards, tasks, and governance', size=50)
cards3(ax, [
    ('Verified Origins', ['Google: April 2025', 'Now Linux Foundation', 'Agentic AI Foundation']),
    ('Mar 2026: v1.0.0', ['JSON-RPC, gRPC', 'HTTP + JSON bindings', 'Official SDKs']),
    ('Core Concepts', ['Agent Card: caps + auth', 'At a well-known URL', 'Tasks: persistent state']),
])
bottomline(ax, 'A complement to MCP, not a rival.', size=27)
save(fig, 'l47-slide3-verified.png')

fig, ax = base()
heading(ax, 'Draw the Boundary Deliberately', size=44)
cards3(ax, [
    ('Use MCP', ['Agent needs a', 'capability: tool,', 'data, or action']),
    ('Use A2A', ['Work crosses an', 'agent boundary', 'Delegation + state']),
    ('Do Not Leak', ['No agent-as-tool', 'No shared tables', 'for coordination']),
])
bottomline(ax, 'A boundary drawn now is a migration avoided.', size=26)
save(fig, 'l47-slide4-boundary.png')

fig, ax = base()
heading(ax, 'The Registry', 'solving discoverability', size=50)
cards3(ax, [
    ('The Problem', ['Thousands of servers', 'Find the right one', 'Lesson 32, at scale']),
    ('Official Registry', ['Canonical catalog', 'Standard manifest', 'REST API discovery']),
    ('Metadata Only', ['Not a code host', 'Not a storefront', 'What, where, how']),
])
bottomline(ax, 'Protocols interoperate. Registries help you find.', size=25)
save(fig, 'l47-slide5-registry.png')

fig, ax = base()
heading(ax, 'Publishing and Registries', 'private registries, and directories', size=46)
cards3(ax, [
    ('Inspect First', ['Who publishes it?', 'Which version?', 'Which transport?']),
    ('Publish Deliberately', ['server.json manifest', 'Reverse-DNS name', 'Verified namespace']),
    ('Private Front Door', ['Approved servers only', 'Version pinning', 'Audit trail']),
])
bottomline(ax, 'Directories are aids, never authorities.', size=26)
save(fig, 'l47-slide6-publishing.png')

fig, ax = base()
heading(ax, 'Emerging Patterns', 'over the stable base', size=50)
cards3(ax, [
    ('Agent Workflows', ['Planner decomposes', 'A2A to specialists', 'Each wields MCP']),
    ('Agent as Primitive', ['Servers in products', 'One surface serves', 'humans + agents']),
    ('Multi-Modal Tools', ['Text, image, audio', 'Clear media schemas', 'Payload discipline']),
])
bottomline(ax, 'Innovation moves up the stack, to patterns.', size=26)
save(fig, 'l47-slide7-patterns.png')

fig, ax = base()
heading(ax, 'Next: Map Your Own Stack', size=48)
cards3(ax, [
    ('Hold the Division', ['Down: MCP', 'Sideways: A2A', 'Discovery: registry']),
    ('Run the Protocol Map', ['Mark MCP-shaped', 'Mark A2A-shaped', 'Mark neither yet']),
    ('Next Lesson', ['Governance', 'Trust', 'Future-proofing']),
])
bottomline(ax, 'Seeing it on one page makes governance concrete.', size=25)
save(fig, 'l47-slide8-next.png')

# ================= LESSON 48 =================
title_card('l48-slide0-title.png', 'Section 12  \u00b7  Lesson 48',
           ['Governance, Trust,', 'and Future-Proofing'])

fig, ax = base()
heading(ax, 'Consolidation', 'the standards war is over', size=50)
cards3(ax, [
    ('One Foundation', ['MCP + A2A together', 'Linux Foundation', 'Agentic AI Foundation']),
    ('Tightening Ahead', ['Auth + identity flow', 'Typing + versioning', 'MCP-A2A boundary']),
    ('Build Accordingly', ['Build to current spec', 'Isolate the seams', 'Config, not rewrite']),
])
bottomline(ax, 'It standardizes the seams. Architecture stands.', size=25)
save(fig, 'l48-slide1-consolidation.png')

fig, ax = base()
heading(ax, 'The Trust Problem', 'interfaces are not intentions', size=50)
cards3(ax, [
    ('Claims, Not Proof', ['Schema = interface', 'Card = claimed caps', 'Not verified behavior']),
    ('Verify Yourself', ['Who maintains it?', 'How often updated?', 'Permissions required?']),
    ('Posture Now', ['Least privilege', 'Provenance tracking', 'Oversight by stakes']),
])
bottomline(ax, 'Verify for yourself, regardless of any badge.', size=26)
save(fig, 'l48-slide2-trust.png')

fig, ax = base()
heading(ax, 'Identity and Economics', 'two more hard problems', size=48)
cards3(ax, [
    ('Identity Question', ['Whose authority?', 'User, operator,', 'or developer?']),
    ('Design for Stricter', ['Centralize policy', 'Log every choice', 'No blanket authority']),
    ('Economics', ["Goodwill won't fund", 'maintenance + review', 'Prefer sustained servers']),
])
bottomline(ax, 'Contribute back to the commons you depend on.', size=26)
save(fig, 'l48-slide3-identity.png')

fig, ax = base()
heading(ax, 'Build Versus Buy', 'applied to the roadmap', size=50)
cards3(ax, [
    ('Buy the Commodity', ['Standards commoditize', 'Connectors + search', 'Cheaper than building']),
    ('Build the Difference', ['Unique data +', 'workflows compose', 'Return rises']),
    ('Apply the Rule', ['Buy commodity', 'Build differentiating', "Question 'special'"]),
])
bottomline(ax, 'Buy the commodity. Build the differentiating.', size=26)
save(fig, 'l48-slide4-roadmap.png')

fig, ax = base()
heading(ax, 'Future-Proofing, Part One', 'contracts and seams', size=46)
cards3(ax, [
    ('Stay Cheap to Adapt', ['Not prediction', 'Cheap adaptation', 'when forecasts fail']),
    ('1: Own Contracts', ['Version + test them', 'Document + deliberate', 'Slow is a feature']),
    ('2: Thin Seams', ['Transport, auth,', 'discovery isolated', 'Localized change']),
])
bottomline(ax, 'Contracts are the slowest-moving part. Good.', size=26)
save(fig, 'l48-slide5-contracts.png')

fig, ax = base()
heading(ax, 'Future-Proofing, Part Two', 'composition, fundamentals, engagement', size=44)
cards3(ax, [
    ('3: Composition', ['Prefer standards', 'Extend at provided', 'points, not around']),
    ('4: Fundamentals', ['Injection testing', 'Observability', 'Safe rollouts']),
    ('5: Stay Engaged', ['Track spec repos', 'Pilot revisions', 'Early warning']),
])
bottomline(ax, 'The surprised organizations stopped looking.', size=26)
save(fig, 'l48-slide6-composition.png')

fig, ax = base()
heading(ax, 'Build on What Endures', size=50)
cards3(ax, [
    ('What Endures', ['Roles + primitives', 'Transports', 'Security posture']),
    ('Hide the Volatile', ['Version details', 'behind facades', 'Lesson 22 pattern']),
    ('Verify Before Ship', ['Check current spec', 'on fast-moving', 'details']),
])
bottomline(ax, 'Survive revisions instead of being stranded.', size=26)
save(fig, 'l48-slide7-endures.png')

fig, ax = base()
heading(ax, 'Next: Your Position Note', 'then the capstone', size=48)
cards3(ax, [
    ('Write the Note', ['Per capability family', 'Adopt, build,', 'buy, or wait']),
    ('Add the Trigger', ['What would change', 'the answer?', 'Opinion to strategy']),
    ('Next: Capstone', ['Section 13 design', 'Production architecture', 'Graded by checklist']),
])
bottomline(ax, 'A position with a trigger is a strategy.', size=27)
save(fig, 'l48-slide8-next.png')

print('ALL SLIDES DONE')
