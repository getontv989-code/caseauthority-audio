"""Site name patch: every page says the site is "CaseAuthority LLC".

Google picks the site name shown in results from the home page: WebSite structured data
(name + alternateName), og:site_name and the home page <title>. Before this patch the sites
said "CaseAuthority" in some places and "Case Authority LLC" in others. This makes every
signal on every page say the same name.

Usage: python3 sitename_patch.py public [main|blog]
  main: the build must contain public/index.html with WebSite name "CaseAuthority LLC" (fails otherwise)
Runs on built output, after the other HTML patches and before split.
"""
import glob, json, re, sys

NAME = 'CaseAuthority LLC'
SITE_ALT = ['CaseAuthority', 'Case Authority', 'Case Authority LLC']
ORG_ALT = ['CaseAuthority', 'Case Authority']
ORG_TYPES = ('Organization', 'ProfessionalService', 'WebSite')

root = sys.argv[1].rstrip('/')
mode = sys.argv[2] if len(sys.argv) > 2 else 'blog'
LD = re.compile(r'(<script[^>]*application/ld\+json[^>]*>)(.*?)(</script>)', re.S)


def fix_ld(s):
    # name on typed organisation / website nodes (flat part of the node, before any nested object)
    s = re.sub(r'("@type":\s*"(?:%s)"[^{}\[\]]*?"name":\s*)"CaseAuthority"' % '|'.join(ORG_TYPES),
               r'\1"%s"' % NAME, s)
    s = re.sub(r'("@id":\s*"[^"]*#(?:org|site|website)"[^{}\[\]]*?"name":\s*)"CaseAuthority"', r'\1"%s"' % NAME, s)
    s = s.replace('"legalName":"Case Authority LLC"', '"legalName":"%s"' % NAME)
    alt = json.dumps(SITE_ALT, separators=(',', ':'))
    s = re.sub(r'("@id":\s*"[^"]*#(?:site|website)"[^{}\[\]]*?"name":\s*"%s")(,\s*"alternateName":\s*\[[^\]]*\])?' % NAME,
               lambda m: m.group(1) + ',"alternateName":' + alt, s)
    oalt = json.dumps(ORG_ALT, separators=(',', ':'))
    s = re.sub(r'("@id":\s*"[^"]*#org"[^{}\[\]]*?"legalName":\s*"%s")(,\s*"alternateName":\s*\[[^\]]*\])?' % NAME,
               lambda m: m.group(1) + ',"alternateName":' + oalt, s)
    return s


def walk(o, bad):
    if isinstance(o, dict):
        t = o.get('@type')
        if t in ORG_TYPES and o.get('name') == 'CaseAuthority':
            bad.append(t)
        for v in o.values():
            walk(v, bad)
    elif isinstance(o, list):
        for v in o:
            walk(v, bad)


changed = 0
problems = []
for fp in glob.glob(root + '/**/*.html', recursive=True):
    h = open(fp, encoding='utf-8').read()
    o = h
    h = LD.sub(lambda m: m.group(1) + fix_ld(m.group(2)) + m.group(3), h)
    h = re.sub(r'(<meta property="og:site_name" content=")CaseAuthority(")', r'\1%s\2' % NAME, h)
    if fp == root + '/index.html':
        h = re.sub(r'(<title>[^<]*\| )CaseAuthority(</title>)', r'\1%s\2' % NAME, h, count=1)
        h = re.sub(r'(<meta (?:property|name)="(?:og|twitter):title" content="[^"]*\| )CaseAuthority(")', r'\1%s\2' % NAME, h)
    for m in LD.finditer(h):
        try:
            j = json.loads(m.group(2))
        except ValueError:
            continue
        bad = []
        walk(j, bad)
        if bad:
            problems.append('%s: %s still named CaseAuthority' % (fp, bad))
    if 'og:site_name' in h and ('og:site_name" content="%s"' % NAME) not in h:
        problems.append('%s: og:site_name is not %s' % (fp, NAME))
    if h != o:
        open(fp, 'w', encoding='utf-8').write(h)
        changed += 1

if mode == 'main':
    home = open(root + '/index.html', encoding='utf-8').read()
    ok = False
    for m in LD.finditer(home):
        j = json.loads(m.group(2))
        for it in (j.get('@graph', [j]) if isinstance(j, dict) else j):
            if it.get('@type') == 'WebSite' and it.get('name') == NAME and it.get('url', '').endswith('/'):
                ok = ok or set(SITE_ALT) <= set(it.get('alternateName', []))
    if not ok:
        problems.append('home page has no WebSite node named %s with alternateName' % NAME)
    if ('| %s</title>' % NAME) not in home:
        problems.append('home page <title> does not end with %s' % NAME)

if problems:
    print('sitename_patch FAILED:')
    print('\n'.join(problems[:20]))
    sys.exit(1)
print('sitename_patch: %d pages updated to "%s"' % (changed, NAME))
