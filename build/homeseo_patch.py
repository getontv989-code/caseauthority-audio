#!/usr/bin/env python3
"""Homepage "personal injury SEO" push (Mash, 2026-11-28).
usage: homeseo_patch.py public <main|blog|divorce|criminal>
Runs after positioning_patch and before schema_patch / sitename patches.
Every edit must match the expected number of times or the build fails."""
import sys, os, re
root, mode = sys.argv[1], sys.argv[2]
HOME = '<a class="in" href="/">'
SVC = '/recommended-seo-services-personal-injury-law-firms'
errors = []

def find(slug):
    if slug == '':
        c = [os.path.join(root, 'index.html')]
    else:
        c = [os.path.join(root, slug + '.html'), os.path.join(root, slug, 'index.html')]
    for p in c:
        if os.path.isfile(p):
            return p
    errors.append(f'missing page: /{slug}')
    return None

def edit(slug, pairs):
    p = find(slug)
    if not p:
        return
    s = open(p, encoding='utf-8').read()
    for old, new, n in pairs:
        k = s.count(old)
        if (n == '+' and k < 1) or (n != '+' and k != n):
            errors.append(f'/{slug}: expected {n} of {old[:70]!r}, found {k}')
            continue
        s = s.replace(old, new)
    open(p, 'w', encoding='utf-8').write(s)

L = lambda t: t.replace('[[', HOME).replace(']]', '</a>')
CARD = ('class="rel-t">Personal Injury SEO Services<', 'class="rel-t">Recommended SEO Services<', 1)
REPOINT = lambda a: (f'<a class="in" href="{SVC}">{a}</a>', f'{HOME}{a}</a>', 1)

MAIN = {
    # step 1: services page
    SVC[1:]: [
        ('Personal Injury SEO Services for Law Firms |', 'Recommended SEO Services for PI Law Firms |', '+'),
        ('Personal injury SEO services that sign cases. The recommended SEO for personal injury law firms: landing pages, technical SEO, citations and AI search.',
         'Recommended SEO services for personal injury law firms that sign cases: landing pages, technical SEO, citations and AI search.', '+'),
        ('Personal Injury SEO Services Built to Sign Cases', 'Recommended SEO Services for Personal Injury Law Firms', '+'),
        ('<span aria-current="page">Personal Injury SEO Services</span></nav>', '<span aria-current="page">Recommended SEO Services</span></nav>', 1),
        ('"name":"Personal Injury SEO Services","item"', '"name":"Recommended SEO Services","item"', '+'),
        ("If you're looking for personal injury SEO services your firm actually needs, not a bloated retainer full of deliverables that don't move rankings, this page is for you. These are the recommended SEO services for personal injury law firms, and the ones we deliver every month.",
         "Recommended SEO services for personal injury law firms are the ones your firm actually needs, not a bloated retainer full of deliverables that don't move rankings. These are the services we recommend, and the ones we deliver every month.", 1),
        ('The best personal injury SEO is the work that signs cases.', 'The best SEO for an injury firm is the work that signs cases.', 1),
        ("Personal injury SEO services firms need vs. what they're usually sold", "SEO services PI firms need vs. what they're usually sold", '+'),
        ('What personal injury SEO includes (vs. what generic agencies sell)', 'What the recommended SEO stack includes (vs. what generic agencies sell)', '+'),
        ('How to choose a personal injury SEO company', 'How to choose an SEO company for your PI firm', '+'),
        ('How much do personal injury SEO services cost?', 'How much do recommended SEO services cost?', '+'),
    ],
    # step 2 + 5: homepage
    '': [
        ('style="--acc:#353945"><i></i>Personal Injury SEO Services<svg', 'style="--acc:#353945"><i></i>Recommended SEO Services<svg', 1),
        ("CaseAuthority was built to fix that: PI attorney SEO measured in signed cases, not traffic.",
         "CaseAuthority is an SEO agency for personal injury firms, built to fix that and measured in signed cases, not traffic.", 1),
        ('Good PI attorney SEO ties all four to one number', 'Good personal injury attorney SEO ties all four to one number', '+'),
        ('Yes. CaseAuthority works with personal injury law firms nationwide.', 'Yes. CaseAuthority provides personal injury law firm SEO nationwide.', '+'),
        ("in your market — 'personal injury lawyer [city]', '[accident type] attorney near me', '[case type] law firm [area]' — and build",
         "in your market, such as 'personal injury lawyer [city]', '[accident type] attorney near me' and '[case type] law firm [area]', and build", 1),
    ],
    # step 2 + 4: /services
    'services': [
        ('class="svc-t">Personal Injury SEO Services<', 'class="svc-t">Recommended SEO Services<', 1),
        ('One partner that specializes in personal injury. New to SEO?',
         L('One partner that specializes in personal injury. Our core service is [[personal injury SEO]], and every other channel is built around it. New to SEO?'), 1),
    ],
    'why-choose-caseauthority': [CARD,
        ('Choosing a personal injury SEO agency comes down to one question', L('Choosing a [[personal injury SEO agency]] comes down to one question'), 1)],
    'personal-injury-lawyer-google-maps-ranking': [CARD,
        ('In addition to traditional SEO, CaseAuthority specializes', L('In addition to traditional [[personal injury SEO]], CaseAuthority specializes'), 1)],
    'bing-seo-for-personal-injury-lawyers': [
        ("It's a second channel built on the same foundation: the same compact", L("It's a second channel built on the same foundation as your [[personal injury attorney SEO]]: the same compact"), 1)],
    'local-seo-personal-injury-lawyers': [CARD],
    'personal-injury-law-firm-website-content-writing': [CARD],
    'personal-injury-law-firm-website-design': [CARD],
}

