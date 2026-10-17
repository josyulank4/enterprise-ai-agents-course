"""Slide deck builder for Skool Course 3, Section 4 (Lessons 13-17).

Visual system copied from Course 2 s00 build_slides.py: dark navy BG,
gold accents, clean cards, DejaVu Sans, 1920x1080.
One title card + one content slide per remaining beat, per lesson.
Footer: MCP ARCHITECTURE · BUILDING TOOL-USING AI SYSTEMS
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import os

D = os.path.expanduser(
    '~/workspace/udemy-skool/skool-course-3-mcp-architecture/sections/s04/slides')
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
    """rows: list of (gold lead, white rest). Rendered as a wide card list."""
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


SEC4 = 'Section 4 \u00b7 Building Your First MCP Server'

# ================= LESSON 13 =================
title_card('l13-slide0-title.png', 'Section 4  \u00b7  Lesson 13',
           ['The Minimal Server', 'and Project Setup'])

fig, ax = base()
heading(ax, 'Four Responsibilities', 'Nothing more.')
list_slide(ax, [
    ('Identity', 'Name, version, instructions'),
    ('Capabilities', 'Primitives declared in handshake'),
    ('Handling', 'List, validate, then act'),
    ('Transport', 'Stdio local, HTTP remote'),
])
bottomline(ax, 'Every server is these four, composed.')
save(fig, 'l13-slide1-responsibilities.png')

fig, ax = base()
heading(ax, 'Identity Is Not Decoration', size=50)
cards3(ax,
       ('The Name', ['Specific, namespaced', 'acme-notes-server', 'Vague names collide']),
       ('The Version', ['Semantic bumps', 'Schema break = major', 'Safe vs breaking']),
       ('Instructions', ['Briefing for the model', 'Short, opinionated', 'Guidance, not marketing']))
bottomline(ax, 'Write it like briefing a capable colleague.')
save(fig, 'l13-slide2-identity.png')

fig, ax = base()
heading(ax, 'Project Setup', 'One dependency, clean layout.')
cards3(ax,
       ('Choose the SDK', ['TypeScript or Python', 'Official, first-tier', 'Concepts transfer']),
       ('Prerequisites', ['Recent Node runtime', 'Or Python 3.10+', 'SDK only, nothing else']),
       ('The Layout', ['Handlers vs transport', 'Schemas beside handlers', 'Tests beside both']))
bottomline(ax, 'Structure at tool one is structure at tool fifty.', size=28)
save(fig, 'l13-slide3-setup.png')

fig, ax = base()
heading(ax, 'Learn the Steps', 'APIs evolve. The steps do not.')
list_slide(ax, [
    ('1 \u00b7 Create', 'Server object: name and version'),
    ('2 \u00b7 Declare', 'Capabilities the server supports'),
    ('3 \u00b7 Register', 'Tool: schema plus handler'),
    ('4 \u00b7 Bind', 'Stdio transport, start the loop'),
])
bottomline(ax, 'If it grows past a screenful, simplify.')
save(fig, 'l13-slide4-steps.png')

fig, ax = base()
heading(ax, 'Transport Binding', 'Logic stays. Binding changes.')
cards3(ax,
       ('The Binding', ['Carries JSON-RPC', 'Knows nothing of tools', 'In and out, that is all']),
       ('Portability', ['Local subprocess', 'Hosted service', 'Same logic, new binding']),
       ('The Boundary', ['Handlers stay pure', 'Validated args in', 'Result out']))
bottomline(ax, 'Never let a handler care how bytes travel.')
save(fig, 'l13-slide5-transport.png')

fig, ax = base()
heading(ax, 'Request Handling', 'List, then act.')
cards3(ax,
       ('It Lists', ['Names', 'Descriptions', 'Schemas']),
       ('It Acts', ['Validate first', 'Then run handler', 'Return usable result']),
       ('Isolation', ['No databases yet', 'No queues, no APIs', 'Fault stays findable']))
bottomline(ax, 'A gate before it is a worker.')
save(fig, 'l13-slide6-handling.png')

fig, ax = base()
heading(ax, 'Hands-On: Scaffold and Ping', 'The s04 starter, answering a client.', size=46)
cards2(ax,
       ('Scaffold', ['Empty server', 'Identity + capabilities', 'Stdio transport']),
       ('Ping It', ['Starts, handshakes', 'Responds cleanly', 'Foundation you trust']))
bottomline(ax, 'If the ping fails, name the layer first.')
save(fig, 'l13-slide7-handson.png')

next_card('l13-slide8-next.png',
          ['Metadata and Capability', 'Declaration'],
          'Identity and capabilities in depth \u2014 and the phantom bug.',
          SEC4)

# ================= LESSON 14 =================
title_card('l14-slide0-title.png', 'Section 4  \u00b7  Lesson 14',
           ['Metadata and Capability', 'Declaration'])

fig, ax = base()
heading(ax, 'A Name a Tired Engineer Can Use', size=44)
cards3(ax,
       ('In the Log', ['Read at midnight', 'Which system?', 'Which process?']),
       ('Namespaced', ['Specific first', 'acme-crm-server', 'Not my-server', 'Hosts run many']),
       ('The Economics', ['Names are cheap', 'Confusion is not', 'Spend cheap generously']))
bottomline(ax, 'A precise name prevents incident confusion.')
save(fig, 'l14-slide1-name.png')

fig, ax = base()
heading(ax, 'Written for Two Audiences', 'Humans choose. The model orients.', size=48)
cards2(ax,
       ('Humans', ['Choosing which servers', 'Reviewing for trust', 'Vague = unselected']),
       ('The Model', ['Choosing tools mid-task', 'Metadata is orientation', 'Nothing else to go on']))
bottomline(ax, 'Write for both readers, first time, every time.', size=28)
save(fig, 'l14-slide2-audiences.png')

fig, ax = base()
heading(ax, 'The Instructions Field', 'Briefing a new colleague.')
cards3(ax,
       ('Write It', ['Short', 'Opinionated', 'Non-obvious only']),
       ('Tell It', ['Preferred sequence', 'Expensive call to avoid', 'What must come first']),
       ('Skip It', ['Restating descriptions', 'Marketing copy', 'Wasted context']))
bottomline(ax, 'Every sentence must change a decision.')
save(fig, 'l14-slide3-instructions.png')

fig, ax = base()
heading(ax, 'Capability Declaration', 'Advertise only what you implement.', size=48)
list_slide(ax, [
    ('Tools', 'listChanged if tools change'),
    ('Resources', 'subscribe, listChanged'),
    ('Prompts', 'listChanged'),
    ('Logging + more', 'Completions, declared if real'),
])
bottomline(ax, 'Each sub-capability is a small contract.')
save(fig, 'l14-slide4-capabilities.png')

fig, ax = base()
heading(ax, 'The Phantom Capability', 'The worst kind of bug.')
cards3(ax,
       ('The Promise', ['Handshake advertises', 'tools', 'Client trusts it']),
       ('The Failure', ['Method not found', 'Model retries, derails', 'Session confuses user']),
       ('The Prevention', ['Declare from', 'handler code', 'Smallest truthful set', 'listChanged to evolve']))
bottomline(ax, 'You cannot evolve from a false start.')
save(fig, 'l14-slide5-phantom.png')

fig, ax = base()
heading(ax, 'Two Versions, Two Jobs', size=50)
cards2(ax,
       ('Server Version', ['Yours, semantic', 'Minor: new tools', 'Major: breaking schema']),
       ('Protocol Version', ["The specification's", 'Negotiated in handshake', 'Not yours to bump']))
bottomline(ax, 'Ask which version failed \u2014 halve the search.', size=28)
save(fig, 'l14-slide6-versions.png')

fig, ax = base()
heading(ax, 'Logging and Completions', 'The quiet declarations.', size=48)
cards2(ax,
       ('Logging', ['Permission to stream', 'Standard severities', 'Declare only if sent']),
       ('Completions', ['Argument autocompletion', 'Guided naming', 'A real implementation']))
bottomline(ax, 'No harmless declarations \u2014 honoured or phantom.', size=28)
save(fig, 'l14-slide7-quiet.png')

fig, ax = base()
heading(ax, 'Hands-On: Declare, Then Verify', 'The s04 metadata exercise.', size=46)
cards2(ax,
       ('Declare', ['Name, version', 'Instructions', 'Capabilities object']),
       ('Verify', ['Checker connects as client', 'Tests every promise', 'Zero gaps, either way']))
bottomline(ax, 'Nothing missing. Nothing forgotten.')
save(fig, 'l14-slide8-handson.png')

next_card('l14-slide9-next.png',
          ['Your First Tool:', 'JSON Schema Inputs'],
          'A name like a command, a schema strict enough to succeed.',
          SEC4)

# ================= LESSON 15 =================
title_card('l15-slide0-title.png', 'Section 4  \u00b7  Lesson 15',
           ['Your First Tool:', 'JSON Schema Inputs'])

fig, ax = base()
heading(ax, 'The Name Reads Like a Command', size=46)
cards3(ax,
       ('Verb Phrases', ['add', 'search_notes', 'lookup_customer']),
       ('Scanned Fast', ['Command palette', 'Mid-reasoning', 'Name says outcome']),
       ('Domain Words', ['Tickets, orders,', 'customers', 'Not table names', 'Not endpoint paths']))
bottomline(ax, 'A noun or a code tells the model nothing.')
save(fig, 'l15-slide1-name.png')

fig, ax = base()
heading(ax, 'The Description', 'Documentation for a smart stranger.', size=50)
cards3(ax,
       ('Four Questions', ['What does it do?', 'When to use it?', 'When not to?', 'Edge cases?']),
       ('Weak vs Strong', ['\u201cAdds numbers\u201d', 'Finite numbers only', 'No string or date math']),
       ('The Payoff', ['Prevents misuse', 'Before it happens', 'Nothing else is visible']))
bottomline(ax, 'The description is the entire interface.')
save(fig, 'l15-slide2-description.png')

fig, ax = base()
heading(ax, 'The Schema, Line by Line', size=50)
cards3(ax,
       ('Types', ['a and b: numbers', 'Per-property notes', 'Reject wrong types early']),
       ('Required', ['Both must be present', 'No half-input calls']),
       ('Closed', ['additionalProperties:', 'false', 'Invented args rejected']))
bottomline(ax, 'Say what you accept. Forbid the rest.')
save(fig, 'l15-slide3-schema.png')

fig, ax = base()
heading(ax, 'Schema as User Interface', size=50)
cards3(ax,
       ('Help It Succeed', ['Enums, not free text', 'Defaults for', 'common calls', 'Ranges in the schema']),
       ("Ambiguity's Cost", ['Two readings possible', 'Model picks the other', 'At the worst moment']),
       ('The Shift', ['User is a model', 'Succeeds without', 'guessing', 'Precision is reliability']))
bottomline(ax, 'Precision here is reliability, bought cheap.')
save(fig, 'l15-slide4-ui.png')

fig, ax = base()
heading(ax, 'Validation: Two Error Paths', size=48)
cards2(ax,
       ('Protocol Error', ['Malformed call', 'Unknown tool, bad args', '\u201cYour call was wrong\u201d']),
       ('Tool Error', ['Valid call, failed work', 'Flagged, with guidance', 'Information to reason on']))
bottomline(ax, 'Never leak an exception as a protocol error.', size=28)
save(fig, 'l15-slide5-errors.png')

fig, ax = base()
heading(ax, 'Annotations', 'Honest hints, not enforcement.')
cards3(ax,
       ('The Hints', ['readOnlyHint', 'destructiveHint', 'idempotentHint', 'openWorldHint']),
       ('The Add Tool', ['Read-only', 'Idempotent', 'Low-risk, auto-approved']),
       ('The Limit', ['Hints, not enforcement', 'Clients may ignore', 'Server still validates']))
bottomline(ax, 'Honesty plus rigour \u2014 you need both.')
save(fig, 'l15-slide6-annotations.png')

fig, ax = base()
heading(ax, 'Keep the Handler Boring', size=50)
cards3(ax,
       ('The Shape', ['Validated args in', 'Result out', 'No hidden state']),
       ('The Result', ['Small, focused', 'Exactly what was asked', 'No padding, no skim']),
       ('The Edges', ['Name the limits', 'Precision, slowness', 'Stated before discovery']))
bottomline(ax, 'Excitement belongs in the agent, not the tool.', size=28)
save(fig, 'l15-slide7-handler.png')

fig, ax = base()
heading(ax, 'Hands-On: The Word-Count Tool', 'Against hostile inputs.', size=46)
cards2(ax,
       ('Implement', ['Name + description', 'Strict schema', 'Annotations, both error paths']),
       ('Attack It', ['Missing fields', 'Wrong types', 'Hostile strings, clean errors']))
bottomline(ax, 'The adversarial set proves it deserves to.')
save(fig, 'l15-slide8-handson.png')

next_card('l15-slide9-next.png',
          ['The Initialization', 'Handshake, Live'],
          'The opening exchange, read field by field on your server.',
          SEC4)

# ================= LESSON 16 =================
title_card('l16-slide0-title.png', 'Section 4  \u00b7  Lesson 16',
           ['The Initialization', 'Handshake, Live'])

fig, ax = base()
heading(ax, 'Message One: The Client Opens', size=48)
cards3(ax,
       ('Version', ['Protocol version wanted', 'Dialect requested']),
       ('Capabilities', ['Roots, sampling', 'Powers: section 5']),
       ('ClientInfo', ['Name and version', 'Identity, declared']))
bottomline(ax, "The client's full hand, face up.")
save(fig, 'l16-slide1-opens.png')

fig, ax = base()
heading(ax, 'Message Two: The Server Answers', size=46)
cards3(ax,
       ('Version Accepted', ['Dialect agreed', 'Terms stated']),
       ('The Contract', ['Capabilities object', 'serverInfo +', 'instructions']),
       ('Not Yet Working', ['Server waits', 'No work served', 'Nothing decorative']))
bottomline(ax, 'A mismatch here is the phantom bug, on schedule.', size=28)
save(fig, 'l16-slide2-answers.png')

fig, ax = base()
heading(ax, 'Message Three: Initialized', 'And only then, work.', size=48)
cards3(ax,
       ('The Notification', ['No reply expected', 'Acceptance confirmed', 'Session operational']),
       ('The Strict Rule', ['No requests before it', 'Beyond pings, logging', 'SDKs enforce it']),
       ('The Diagnostic', ['Tool not called?', 'Check the handshake', 'Session may', 'never open']))
bottomline(ax, "The notification is the client's signature.", size=28)
save(fig, 'l16-slide3-initialized.png')

fig, ax = base()
heading(ax, 'Version Negotiation', 'Evolution without breakage.', size=50)
cards3(ax,
       ('If Unsupported', ['Server offers its version', 'Client accepts or leaves']),
       ('Evolution', ['New versions appear', 'Old clients keep working', 'No silent', 'misunderstanding']),
       ('Debug First', ['Check versions first', 'Explains all downstream', 'Nothing downstream', 'fixes it']))
bottomline(ax, 'Agree explicitly, or do not begin.')
save(fig, 'l16-slide4-version.png')

fig, ax = base()
heading(ax, 'Capability Negotiation', 'The session narrows gracefully.', size=48)
cards3(ax,
       ('After Exchange', ['Legal methods known', 'Both directions']),
       ('Narrowing', ['Graceful narrowing', 'No sampling, no roots', 'Session narrows', 'Server adapts']),
       ('The Principle', ['Negotiation,', 'not assumption', 'Works on', 'untested clients']))
bottomline(ax, 'Read the grant. Never assume it.')
save(fig, 'l16-slide5-capability.png')

fig, ax = base()
heading(ax, 'Reading Real Traces', 'Your permanent debugging habit.', size=50)
cards3(ax,
       ('Capture It', ['Logging both sides', 'Annotate each field', 'What it promises']),
       ('Read in Order', ['Handshake complete?', 'Version settled?', 'Capabilities survived?']),
       ('The Habit', ['Traces first, always', 'Minutes, not guesses', 'Restarting', 'teaches nothing']))
bottomline(ax, 'The trace is short. Read it first.')
save(fig, 'l16-slide6-traces.png')

fig, ax = base()
heading(ax, 'What the Wire Looks Like', size=50)
cards3(ax,
       ('The Frames', ['JSON-RPC 2.0 objects', 'id, method, params', 'Result mirrors the id']),
       ('By Design', ['No hidden channel', 'No side agreement', 'Inspector shows', 'verbatim']),
       ('The Principle', ['Negotiate first, explicitly', 'Before any real work', 'Across every version']))
bottomline(ax, 'Everything travels in readable objects, in order.', size=28)
save(fig, 'l16-slide7-wire.png')

fig, ax = base()
heading(ax, 'Hands-On: Negotiate Twice', 'The s04 handshake lab.', size=48)
cards2(ax,
       ('Two Sessions', ['Full capabilities', 'Then stripped away']),
       ('Diff Them', ['Offers change', 'Legal methods change', 'Degrades cleanly']))
bottomline(ax, 'Same server, two honest negotiations.')
save(fig, 'l16-slide8-handson.png')

next_card('l16-slide9-next.png',
          ['Testing with the Inspector \u2014', 'and First-Server Mistakes'],
          'Test the way real consumers will \u2014 happily and hostilely.',
          SEC4)

# ================= LESSON 17 =================
title_card('l17-slide0-title.png', 'Section 4  \u00b7  Lesson 17',
           ['Testing with the Inspector \u2014', 'and First-Server Mistakes'])

fig, ax = base()
heading(ax, 'The Inspector', 'Seeing what your server actually says.', size=50)
cards3(ax,
       ('Connect', ['Stdio: launch command', 'HTTP: by address', 'Performs handshake']),
       ('Browse + Invoke', ['List tools, resources', 'Fetch prompts', 'Typed arguments']),
       ('The Lens', ['Raw JSON-RPC frames', 'Both directions', 'What it actually says']))
bottomline(ax, 'Intention vs reality, visible in plain text.', size=28)
save(fig, 'l17-slide1-inspector.png')

fig, ax = base()
heading(ax, 'The Testing Loop, Step by Step', size=48)
list_slide(ax, [
    ('Point', 'Inspector at the launch command'),
    ('Watch', 'Handshake complete \u2014 or fault found'),
    ('List + call', 'Correctly, then badly: clean errors'),
    ('Wire in', 'Real host: model finds and calls it'),
])
bottomline(ax, 'Four layers work as the diagnostic map.')
save(fig, 'l17-slide2-loop.png')

fig, ax = base()
heading(ax, 'Logging Without Breaking the Wire', size=44)
cards3(ax,
       ('The Rule', ['Stdout is the wire', 'Protocol only', 'Prints corrupt', 'the stream']),
       ('Route to Stderr', ['Always, no exception', 'Timestamp + severity', 'Correlation ID', 'per request']),
       ('Two Channels', ['Protocol logging: client', 'Stderr: your own', 'Section 11:', 'observability']))
bottomline(ax, 'A correlation ID turns guessing into lookup.', size=28)
save(fig, 'l17-slide3-logging.png')

fig, ax = base()
heading(ax, 'Mistakes One and Two', size=52)
cards2(ax,
       ('1 \u00b7 Stdout Prints', ['Debug print, banner', 'Stream corrupts', 'Handshake dies silently']),
       ('2 \u00b7 Phantom Capabilities', ['Promised, not built', 'Method not found', 'Declare from handler code']))
bottomline(ax, 'Log to stderr. Start with the truthful set.')
save(fig, 'l17-slide4-mistakes12.png')

fig, ax = base()
heading(ax, 'Mistakes Three and Four', size=52)
cards2(ax,
       ('3 \u00b7 Vague Descriptions', ['Never crashes', 'Model misuses forever', 'Four questions fix it']),
       ('4 \u00b7 Sprawling Schemas', ['Accepts anything', 'Twenty optional params', 'Split, tighten, close']))
bottomline(ax, 'additionalProperties: false \u2014 reject, don\u2019t ignore.', size=27)
save(fig, 'l17-slide5-mistakes34.png')

fig, ax = base()
heading(ax, 'Mistakes Five and Six', size=52)
cards3(ax,
       ('5 \u00b7 Output Flood', ['Context flooded', 'Summaries + pages', 'Bulk data as resources']),
       ('6 \u00b7 Exceptions', ['Escaping exceptions', 'Looks like vanishing', 'Catch at boundary', 'Proper tool error']),
       ('And the Rest', ['Blocking the loop', 'Hardcoded secrets', 'Skipped instructions']))
bottomline(ax, 'Each skipped entry will find you.')
save(fig, 'l17-slide6-mistakes56.png')

fig, ax = base()
heading(ax, 'Debug the Conversation', 'Not just the code.', size=50)
cards3(ax,
       ('The Transcript', ['Handshake complete?', 'Exact arguments out', 'Exact result or error back']),
       ('The Vocabulary', ['Parse error: transport', 'Method not found:', 'capability', 'Invalid params: data']),
       ('The Order', ['Frames first', 'Vocabulary second', 'Theories third']))
bottomline(ax, 'Test the weird-but-legal corners deliberately.', size=28)
save(fig, 'l17-slide7-debug.png')

fig, ax = base()
heading(ax, 'Hands-On: The Mistake Hunt', 'The s04 mistake hunt.', size=50)
cards2(ax,
       ('Hunt', ['Five planted mistakes', 'From this catalog', 'Find all five']),
       ('Fix + Verify', ['Fix all five', 'Inspector fully clean', 'Handshake, calls, frames']))
bottomline(ax, '\u201cMostly works\u201d is where these bugs live.', size=28)
save(fig, 'l17-slide8-handson.png')

next_card('l17-slide9-next.png',
          ['Three Control Models and', 'Resources in Depth'],
          'Who decides that a capability gets used.',
          'Section 5 \u00b7 Going Deeper')

print('ALL SLIDES DONE')
