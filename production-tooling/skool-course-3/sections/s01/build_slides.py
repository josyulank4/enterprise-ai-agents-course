"""Slide builder for Skool Course 3, Section 1 (Lessons 1-4).

Visual system copied from Course 2 s00 build_slides.py: dark navy BG
#0e1a2b, gold #e0a83c, white, grey #b8c4d4, card #16283f, DejaVu Sans,
1920x1080, gold rule near top, footer centered at bottom.
Footer: MCP ARCHITECTURE - BUILDING TOOL-USING AI SYSTEMS
One title card + one content slide per remaining beat, per lesson.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import os

D = os.path.expanduser(
    '~/workspace/udemy-skool/skool-course-3-mcp-architecture/sections/s01/slides')
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


def heading(ax, text, sub=None, size=52):
    ax.text(W / 2, 9.3, text, color=WHITE, fontsize=size, ha='center',
            va='center', weight='bold', family=FONT)
    if sub:
        ax.text(W / 2, 8.35, sub, color=GOLD, fontsize=32, ha='center',
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


def bottomline(ax, text, size=29):
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


# ================= LESSON 1 =================
title_card('l01-slide0-title.png', 'Section 1  \u00b7  Lesson 1',
           ['Welcome: The Protocol', 'That Gives Agents Hands'])

fig, ax = base()
heading(ax, "Priya's Forty Minutes", '12 steps, 4 systems')
cards3(ax, [
    ('The Ticket', ['Invoices generating', 'with the wrong', 'tax rate']),
    ('The Work', ['Ticketing + account', 'Billing console', 'Tax-rate database']),
    ('The Cost', ['Correct, re-run, verify', 'Reply to customer', 'Forty minutes']),
])
bottomline(ax, 'Mostly lookups and small, careful writes.')
save(fig, 'l01-slide1-priya.png')

fig, ax = base()
heading(ax, 'The Fluent, Paralyzed Agent', 'all brain, no hands', size=48)
cards3(ax, [
    ('It Understands', ['Reads the ticket', 'Summarizes beautifully', 'Drafts a reply']),
    ('It Cannot Act', ['Open admin console', 'Query the tax table', 'Re-run invoice job']),
    ('The Gap', ['What it can say', 'vs what it can do', 'An engineering problem']),
])
bottomline(ax, "Same model, right tools: forty minutes in four.")
save(fig, 'l01-slide2-paralyzed.png')

fig, ax = base()
heading(ax, 'Before / After the Standard', size=48)
cards3(ax, [
    ('The Pattern', ['Relational databases', 'HTTP for the web', 'Containers for', 'deployment']),
    ('Before', ['Every integration', 'bespoke', 'Expensive to build', 'Impossible to reuse']),
    ('After', ['An ecosystem explodes', 'Compose, not reinvent', 'Builders can build']),
])
bottomline(ax, 'One abstraction reorganizes an industry.')
save(fig, 'l01-slide3-standard.png')

fig, ax = base()
heading(ax, 'MCP', 'one protocol, many models, many servers')
cards3(ax, [
    ('Open Standard', ['Connects AI systems', 'to tools and data', 'they need']),
    ('Build Once', ['Each integration', 'as an MCP server', 'Composable by design']),
    ('Every Client', ['Every compatible', 'MCP client', 'can use it']),
])
bottomline(ax, 'How it works. How to build, secure, and run it.', size=28)
save(fig, 'l01-slide4-mcp.png')

fig, ax = base()
heading(ax, 'Course Map', 'model \u2192 build \u2192 harden \u2192 production', size=44)
cards3(ax, [
    ('Model: 1\u20133', ['Why tools matter', 'What the protocol is', 'Hosts, clients, servers']),
    ('Build: 4\u20136', ['Your first server', 'The three primitives', 'Enterprise systems']),
    ('Beyond: 7\u201313', ['Security + orchestration', 'Honest comparisons', 'Production + capstone']),
])
bottomline(ax, 'From first principles to production fleets.')
save(fig, 'l01-slide5-course-map.png')

fig, ax = base()
heading(ax, 'The Honest Bar', 'architecture endures, syntax churns')
cards3(ax, [
    ('Fast-Moving', ['MCP is a standard', 'still evolving', 'SDK details change']),
    ('What Endures', ['Host / client / server', 'The three primitives', 'Transports + security']),
    ('My Promise', ['Scenarios labelled', 'Uncertainty stated', 'Principles taught']),
])
bottomline(ax, 'Written against architecture, not a snapshot.')
save(fig, 'l01-slide6-honest-bar.png')

fig, ax = base()
heading(ax, 'Who This Is For')
cards3(ax, [
    ('Engineers', ['Build MCP servers', 'and clients']),
    ('Architects', ['Decide where MCP fits', 'in platform strategy']),
    ('Leaders', ['Understand what the', 'standard changes', 'about AI investment']),
])
bottomline(ax, 'Prerequisites: APIs, JSON, distributed systems.', size=28)
save(fig, 'l01-slide7-audience.png')

fig, ax = base()
heading(ax, 'Next', 'setting up, then the brilliant prisoner')
cards3(ax, [
    ('Two Habits', ['Run each section demo', 'before continuing', 'Keep the checklists']),
    ('Next Lesson', ['Use this course', 'Set up the repository', 'Hello-MCP check']),
    ('Then We Begin', ['The brilliant prisoner', 'What models can', 'and cannot do']),
])
bottomline(ax, 'Patterns to copy, not a framework to install.', size=28)
save(fig, 'l01-slide8-next.png')

# ================= LESSON 2 =================
title_card('l02-slide0-title.png', 'Section 1  \u00b7  Lesson 2',
           ['How to Use This Course', 'and the Code Repository'])

fig, ax = base()
heading(ax, 'Thirteen Sections', 'twelve chapters, one appendix')
cards3(ax, [
    ('The Mapping', ['13 sections', '12 book chapters', '+ production appendix']),
    ('Two Forms', ['Narration: reasoning', 'Written: the detail', 'you return to']),
    ('Use the Detail', ['When building', 'When reviewing', 'Defending a design']),
])
bottomline(ax, 'The book and the course make the same journey.', size=28)
save(fig, 'l02-slide1-sections.png')

fig, ax = base()
heading(ax, 'The Journey', 'model, build, harden, production')
cards3(ax, [
    ('Build the Model', ['Sections 1\u20133', 'Concepts first', 'Deliberately']),
    ('The Build', ['Sections 4\u20136', 'Servers, primitives', 'Enterprise connections']),
    ('Harden + Produce', ['Sections 7\u201313', 'Security to production', 'Capstone design studio']),
])
bottomline(ax, 'Experienced? Enter later sections diagnostically.', size=27)
save(fig, 'l02-slide2-journey.png')

fig, ax = base()
heading(ax, 'Every Section Ends Runnable', size=46)
cards3(ax, [
    ('Runnable Demo', ['Every section', 'ends the same way', 'with a demo']),
    ('Reusable Aid', ['A checklist', 'or decision aid', 'to keep']),
    ('Finished Means', ['Demo run', 'Artifact kept', 'Not just listened']),
])
bottomline(ax, 'Skip the demos and the vocabulary will not hold.', size=27)
save(fig, 'l02-slide3-runnable.png')

fig, ax = base()
heading(ax, 'The Repository', 'one demo per section')
cards3(ax, [
    ('Real Code', ['MCP servers', 'MCP clients', 'Written to be read']),
    ('Patterns to Copy', ['Not a framework', 'to install', 'Nothing hidden']),
    ('Why It Matters', ['See a client connect', 'and make a tool call', 'Magic breaks first']),
])
bottomline(ax, 'Adapt the pattern to your own system.')
save(fig, 'l02-slide4-repository.png')

fig, ax = base()
heading(ax, 'Plain Python', 'standard library only')
cards2(ax, [
    ('The Choice', ['The protocol stays visible', 'Discovery and invocation', 'The shape of the exchange']),
    ('Later, an SDK', ['Choose one for real work', 'Know what it does for you', 'Debug it when it leaks']),
])
bottomline(ax, 'Learn MCP, not a favourite library.')
save(fig, 'l02-slide5-plain-python.png')

fig, ax = base()
heading(ax, 'How to Study', 'run it, then map it to your systems', size=46)
cards3(ax, [
    ('Step 1: Run It', ['After each section', 'Run its demo', 'Before you continue']),
    ('Step 2: Map It', ['Point the demo at', 'your own systems', 'on paper']),
    ('The Question', ['What would the server', 'expose \u2014 and what', 'would it refuse?']),
])
bottomline(ax, 'That is where a course becomes your architecture.', size=27)
save(fig, 'l02-slide6-study.png')

fig, ax = base()
heading(ax, 'What Lasts', 'checklists, tables, code')
cards3(ax, [
    ('Durable Artifacts', ['The checklists', 'The comparison tables', 'The repository code']),
    ('Decision Aids', ['Tables are aids', 'not verdicts', 'Reason with constraints']),
    ('The Walkthrough', ['Narration guides you', 'The reference', 'is what you keep']),
])
bottomline(ax, 'The right answer depends on your systems.')
save(fig, 'l02-slide7-lasts.png')

fig, ax = base()
heading(ax, 'A Note on the Voice', 'and your first run')
cards3(ax, [
    ('AI Voiceover', ['Every lesson', 'Listen for concepts', 'Written material governs']),
    ('Your Hands-On', ['Clone the repository', 'Run python validate.py', 'Section one check']),
    ('Hello-MCP', ['Client to server', 'One tool call', 'Under a minute']),
])
bottomline(ax, 'Do not continue until it passes on your machine.', size=27)
save(fig, 'l02-slide8-voice.png')

# ================= LESSON 3 =================
title_card('l03-slide0-title.png', 'Section 1  \u00b7  Lesson 3',
           ['The Brilliant Prisoner:', 'What Models Can and Cannot Do'])

fig, ax = base()
heading(ax, 'What a Model Actually Is', size=48)
cards3(ax, [
    ('One Thing', ['Trained on vast text', 'to predict what', 'should come next']),
    ('Emergent Feats', ['Fluency + reasoning', 'Summarization', 'Translation + code']),
    ('Versatile', ['Draft a legal memo', 'Debug a system', 'Explain anything']),
])
bottomline(ax, 'The most versatile text engine ever built.', size=28)
save(fig, 'l03-slide1-model.png')

fig, ax = base()
heading(ax, 'Every Feat Is a Performance', 'of language', size=46)
cards3(ax, [
    ('Inside Its Mind', ['Drafting + reasoning', 'Summarizing + coding', 'Staged in language']),
    ('Touches Nothing', ['Systems it cannot see', 'Data it cannot reach', 'Words about the world']),
    ('The Boundary', ['Not a criticism', 'A description', 'Architecture is', 'boundaries']),
])
bottomline(ax, 'Brilliant \u2014 and entirely inside its own mind.', size=28)
save(fig, 'l03-slide2-performance.png')

fig, ax = base()
heading(ax, 'The World Ends', 'at the context boundary')
cards3(ax, [
    ('No Eyes', ['On your systems', "Today's sales figures?", 'It cannot look them up']),
    ('No Hands', ['On your data', 'Cancel that order?', 'It cannot touch it']),
    ('No Standing', ['In your organization', 'A mind with no body', 'It can only advise']),
])
bottomline(ax, 'A consultant who can never pick up the phone.', size=28)
save(fig, 'l03-slide3-boundary.png')

fig, ax = base()
heading(ax, 'Work Starts at Zero', 'and you do the execution')
cards3(ax, [
    ('Systems of Record', ['Customer databases', 'Code + calendars', 'Tickets + ledgers']),
    ('Starting From Zero', ['Whatever you paste in', 'is all it has', 'You execute the work']),
    ('What Is Needed', ['Not better suggestions', 'Systems that can', 'safely act']),
])
bottomline(ax, 'The central bottleneck of applied AI.')
save(fig, 'l03-slide4-zero.png')

fig, ax = base()
heading(ax, 'The Agentic Turn', 'answering versus acting')
cards3(ax, [
    ('A Chatbot Answers', ['Waits for your message', 'Output is text', 'Questions answered']),
    ('An Agent Acts', ['Plans + executes steps', 'Observes + adjusts', 'Output: changed state']),
    ('An Agent Needs', ['A goal + reasoning', 'Memory of attempts', 'Tools \u2014 crucially']),
])
bottomline(ax, 'A strategist with no army changes nothing.')
save(fig, 'l03-slide5-agentic.png')

fig, ax = base()
heading(ax, 'The Same Request', 'two different systems')
cards3(ax, [
    ('Ask a Chatbot', ['A template', 'Advice on content', 'Yours to execute']),
    ('Ask an Agent', ['Queries the tracker', 'Pulls commits + calendar', 'Drafts + saves report']),
    ('The Difference', ['Not a smarter model', 'The same model', 'Armed with tools']),
])
bottomline(ax, 'Helpful is good. Transformative is armed.')
save(fig, 'l03-slide6-request.png')

fig, ax = base()
heading(ax, 'Capability Means What It Can Do', size=44)
cards3(ax, [
    ('Old Benchmarks', ['Bar exams + puzzles', 'Math competitions', 'What a model knows']),
    ('The New Measure', ['Tools it can wield', 'Reliability of calls', 'Handling failure']),
    ('The Result', ['Mid-tier + tooling', 'outperforms a frontier', 'model in a chat box']),
])
bottomline(ax, 'The revolution is not in the brain. It is in the hands.', size=26)
save(fig, 'l03-slide7-capability.png')

fig, ax = base()
heading(ax, 'The Trust Stakes Rise', 'the moment it can act')
cards3(ax, [
    ('Chatbot Error', ['A wrong answer', 'You notice it', 'You correct it']),
    ('Agent Error', ['Data deleted', 'Wrong message sent', 'Wrong account charged']),
    ('Trust Infrastructure', ['Discover + describe', 'Authorize + invoke', 'Audit every call']),
])
bottomline(ax, 'A protocol for tool use is a protocol for trust.', size=27)
save(fig, 'l03-slide8-trust.png')

fig, ax = base()
heading(ax, 'Your Capability Audit', 'then the integration chaos')
cards3(ax, [
    ('Run the Audit', ['Section one audit', 'In the repository', 'One use-case you own']),
    ('List It Honestly', ['What must it perceive?', 'What must it change?', 'In the world']),
    ('Mark the Tools', ['Which actions exist', 'as tools today?', 'Empty list = roadmap']),
])
bottomline(ax, 'Next: The N\u00d7M Problem \u2014 why a standard had to exist.', size=26)
save(fig, 'l03-slide9-audit.png')

# ================= LESSON 4 =================
title_card('l04-slide0-title.png', 'Section 1  \u00b7  Lesson 4',
           ['The N\u00d7M Problem:', 'Why a Standard Had to Exist'])

fig, ax = base()
heading(ax, 'The Patchwork', 'every vendor, its own format')
cards3(ax, [
    ('Each Provider', ['Own function format', 'Own JSON dialect', 'Own conventions']),
    ('Your Code', ['Parse the output', 'Dispatch + execute', 'Format the result back']),
    ('Switch Models', ['Rewrite', 'the integration', 'Start again']),
])
bottomline(ax, 'Patchwork is a generous word for it.')
save(fig, 'l04-slide1-patchwork.png')

fig, ax = base()
heading(ax, 'Fragmentation Ran Deeper', 'than formats', size=48)
cards3(ax, [
    ('The Tool-Use Loop', ['How calls are signalled', 'Parallel calls?', 'Results fed back']),
    ('No Shared Vocabulary', ['For the life', 'of a tool call', 'Errors included']),
    ('Nothing Transferred', ['Tutorials + libraries', 'Security reviews', 'Best practices']),
])
bottomline(ax, 'Every team paid tuition nobody could reuse.', size=28)
save(fig, 'l04-slide2-fragmentation.png')

fig, ax = base()
heading(ax, 'The Mirror Problem', 'the tools faced it too', size=48)
cards3(ax, [
    ('Same Question', ['Database vendor', 'SaaS company', 'Internal platform team']),
    ('The Grim Choice', ['One connector', 'per provider, forever', 'Or pick just one']),
    ('The Cost', ['Roadmaps filled with', 'connector maintenance', 'Debugging was miserable']),
])
bottomline(ax, 'How do we expose this to agents? No standard answer.', size=26)
save(fig, 'l04-slide3-mirror.png')

fig, ax = base()
heading(ax, 'The Arithmetic', 'N times M')
cards3(ax, [
    ('Without a Standard', ['N AI applications', 'M useful tools', 'Every pair custom']),
    ('The Burden', ['N multiplied by M', 'Built, tested, secured', 'Maintained', 'independently']),
    ('In Practice', ['10 \u00d7 100 = 1,000', 'bespoke integrations', 'The matrix stayed sparse']),
])
bottomline(ax, 'Users got a thin slice of what was possible.', size=28)
save(fig, 'l04-slide4-arithmetic.png')

fig, ax = base()
heading(ax, 'Both Sides Exploding', 'at once', size=48)
cards3(ax, [
    ('The N Side', ['New model providers', 'Agent frameworks', 'AI applications monthly']),
    ('The M Side', ['Every software product', 'Database + dev tool', 'Every internal system']),
    ('The Need', ['A neutral meeting ground', 'Belonging to', 'no single vendor']),
])
bottomline(ax, 'A multiplicative burden only gets worse with time.', size=26)
save(fig, 'l04-slide5-exploding.png')

fig, ax = base()
heading(ax, 'How Standards Collapse It', 'N\u00d7M into N+M', size=46)
cards3(ax, [
    ('The Precedents', ['USB for peripherals', 'HTTP for information', 'SQL for databases']),
    ('Build Once', ['Each side builds', 'to the standard once', 'Combinations follow']),
    ('Beyond Cost', ['Ecosystems unlock', 'that fragmentation', 'could never sustain']),
])
bottomline(ax, 'The shipping container did it for logistics.', size=28)
save(fig, 'l04-slide6-collapse.png')

fig, ax = base()
heading(ax, 'The Illustrative Case', 'fifteen becomes eight')
cards3(ax, [
    ('Five Systems', ['Ticketing platform', 'Customer database', 'Knowledge base']),
    ('Plus Two More', ['Billing system', 'Deployment dashboard', 'Data in five places']),
    ('Three Surfaces', ['Desktop app', 'Internal web portal', 'Customer chat']),
])
bottomline(ax, '15 bespoke projects \u2192 8 standard components.', size=28)
save(fig, 'l04-slide7-case.png')

fig, ax = base()
heading(ax, 'What a Protocol Unlocks', 'beyond cost', size=48)
cards2(ax, [
    ('Composability', ['Chain tools from', 'different vendors', 'in one workflow']),
    ('Substitutability', ['Swap the model beneath', 'without re-plumbing tools', 'Lock-in loses its grip']),
])
bottomline(ax, 'Each layer can innovate and compete independently.', size=27)
save(fig, 'l04-slide8-unlocks.png')

fig, ax = base()
heading(ax, 'Ecosystem, Governance', 'and your own count')
cards3(ax, [
    ('Tooling Ecosystem', ['Server registries', 'Conformance suites', 'Scanners +', 'observability']),
    ('Governance', ['One choke point', 'Log + audit + policy', 'Rate-limit uniformly']),
    ('Your Hands-On', ['Run the counter', 'Your N\u00d7M vs N+M', 'Bring that number']),
])
bottomline(ax, 'Next: What MCP Is (and Is Not).', size=28)
save(fig, 'l04-slide9-ecosystem.png')

print('ALL SLIDES DONE')
