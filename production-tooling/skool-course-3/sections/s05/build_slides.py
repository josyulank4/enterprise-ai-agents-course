"""Slide deck builder for Skool Course 3, Section 5 (Lessons 18-21).

Visual system copied from Course 2 s00 / Course 3 s04 build_slides.py:
dark navy BG, gold accents, clean cards, DejaVu Sans, 1920x1080.
One title card + one content slide per remaining beat, per lesson.
Footer: MCP ARCHITECTURE · BUILDING TOOL-USING AI SYSTEMS
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import os

D = os.path.expanduser(
    '~/workspace/udemy-skool/skool-course-3-mcp-architecture/sections/s05/slides')
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


def heading(ax, text, sub=None, size=54):
    ax.text(W / 2, 9.3, text, color=WHITE, fontsize=size, ha='center',
            va='center', weight='bold', family=FONT)
    if sub:
        ax.text(W / 2, 8.35, sub, color=GOLD, fontsize=31, ha='center',
                va='center', family=FONT)


def card(ax, x, y, w, h, title, lines, title_size=26, line_size=22):
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


def cards3(ax, c1, c2, c3):
    card(ax, 1.0, 3.05, 5.3, 4.35, c1[0], c1[1])
    card(ax, 6.95, 3.05, 5.3, 4.35, c2[0], c2[1])
    card(ax, 12.9, 3.05, 5.3, 4.35, c3[0], c3[1])


def cards2(ax, c1, c2):
    card(ax, 1.6, 3.05, 7.4, 4.35, c1[0], c1[1])
    card(ax, 10.2, 3.05, 7.4, 4.35, c2[0], c2[1])


def list_slide(ax, rows):
    ax.add_patch(FancyBboxPatch((2.1, 2.95), 15.0, 4.55,
                                boxstyle='round,pad=0.08,rounding_size=0.25',
                                facecolor=CARD, edgecolor=GOLD, linewidth=1.5))
    yy = 6.85
    for lead, rest in rows:
        ax.text(3.0, yy, lead, color=GOLD, fontsize=25, ha='left',
                va='center', weight='bold', family=FONT)
        ax.text(8.4, yy, rest, color=WHITE, fontsize=25, ha='left',
                va='center', family=FONT)
        yy -= 0.92


def bottomline(ax, text, size=30):
    ax.text(W / 2, 1.95, text, color=GOLD, fontsize=size, ha='center',
            va='center', weight='bold', family=FONT)


def save(fig, name):
    fig.savefig(os.path.join(D, name), facecolor=BG)
    plt.close(fig)
    print('saved', name)


def title_card(name, section_line, title_lines, author='Naveen Kumar Josyula'):
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
    ax.text(W / 2, 1.85, author, color=GREY, fontsize=30,
            ha='center', va='center', family=FONT)
    save(fig, name)


def next_card(name, gold_lines, white_line, section_line):
    fig, ax = base()
    ax.text(W / 2, 7.9, 'Next Lesson', color=WHITE, fontsize=84, ha='center',
            va='center', weight='bold', family=FONT)
    yy = 6.15
    for gl in gold_lines:
        ax.text(W / 2, yy, gl, color=GOLD, fontsize=40, ha='center',
                va='center', weight='bold', family=FONT)
        yy -= 0.85
    ax.text(W / 2, 4.35, white_line, color=WHITE, fontsize=28,
            ha='center', va='center', family=FONT)
    ax.text(W / 2, 3.15, section_line, color=GREY, fontsize=25,
            ha='center', va='center', family=FONT)
    save(fig, name)


SEC5 = 'Section 5 \u00b7 The Three Primitives in Depth'

# ================= LESSON 18 =================
title_card('l18-slide0-title.png', 'Section 5  \u00b7  Lesson 18',
           ['Three Control Models', 'and Resources in Depth'])

fig, ax = base()
heading(ax, 'Who Decides?', 'The most important sentence in this section.', size=46)
list_slide(ax, [
    ('Tools', 'Model-controlled'),
    ('Resources', 'Application-controlled'),
    ('Prompts', 'User-controlled'),
    ('Control', 'Meaning, not mechanism'),
])
bottomline(ax, 'Who decides this capability gets used?')
save(fig, 'l18-slide1-control.png')

fig, ax = base()
heading(ax, 'The Category Error', 'Wrong primitive, broken design.')
cards3(ax,
       ('The Error', ['Model initiative', 'where user should', 'have it']),
       ('The Cost', ['Wrong party decides', 'Correctly executing', 'wrong authority']),
       ('The Lens', ['Ask who decides', 'before how it works', 'Every capability']))
bottomline(ax, 'No schema polish saves a wrong control model.', size=28)
save(fig, 'l18-slide2-error.png')

fig, ax = base()
heading(ax, 'Resources: Stable URIs', 'Data behind stable addresses.')
cards3(ax,
       ('The Data', ['Files, records', 'API responses', 'Reports']),
       ('The URI', ['A namespace', 'Not a transport', 'Server maps it']),
       ('Stability', ['Meaningful, boring', 'Same record,', 'same address']))
bottomline(ax, 'Design URIs like public identifiers.')
save(fig, 'l18-slide3-uris.png')

fig, ax = base()
heading(ax, 'Direct vs Templates', 'Bounded lists, unbounded patterns.')
cards2(ax,
       ('Direct Resources', ['Individually listed', 'URI, name, type', 'Bounded sets']),
       ('Templates', ['Pattern + parameter', 'Client expands it', 'Too large to list']))
bottomline(ax, 'Honest types. Annotations. Last-modified.', size=28)
save(fig, 'l18-slide4-templates.png')

fig, ax = base()
heading(ax, 'Subscriptions', 'Context that tracks a living system.')
cards2(ax,
       ('The Problem', ['Snapshot at start', 'World moves on', 'Stale context']),
       ('The Fix', ['Change notifications', 'listChanged re-list', 'Host refreshes view']))
bottomline(ax, 'Design for resources whose value decays.', size=28)
save(fig, 'l18-slide5-subscriptions.png')

fig, ax = base()
heading(ax, 'Resources Never Act', 'Read-only, with no exceptions.')
cards3(ax,
       ('The Rule', ['Reading changes', 'nothing', 'Ever']),
       ('The Smuggle', ['Counter, mark-read', 'Recalculation', 'A tool in disguise']),
       ('The Guarantee', ['Safe to surface', 'Safe to cache', 'Safe to share']))
bottomline(ax, 'Break it once, no host trusts any read.')
save(fig, 'l18-slide6-never-act.png')

fig, ax = base()
heading(ax, 'Resource or Tool?', 'The first pass.')
cards2(ax,
       ('Resource', ['Host decides reads', 'Changes nothing', 'Stable identifier']),
       ('Tool', ['Model decides to act', 'Changes the world', 'Situational params']))
bottomline(ax, 'Customer record: resource. Refund: tool.', size=28)
save(fig, 'l18-slide7-first-pass.png')

fig, ax = base()
heading(ax, 'Hands-On: Five Resources', 'The s05 resource planner.', size=46)
cards2(ax,
       ('Model Each Source', ['Write the URI', 'Direct or template', 'State content type']),
       ('Note Behaviour', ['Static or live?', 'Subscription-worthy?', 'Catalog-changing?']))
bottomline(ax, 'A read that changes something is a tool.')
save(fig, 'l18-slide8-handson.png')

next_card('l18-slide9-next.png',
          ['Tools in Depth'],
          'Granularity, outputs, and errors a model can use.',
          SEC5)

# ================= LESSON 19 =================
title_card('l19-slide0-title.png', 'Section 5  \u00b7  Lesson 19',
           ['Tools in Depth'])

fig, ax = base()
heading(ax, 'Granularity: One Job', 'One tool, one job.')
cards3(ax,
       ('The Monolith', ['Create + assign', '+ notify', 'Wrong third, often']),
       ('Compose Instead', ['Small tools', 'Model sequences', 'Each step legible']),
       ('Small Surface', ['Three params beat', 'fifteen', 'Split the tool']))
bottomline(ax, 'You made the decision easier. That is the job.', size=28)
save(fig, 'l19-slide1-granularity.png')

fig, ax = base()
heading(ax, 'Schemas at Scale', 'Constrain what the domain constrains.', size=46)
cards2(ax,
       ('Prefer Enums', ['low, medium, high', 'Legal every time', 'No normalization']),
       ('Free Text', ['urgent, P1, ASAP', 'Interpret forever', 'Audit for hidden enums']))
bottomline(ax, 'Every constraint deletes runtime failures.', size=28)
save(fig, 'l19-slide2-schemas.png')

fig, ax = base()
heading(ax, 'Output Design', 'Shape results for the next decision.', size=46)
cards3(ax,
       ('Give Fields', ['What model needs', 'IDs to pass on', 'Nothing buried']),
       ('Output Schemas', ['Parse reliably', 'Not scraped prose', 'If fields extracted']),
       ('Large Results', ['Summary + resource', 'Read in pieces', 'Progress notices']))
bottomline(ax, 'The tool acts. The resource carries bulk.', size=28)
save(fig, 'l19-slide3-output.png')

fig, ax = base()
heading(ax, 'Errors Are Interface', 'Classify every error you return.')
list_slide(ax, [
    ('Retryable', 'Same call may succeed shortly'),
    ('Caller-fixable', 'Argument must change'),
    ('Fatal', 'Stop and re-plan'),
    ('Specific', 'Name record and problem'),
])
bottomline(ax, 'A model that understands errors recovers.')
save(fig, 'l19-slide4-errors.png')

fig, ax = base()
heading(ax, 'Annotations and Honesty', 'Hints become policy inputs.')
cards3(ax,
       ('The Hints', ['Read-only', 'Destructive', 'Open-world']),
       ('Client Use', ['Auto-approve safe', 'Confirm destructive', 'Trust decisions']),
       ('The Limit', ['Hints inform policy', 'Never enforce', 'Server validates']))
bottomline(ax, 'A dressed-up destructive tool is a lie.', size=28)
save(fig, 'l19-slide5-annotations.png')

fig, ax = base()
heading(ax, 'Naming Decides Calls', "The model's first decision.")
cards3(ax,
       ('Verb Phrases', ['Domain vocabulary', 'Consistent prefixes', 'Predictable names']),
       ('Audit as a Set', ['Side by side', 'As model sees them', 'No near-twins']),
       ('Make It Easy', ['Right choice is', 'the easy choice', 'Obvious distinction']))
bottomline(ax, 'Audit names the way the model sees them.')
save(fig, 'l19-slide6-naming.png')

fig, ax = base()
heading(ax, 'Hands-On: Refactor It', 'The s05 monolith tool.', size=46)
cards2(ax,
       ('Refactor', ['Small tools', 'Tight schemas', 'Classified errors']),
       ('Measure', ['Same task suite', 'Compare call success', 'Defend with numbers']))
bottomline(ax, 'See granularity win in numbers.')
save(fig, 'l19-slide7-handson.png')

next_card('l19-slide8-next.png',
          ['Prompts in Depth'],
          'The user-controlled playbooks of a domain.',
          SEC5)

# ================= LESSON 20 =================
title_card('l20-slide0-title.png', 'Section 5  \u00b7  Lesson 20',
           ['Prompts in Depth'])

fig, ax = base()
heading(ax, "The Domain's Rituals", 'Repeatable patterns, captured once.', size=46)
cards3(ax,
       ('The Rituals', ['Code review', 'Incident triage', 'Weekly report']),
       ('Captured Once', ['Parameterized', 'User invokes it', 'Order preserved']),
       ('With Context', ['Resources embedded', 'Arrives grounded', 'Specs from user']))
bottomline(ax, 'Where institutional knowledge lives.')
save(fig, 'l20-slide1-rituals.png')

fig, ax = base()
heading(ax, 'Template Design', 'Arguments, defaults, and friction.', size=46)
cards3(ax,
       ('Command Names', ['review_pull_request', 'Not prompt one', 'Says what happens']),
       ('Few Required Args', ['Each one is friction', 'Defaults carry', 'common case']),
       ('Examples', ['review_code', 'onboard_vendor', 'Embedded diff']))
bottomline(ax, 'Arguments carry the variation that matters.', size=28)
save(fig, 'l20-slide2-template.png')

fig, ax = base()
heading(ax, 'Opinionated by Design', 'Structure the user chose.')
cards2(ax,
       ('Prompts May Insist', ['Best practices', 'Mandatory orderings', 'Confirmations']),
       ('Tools Stay Free', ['Model judgment', 'Mid-task freedom', 'Do not mix postures']))
bottomline(ax, 'Structure the workflow. Model does thinking.', size=28)
save(fig, 'l20-slide3-opinionated.png')

fig, ax = base()
heading(ax, 'Prompts vs Tool Text', 'Guidance belongs where users invoke it.', size=44)
cards2(ax,
       ('Buried Playbook', ['Fires unasked', 'Mid-task ritual', 'Wrong context']),
       ('The Test', ['Who decides it runs?', 'User, deliberately', 'Then it is a prompt']))
bottomline(ax, 'An authority error users feel as surprise.', size=28)
save(fig, 'l20-slide4-versus.png')

fig, ax = base()
heading(ax, 'A Prompt That Is a Tool', 'The warning sign.')
cards2(ax,
       ('The Pattern', ['One tool, boilerplate', 'Same shape, always', 'Manual step tax']),
       ('The Fix', ['Better tool', 'Smarter defaults', 'Absorb boilerplate']))
bottomline(ax, 'Prompts orchestrate. Tools execute.')
save(fig, 'l20-slide5-warning.png')

fig, ax = base()
heading(ax, 'Versioning and Care', 'Templates are behaviour.')
cards3(ax,
       ('Treat as Code', ['Review edits', 'Stable arg surface', 'Version reflects it']),
       ('Write Clearly', ['Purpose stated', 'Args explained', 'Readable sequence']),
       ('Prune Honestly', ['Owned, current', 'Well-kept shelf', 'Drop dead rituals']))
bottomline(ax, 'Maintain playbooks like product surface.', size=28)
save(fig, 'l20-slide6-versioning.png')

fig, ax = base()
heading(ax, 'Hands-On: Triage Prompt', 'The s05 incident-triage prompt.', size=44)
cards2(ax,
       ('Write It', ['Clear arg names', 'Sensible defaults', 'One embedded resource']),
       ('Invoke and Read', ['From a real client', 'Read as a user', 'Right order? Right checks?']))
bottomline(ax, 'Is this the ritual you meant to encode?', size=28)
save(fig, 'l20-slide7-handson.png')

next_card('l20-slide8-next.png',
          ['Roots, Sampling,', 'Pagination'],
          'Client capabilities and clean boundaries.',
          SEC5)

# ================= LESSON 21 =================
title_card('l21-slide0-title.png', 'Section 5  \u00b7  Lesson 21',
           ['Roots, Sampling, Pagination', 'and Clean Boundaries'])

fig, ax = base()
heading(ax, 'Roots: Sense of Place', 'Where the server may work.')
cards3(ax,
       ('Declared', ['Client offers roots', 'Server never finds', 'them alone']),
       ('Boundaries', ['Respected, always', 'Outside = off-limits', 'Scoped capability']),
       ('In Practice', ['Default scope', 'Degrade gracefully', 'Adjust on change']))
bottomline(ax, 'Servers ask. They never assume.')
save(fig, 'l21-slide1-roots.png')

fig, ax = base()
heading(ax, "Sampling: Borrowed Brain", "Borrowing the client's model.", size=46)
cards3(ax,
       ('The Request', ['Sends messages', 'Client runs model', 'Returns completion']),
       ('Why Borrow', ['Language-shaped jobs', 'Summarize, classify', 'No own keys needed']),
       ('Stay Small', ['Model-agnostic', 'Any client works', "User's trust + cost"]))
bottomline(ax, 'Bounded tasks tied to a visible goal.', size=28)
save(fig, 'l21-slide2-sampling.png')

fig, ax = base()
heading(ax, "Sampling's Risks", 'Design for refusal.')
cards2(ax,
       ('The Risks', ['Crafted exfiltration', 'Budget burn', 'Endless requests']),
       ('Design For It', ['Approval at client', 'Bound completions', 'Fallbacks ready']))
bottomline(ax, 'Keep your hands on the consequences.', size=28)
save(fig, 'l21-slide3-risks.png')

fig, ax = base()
heading(ax, 'Pagination', 'Never swallow the whole world at once.', size=44)
cards3(ax,
       ('Cursor-Based', ['Opaque token', 'Pass it back', 'Next page arrives']),
       ('The Discipline', ['Treat as meaningless', 'No cursor = done', 'Server pages freely']),
       ('Page Well', ['Balance size, trips', 'Stable snapshot', 'No internals leaked']))
bottomline(ax, 'The cursor is a bookmark, not an API.', size=28)
save(fig, 'l21-slide4-pagination.png')

fig, ax = base()
heading(ax, 'Completion', 'Guided names for large spaces.')
cards2(ax,
       ('The Need', ['Name what you want', 'Partial identifier', 'Server suggests']),
       ('The Payoff', ['Guided experience', 'Huge ID spaces', 'No guessing']))
bottomline(ax, 'Pages to walk, suggestions to follow.', size=28)
save(fig, 'l21-slide5-completion.png')

fig, ax = base()
heading(ax, 'Boundaries One and Two', 'One primitive. Domain names.', size=46)
list_slide(ax, [
    ('One primitive', 'Never resource and tool'),
    ('Split it', 'Read = resource, act = tool'),
    ('Domain names', "Consumer's vocabulary"),
    ('Not internals', 'No table names leaked'),
])
bottomline(ax, 'Names are your most-read documentation.', size=28)
save(fig, 'l21-slide6-boundaries12.png')

fig, ax = base()
heading(ax, 'Boundaries Three and Four', 'Granularity, and control.', size=46)
list_slide(ax, [
    ('Granularity', 'One step, one document'),
    ('Control', 'Who decides this runs?'),
    ('Test order', 'Side effects first'),
    ('Then', 'Initiative, scale, freshness'),
])
bottomline(ax, 'Side effects and initiative outvote rest.', size=28)
save(fig, 'l21-slide7-boundaries34.png')

fig, ax = base()
heading(ax, 'Hands-On: Boundary Review', 'The s05 boundary review.', size=44)
cards2(ax,
       ('Classify', ['Every capability', 'Against framework', 'Flag two violations']),
       ('Redesign', ['Corrected primitive', 'Name + granularity', 'Reviews must change things']))
bottomline(ax, 'A review that only complains changes nothing.', size=27)
save(fig, 'l21-slide8-handson.png')

next_card('l21-slide9-next.png',
          ['The Adapter Pattern:', 'MCP as a Facade'],
          'Primitives meet enterprise systems.',
          'Section 6 \u00b7 The Enterprise Facade')

print('ALL SLIDES DONE')
