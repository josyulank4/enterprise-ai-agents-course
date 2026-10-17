"""Slide deck builder for Skool Course 3, Section 7 (Lessons 27-31).

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
    '~/workspace/udemy-skool/skool-course-3-mcp-architecture/sections/s07/slides')
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


SEC7 = 'Section 7 \u00b7 Security: Authentication, Permissions, and Sandboxing'
SEC7_SHORT = 'Section 7 \u00b7 Security'

# ================= LESSON 27 =================
title_card('l27-slide0-title.png', 'Section 7  \u00b7  Lesson 27',
           ['The New Attack Surface:', 'Injection Through Tool Outputs'])

fig, ax = base()
heading(ax, 'Why the Old Model Breaks', 'The decider is persuadable.')
cards3(ax,
       ('Deterministic Code', ['Request arrives', 'Rules run, action follows', 'No persuasion possible']),
       ('Persuadable Decider', ['A language model chooses', 'Moved by text it reads', 'Including tool outputs']),
       ('Many Doorways', ['Dozens of tools a session', 'Half a dozen servers', 'Every output talks back']))
bottomline(ax, 'Injection: a top risk, now with actions attached.', size=28)
save(fig, 'l27-slide1-why.png')

fig, ax = base()
heading(ax, 'Indirect Injection', 'The poisoned record.')
cards3(ax,
       ('The Delivery', ['Issue text from strangers', 'Pages from site owners', 'Rows customers submitted']),
       ('No Distinction', ['Flows beside instructions', 'Protocol cannot tell', 'Data from direction']),
       ('The Payload', ['Polite, friendly phrasing', '\u201cRefund everything\u201d', 'Legit tool, poisoned text']))
bottomline(ax, 'Trustworthy server. Poisoned content. Real damage.')
save(fig, 'l27-slide2-injection.png')

fig, ax = base()
heading(ax, 'Security at Every Layer', 'A failure anywhere exploits upward.')
cards3(ax,
       ('The Host', ['Chooses the servers', 'it connects to', 'Trust starts here']),
       ('The Server', ['Tools it exposes', 'Scopes it requires', 'Surface it offers']),
       ('The Tools', ['Validate arguments', 'Enforce in code', 'Real footholds exist']))
bottomline(ax, 'Every defense anchored to the attack it defeats.')
save(fig, 'l27-slide3-layers.png')

fig, ax = base()
heading(ax, 'Defense One: Untrusted Output', 'Reputation is not authorship.', size=44)
cards2(ax,
       ('The Posture', ['Every output is untrusted', 'Who sent it \u2260 who wrote it', 'Content often from strangers']),
       ('The Structure', ['Label and delimit the data', 'Prefer typed, schema outputs', 'Free text impersonates talk']))
bottomline(ax, 'Form is a defense. Less prose, less impersonation.', size=28)
save(fig, 'l27-slide4-defense1.png')

fig, ax = base()
heading(ax, 'Defense Two: Validate and Bound', 'Check again, in a fresh context.', size=42)
cards3(ax,
       ('Sanitize', ['Strip instruction-like text', 'Strip code-like sequences', 'Before it flows onward']),
       ('Bound', ['Enforce size limits', 'No context flooding', 'One guest cannot shout']),
       ('Check Again', ['A second, narrow check', 'Fresh context, call only', 'Never read the poison']))
bottomline(ax, 'Defense in depth: no layer carries it all.')
save(fig, 'l27-slide5-defense2.png')

fig, ax = base()
heading(ax, 'The System Prompt Is Not a Defense', 'Guidance is not enforcement.', size=38)
cards2(ax,
       ('The Common Mistake', ['One line in the prompt', '\u201cNever follow tool text\u201d', 'Believed handled \u2014 it is not']),
       ('The Real Defense', ['Deterministic code checks', 'Policy refuses, regardless', 'Prompts supplement. Code is law.']))
bottomline(ax, 'Ask which layer of code enforces the claim.')
save(fig, 'l27-slide6-prompt.png')

next_card('l27-slide7-next.png',
          ['Tool Poisoning, Rug Pulls,', 'and the Confused Deputy'],
          'The attack moves from the data to the supply side.',
          SEC7_SHORT)

# ================= LESSON 28 =================
title_card('l28-slide0-title.png', 'Section 7  \u00b7  Lesson 28',
           ['Tool Poisoning, Rug Pulls,', 'and the Confused Deputy'])

fig, ax = base()
heading(ax, 'Tool Poisoning', 'Instructions wearing documentation.')
cards3(ax,
       ('Hidden Directives', ['Buried in descriptions', 'Reads as helpful docs', 'Aimed at the model']),
       ('Reviewers Skim', ['Read for clarity', 'Poison looks like clarity', 'Skims straight past']),
       ('Parameter Bait', ['Suggestive parameters', 'Invite session history', 'It completes the schema']))
bottomline(ax, "It runs on the model's virtues, not its failures.", size=28)
save(fig, 'l28-slide1-poisoning.png')

fig, ax = base()
heading(ax, 'The Rug Pull', 'Approval outlives behavior.')
cards3(ax,
       ('Earns Trust', ['Clean descriptions', 'Approved, stays clean', 'For weeks']),
       ('Then It Changes', ['Update swaps the text', 'Or a silent remote change', 'New acts, old approval']),
       ('The Flaw', ['Clients rarely re-prompt', 'Approval covers the new', 'You reviewed a snapshot']))
bottomline(ax, 'Pin the definition. A hash makes change loud.')
save(fig, 'l28-slide2-rugpull.png')

fig, ax = base()
heading(ax, 'Countermeasures', 'Scrutiny first, then mechanics.')
cards3(ax,
       ('Scrutiny', ['Hunt model-directed text', 'Secrecy language', 'Params with no honest job']),
       ('Mechanics', ['Hash name, text, schema', 'Fresh approval on change', 'No auto-updates in prod']),
       ('Shrink the Surface', ['Read-only tools preferred', 'Minimal workflow subsets', 'Pinned = known quantity']))
bottomline(ax, 'Scrutiny that is not mechanical does not last.')
save(fig, 'l28-slide3-counter.png')

fig, ax = base()
heading(ax, 'The Confused Deputy', 'Misdirected authorization.')
cards3(ax,
       ('An Old Problem', ['Trusted component holds', 'authority others lack', 'Tricked into using it']),
       ('Agent as Deputy', ['Holds tokens, credentials', 'Delegated user authority', 'Legitimately, by design']),
       ('The Damage', ['Planted instruction calls', 'Valid token, full scope', 'Server did nothing wrong']))
bottomline(ax, 'Not broken authorization \u2014 misdirected.', size=28)
save(fig, 'l28-slide4-deputy.png')

fig, ax = base()
heading(ax, 'Audience Binding', 'And its limits.')
cards2(ax,
       ('What It Stops', ['Tokens bound to one server', 'Audience checked per request', 'Passthrough forbidden outright']),
       ('What It Cannot', ['Stop persuasion', 'A bad call, validly tokened', 'That half is design + approval']))
bottomline(ax, 'Token layer and decision layer: both must hold.')
save(fig, 'l28-slide5-audience.png')

fig, ax = base()
heading(ax, 'Exfiltration', 'The attack in the combination.')
cards3(ax,
       ('The Vehicle', ['Internal access plus', 'external tools', 'Ideal for moving data']),
       ('The Flow', ['Reads sensitive data here', 'Writes it out there', 'Step by plausible step']),
       ('The Defense', ['Separate read and write', 'Sanitized results only', 'Allowlisted destinations']))
bottomline(ax, 'Review surfaces as sets, not tool by tool.')
save(fig, 'l28-slide6-exfil.png')

next_card('l28-slide7-next.png',
          ['Authentication: OAuth 2.1,', 'Keys, and Tokens'],
          'Who is calling \u2014 proven properly.',
          SEC7_SHORT)

# ================= LESSON 29 =================
title_card('l29-slide0-title.png', 'Section 7  \u00b7  Lesson 29',
           ['Authentication: OAuth 2.1,', 'Keys, and Tokens'])

fig, ax = base()
heading(ax, 'Discovery and the Flow', 'A fixed order, every time.')
cards3(ax,
       ('Advertise', ['Metadata document at a', 'well-known address', 'Names trusted issuers']),
       ('Discover + Register', ['Authorization metadata', 'Pre-register when known', 'PKCE guards the code']),
       ('Bind + Validate', ['Resource indicator binds', 'Audience checked per call', 'Challenge, or refusal']))
bottomline(ax, 'Short lifetimes. A path to revoke. No exceptions.', size=28)
save(fig, 'l29-slide1-flow.png')

fig, ax = base()
heading(ax, 'Two Details Everyone Gets Wrong', 'Both are expensive.', size=42)
cards2(ax,
       ('\u201cOptional\u201d in the Spec', ['A server may skip auth', "The protocol won't force you", "The internet won't forgive you"]),
       ('Passthrough Forbidden', ['Upstream: own credential', 'Never forward client tokens', 'Or rebuild the confused deputy']))
bottomline(ax, "Long-lived, broad tokens: the field's top failure.", size=28)
save(fig, 'l29-slide2-details.png')

fig, ax = base()
heading(ax, 'Local Servers', 'The environment is the answer.')
cards2(ax,
       ('No OAuth Locally', ['The spec is explicit', 'Subprocess trust boundary', 'is the local machine']),
       ('The Discipline', ['Secrets via environment or vault', 'Scoped to the server', 'Rotate as a practiced drill']))
bottomline(ax, 'Never hard-code. Never log a secret.')
save(fig, 'l29-slide3-local.png')

fig, ax = base()
heading(ax, 'Bearer Tokens', 'Acceptable, with caveats.')
cards3(ax,
       ('The Conditions', ['Encrypted transport only', 'Stored as a hash', 'Narrowest scope, rotated']),
       ('The Limit', ['Identifies the holder', 'Not the end user', 'No real delegation']),
       ('Identities Distinct', ['Agent is not the user', 'Separate in every record', 'Or accountability dies']))
bottomline(ax, 'A fit for single-tenant. A poor fit beyond it.')
save(fig, 'l29-slide4-bearer.png')

fig, ax = base()
heading(ax, 'Where Tokens Must Never Travel', 'One legitimate road: headers.', size=42)
cards3(ax,
       ('Not in Arguments', ['The model can see them', 'Repeat them, log them', 'Arguments are content']),
       ('Not in Prompts/Logs', ['Prompts get stored', 'Logs wait for readers', 'you did not intend']),
       ('Plan Revocation', ['Short life = cheap revoke', 'Real kill path at the issuer', 'Practise it in a drill']))
bottomline(ax, 'A secrets manager is storage. A transcript is not.', size=28)
save(fig, 'l29-slide5-leaks.png')

fig, ax = base()
heading(ax, 'Scoped, Short-Lived, Audience-Bound', 'The consolidated pattern.', size=38)
cards3(ax,
       ('Short-Lived', ['Minutes, not months', 'Refresh path included', 'Expiry does the revoking']),
       ('Audience-Bound', ['Issued for one server', 'Useless anywhere else', 'Checked every request']),
       ('Scoped', ['Bounded permissions', 'One breach \u2260 total loss', 'Hands over to Lesson 30']))
bottomline(ax, 'Authentication proves who. Authorization decides.', size=27)
save(fig, 'l29-slide6-pattern.png')

next_card('l29-slide7-next.png',
          ['Least-Privilege Authorization', 'and Human Approval'],
          'What an authenticated caller may actually do.',
          SEC7_SHORT)

# ================= LESSON 30 =================
title_card('l30-slide0-title.png', 'Section 7  \u00b7  Lesson 30',
           ['Least-Privilege Authorization', 'and Human Approval'])

fig, ax = base()
heading(ax, 'Authorization Lives in Server Code', 'Per tool. Enforced. In the execution path.', size=40)
cards3(ax,
       ('The Check', ['Every call vs scopes', 'Before it executes', 'Refusal: no side effects']),
       ('Not Authorization', ['A line in a description', 'A prompt instruction', 'Schema validation alone']),
       ('Tenant Identity', ['From the auth context', 'Never from an argument', 'Arguments can be swayed']))
bottomline(ax, 'A wrong principal, well-formatted, is still wrong.', size=27)
save(fig, 'l30-slide1-servercode.png')

fig, ax = base()
heading(ax, 'Narrow Tools, Split Credentials', 'Least privilege, made concrete.', size=42)
cards3(ax,
       ('One Capability', ['Minimum credentials', 'Declared as metadata', 'Reviewed before it runs']),
       ('Split Credentials', ['Read split from write', 'Scoped per family', 'A breach hands over less']),
       ('Default-Deny', ['No declared scope: denied', 'Feels slow for one week', 'Then reviews get fast']))
bottomline(ax, "A tool's demanded scope is part of its design.", size=28)
save(fig, 'l30-slide2-narrow.png')

fig, ax = base()
heading(ax, 'The Permission Ladder', 'A ladder, not a switch.')
cards3(ax,
       ('Read Tools', ['Broad, cheap', 'No side effects', 'The bottom rung']),
       ('Write Tools', ['Scoped per operation', 'Strictly validated', 'Carefully logged']),
       ('Destructive Tools', ['Delete, pay, publish', 'Narrowest scopes', 'Human approval required']))
bottomline(ax, "Refuse the god-tool. Bound every tool's cost.")
save(fig, 'l30-slide3-ladder.png')

fig, ax = base()
heading(ax, 'Human Approval', 'For the calls that deserve a person.')
cards2(ax,
       ('Never on Model Authority', ['Deleting data, sending money', 'Publishing, permission changes', 'A wrong guess is an incident']),
       ('How It Works', ['Agent prepares, execution pauses', 'Elicitation shows the full call', 'Approval covers that call only']))
bottomline(ax, 'One refund approved approves one refund. Only.')
save(fig, 'l30-slide4-approval.png')

fig, ax = base()
heading(ax, 'Approval That Is Real', 'Not ceremonial.')
cards3(ax,
       ('Beat Fatigue', ['Reserve for the top tier', 'Destructive, external', 'Irreversible, high-value']),
       ('Show the Details', ['Tool name, full arguments', 'Plain-language account', 'Danger lives in details']),
       ('Recheck Beforehand', ['Permissions and state', 'may have changed', 'Approval \u2260 authorization']))
bottomline(ax, 'Both checks. Every time.')
save(fig, 'l30-slide5-real.png')

fig, ax = base()
heading(ax, 'When No Human Is Available', 'The policy engine is the equivalent.', size=44)
cards2(ax,
       ('Deterministic Rules', ['Approve, deny, or escalate', 'By tool, arguments, context', 'Code the model cannot negotiate']),
       ('The Principle', ['Independent second check', 'Blind to the poisoned context', 'Not the first check repeated']))
bottomline(ax, 'Fast where speed is safe. Paused where it is not.', size=28)
save(fig, 'l30-slide6-policy.png')

next_card('l30-slide7-next.png',
          ['Sandboxing, Audit Logging,', 'and the Security Checklist'],
          'Contain what executes. Record everything it does.',
          SEC7_SHORT)

# ================= LESSON 31 =================
title_card('l31-slide0-title.png', 'Section 7  \u00b7  Lesson 31',
           ['Sandboxing, Audit Logging,', 'and the Security Checklist'])

fig, ax = base()
heading(ax, 'Isolation Proportional to the Tool', 'Dynamic behavior earns the stronger sandbox.', size=40)
cards3(ax,
       ('Remote-API Tools', ['Little local isolation', "Containment is the API's", 'own authorization']),
       ('Code + File Tools', ['Restricted process floor', 'Container, read-only FS', 'No network as stakes rise']),
       ('Explicit Budgets', ['CPU, memory, disk caps', 'Egress to an allowlist', 'Deny everything else']))
bottomline(ax, 'Allowlist what a tool may reach. Deny the rest.')
save(fig, 'l31-slide1-isolation.png')

fig, ax = base()
heading(ax, 'Concentric Rings', 'No single ring holds alone.')
list_slide(ax, [
    ('Model proposes', 'Policy layer approves'),
    ('Server authorizes', 'Sandbox contains'),
    ('Platform enforces', 'Quotas and budgets'),
    ('Each ring', 'Named code enforces it'),
])
bottomline(ax, 'Cannot name the enforcing code? A diagram, not layers.', size=27)
save(fig, 'l31-slide2-rings.png')

fig, ax = base()
heading(ax, 'Audit Logging', 'The witness that cannot be prompted.', size=46)
cards3(ax,
       ('Every Call', ['Timestamp, identity', 'User and agent distinct', 'Server, tool, arguments']),
       ('The Decisions', ['Authorization + scopes', 'Approval record', 'Result, secrets redacted']),
       ('Log Discovery Too', ['Tool lists are events', 'A new definition appears', 'is a security event']))
bottomline(ax, "Log effects, not the model's reasoning.")
save(fig, 'l31-slide3-audit.png')

fig, ax = base()
heading(ax, 'Tamper-Evident and Actually Read', 'Logs must survive the incident.', size=42)
cards2(ax,
       ('Survive the Incident', ['Append-only storage', 'Shipped off the host', 'Retained per real needs']),
       ('Early Warning', ['Error-rate spikes', 'Sensitive calls at odd hours', 'Sessions enumerating tools']))
bottomline(ax, 'Review on a cadence, not only during incidents.', size=28)
save(fig, 'l31-slide4-tamper.png')

fig, ax = base()
heading(ax, 'The MCP Security Checklist', 'One artifact for the whole section.')
list_slide(ax, [
    ('Injection', 'Untrusted, structured, bounded'),
    ('Supply side', 'Pinned; re-approved on change'),
    ('Identity', 'OAuth remote; env credentials local'),
    ('Containment', 'Sandboxed; audit tamper-evident'),
])
bottomline(ax, 'A starting point, not a certification.')
save(fig, 'l31-slide5-checklist.png')

fig, ax = base()
heading(ax, 'Close the Gaps in Order', 'Identity first, then authorization.')
cards2(ax,
       ('Work It Honestly', ['Gaps mean it is working', 'Embarrassed in private', 'beats exposed in an incident']),
       ('The Capstone Standard', ['Section 13 design is graded', 'against this checklist', 'Build the habit in the lab']))
bottomline(ax, 'A posture, maintained \u2014 not a one-time event.')
save(fig, 'l31-slide6-gaps.png')

next_card('l31-slide7-next.png',
          ['Why One Agent Needs', 'Many Servers: Discovery'],
          'Section 8 takes the architecture outward.',
          'Section 8 \u00b7 Scaling Out')

print('ALL SLIDES DONE')