BLOG = {
    # step 3: repoint to the homepage, same anchors
    'blog/law-firm-marketing-plan': [CARD, REPOINT('personal injury SEO')],
    'blog/how-to-get-personal-injury-clients': [CARD, REPOINT('personal injury SEO services')],
    'blog/seo-for-accident-claims': [REPOINT('personal injury SEO services')],
    'blog/seo-roi-case-studies-personal-injury-attorneys': [CARD, REPOINT('personal injury SEO services')],
    'blog/why-is-my-law-firm-website-not-ranking-on-google': [REPOINT('personal injury SEO services')],
    # step 4: new in-body homepage links
    'blog/mass-tort-marketing': [('for firms that want a steady flow of inquiries they do not have to buy.</p>',
        L('for firms that want a steady flow of inquiries they do not have to buy. As a [[personal injury SEO agency]], this kind of long-term visibility is the work we focus on.</p>'), 1)],
    'blog/personal-injury-lead-generation': [('explains how these fit together.</p>',
        L('explains how these fit together. If you would rather hand this work to a specialist, CaseAuthority is an [[SEO agency for personal injury firms]].</p>'), 1)],
    'blog/personal-injury-lawyer-advertising': [('explains what that work involves.</p>',
        L('explains what that work involves. For the bigger picture, see how [[personal injury SEO]] builds that free visibility over time.</p>'), 1)],
    'blog/website-design-for-personal-injury-lawyers': [('and much of it depends on how the site is built.</p>',
        L('and much of it depends on how the site is built. That is why good [[personal injury law firm SEO]] starts with the website itself.</p>'), 1)],
    'blog/law-firm-marketing-trends': [('explains this in more depth.</p>',
        L('explains this in more depth. It is the same steady work a good [[personal injury SEO agency]] already does.</p>'), 1)],
    'blog/is-local-seo-worth-it-for-personal-injury-attorneys': [('at the moment someone in your area decides they need a lawyer.</p>',
        L('at the moment someone in your area decides they need a lawyer. Local SEO is one part of wider [[personal injury attorney SEO]], which also covers your website, content and reputation.</p>'), 1)],
    'blog/is-super-lawyers-legit': [CARD, ('Recognition, reviews and clear case pages then help them choose you.</p>',
        L('Recognition, reviews and clear case pages then help them choose you. If you want help with the search side, CaseAuthority is an [[SEO agency for personal injury firms]].</p>'), 1)],
    'blog/reputation-management-for-attorneys': [('covers how reviews help you show up in the map in the first place.</p>',
        L('covers how reviews help you show up in the map in the first place. Reviews are also one of the signals behind strong [[personal injury law firm SEO]].</p>'), 1)],
    # step 2: card label only on these
    **{f'blog/{s}': [CARD] for s in ['how-long-does-seo-take-for-law-firms', 'how-to-compare-seo-proposals-for-personal-injury-law-firms',
        'million-dollar-advocates-forum', 'multi-location-seo-for-personal-injury-law-firms', 'personal-injury-intake-form', 'seo-guarantee',
        'seo-kpis-for-personal-injury-law-firms', 'why-seo-for-personal-injury-lawyers-matters']},
}

