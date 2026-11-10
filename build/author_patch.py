#!/usr/bin/env python3
"""Author byline + bio card + Person schema on every blog post (all CaseAuthority blogs).
Author: Armash Peer (LinkedIn), vetted by the CaseAuthority Team.
Runs on built output, so every current and future post gets it with no per-post field.
Usage: author_patch.py [public]. Fails the build if any BlogPosting page is left unpatched."""
import json, os, re, sys

NAME = 'Armash Peer'
LI = 'https://www.linkedin.com/in/mohamed-armash/'
TEAM = 'CaseAuthority Team'
OLD_BY = '<span>By the CaseAuthority team</span>'
LI_SVG = ('<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" focusable="false"><path d="M20.45 20.45h-3.55v-5.57c0-1.33-.03-3.04-1.85-3.04-1.86 0-2.14 1.45-2.14 2.94v5.67H9.35V9h3.41v1.56h.05c.48-.9 1.64-1.85 3.37-1.85 3.6 0 4.27 2.37 4.27 5.46v6.28zM5.34 7.43a2.06 2.06 0 1 1 0-4.13 2.06 2.06 0 0 1 0 4.13zM7.12 20.45H3.56V9h3.56v11.45zM22.22 0H1.77C.79 0 0 .77 0 1.73v20.54C0 23.23.79 24 1.77 24h20.45c.98 0 1.78-.77 1.78-1.73V1.73C24 .77 23.2 0 22.22 0z"/></svg>')
CHECK = ('<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" '
         'stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="M8 1.5 2.5 3.8v3.6c0 3.3 2.3 6 5.5 7.1 3.2-1.1 5.5-3.8 5.5-7.1V3.8z"/><path d="m5.6 8.1 1.7 1.7 3.2-3.4"/></svg>')
A = f'href="{LI}" target="_blank" rel="author noopener noreferrer"'
BYLINE = (f'<span class="pm-au">By <a {A}>{NAME}</a></span>'
          f'<span class="pm-vet">{CHECK}Vetted by {TEAM}</span>')
CARD = ('<aside class="post-author" aria-label="About the author">'
        '<span class="pa-av" aria-hidden="true">AP</span>'
        '<div class="pa-body">'
        '<p class="pa-k">Written by</p>'
        f'<p class="pa-name"><a {A}>{NAME}</a></p>'
        f'<p class="pa-bio">{NAME} writes the CaseAuthority guides on SEO and marketing for law firms. '
        f'Every article is reviewed by the {TEAM} before it is published.</p>'
        '<div class="pa-foot">'
        f'<span class="pa-vet">{CHECK}Vetted by {TEAM}</span>'
        f'<a class="pa-li" {A} aria-label="{NAME} on LinkedIn">{LI_SVG}<span>LinkedIn</span></a>'
        '</div></div></aside>')
CSS = ('<style id="post-author-css">'
       '.post-meta .pm-au a{color:inherit;text-decoration:underline;text-decoration-thickness:1px;text-underline-offset:3px}'
       '.post-meta .pm-au a:hover{color:var(--color-gray-900,#0E0E0F)}'
       '.post-meta .pm-vet,.post-author .pa-vet{display:inline-flex;align-items:center;gap:6px}'
       '.post-meta .pm-vet svg,.post-author .pa-vet svg{width:16px;height:16px;flex:none;color:var(--acc,#CEAA32)}'
       '.post-author{display:grid;grid-template-columns:56px 1fr;gap:18px;align-items:start;margin:48px 0 32px;'
       'padding:26px 22px;background:var(--color-gray-5,#f3f4f6);border-top:3px solid var(--acc,#CEAA32)}'
       '.post-author .pa-av{width:56px;height:56px;border-radius:50%;background:var(--color-gray-900,#171921);color:#fff;'
       'display:flex;align-items:center;justify-content:center;font-weight:700;font-size:19px;letter-spacing:.02em;position:relative}'
       '.post-author .pa-av:after{content:"";position:absolute;right:1px;bottom:1px;width:13px;height:13px;border-radius:50%;'
       'background:var(--acc,#CEAA32);border:2px solid var(--color-gray-5,#f3f4f6)}'
       '.post-author .pa-body{display:grid;gap:6px;min-width:0}'
       '.post-author p{margin:0}'
       '.post-author .pa-k{font-size:13px;font-weight:700;text-transform:uppercase;letter-spacing:.06em;color:var(--color-gray-600,#666c7a)}'
       '.post-author .pa-name{font-size:22px;line-height:1.2;font-weight:700;letter-spacing:-.02em}'
       '.post-author .pa-name a{color:var(--color-gray-900,#0E0E0F);text-decoration:none;background:linear-gradient(currentColor,currentColor) 0 100%/0 1px no-repeat;transition:background-size .25s ease}'
       '.post-author .pa-name a:hover,.post-author .pa-name a:focus-visible{background-size:100% 1px}'
       '.post-author .pa-bio{font-size:16px;line-height:1.55;color:var(--color-gray-700,#4e5361)}'
       '.post-author .pa-foot{display:flex;flex-wrap:wrap;align-items:center;gap:10px 22px;margin-top:8px;padding-top:12px;'
       'border-top:1px solid var(--color-gray-100,#e6e8eb);font-size:14px;font-weight:600;color:var(--color-gray-800,#353945)}'
       '.post-author .pa-li{display:inline-flex;align-items:center;gap:8px;color:var(--color-gray-800,#353945);text-decoration:none;padding:6px 0}'
       '.post-author .pa-li svg{width:16px;height:16px;display:block}'
       '.post-author .pa-li:hover span{text-decoration:underline;text-underline-offset:3px}'
       '@media (min-width:768px){.post-author{grid-template-columns:72px 1fr;gap:24px;padding:32px 34px}'
       '.post-author .pa-av{width:72px;height:72px;font-size:23px}.post-author .pa-name{font-size:26px}.post-author .pa-bio{font-size:17px}}'
       '</style>')


