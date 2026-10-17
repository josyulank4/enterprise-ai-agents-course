"""Slide deck builder for Skool Course 3, Section 6 (Lessons 22-26).

Visual system copied from Course 2 s00 / Course 3 s04 build_slides.py:
dark navy BG, gold accents, clean cards, DejaVu Sans, 1920x1080.
One title card + one content slide per remaining beat, per lesson.
Footer: MCP ARCHITECTURE - BUILDING TOOL-USING AI SYSTEMS
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import os

D = os.path.expanduser(
    '~/workspace/udemy-skool/skool-course-3-mcp-architecture/sections/s06/slides')
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
    # length-based auto-fit so no title/line ever overflows its card
    scale = w / 5.3
    if title:
        title_size = min(title_size, 460 * scale / len(title))
    if lines:
        line_size = min(line_size, 500 * scale / max(len(ln) for ln in lines))
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
    ax.text(W / 2, 4.35, white_line, color=WHITE, fontsize=27,
            ha='center', va='center', family=FONT)
    ax.text(W / 2, 3.15, section_line, color=GREY, fontsize=25,
            ha='center', va='center', family=FONT)
    save(fig, name)


SEC6 = 'Section 6 \u00b7 Connecting MCP to Enterprise Systems'

# ================= LESSON 22 =================
title_card('l22-slide0-title.png', 'Section 6  \u00b7  Lesson 22',
           ['The Adapter Pattern:', 'MCP as a Facade'])

fig, ax = base()
heading(ax, 'The Diplomat, Not the Program', 'Represents systems. Protects both sides.', size=48)
cards3(ax,
       ('The Model', ['Never learns vendor', 'pagination quirks', 'or strange field names']),
       ('The Upstream', ['No malformed requests', 'No model inventions', 'on a confident day']),
       ('Build Once', ['Auth, error dialects', 'Rate limits, quirks', 'Fixed in one adapter']))
bottomline(ax, 'Localize the mess and the change.')
save(fig, 'l22-slide1-diplomat.png')

fig, ax = base()
heading(ax, 'Designed, Not Derived', "Start from the model's needs.", size=54)
cards3(ax,
       ('Transliteration Leaks', ['One tool per table', 'One per endpoint', 'Names copied straight']),
       ('Designed Primitives', ['Find open orders', 'Show ticket + history', 'Intention-revealing']),
       ('The Replacement Test', ['Swap upstream tomorrow', 'Model notices nothing', 'Tools read as yesterday']))
bottomline(ax, 'If the model notices a swap, the facade leaks.', size=28)
save(fig, 'l22-slide2-designed.png')

fig, ax = base()
heading(ax, 'An Anti-Corruption Layer', 'Translation \u2014 and improvement.', size=52)
cards3(ax,
       ('Enforce Invariants', ['Stricter validation', 'Narrower outputs', 'Clearer errors']),
       ('Better Than Upstream', ['Surface behaves better', 'System never changes', 'to provide it']),
       ('Stable Contracts', ['Upstream will change', 'Tool contracts stay', 'Teams build without fear']))
bottomline(ax, 'The facade is improvement, not just translation.', size=28)
save(fig, 'l22-slide3-anticorruption.png')

fig, ax = base()
heading(ax, 'What Stays Behind the Facade', 'Only the declared surface crosses.', size=46)
cards3(ax,
       ('Stays Behind', ['Credentials', 'Connection pools', 'Retry logic, vendor SDKs']),
       ('What Crosses', ['Tools and resources', 'Prompts', 'In domain language']),
       ("Priya's Ticket", ['Agent sees tickets', 'Accounts and invoices', 'Never tax-rate storage']))
bottomline(ax, 'Expose the surface. Hide everything else.')
save(fig, 'l22-slide4-behind.png')

fig, ax = base()
heading(ax, 'Expose the Domain', 'Never the plumbing.', size=54)
cards3(ax,
       ('Domain Concepts', ['The ticket', 'The account', 'The invoice']),
       ('Never Exposed', ['Table names', 'Endpoint shapes', "A dead vendor's words"]),
       ('Better Reasoning', ['Business actions', 'Model reasons about', 'the business itself']))
bottomline(ax, 'The surface outlives the system behind it.')
save(fig, 'l22-slide5-domain.png')

fig, ax = base()
heading(ax, 'Per System, or Per Domain?', 'Prefer domain-shaped servers.', size=50)
cards3(ax,
       ('Per System', ['Simpler, clean ownership', 'Each team runs its own', 'Model sees boundaries']),
       ('Per Domain', ['Joins several systems', 'Coherent capabilities', 'In business terms']),
       ('Keep It Small', ['Stateless where possible', 'Eight real tools', 'Not forty accumulated']))
bottomline(ax, 'Every tool costs context, review, and trust.', size=28)
save(fig, 'l22-slide6-structure.png')

next_card('l22-slide7-next.png',
          ['Wrapping Databases', 'and File Stores'],
          'Hands-on: sketch a facade on the s06 adapter canvas.',
          SEC6)

# ================= LESSON 23 =================
title_card('l23-slide0-title.png', 'Section 6  \u00b7  Lesson 23',
           ['Wrapping Databases', 'and File Stores'])

fig, ax = base()
heading(ax, 'Never Raw SQL', 'Free text cannot be defended.', size=54)
cards3(ax,
       ('The Temptation', ['One query tool', 'Maximum flexibility', 'Demos beautifully']),
       ('No Guardrails', ['Cannot be tiered', 'Cannot be limited', 'Cannot be audited']),
       ('The Rule', ['Never expose raw SQL', 'Not in a demo', 'Later never comes']))
bottomline(ax, 'Raw SQL is for anything \u2014 so nothing defensible.', size=27)
save(fig, 'l23-slide1-rawsql.png')

fig, ax = base()
heading(ax, 'Intention-Shaped Tools', 'Parameterized, reviewed queries.', size=50)
cards3(ax,
       ('One Tool Per Need', ['Tight schema', 'Fixed prepared statement', 'Written and reviewed']),
       ("The Model's Freedom", ['Inside validated', 'parameters only', 'Lookup, search, limit']),
       ('Why Slower Is Right', ['Review catches injection', 'Narrows broad access', 'Ship late, not exposed']))
bottomline(ax, 'Review is the only human read of the exact query.', size=27)
save(fig, 'l23-slide2-intention.png')

fig, ax = base()
heading(ax, 'Reads and Writes', 'Reads as resources, writes with guards.', size=50)
cards3(ax,
       ('Reads', ['Reference data: resources', 'URI templates', 'Situational: tools']),
       ('Writes', ['Name what changes', 'Validate aggressively', 'Inside a transaction']),
       ('The Plumbing', ['Pooled connections', 'Bounded lifetimes', 'Statement timeouts']))
bottomline(ax, 'Narrow writes show intent. Broad writes show a difference.', size=26)
save(fig, 'l23-slide3-readswrites.png')

fig, ax = base()
heading(ax, 'File Stores: The Natural Fit', 'Resources were designed for files.', size=48)
cards3(ax,
       ('A Resource Server', ['Files are resources', 'Directories: listings', 'Read as intended']),
       ('URI Design', ['How enterprise thinks', 'Policy by name', 'Not bucket addresses']),
       ('Adapter Mapping', ['Resolves current version', 'Hides archival prefixes', 'Normalizes encodings']))
bottomline(ax, 'Design URIs around documents, not storage.', size=28)
save(fig, 'l23-slide4-filestores.png')

fig, ax = base()
heading(ax, 'Honest Types, Partial Reads', 'Search, then read.', size=48)
cards3(ax,
       ('Honest Types', ['Content types truthful', 'Hosts present', 'data correctly']),
       ('Partial Reads', ['Ranged, sectioned', 'No 200-page dumps', 'into the context']),
       ('Search Then Read', ['Search is a tool', 'Returns summaries + URIs', 'Model reads promising']))
bottomline(ax, 'The tool narrows. The resources inform.')
save(fig, 'l23-slide5-searchread.png')

fig, ax = base()
heading(ax, 'Writes, Roots, Failing Closed', 'Permissions are absolute.', size=48)
cards3(ax,
       ('Concurrency', ['Check preconditions', 'Write atomically', 'Conflict = clean error']),
       ('Permissions', ["Caller's access", "Never service account's", 'Checked every operation']),
       ('Errors Translated', ['Malformed or missing', 'Or transient failure', 'No vendor codes leak']))
bottomline(ax, 'Resolve identity. Check per access. Fail closed.', size=28)
save(fig, 'l23-slide6-writesroots.png')

next_card('l23-slide7-next.png',
          ['Wrapping REST APIs', 'and SaaS Tools'],
          'Hands-on: query the s06 wrapper; test the planted guards.',
          SEC6)

# ================= LESSON 24 =================
title_card('l24-slide0-title.png', 'Section 6  \u00b7  Lesson 24',
           ['Wrapping REST APIs', 'and SaaS Tools'])

fig, ax = base()
heading(ax, 'Select and Compose', 'Do not transliterate.', size=54)
cards3(ax,
       ('Select, Not Copy', ["Group by model's tasks", 'One tool, several calls', 'Composes one answer']),
       ('One Business Question', ['Look up an order', 'and its shipment', 'One call, one answer']),
       ('The Budget', ['Every tool costs context', 'Eight chosen beat', 'eighty endpoints']))
bottomline(ax, 'A catalog nobody can search is clutter.')
save(fig, 'l24-slide1-select.png')

fig, ax = base()
heading(ax, 'Hide the Mechanics', 'The wrapper absorbs the change.', size=52)
cards3(ax,
       ('Hidden Mechanics', ['Base addresses', 'Versioning, pagination', 'Retry semantics']),
       ('One Error Vocabulary', ['Retryable failure', 'Definitive failure', 'What to change']),
       ('Honest Partial Answers', ['Order, shipment down', 'Label unavailable', 'Decide at design time']))
bottomline(ax, 'The adapter absorbs change. The contract stands still.', size=27)
save(fig, 'l24-slide2-mechanics.png')

fig, ax = base()
heading(ax, 'Pagination', 'Never lie by omission.', size=54)
cards3(ax,
       ('The Lie', ['First page only', 'Model believes complete', 'Decisions inherit it']),
       ('Option A: Walk Pages', ['Adapter walks pages', 'Up to a sane bound', 'One coherent result']),
       ('Option B: Expose Bound', ['Documented parameter', 'Caller controls it', 'Stated in description']))
bottomline(ax, 'Returning page one silently is not honest.')
save(fig, 'l24-slide3-pagination.png')

fig, ax = base()
heading(ax, "SaaS: A Guest in the Vendor's House", 'Rented infrastructure, vendor rules.', size=42)
cards3(ax,
       ('Rented Infrastructure', ['Limits are contractual', "APIs change on vendor's", 'schedule, not yours']),
       ('Authentication', ['Keys held server-side', 'Never in tool schemas', 'Scoped, rotated, billed']),
       ('Token Lifecycle', ['Tokens expire', 'Refresh flows fail', 'Clean reauth error']))
bottomline(ax, 'Design for expiry \u2014 not a 3 a.m. crash.', size=28)
save(fig, 'l24-slide4-saas.png')

fig, ax = base()
heading(ax, 'Quotas Shared with Humans', 'A political limit, not just technical.', size=46)
cards3(ax,
       ('The Shared Quota', ['Same license tier', "Model can burn the day's", 'quota before sales logs in']),
       ('Budget and Cap', ['Budget per tool', 'Cap per day', 'Visible to humans']),
       ('Translate the Model', ['Vendor model to domain', 'Document mapping loss', 'Prefer events to polling']))
bottomline(ax, 'Treat the quota as shared \u2014 because it is.', size=28)
save(fig, 'l24-slide5-quotas.png')

fig, ax = base()
heading(ax, 'Identity Mapping', 'The quiet danger.', size=54)
cards3(ax,
       ('The Mismatch', ['Host identity differs', 'Vendor account differs', 'Permissions differ']),
       ('The Wrapper Maps It', ['Explicitly, in code', 'Never the model', 'Never a guess']),
       ('Watch for Drift', ['Versioned APIs', 'Fields change meaning', 'Contract tests catch it']))
bottomline(ax, 'Map explicitly. Check permissions. Fail closed.', size=28)
save(fig, 'l24-slide6-identity.png')

next_card('l24-slide7-next.png',
          ['Upstream Authentication', 'and Safety Tiers'],
          'Hands-on: extend the s06 wrapper; pass its contract tests.',
          SEC6)

# ================= LESSON 25 =================
title_card('l25-slide0-title.png', 'Section 6  \u00b7  Lesson 25',
           ['Upstream Authentication', 'and Safety Tiers'])

fig, ax = base()
heading(ax, 'Server-Side Only', 'Without exception.', size=54)
cards3(ax,
       ('One Home', ['Server environment', 'Injected from the vault', 'Used in upstream calls']),
       ('Never Appears', ['Tool schemas', 'Descriptions', 'Resources, logs, errors']),
       ('The Small Failure', ['A key parameter added', 'Transits context + logs', 'Every transcript too']))
bottomline(ax, 'If the model can type a credential, design is wrong.', size=27)
save(fig, 'l25-slide1-serverside.png')

fig, ax = base()
heading(ax, 'Least Privilege, Short Lives', 'Separate identities.', size=48)
cards3(ax,
       ('Least Privilege', ['Exactly what tools need', 'Read tools: read-only', 'No admin for one write']),
       ('Short Lives', ['Expiring credentials', 'Automatically rotated', 'Reload, no restarts']),
       ('Identity Separation', ['Propagate the caller', 'Or enforce per user', 'Always fail closed']))
bottomline(ax, 'Rehearse rotation in daylight, with the runbook open.', size=27)
save(fig, 'l25-slide2-privilege.png')

fig, ax = base()
heading(ax, 'Auditability Closes the Loop', 'Every upstream call, logged.', size=46)
cards3(ax,
       ('Log Every Call', ['Who asked', 'What was done', 'When it happened']),
       ('Where It Lives', ['Enterprise audit systems', 'Not an unread', 'server log']),
       ('No Product Named', ['No vault prescribed', 'Platform teams differ', 'Principles travel']))
bottomline(ax, 'Principles travel. Products change.')
save(fig, 'l25-slide3-audit.png')

fig, ax = base()
heading(ax, 'Tier 0 and Tier 1', 'Reads and gentle writes.', size=52)
cards3(ax,
       ('Tier 0 \u2014 Reads', ['Lookups and searches', 'Reads, calculations', 'No side effects at all']),
       ('Tier 1 \u2014 Gentle Writes', ['Create a ticket', 'Add a comment', 'Update a status']),
       ('The Disciplines', ['Tier 0: purity', 'Tier 1: reversibility', 'One additive thing']))
bottomline(ax, 'If it changes anything, it is not Tier 0.')
save(fig, 'l25-slide4-tiers01.png')

fig, ax = base()
heading(ax, 'Tier 2: Where Doors Close', 'Destructive and irreversible.', size=48)
cards3(ax,
       ('What Is Tier 2', ['Deletes and purges', 'Mass updates', 'Money, external messages']),
       ('Heaviest Friction', ['Approval for every call', 'Confirm exact target', 'Comprehensive audit']),
       ('Craft Details', ['State irreversibility', 'Require confirmation', 'Re-verify, dry run']))
bottomline(ax, 'No apology reopens a closed door.')
save(fig, 'l25-slide5-tier2.png')

fig, ax = base()
heading(ax, 'Keep Tiers Honest', 'Assigned in review, never solo.', size=50)
cards3(ax,
       ('Assign in Review', ['Worst plausible outcome', 'Who stands in the way?', 'Never solo judgment']),
       ('Make Them Visible', ['Documentation', 'Descriptions', 'Host-readable metadata']),
       ('Declarations Are Claims', ['Declare truthfully', 'Code enforces the tier', 'Review on every change']))
bottomline(ax, 'A false declaration is worse than none.')
save(fig, 'l25-slide6-honest.png')

next_card('l25-slide7-next.png',
          ['Rate Limits, Quotas, and', 'the Ticketing Scenario'],
          'Hands-on: build the s06 safety register for the sample server.',
          SEC6)

# ================= LESSON 26 =================
title_card('l26-slide0-title.png', 'Section 6  \u00b7  Lesson 26',
           ['Rate Limits, Quotas, and', 'the Ticketing Scenario'])

fig, ax = base()
heading(ax, 'Two Layers of Limiting', 'Protective and economic.', size=52)
cards3(ax,
       ('Protective Layer', ['Per-tool rate limits', 'Concurrency bounds', 'Timeouts = clean errors']),
       ('Economic Layer', ['Tools weighted by cost', 'Per session, user, day', 'Capped to real budgets']),
       ('At Exhaustion', ['Queue the work', 'Degrade to cached results', 'Or fail clearly']))
bottomline(ax, 'Clear failure beats mysterious throttling.')
save(fig, 'l26-slide1-layers.png')

fig, ax = base()
heading(ax, 'Cache, Batch, Back Off', 'Make quotas livable.', size=52)
cards3(ax,
       ('Cache and Batch', ['Cache repeated reads', 'Batch where allowed', 'Fifty in one call']),
       ('Make It Visible', ['A status tool', 'A dashboard', 'Honest log summaries']),
       ('Back Off', ['Exponential, with jitter', 'Bounded retries', 'Adapter, not model, decides']))
bottomline(ax, 'Quota is a business decision expressed in code.', size=27)
save(fig, 'l26-slide2-cachebatch.png')

fig, ax = base()
heading(ax, 'The Ticketing Scenario', 'Meet Meridian.', size=52)
cards3(ax,
       ('The Setting', ['Internal ticketing system', 'Database-backed, own API', 'Hypothetical: Meridian']),
       ('Four Questions', ['Status of one ticket', 'Open high-priority list', 'Add a note, close ticket']),
       ("Priya's World", ['The wrong tax rate', 'Twelve steps, four systems', 'The hands she needed']))
bottomline(ax, 'Compose the section, one careful layer at a time.', size=27)
save(fig, 'l26-slide3-meridian.png')

fig, ax = base()
heading(ax, 'Facade First, Tiers on Top', 'Authentication follows Lesson 25.', size=46)
cards3(ax,
       ('The Facade', ['Ticket resource template', 'Search and note tools', 'Status and close tools']),
       ('Credentials + Quotas', ['Scoped service credential', 'Reads cache, lookups batch', 'Daily caps, clear failure']),
       ('The Tiers', ['Reads: Tier 0', 'Notes, status: Tier 1', 'Closing: Tier 2']))
bottomline(ax, 'Closing re-verifies the ticket is still closeable.', size=27)
save(fig, 'l26-slide4-facadetiers.png')

fig, ax = base()
heading(ax, 'What Meridian Did Not Build', 'The omissions are the lesson.', size=46)
cards3(ax,
       ('The Omissions', ['No raw query tool', 'No transliteration', 'No credentials in schemas']),
       ('No Silent Approval', ['Tier 2 close', 'Never automatic', 'Approval per call']),
       ('The Result', ['Trusted by support', 'Visible boundaries', 'Tiered and graceful']))
bottomline(ax, 'Trust makes an enterprise deployment succeed.', size=28)
save(fig, 'l26-slide5-notbuilt.png')

fig, ax = base()
heading(ax, 'The Mistakes Catalog', 'Recognize these in the wild.', size=50)
cards3(ax,
       ('Design Traps', ['Transliteration trap', 'Raw-query temptation', 'Credential leakage']),
       ('Governance Traps', ['Tier blindness', 'Quota obliviousness', 'No caching or caps']),
       ('Build Jointly', ['Database team', 'API team and security', 'Never as a surprise']))
bottomline(ax, "Priya's fix: reads, updates, a human approves.", size=27)
save(fig, 'l26-slide6-mistakes.png')

next_card('l26-slide7-next.png',
          ['The New Attack Surface:', 'Injection Through Tool Outputs'],
          'Hands-on: run the ticketing scenario under the rate-limit simulator.',
          'Section 6 closes \u00b7 Section 7 begins')

print('ALL SLIDES DONE')
