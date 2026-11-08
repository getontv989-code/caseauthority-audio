#!/usr/bin/env python3
"""Adds the CaseAuthority LinkedIn icon to the footer bottom bar of every built page and
LinkedIn to sameAs on every CaseAuthority Organization/ProfessionalService JSON-LD node.
Usage: linkedin_patch.py [public]. Fails the build if any footer page is left without the link."""
import json, os, re, sys
URL = 'https://www.linkedin.com/company/caseauthority/'
ICON = ('<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" focusable="false"><path d="M20.45 20.45h-3.55v-5.57c0-1.33-.03-3.04-1.85-3.04-1.86 0-2.14 1.45-2.14 2.94v5.67H9.35V9h3.41v1.56h.05c.48-.9 1.64-1.85 3.37-1.85 3.6 0 4.27 2.37 4.27 5.46v6.28zM5.34 7.43a2.06 2.06 0 1 1 0-4.13 2.06 2.06 0 0 1 0 4.13zM7.12 20.45H3.56V9h3.56v11.45zM22.22 0H1.77C.79 0 0 .77 0 1.73v20.54C0 23.23.79 24 1.77 24h20.45c.98 0 1.78-.77 1.78-1.73V1.73C24 .77 23.2 0 22.22 0z"/></svg>')
LINK = f'<a class="ftr-li" href="{URL}" target="_blank" rel="noopener noreferrer" aria-label="CaseAuthority on LinkedIn" title="CaseAuthority on LinkedIn">{ICON}</a>'
CSS = ('<style id="ftr-li-css">.ftr-soc{display:inline-flex;align-items:center;gap:16px}'
       '.ftr-bot .ftr-li{display:inline-flex;color:var(--color-gray-600);padding:14px 6px;margin:-14px -6px;transition:color .2s ease}'
       '.ftr-bot .ftr-li:hover,.ftr-bot .ftr-li:focus-visible{color:var(--ca-black,#0E0E0F)}'
       '.ftr-li svg{width:20px;height:20px;display:block}</style>')
COPY = '<span>© 2026 Case Authority LLC</span>'
ORG_TYPES = {'Organization', 'ProfessionalService'}

def add_same_as(node):
    if isinstance(node, list):
        return any([add_same_as(n) for n in node])
    if not isinstance(node, dict):
        return False
    hit = False
    t = node.get('@type')
    if t in ORG_TYPES and (str(node.get('name', '')).startswith('CaseAuthority') or str(node.get('@id', '')).endswith('#org')) and len(node) > 2:
        s = node.get('sameAs') or []
        s = [s] if isinstance(s, str) else list(s)
        if URL not in s:
            node['sameAs'] = s + [URL]
            hit = True
    for v in node.values():
        if isinstance(v, (dict, list)) and add_same_as(v):
            hit = True
    return hit

def ld(m):
    try:
        data = json.loads(m.group(2))
    except Exception:
        return m.group(0)
    if not add_same_as(data):
        return m.group(0)
    return m.group(1) + json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/') + m.group(3)

root = sys.argv[1] if len(sys.argv) > 1 else 'public'
done = missing = 0
bad = []
for d, _, fs in os.walk(root):
    for f in fs:
        if not f.endswith('.html'):
            continue
        p = os.path.join(d, f)
        h = open(p, encoding='utf-8').read()
        if 'class="ftr-bot"' not in h:
            continue
        if 'class="ftr-li"' not in h:
            if h.count(COPY) != 1 or h.count('</head>') > 1:
                bad.append(p); continue
            h = h.replace(COPY, f'<span class="ftr-soc">{LINK}{COPY[6:-7]}</span>', 1)
            # some minified pages omit </head>; a <style> just before the footer works the same there
            h = h.replace('</head>', CSS + '</head>', 1) if '</head>' in h else h.replace('<footer', CSS + '<footer', 1)
        h = re.sub(r'(<script type="application/ld\+json"[^>]*>)(.*?)(</script>)', ld, h, flags=re.S)
        open(p, 'w', encoding='utf-8').write(h)
        done += 1
        if h.count(f'href="{URL}"') != 1:
            bad.append(p)
if bad:
    print('linkedin_patch: footer not patched in', *bad[:20], sep='\n  '); sys.exit(1)
print(f'linkedin_patch: {done} pages have the LinkedIn footer icon')