def person(site):
    return {'@type': 'Person', '@id': site + '#armash-peer', 'name': NAME, 'url': LI, 'sameAs': [LI]}


def team(site):
    return {'@type': 'Organization', 'name': TEAM, 'url': site}


def fix_node(n):
    if isinstance(n, list):
        return any([fix_node(x) for x in n])
    if not isinstance(n, dict):
        return False
    hit = False
    if n.get('@type') == 'BlogPosting':
        url = n.get('url') or (n.get('mainEntityOfPage') if isinstance(n.get('mainEntityOfPage'), str) else '') or ''
        m = re.match(r'https://[^/]+/', str(url) or str(n.get('@id', '')))
        site = m.group(0) if m else 'https://seopersonalinjurylawyer.com/'
        n['author'] = person(site)
        mep = n.get('mainEntityOfPage')
        if isinstance(mep, str):
            n['mainEntityOfPage'] = {'@type': 'WebPage', '@id': mep, 'reviewedBy': team(site)}
        elif isinstance(mep, dict):
            mep['reviewedBy'] = team(site)
        return True
    for v in n.values():
        if isinstance(v, (dict, list)) and fix_node(v):
            hit = True
    return hit


def ld(m):
    try:
        data = json.loads(m.group(2))
    except Exception:
        return m.group(0)
    if not fix_node(data):
        return m.group(0)
    return m.group(1) + json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/') + m.group(3)


def patch(h):
    if 'id="post-author-css"' in h:
        return h
    h = h.replace(OLD_BY, BYLINE, 1)
    a0 = h.find('<article class="post"')
    a1 = h.find('</article>', a0)
    c = h.find('<div class="post-cta', a0, a1)
    at = c if c != -1 else a1
    h = h[:at] + CARD + h[at:]
    h = h.replace('</head>', CSS + '</head>', 1) if '</head>' in h else h.replace('<main', CSS + '<main', 1)
    return re.sub(r'(<script type="application/ld\+json"[^>]*>)(.*?)(</script>)', ld, h, flags=re.S)


def ok(h):
    return (h.count('class="post-author"') == 1 and BYLINE in h and OLD_BY not in h
            and '"@type":"Person"' in h.replace('": "', '":"') and 'id="post-author-css"' in h)


root = sys.argv[1] if len(sys.argv) > 1 else 'public'
done, bad = 0, []
for d, _, fs in os.walk(root):
    for f in fs:
        if not f.endswith('.html'):
            continue
        p = os.path.join(d, f)
        h = open(p, encoding='utf-8').read()
        if '"BlogPosting"' not in h or 'class="post-meta"' not in h:
            continue  # blog index / non-post pages
        if '<article class="post"' not in h or '</article>' not in h:
            bad.append(p); continue
        h = patch(h)
        open(p, 'w', encoding='utf-8').write(h)
        done += 1
        if not ok(h):
            bad.append(p)
if bad or not done:
    print('author_patch: posts not patched:', *bad[:20], sep='\n  '); sys.exit(1)
print(f'author_patch: {done} posts have the {NAME} byline, bio card and Person schema')
