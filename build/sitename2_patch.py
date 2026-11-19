"""Site name patch v2 (2026-11-19). Runs LAST on final output (after schema_patch).

Usage: python3 sitename2_patch.py public <pi|criminal|divorce|estate> <main|blog>

Fixes, on every HTML page:
- Pages missing </head>/<body>/</body></html> (the PI home page since launch) get a proper document structure.
- Visible "Case Authority LLC" (footer, menu) -> "CaseAuthority LLC" so the name is spelled one way everywhere.
- WebSite JSON-LD name -> the site's own name, alternateName -> [lowercase domain, ...].
- Organization / ProfessionalService / publisher name -> "CaseAuthority", legalName -> "CaseAuthority LLC".
- og:site_name -> the site's own name; home <title> ends "| <site name>".
Fails the build if any check below does not hold.
"""
import glob, json, re, sys

SITES = {
    'pi': ('seopersonalinjurylawyer.com', 'CaseAuthority'),
    'criminal': ('seocriminaldefenselawyer.com', 'CaseAuthority Criminal Defense'),
    'divorce': ('seodivorcelawyer.com', 'CaseAuthority Family Law'),
    'estate': ('seoestatelawyer.com', 'CaseAuthority Estate Planning'),
}
BRAND, LEGAL = 'CaseAuthority', 'CaseAuthority LLC'
root, brand, mode = sys.argv[1].rstrip('/'), sys.argv[2], sys.argv[3]
DOMAIN, SITE = SITES[brand]
SITE_ALT = [DOMAIN] + ([LEGAL] if SITE == BRAND else [])
ORG_TYPES = ('Organization', 'ProfessionalService', 'LocalBusiness')
LD = re.compile(r'(<script[^>]*application/ld\+json[^>]*>)(.*?)(</script>)', re.S)
OLD_NAMES = ('CaseAuthority', 'CaseAuthority LLC', 'Case Authority', 'Case Authority LLC')


def fix_node(o):
    if isinstance(o, dict):
        t = o.get('@type')
        if t == 'WebSite' and o.get('name') in OLD_NAMES + (SITE,):
            o['name'] = SITE
            if str(o.get('url', '')).rstrip('/') == 'https://' + DOMAIN or '@id' in o:
                o['alternateName'] = SITE_ALT
        elif t in ORG_TYPES and o.get('name') in OLD_NAMES:
            o['name'] = BRAND
            if 'legalName' in o or str(o.get('@id', '')).endswith('#org'):
                o['legalName'] = LEGAL
            if 'alternateName' in o or str(o.get('@id', '')).endswith('#org'):
                o['alternateName'] = [LEGAL]
        for v in o.values():
            fix_node(v)
    elif isinstance(o, list):
        for v in o:
            fix_node(v)
    return o


def fix_ld(m):
    raw = m.group(2)
    try:
        j = json.loads(raw)
    except ValueError:
        return m.group(0)
    spaced = '": "' in raw or '", "' in raw
    out = json.dumps(fix_node(j), ensure_ascii=False, separators=((', ', ': ') if spaced else (',', ':')))
    out = out.replace('</', '<\\/')
    return m.group(1) + out + m.group(3)


def fix_structure(h):
    if '<head' in h and '</head>' not in h:
        # first body content after the head: GTM noscript, progress bar, skip link or header
        cands = [h.find(x) for x in ('<noscript><iframe', '<div class="progress"', '<a class="skip"', '<header')]
        cands = [c for c in cands if c > 0]
        k = min(cands)
        h = h[:k] + '</head>\n<body>\n' + h[k:]
    if '<body' in h and '</body>' not in h:
        h = h.rstrip() + '\n</body>\n'
    if '<html' in h and '</html>' not in h:
        h = h.rstrip() + '\n</html>\n'
    return h


problems, changed = [], 0
for fp in glob.glob(root + '/**/*.html', recursive=True):
    h = open(fp, encoding='utf-8').read()
    o = h
    h = fix_structure(h)
    h = LD.sub(fix_ld, h)
    # visible text spelling (outside JSON-LD, which was handled above)
    parts = LD.split(h)
    for i in range(0, len(parts), 4):
        parts[i] = parts[i].replace('Case Authority LLC', LEGAL)
    h = ''.join(parts)
    h = re.sub(r'(<meta property="og:site_name" content=")[^"]*(")', r'\g<1>%s\g<2>' % SITE, h)
    if fp == root + '/index.html':
        h = re.sub(r'(<title>[^<]*\| )CaseAuthority(?: LLC)?(</title>)', r'\g<1>%s\g<2>' % SITE, h, count=1)
    # checks
    if '<head' in h and not ('</head>' in h and '<body' in h and '</body>' in h and '</html>' in h):
        problems.append(fp + ': document structure incomplete')
    if h.find('</head>') > h.find('<body') > -1:
        problems.append(fp + ': </head> after <body>')
    vis = re.sub(r'<script.*?</script>', '', h, flags=re.S)
    if 'Case Authority LLC' in vis:
        problems.append(fp + ': "Case Authority LLC" still visible')
    if 'og:site_name' in h and ('og:site_name" content="%s"' % SITE) not in h:
        problems.append(fp + ': og:site_name not ' + SITE)
    for m in LD.finditer(h):
        try:
            j = json.loads(m.group(2))
        except ValueError:
            problems.append(fp + ': unparsable JSON-LD')
            continue
        def walk(x):
            if isinstance(x, dict):
                if x.get('@type') == 'WebSite' and x.get('name') != SITE:
                    problems.append(fp + ': WebSite name %r' % x.get('name'))
                for v in x.values():
                    walk(v)
            elif isinstance(x, list):
                for v in x:
                    walk(v)
        walk(j)
    if h != o:
        open(fp, 'w', encoding='utf-8').write(h)
        changed += 1

if mode == 'main':
    home = open(root + '/index.html', encoding='utf-8').read()
    ok = False
    for m in LD.finditer(home):
        j = json.loads(m.group(2))
        for it in (j.get('@graph', [j]) if isinstance(j, dict) else [j]):
            if it.get('@type') == 'WebSite' and it.get('name') == SITE and it.get('url') == 'https://%s/' % DOMAIN \
                    and DOMAIN in it.get('alternateName', []):
                ok = True
    if not ok:
        problems.append('home: no WebSite {name:%s, url:https://%s/, alternateName incl. domain}' % (SITE, DOMAIN))
    if ('| %s</title>' % SITE) not in home:
        problems.append('home: <title> does not end with | ' + SITE)

if problems:
    print('sitename2_patch FAILED:\n' + '\n'.join(problems[:25]))
    sys.exit(1)
print('sitename2_patch: %d pages updated, site name "%s"' % (changed, SITE))
