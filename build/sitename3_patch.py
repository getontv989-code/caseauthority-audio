"""Site name patch v3 (2026-11-28). Runs LAST, after sitename2_patch.

Usage: python3 sitename3_patch.py public <pi|criminal|divorce|estate>

Every page title, og:title and twitter:title that ends "| CaseAuthority" or
"| CaseAuthority LLC" now ends with the site's own name, so a sister site never
calls itself by the PI site's name ("CaseAuthority") on its inner pages, and the
homepage og:title no longer says "CaseAuthority LLC". Fails the build if any
title still ends with a different CaseAuthority name.
"""
import glob, re, sys

SITES = {'pi': 'CaseAuthority', 'criminal': 'CaseAuthority Criminal Defense',
         'divorce': 'CaseAuthority Family Law', 'estate': 'CaseAuthority Estate Planning'}
root, SITE = sys.argv[1].rstrip('/'), SITES[sys.argv[2]]
OLD = r'CaseAuthority(?: LLC)?'
T = re.compile(r'(<title>[^<]*\|\s*)%s(\s*</title>)' % OLD)
M = re.compile(r'(<meta (?:property|name)="(?:og|twitter):title" content="[^"]*\|\s*)%s(")' % OLD)
END = re.compile(r'(?:<title>[^<]*\|\s*(CaseAuthority[^<|]*?)\s*</title>|<meta (?:property|name)="(?:og|twitter):title" content="[^"]*\|\s*(CaseAuthority[^"|]*?)")')
changed, bad = 0, []
for fp in glob.glob(root + '/**/*.html', recursive=True):
    h = open(fp, encoding='utf-8').read()
    o = h
    h = T.sub(lambda m: m.group(1) + SITE + m.group(2), h)
    h = M.sub(lambda m: m.group(1) + SITE + m.group(2), h)
    for m in END.finditer(h):
        n = m.group(1) or m.group(2)
        if n != SITE:
            bad.append('%s: title ends with %r' % (fp, n))
    if h != o:
        open(fp, 'w', encoding='utf-8').write(h)
        changed += 1
if bad:
    print('sitename3_patch FAILED:\n' + '\n'.join(bad[:25]))
    sys.exit(1)
print('sitename3_patch: %d pages updated, titles end with "%s"' % (changed, SITE))
