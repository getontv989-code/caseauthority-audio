"""guide_patch.py (2026-11-24, Mash): make the blog guide the page for "seo for personal injury lawyers"
and step the homepage back to "personal injury seo".

usage: python3 guide_patch.py public main|blog
Runs after split.py/verify.py and BEFORE positioning_patch.py (schema_patch then sitename2_patch stay last).
- Guide moves from /blog/get-found-online-first-seo-for-personal-injury-lawyers to /blog/seo-for-personal-injury-lawyers
  (301 lives in both vercel.json files). New title, H1, meta, phrase in the intro, homepage link text changed.
- Homepage: new title, meta, H1, H2, body uses of the phrase rewritten, one link to the guide.
- Why-SEO post retitled, phrase cut to one use (a link to the guide).
- Six posts + /services get a guide link in the opening paragraph; every footer gets "PI SEO Guide".
Fails the build if any change did not apply or the old guide URL is left anywhere.
"""
import os, re, sys

OUT, MODE = sys.argv[1], sys.argv[2]
assert MODE in ('main', 'blog'), 'usage: guide_patch.py public main|blog'
OLD_SLUG = 'blog/get-found-online-first-seo-for-personal-injury-lawyers'
NEW_SLUG = 'blog/seo-for-personal-injury-lawyers'
GUIDE = '/' + NEW_SLUG
PHRASE = 'SEO for personal injury lawyers'
errors = []

def link(text=PHRASE):
    return '<a class="in" href="%s">%s</a>' % (GUIDE, text)

# Replacements applied to every text file of the build (only where the old string exists).
GLOBAL = [
    (OLD_SLUG, NEW_SLUG),
    # guide
    ('Get Found Online First: SEO for Personal Injury Lawyers |', 'SEO for Personal Injury Lawyers: A Starter Guide |'),
    ('Get Found Online First: A Starter Guide to SEO for Personal Injury Lawyers', 'SEO for Personal Injury Lawyers: How to Get Found Online First'),
    ('Why the personal injury firm that gets found first online usually gets the call, and the SEO steps that put your firm in front of injured people first.',
     "A simple guide to SEO for personal injury lawyers: where injured people search, how Google ranks firms, and the steps that put yours first."),
    ('This guide explains what getting found online first really means for a personal injury firm,',
     'This guide to SEO for personal injury lawyers explains what getting found online first really means for a personal injury firm,'),
    ('If you want the full picture of what that work involves for an injury firm, our main guide to <a class="in" href="/">SEO for personal injury lawyers</a> covers it in more depth. This article focuses on the first step: being found.',
     'If you would rather hand that work to a specialist team, see <a class="in" href="/">our personal injury SEO services</a>. This guide walks through what the work involves, starting with the first step: being found.'),
    # why-seo post
    ('Why SEO for Personal Injury Lawyers Matters |', 'Why Does SEO Matter for Personal Injury Lawyers? |'),
    ('Why SEO for personal injury lawyers matters (and how to judge an SEO proposal)', 'Why Does SEO Matter for Personal Injury Lawyers?'),
    ('Why SEO for personal injury lawyers matters: what PI SEO is,', 'Why SEO matters for personal injury lawyers: what PI SEO is,'),
    ('>why SEO for personal injury lawyers matters</a>', '>why SEO matters for personal injury lawyers</a>'),
    ('SEO for personal injury lawyers matters because injured people', 'SEO matters for personal injury lawyers because injured people'),
    ('Why does SEO for personal injury lawyers matter?', 'Why does SEO matter so much for injury firms?'),
    ('To rank in those places, SEO for personal injury lawyers combines', 'To rank in those places, personal injury SEO combines'),
    ('That is the core of why SEO for personal injury lawyers matters:', 'That is the core of why SEO matters for injury firms:'),
    ('You can also read more on <a class="in" href="/">SEO for personal injury lawyers</a>', 'You can also read our guide to ' + link()),
    # share-image alt text (og + twitter) on every page
    ('content="CaseAuthority: SEO for personal injury lawyers. Rank #1. Sign more cases."',
     'content="CaseAuthority: personal injury SEO agency. Rank #1. Sign more cases."'),
    # footer link on every page, next to the service pages
    ('<div class="fl-cols"><a href="/recommended-seo-services-personal-injury-law-firms">Personal Injury SEO Services</a>',
     '<div class="fl-cols"><a href="/recommended-seo-services-personal-injury-law-firms">Personal Injury SEO Services</a><a href="%s">PI SEO Guide</a>' % GUIDE),
]

