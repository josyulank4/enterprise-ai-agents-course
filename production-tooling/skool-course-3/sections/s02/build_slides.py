"""Slide deck builder for Skool Course 3, Section 2 (Protocol Fundamentals): Lessons 5-8.

Visual system copied from Course 2 s00 build_slides.py: dark navy BG, gold accents,
clean cards, 1920x1080, DejaVu Sans. Footer per Course 3 spec.
All slide text is faithful, proofread distillation of each beat's narration.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import os

D = os.path.expanduser(
    '~/workspace/udemy-skool/skool-course-3-mcp-architecture/sections/s02/slides')
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


def heading(ax, text, sub=None, size=58, sub_size=32):
    ax.text(W / 2, 9.3, text, color=WHITE, fontsize=size, ha='center',
            va='center', weight='bold', family=FONT)
    if sub:
        ax.text(W / 2, 8.35, sub, color=GOLD, fontsize=sub_size, ha='center',
                va='center', family=FONT)


def card(ax, x, y, w, h, title, lines, title_size=29, line_size=24):
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


def row3(ax, cards):
    for (x, t, lines) in cards:
        card(ax, x, 3.05, 5.3, 4.35, t, lines)


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


XS = [1.0, 6.95, 12.9]

# ================= LESSON 5 =================
title_card('l05-slide0-title.png', 'Section 2  \u00b7  Lesson 5',
           ['What MCP Is (and Is Not)'])

fig, ax = base()
heading(ax, 'One Protocol', 'Between applications and tools')
row3(ax, [(XS[0], 'The Definition',
           ['An open standard', 'Client-server', 'JSON-RPC 2.0 protocol']),
          (XS[1], 'The Server',
           ['Wraps a real system', 'Databases, APIs, files', 'In standard form']),
          (XS[2], 'The Payoff',
           ['Write the server once', 'Build the client once', 'N + M, not N \u00d7 M'])])
bottomline(ax, 'Build to the standard once \u2014 the combinations follow.', size=29)
save(fig, 'l05-slide1-protocol.png')

fig, ax = base()
heading(ax, 'The USB Analogy', 'Build once, use everywhere')
row3(ax, [(XS[0], 'Before USB',
           ['Every peripheral', 'Its own connector', 'Its own negotiation']),
          (XS[1], 'After USB',
           ['Build to the standard', 'Works with', 'any computer', 'Maker does not matter']),
          (XS[2], 'For AI',
           ['Swap the model,', 'keep the tools', 'Swap the app,', 'keep the tools'])])
bottomline(ax, 'Independence is what lets an ecosystem form.')
save(fig, 'l05-slide2-usb.png')

fig, ax = base()
heading(ax, 'The Interface Layer', 'Discovery, invocation, results')
row3(ax, [(XS[0], 'Discover',
           ['What a server offers', 'Tools, resources', 'And prompts']),
          (XS[1], 'Invoke and Read',
           ['Structured arguments', 'Read resources', 'One uniform interface']),
          (XS[2], 'Understand',
           ['Clear descriptions', 'Chooses sensibly', 'Humans can review'])])
bottomline(ax, 'That narrow set is standardized \u2014 the rest is left alone.', size=29)
save(fig, 'l05-slide3-interface.png')

fig, ax = base()
heading(ax, 'What MCP Is Not', 'Four clear nos')
for x, t, lines in [(0.5, 'Not a Model', ['Says nothing', 'about the model']),
                    (5.15, 'Not an Agent', ['Does not plan', 'No workflows']),
                    (9.8, 'Not Plumbing', ['Standard', 'transports']),
                    (14.45, 'Not Your Data', ['No domain', 'schema'])]:
    card(ax, x, 3.05, 4.3, 4.35, t, lines, title_size=26, line_size=22)
bottomline(ax, 'Thinking stays in the application and the model.', size=29)
save(fig, 'l05-slide4-not.png')

fig, ax = base()
heading(ax, 'The Narrow Waist', 'Why restraint wins')
row3(ax, [(XS[0], 'Standardized',
           ['Discovery', 'Negotiation', 'Invocation and results']),
          (XS[1], 'Above the Waist',
           ['Agent frameworks', 'Applications', 'Evolve independently']),
          (XS[2], 'Below the Waist',
           ['Tools', 'Data sources', 'Evolve independently'])])
bottomline(ax, 'Like an outlet: valued because every plug fits.')
save(fig, 'l05-slide5-waist.png')

fig, ax = base()
heading(ax, 'A Brief History', 'An internal fix becomes infrastructure')
row3(ax, [(XS[0], '2024',
           ['Mid-2024: internal fix', 'at Anthropic', 'Nov 25, 2024: release', 'Open-source SDKs']),
          (XS[1], '2025',
           ['Adoption compounds', 'Mar 2025: auth', 'Sep 2025: registry']),
          (XS[2], 'December 2025',
           ['Donated to Agentic', 'AI Foundation', 'Linux Foundation'])])
bottomline(ax, 'Infrastructure this central cannot belong to one vendor.', size=29)
save(fig, 'l05-slide6-history.png')

fig, ax = base()
heading(ax, 'Try It: The Discovery Demo', 'Section 2 discovery demo')
row3(ax, [(XS[0], 'Connect',
           ['To the sample server', 'As a client']),
          (XS[1], 'List Everything',
           ['Its tools', 'Its resources', 'Its prompts']),
          (XS[2], 'The Point',
           ['What the server declares', 'Is what you get'])])
bottomline(ax, 'Next: Lesson 6 \u2014 Design Philosophy and the Three Roles', size=27)
save(fig, 'l05-slide7-tryit.png')

# ================= LESSON 6 =================
title_card('l06-slide0-title.png', 'Section 2  \u00b7  Lesson 6',
           ['Design Philosophy', 'and the Three Roles'])

fig, ax = base()
heading(ax, 'Composability', 'Interoperability over integration')
row3(ax, [(XS[0], 'The First Duty',
           ['Any compliant client', 'Any compliant server', 'The N + M promise']),
          (XS[1], 'The Discipline',
           ['No vendor shortcuts', 'Universality first', 'Convenience second']),
          (XS[2], 'The Result',
           ['Compose across teams', 'Compose across vendors', 'No hand-wiring'])])
bottomline(ax, 'An estate you can grow \u2014 not one that grows heavier.', size=29)
save(fig, 'l06-slide1-composability.png')

fig, ax = base()
heading(ax, 'Simplicity at the Waist', 'Architecture endures while SDK details churn', sub_size=30)
row3(ax, [(XS[0], 'Standardized',
           ['Discovery', 'Negotiation', 'And little else']),
          (XS[1], 'Not Defined',
           ['Agent planning', 'Prompt engineering', 'Domain data models']),
          (XS[2], 'Why Principles',
           ['SDK details churn', 'Architecture endures', 'Learnable in days'])])
bottomline(ax, 'Know why a shape exists, and changed details stay small.', size=29)
save(fig, 'l06-slide2-simplicity.png')

fig, ax = base()
heading(ax, 'Security as a Constraint', 'Designed in, not bolted on')
row3(ax, [(XS[0], 'Separation',
           ['Hosts: user, model', 'Clients: connections', 'Servers: capabilities']),
          (XS[1], 'Trust Is Earned',
           ['OAuth 2.1 authorization', 'Descriptions untrusted', 'No automatic trust']),
          (XS[2], 'Evolution',
           ['Versioned by date', 'Negotiated explicitly', 'Backward compatible'])])
bottomline(ax, 'Interoperability \u00b7 simplicity \u00b7 separation \u00b7 security \u00b7 evolution.', size=27)
save(fig, 'l06-slide3-security.png')

fig, ax = base()
heading(ax, 'The Host', 'Experience, model, and trust')
row3(ax, [(XS[0], 'What It Is',
           ['The app users touch', 'Desktop assistant', 'IDE, chat app, runtime']),
          (XS[1], 'What It Owns',
           ['The user experience', 'The conversation', 'The language model']),
          (XS[2], 'Where Trust Sits',
           ['Approves tool calls', 'Checks policies', 'Logs for audit'])])
bottomline(ax, 'The host ultimately decides whether a call proceeds.')
save(fig, 'l06-slide4-host.png')

fig, ax = base()
heading(ax, 'The Client', 'One connection per server')
row3(ax, [(XS[0], 'Inside the Host',
           ['One client per server', 'Five servers', 'Five clients']),
          (XS[1], 'Its Job',
           ['Initialize and negotiate', 'Send requests', 'Route responses faithfully']),
          (XS[2], 'Not the User',
           ['Not the end user', 'Not the model', 'Essential plumbing'])])
bottomline(ax, 'A dedicated telephone line between host and server.')
save(fig, 'l06-slide5-client.png')

fig, ax = base()
heading(ax, 'The Server', 'Focused, narrow, reusable')
row3(ax, [(XS[0], 'What It Does',
           ['Exposes capabilities', 'Tools, resources,', 'prompts', 'Wraps a real system']),
          (XS[1], 'Built Separate',
           ['A different process', 'A different language', 'A different machine']),
          (XS[2], 'Why Three Roles',
           ['Uniform connections', 'Failure isolation', 'Policy stays in the host'])])
bottomline(ax, 'The same server is reusable across every host.')
save(fig, 'l06-slide6-server.png')

fig, ax = base()
heading(ax, 'Try It: The Three-Role Trace', 'Follow one request end to end')
row3(ax, [(XS[0], 'The Request',
           ['One user request', 'Through all three roles']),
          (XS[1], 'Label Each Step',
           ['Who held the policy?', 'Who carried the message?', 'Who executed the work?']),
          (XS[2], 'The Test',
           ['Answer all three', 'Without hesitation'])])
bottomline(ax, 'Next: Lesson 7 \u2014 The Three Primitives', size=29)
save(fig, 'l06-slide7-tryit.png')

# ================= LESSON 7 =================
title_card('l07-slide0-title.png', 'Section 2  \u00b7  Lesson 7',
           ['The Three Primitives: Tools,', 'Resources, and Prompts'])

fig, ax = base()
heading(ax, 'Tools', 'The model\u2019s hands \u2014 model-controlled')
row3(ax, [(XS[0], 'What a Tool Is',
           ['A named function', 'A readable description', 'JSON Schema inputs']),
          (XS[1], 'Who Decides',
           ['The model chooses', 'Which tool to call', 'With what arguments']),
          (XS[2], 'The Risk',
           ['Tools change state', 'Query, create, send, write', 'Design with care'])])
bottomline(ax, 'A lever connected to a real system \u2014 you own what it moves.', size=29)
save(fig, 'l07-slide1-tools.png')

fig, ax = base()
heading(ax, 'Resources', 'The agent\u2019s eyes \u2014 application-controlled')
row3(ax, [(XS[0], 'What It Is',
           ['Data models can read', 'Files, records, replies', 'Exposed at a URI']),
          (XS[1], 'Who Decides',
           ['The host curates', 'What to expose', 'When to attach it']),
          (XS[2], 'Why Curation',
           ['Grounds in facts', 'The actual record', 'Not model memory'])])
bottomline(ax, 'Attach everything, and you built exposure \u2014 not context.', size=29)
save(fig, 'l07-slide2-resources.png')

fig, ax = base()
heading(ax, 'Prompts', 'The user\u2019s playbooks \u2014 user-controlled')
row3(ax, [(XS[0], 'What a Prompt Is',
           ['A reusable template', 'A pre-built task', 'structure', 'Placeholders to fill in']),
          (XS[1], 'Who Decides',
           ['The user selects it', 'Explicitly, on purpose', 'Nothing fires silently']),
          (XS[2], 'The Package',
           ['Domain expertise', 'The right way to ask', 'Captured once, for all'])])
bottomline(ax, 'The user decides which play to run, and when.')
save(fig, 'l07-slide3-prompts.png')

fig, ax = base()
heading(ax, 'Why Three, Not One', 'Three kinds of control')
row3(ax, [(XS[0], 'Model Decides',
           ['Tools', 'The AI picks', 'An action']),
          (XS[1], 'The App Decides',
           ['Resources', 'The app picks', 'The context']),
          (XS[2], 'User Decides',
           ['Prompts', 'The user picks', 'A workflow'])])
bottomline(ax, 'First design question: who should be in control here?')
save(fig, 'l07-slide4-whythree.png')

fig, ax = base()
heading(ax, 'The Beginner Mistake', 'Conflating the primitives')
row3(ax, [(XS[0], 'Record as a Tool',
           ['The model fetches it', 'Invented arguments', 'Host should curate']),
          (XS[1], 'Workflow in Tool',
           ['Playbook fires unasked', 'Belongs in a prompt', 'Chosen deliberately']),
          (XS[2], 'All Resources',
           ['Can look at the world', 'Never act on it', 'Wrong in control'])])
bottomline(ax, 'Control errors are the ones that become incidents.')
save(fig, 'l07-slide5-mistake.png')

fig, ax = base()
heading(ax, 'Try It: The Primitive Sorter', 'Classify ten capabilities')
row3(ax, [(XS[0], 'Judgments',
           ['Order status: tool', 'Contract: resource', 'Weekly review:', 'a prompt']),
          (XS[1], 'Sort Your Own',
           ['Ten capabilities', 'From your own systems', 'Tool, resource,', 'or prompt']),
          (XS[2], 'Disagreement',
           ['Read the reasoning', 'Find the control', 'question you missed'])])
bottomline(ax, 'Next: Lesson 8 \u2014 Lifecycle, Messages, and Versioning', size=27)
save(fig, 'l07-slide6-tryit.png')

# ================= LESSON 8 =================
title_card('l08-slide0-title.png', 'Section 2  \u00b7  Lesson 8',
           ['Lifecycle, Messages,', 'and Versioning'])

fig, ax = base()
heading(ax, 'Initialization', 'The handshake')
row3(ax, [(XS[0], 'The Handshake',
           ['Client sends initialize', 'Version and capabilities', 'Server replies']),
          (XS[1], 'Stateless Core',
           ['Metadata per request', 'Discover mechanism', 'Legacy still supported']),
          (XS[2], 'The Payoff',
           ['No session-state bugs', 'Easier scaling', 'No work assumed'])])
bottomline(ax, 'You will perform this handshake live in Section 4.', size=29)
save(fig, 'l08-slide1-init.png')

fig, ax = base()
heading(ax, 'Capability Negotiation', 'A contract, not an assumption')
row3(ax, [(XS[0], 'The One Rule',
           ['Neither side assumes', 'Each side declares', 'Work on the intersection']),
          (XS[1], 'Server Declares',
           ['Tools, resources, prompts', 'Options it supports', 'Such as list changes']),
          (XS[2], 'Client Declares',
           ['Sampling', 'Roots', 'Its own features'])])
bottomline(ax, 'Advertise only what you have implemented.')
save(fig, 'l08-slide2-negotiation.png')

fig, ax = base()
heading(ax, 'Requests and Results', 'Two of the four message shapes')
row3(ax, [(XS[0], 'A Request',
           ['Expects a reply', 'An ID and a method', 'Structured parameters']),
          (XS[1], 'Why the ID Matters',
           ['Matches replies to requests', 'Many requests in flight', 'At the same time']),
          (XS[2], 'A Result',
           ['The same ID', 'A result object', 'The operation\u2019s output'])])
bottomline(ax, 'Ask in a structured way \u2014 receive a structured answer.', size=29)
save(fig, 'l08-slide3-requests.png')

fig, ax = base()
heading(ax, 'Errors and Notifications', 'The other two shapes')
row3(ax, [(XS[0], 'An Error',
           ['The request\u2019s ID', 'Code, message, data', 'Structured and first-class']),
          (XS[1], 'A Notification',
           ['One-way, no reply', 'A method, no ID', 'Asynchronous events']),
          (XS[2], 'In Practice',
           ['The client drives', 'The server responds', 'Everything explicit'])])
bottomline(ax, 'Not in a JSON-RPC message? It did not happen.', size=29)
save(fig, 'l08-slide4-errors.png')

fig, ax = base()
heading(ax, 'Versioning', 'Dates, negotiated per session')
row3(ax, [(XS[0], 'Date Versions',
           ['2024-11-05', '2025-03-26', '2025-11-25', 'Current: 2026-07-28']),
          (XS[1], 'Negotiation',
           ['The client offers a version', 'The server selects', 'The newest both support']),
          (XS[2], 'Three Lessons',
           ['Transports consolidated', 'Statefulness simplified', 'Governance matured'])])
bottomline(ax, 'Every implementation declares what it speaks.')
save(fig, 'l08-slide5-versioning.png')

fig, ax = base()
heading(ax, 'Designing Against Revisions', 'Survive the specification\u2019s evolution', size=52)
row3(ax, [(XS[0], 'Negotiate',
           ['Do not assume', 'Let the handshake work', 'No hard-coded peers']),
          (XS[1], 'Test Broadly',
           ['Target the current stable', 'Test older revisions', 'Watch the extensions path']),
          (XS[2], 'Source of Truth',
           ['The specification', 'Check it as it moves', 'Design against architecture'])])
bottomline(ax, 'Design against one revision, and it becomes your outage.', size=29)
save(fig, 'l08-slide6-revisions.png')

fig, ax = base()
heading(ax, 'Try It: The Handshake Capture', 'Read the real exchange')
row3(ax, [(XS[0], 'Run the Capture',
           ['S02 handshake capture', 'On the sample server']),
          (XS[1], 'Find the Versions',
           ['The version offered', 'The version selected']),
          (XS[2], 'The Declarations',
           ['What the server declared', 'What the client declared'])])
bottomline(ax, 'Next: Lesson 9 \u2014 Separation of Concerns and Server Anatomy', size=26)
save(fig, 'l08-slide7-tryit.png')

print('ALL SLIDES DONE')