PI_LINK = '<a class="in" href="https://seopersonalinjurylawyer.com/">personal injury SEO</a>'
SISTER = {'': [('who do the actual work. No middleman, no hidden fees.</p>',
    f'who do the actual work. No middleman, no hidden fees. The same team runs {PI_LINK} for injury firms.</p>', 1)]}

plan = {'main': MAIN, 'blog': BLOG, 'divorce': SISTER, 'criminal': SISTER}[mode]
for slug, pairs in plan.items():
    edit(slug, pairs)

# checks on the result
def body(slug):
    p = find(slug)
    s = open(p, encoding='utf-8').read() if p else ''
    i, j = s.find('<main'), s.find('</main>')
    return s, (s[i:j] if i >= 0 and j > i else '')
if mode == 'main':
    s, _ = body(SVC[1:])
    t = re.search(r'<title>(.*?)</title>', s).group(1)
    h = re.search(r'<h1[^>]*>(.*?)</h1>', s).group(1)
    if not t.startswith('Recommended SEO Services for PI Law Firms |'): errors.append('services title: ' + t)
    if h != 'Recommended SEO Services for Personal Injury Law Firms': errors.append('services h1: ' + h)
    m = re.search(r'<meta name="description" content="([^"]*)"', s).group(1)
    if not m.startswith('Recommended SEO services for personal injury law firms'): errors.append('services meta')
    _, b = body(SVC[1:])
    vis = re.sub(r'<[^>]+>', ' ', re.sub(r'<script.*?</script>', '', b, flags=re.S))
    if len(re.findall(r'(?i)personal injury seo', vis)) > 3: errors.append('services body has more than 3 "personal injury SEO"')
    if b.count(HOME + 'personal injury SEO</a>') != 1: errors.append('services page lost its homepage link')
    s, b = body('')
    for ph in ['SEO agency for personal injury firms', 'personal injury law firm SEO', 'personal injury attorney SEO']:
        if ph not in b: errors.append('home missing ' + ph)
want = {'main': ['services', 'why-choose-caseauthority', 'personal-injury-lawyer-google-maps-ranking', 'bing-seo-for-personal-injury-lawyers'],
        'blog': [k for k, v in BLOG.items() if any(HOME in x[1] for x in v)], 'divorce': [], 'criminal': []}[mode]
for slug in want:
    _, b = body(slug)
    if HOME not in b: errors.append(f'/{slug}: no in-body homepage link')
for slug in plan:
    s, _ = body(slug)
    if '—' in re.sub(r'<h1.*?</h1>|"name":"[^"]*"', '', s, flags=re.S) and slug in ('', 'blog/mass-tort-marketing'):
        errors.append(f'/{slug}: em dash')
if mode in ('divorce', 'criminal'):
    _, b = body('')
    if PI_LINK not in b: errors.append('sister home missing PI link')
if errors:
    print('homeseo_patch FAILED:'); [print('  ' + e) for e in errors]; sys.exit(1)
print(f'homeseo_patch {mode}: OK ({len(plan)} pages)')