# Replacements that must apply to one file (path relative to OUT): (old, new, expected count or None for >=1)
HOME_META = "CaseAuthority is a personal injury SEO agency. We rank PI firms in Google's Map Pack, organic search and AI answers, so searches become signed cases."
OLD_HOME_META = "SEO for personal injury lawyers and PI attorneys. We rank your firm in Google's Map Pack, organic search and AI answers, so searches become signed cases."
FILE = {
    'main': {
        'index.html': [
            ('<title>SEO for Personal Injury Lawyers &amp; Attorneys |', '<title>Personal Injury SEO Agency for PI Law Firms |', 1),
            ('| SEO for Personal Injury Lawyers"', '| Personal Injury SEO Agency for PI Law Firms"', 2),
            (OLD_HOME_META, HOME_META, None),
            ('<h1 class="t-h1">Personal injury lawyer SEO that fills your intake,', '<h1 class="t-h1">Personal injury SEO that fills your intake,', 1),
            ('<h2 class="t-h2">SEO for Personal Injury Lawyers, Tailored to PI Law Firms</h2>', '<h2 class="t-h2">Personal Injury SEO, Tailored to PI Law Firms</h2>', 1),
            ('<p class="t-lead hero-sub">SEO for personal injury lawyers and attorneys. We rank', '<p class="t-lead hero-sub">Personal injury SEO for PI law firms and attorneys. We rank', 1),
            ('What does SEO for personal injury lawyers include?', 'What does personal injury SEO include?', 2),
            ('SEO for personal injury lawyers covers four things', 'Personal injury SEO covers four things', 2),
        ],
        'services.html': [],
    },
    'blog': {
        'blog/seo-for-personal-injury-lawyers.html': [],
    },
}

# Guide link in the opening paragraph (end of the lead under the H1).
LEAD_LINK = {
    'main': {
        'services.html': 'New to SEO? Start with our guide to %s.',
    },
    'blog': {
        'blog/is-local-seo-worth-it-for-personal-injury-attorneys.html': 'If you are new to search, start with our guide to %s.',
        'blog/how-to-compare-seo-proposals-for-personal-injury-law-firms.html': 'If you want the basics first, read our guide to %s.',
        'blog/seo-roi-case-studies-personal-injury-attorneys.html': 'For the basics behind these results, see our guide to %s.',
        'blog/how-long-does-seo-take-for-law-firms.html': 'For the bigger picture, see our guide to %s.',
        'blog/how-to-rank-in-chatgpt.html': 'For the groundwork behind it, see our guide to %s.',
        'blog/seo-guarantee.html': 'For what good SEO work looks like, see our guide to %s.',
    },
}
HOME_GUIDE_P = '<p class="t-lead muted">New to SEO? Read our guide to %s.</p>' % link()

def files():
    for root, _, fs in os.walk(OUT):
        for f in fs:
            if f.endswith(('.html', '.xml', '.txt', '.json')):
                yield os.path.join(root, f)

# 1. move the guide (blog build only)
if MODE == 'blog':
    src = os.path.join(OUT, OLD_SLUG + '.html'); dst = os.path.join(OUT, NEW_SLUG + '.html')
    if not os.path.isfile(src):
        errors.append('guide page %s not built' % src)
    else:
        os.rename(src, dst)

# 2. global replacements
for p in files():
    s = open(p, encoding='utf-8').read(); o = s
    for a, b in GLOBAL:
        s = s.replace(a, b)
    if s != o:
        open(p, 'w', encoding='utf-8').write(s)

# 3. per-file replacements
for rel, reps in FILE[MODE].items():
    p = os.path.join(OUT, rel)
    if not os.path.isfile(p):
        errors.append('missing ' + rel); continue
    s = open(p, encoding='utf-8').read()
    for a, b, n in reps:
        c = s.count(a)
        if (n is None and c < 1) or (n is not None and c != n):
            errors.append('%s: expected %s of %r, found %d' % (rel, n if n is not None else '>=1', a[:70], c))
        s = s.replace(a, b)
    if rel == 'index.html':
        # one link to the guide, under the services intro paragraph (below the H2)
        m = re.search(r'(<div class="svc-intro">\s*<h2 class="t-h2">Personal Injury SEO, Tailored to PI Law Firms</h2>\s*<p class="t-lead muted">.*?</p>)', s, re.S)
        if not m:
            errors.append('home: services intro not found')
        elif HOME_GUIDE_P not in s:
            s = s[:m.end()] + '\n        ' + HOME_GUIDE_P + s[m.end():]
    open(p, 'w', encoding='utf-8').write(s)

