"""Slide builder for Skool Course 3, Section 13 (Lessons 49-50).

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
    '~/workspace/udemy-skool/skool-course-3-mcp-architecture/sections/s13/slides')
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


# ================= LESSON 49 =================
title_card('l49-slide0-title.png', 'Section 13  \u00b7  Lesson 49',
           ['Capstone Studio: Design Your', 'Production MCP Architecture'])

fig, ax = base()
heading(ax, 'The Brief', 'one workflow that dies at the boundary', size=46)
cards3(ax, [
    ('Pick Real Work', ['One real workflow', 'Dies at the context', 'boundary today']),
    ('The Model: Lesson 3', ['Wrong tax rate invoice', '12 steps, 4 systems', '40 minutes by hand']),
    ('Write It Plain First', ['Steps as a human', 'performs them now', 'Before any boxes']),
])
bottomline(ax, 'If it does not hurt today, it teaches nothing.', size=27)
save(fig, 'l49-slide1-brief.png')

fig, ax = base()
heading(ax, 'The Architecture, End to End', 'every item: an owner + a verification', size=46)
cards3(ax, [
    ('Owner + Verification', ['No owner = a wish', 'No method = a claim', 'Review asks for both']),
    ('Servers + Primitives', ['One job per server', 'Tools, resources,', 'prompts: who decides']),
    ('Facade + Callers', ['Domain on surface', 'Quirks behind it', 'Host, users, upstreams']),
])
bottomline(ax, 'A peer must be able to rebuild it from the page.', size=27)
save(fig, 'l49-slide2-architecture.png')

fig, ax = base()
heading(ax, 'Rubric Part One', 'design, scope, and security', size=46)
cards3(ax, [
    ('Design + Scope', ['One purpose per tool', 'Descriptions reviewed', 'Schemas strict, closed']),
    ('Security: Auth First', ['Auth on remote servers', 'OAuth scopes per tool', 'Least privilege always']),
    ('Gates, Secrets, Audit', ['Approval on destructive', 'Secrets never logged', 'Every call audited']),
])
bottomline(ax, 'Missing one sentence = not production-ready.', size=27)
save(fig, 'l49-slide3-rubric1.png')

fig, ax = base()
heading(ax, 'Rubric Part Two', 'reliability: name every failure', size=46)
cards3(ax, [
    ('Timeouts + Retries', ['Timeout on every call', 'Retries with backoff', 'Idempotency keys set']),
    ('Breakers + Bulkheads', ['One slow upstream', 'cannot exhaust', 'the whole server']),
    ('Degrade + Health', ['Each dependency down:', 'a named behavior', 'Health signal live']),
])
bottomline(ax, 'Reliability is named behavior, not intentions.', size=27)
save(fig, 'l49-slide4-rubric2.png')

fig, ax = base()
heading(ax, 'Rubric Part Three', 'testing: five named suites', size=46)
cards3(ax, [
    ('Unit + Contract', ['Handlers + error paths', 'Schemas pinned', 'Error shapes pinned']),
    ('Real Client + Attacks', ['Real client, in CI', 'Poisoned record fixture', 'Injection probed always']),
    ('Regression Suite', ['Re-runs on every', 'behavior change', 'Wording = behavior']),
])
bottomline(ax, 'A design without a test plan is a hope.', size=27)
save(fig, 'l49-slide5-rubric3.png')

fig, ax = base()
heading(ax, 'Rubric Part Four', 'operations and governance', size=46)
cards3(ax, [
    ('Observe + Alert', ['Correlation IDs', 'Metrics per tool', 'Alerts on spikes']),
    ('Release Safely', ['Versioned releases', 'Rollback + canary', 'Runbook: who to page']),
    ('Govern + Classify', ['Data classified', 'PII redacted, minimal', 'Registered inventory']),
])
bottomline(ax, 'Built to be run by people, at night, under pressure.', size=25)
save(fig, 'l49-slide6-rubric4.png')

fig, ax = base()
heading(ax, 'The Review Discipline', 'cite your reasons', size=46)
cards3(ax, [
    ('Every Decision Cites', ['Transport: Section 3', 'Safety tiers: L25', 'Approval gates: L30']),
    ('Uncited = a Draft', ['A design without', 'reasons is a draft', 'Studio treats it so']),
    ('When Specs Change', ['Citations show which', 'decisions to revisit', 'Argument starts there']),
])
bottomline(ax, 'Architecture, not taste: name the lesson.', size=27)
save(fig, 'l49-slide7-review.png')

fig, ax = base()
heading(ax, 'Produce the Design', 'the deliverable of this course', size=46)
cards3(ax, [
    ('The Document', ['Architecture itself', 'Safety register (L25)', 'Security checklist (L31)']),
    ('The Bar, Made Clear', ['Servers in one page', 'Every tool tiered', 'Poisoned output named']),
    ('Test Plan Too', ['From Section 10', 'Peer can build from it', 'That is the standard']),
])
bottomline(ax, 'Let the checklist drive the design.', size=27)
save(fig, 'l49-slide8-document.png')

# ================= LESSON 50 =================
title_card('l50-slide0-title.png', 'Section 13  \u00b7  Lesson 50',
           ['Course Close: The Durable', 'Principles and Your Roadmap'])

fig, ax = base()
heading(ax, 'Tools Are Contracts', 'the model is a consumer', size=46)
cards3(ax, [
    ('Contracts First', ['Schemas, outputs,', 'errors: all an agent', 'knows of your system']),
    ('Precise + Stable', ['Make contracts exact', 'Let them drift and', 'no model compensates']),
    ('A Literal Reader', ['Cannot ask questions', 'Cannot read intentions', 'Design for no context']),
])
bottomline(ax, 'Brilliant, literal, and without your context.', size=27)
save(fig, 'l50-slide1-contracts.png')

fig, ax = base()
heading(ax, 'Boundaries, Control, Trust', 'the architectural principles', size=46)
cards3(ax, [
    ('Keep Roles Apart', ['Host, client, server', 'Each side replaceable', 'Boundaries load-bearing']),
    ('Who Decides', ['Tools: model chooses', 'Resources: app surfaces', 'Prompts: user invokes']),
    ('Verify Every Claim', ['Outputs untrusted', 'Descriptions verified', 'Authorize in code']),
])
bottomline(ax, 'Audit everything. Test like it is probabilistic.', size=26)
save(fig, 'l50-slide2-boundaries.png')

fig, ax = base()
heading(ax, 'Defense in Depth', 'and behavior is the API', size=46)
cards3(ax, [
    ('Layer the Defenses', ['Validation, filtering', 'Alignment, review', 'Assume each can fail']),
    ('Behavior Is the API', ['What a tool does', 'matters as much as', 'its declared interface']),
    ('Ops Is a Feature', ['Reliability, rollouts', 'Observability, response', 'Not overhead: the work']),
])
bottomline(ax, 'An unobservable tool is a liability in a schema.', size=26)
save(fig, 'l50-slide3-defense.png')

fig, ax = base()
heading(ax, 'Build for Today', 'architect for what comes', size=46)
cards3(ax, [
    ('Ship for Today', ["Today's agents", 'models you can name', 'Systems that work now']),
    ('Build for Tomorrow', ['Models + protocols', 'you cannot yet name', 'Contracts carry over']),
    ('What Carries Forward', ['Your contracts', 'Testing discipline', 'Operational rigor']),
])
bottomline(ax, 'Principles decide if it is worth trusting.', size=27)
save(fig, 'l50-slide4-build.png')

fig, ax = base()
heading(ax, 'Your Roadmap', 'the sequence matters', size=46)
cards3(ax, [
    ('First Server First', ['Highest reuse', 'Lowest risk', 'Early wins fund it']),
    ('Facades First', ['Clean surface first', 'Consumers one by one', 'Retire bespoke last']),
    ('Gates Before Writes', ['Checklist passes full', 'before first write', 'Reads earn trust first']),
])
bottomline(ax, 'Writes spend trust. They do not ship on credit.', size=27)
save(fig, 'l50-slide5-roadmap.png')

fig, ax = base()
heading(ax, 'Watched, Not Chased', 'protect what transfers under any future', size=46)
cards3(ax, [
    ('Own Your Contracts', ['Keep seams thin:', 'transport, auth,', 'discovery']),
    ('Fund Fundamentals', ['Injection testing', 'Contract discipline', 'Observability, rollouts']),
    ('Watch the Ecosystem', ['Pilot major revisions', 'on lowest-risk server', 'Track trust, A2A seams']),
])
bottomline(ax, 'Future-proof: guessing wrong stays cheap.', size=27)
save(fig, 'l50-slide6-watched.png')

fig, ax = base()
heading(ax, 'The Closing Frame', 'from talking to doing', size=46)
cards3(ax, [
    ('An Era Ending', ['The chatbot that', 'can only talk', 'is ending']),
    ('An Era Beginning', ['Agents that do things', 'Open standards decide', 'how fast it arrives']),
    ('Tools Are the Medium', ["The model's reach", 'into the real world', 'Build them carefully']),
])
bottomline(ax, 'You now hold the map of the protocol.', size=27)
save(fig, 'l50-slide7-closing.png')

fig, ax = base()
heading(ax, 'Commit the Roadmap', 'the final hands-on work', size=46)
cards3(ax, [
    ('Open the Planner', ['The s13 roadmap', 'planner in the repo', 'Commit it in writing']),
    ('Name Three Firsts', ['First server', 'First consumers', 'First security gate']),
    ('Dates You Keep', ['Sequenced as taught', 'Dates written down', 'Held to them']),
])
bottomline(ax, 'Ship the first read. Then earn the first write.', size=25)
save(fig, 'l50-slide8-commit.png')

print('ALL SLIDES DONE')