# 4. guide link in the opening paragraph
for rel, sentence in LEAD_LINK[MODE].items():
    p = os.path.join(OUT, rel)
    if not os.path.isfile(p):
        errors.append('missing ' + rel); continue
    s = open(p, encoding='utf-8').read()
    m = re.search(r'<p class="t-lead phero-lead">(.*?)</p>', s, re.S)
    if not m:
        errors.append(rel + ': no opening paragraph'); continue
    if ('href="%s"' % GUIDE) not in m.group(1):
        s = s[:m.end(1)] + ' ' + (sentence % link()) + s[m.end(1):]
        open(p, 'w', encoding='utf-8').write(s)

# 5. checks
for p in files():
    s = open(p, encoding='utf-8').read()
    if 'CaseAuthority: SEO for personal injury lawyers. Rank #1' in s:
        errors.append('%s still has the old share-image alt text' % p)
    if OLD_SLUG in s:
        errors.append('%s still has the old guide URL' % p)
    if 'href="%s"' % GUIDE not in s and p.endswith('.html') and '</footer>' in s:
        errors.append('%s has no link to the guide' % p)

def body_uses(h):
    """Visible + structured uses of the exact phrase, minus the share-image alt text and other service names."""
    h = re.sub(r'<meta[^>]+image:alt[^>]*>', '', h)
    return [m.start() for m in re.finditer(r'(?i)(?<!local )(?<!ai )(?<!bing )(?<!regular )seo for personal injury lawyers', h)]

if MODE == 'main':
    h = open(os.path.join(OUT, 'index.html'), encoding='utf-8').read()
    uses = body_uses(h)
    if len(uses) != 1 or h.count('>%s</a>' % PHRASE) != 1 or h.count('href="%s"' % GUIDE) < 1:
        errors.append('home: expected exactly 1 use of the phrase (the guide link), found %d' % len(uses))
    if re.search(r'(?i)personal injury lawyer seo', h):
        errors.append('home: "personal injury lawyer SEO" still present')
    if 'noindex' in h.split('</head>')[0] or '<link rel="canonical" href="https://seopersonalinjurylawyer.com/">' not in h:
        errors.append('home: canonical/robots changed')
    sv = open(os.path.join(OUT, 'services.html'), encoding='utf-8').read()
    if link() not in sv:
        errors.append('services: no guide link')
else:
    g = open(os.path.join(OUT, NEW_SLUG + '.html'), encoding='utf-8').read()
    need = ['<title>SEO for Personal Injury Lawyers: A Starter Guide | CaseAuthority',
            '<link rel="canonical" href="https://seopersonalinjurylawyer.com/%s">' % NEW_SLUG,
            'SEO for Personal Injury Lawyers: How to Get Found Online First</h1>',
            '<a class="in" href="/">our personal injury SEO services</a>']
    for n in need:
        if n not in g:
            errors.append('guide: missing %r' % n[:70])
    if '<a class="in" href="/">SEO for personal injury lawyers</a>' in g:
        errors.append('guide: still links the homepage with the phrase')
    lead = re.search(r'<p class="t-lead phero-lead">(.*?)</p>', g, re.S).group(1)
    if PHRASE.lower() not in ' '.join(re.sub('<[^>]+>', ' ', lead).split()[:100]).lower():
        errors.append('guide: phrase not in the first 100 words')
    w = open(os.path.join(OUT, 'blog/why-seo-for-personal-injury-lawyers-matters.html'), encoding='utf-8').read()
    wu = len(body_uses(w.split('</head>', 1)[1]))
    if not 1 <= wu <= 2 or link() not in w or '<a class="in" href="/">SEO for personal injury lawyers</a>' in w:
        errors.append('why-seo: expected 1-2 uses with the guide link, found %d' % wu)
    if '<title>Why Does SEO Matter for Personal Injury Lawyers? | CaseAuthority' not in w:
        errors.append('why-seo: title not changed')
    for rel in LEAD_LINK['blog']:
        s = open(os.path.join(OUT, rel), encoding='utf-8').read()
        if link() not in s:
            errors.append(rel + ': no guide link')
    sm = open(os.path.join(OUT, 'blog/sitemap.xml'), encoding='utf-8').read()
    if 'https://seopersonalinjurylawyer.com/%s</loc>' % NEW_SLUG not in sm:
        errors.append('blog sitemap: guide missing')

for p in files():
    if 'plain-English' in open(p, encoding='utf-8').read() and NEW_SLUG in p:
        errors.append(p + ': plain-English')

if errors:
    print('guide_patch FAILED:'); [print(' -', e) for e in errors]; sys.exit(1)
print('guide_patch ok (%s)' % MODE)
