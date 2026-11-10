#!/usr/bin/env python3
"""Author byline + bio card + Person schema on every blog post (all CaseAuthority blogs).
Author: Armash Peer (LinkedIn), vetted by the CaseAuthority Team.
Runs on built output, so every current and future post gets it with no per-post field.
Usage: author_patch.py [public]. Fails the build if any BlogPosting page is left unpatched."""
import base64, json, os, re, sys

NAME = 'Armash Peer'
LI = 'https://www.linkedin.com/in/mohamed-armash/'
TEAM = 'CaseAuthority Team'
IMG_PATH = '/blog/author/armash-peer.webp'
IMG_B64 = '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'
OLD_BY = '<span>By the CaseAuthority team</span>'
LI_SVG = ('<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" focusable="false"><path d="M20.45 20.45h-3.55v-5.57c0-1.33-.03-3.04-1.85-3.04-1.86 0-2.14 1.45-2.14 2.94v5.67H9.35V9h3.41v1.56h.05c.48-.9 1.64-1.85 3.37-1.85 3.6 0 4.27 2.37 4.27 5.46v6.28zM5.34 7.43a2.06 2.06 0 1 1 0-4.13 2.06 2.06 0 0 1 0 4.13zM7.12 20.45H3.56V9h3.56v11.45zM22.22 0H1.77C.79 0 0 .77 0 1.73v20.54C0 23.23.79 24 1.77 24h20.45c.98 0 1.78-.77 1.78-1.73V1.73C24 .77 23.2 0 22.22 0z"/></svg>')
CHECK = ('<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" '
         'stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="M8 1.5 2.5 3.8v3.6c0 3.3 2.3 6 5.5 7.1 3.2-1.1 5.5-3.8 5.5-7.1V3.8z"/><path d="m5.6 8.1 1.7 1.7 3.2-3.4"/></svg>')
A = f'href="{LI}" target="_blank" rel="author noopener noreferrer"'
BYLINE = (f'<span class="pm-au"><img class="pm-av" src="{IMG_PATH}" alt="" width="28" height="28" decoding="async"><span>By <a {A}>{NAME}</a></span></span>'
          f'<span class="pm-vet">{CHECK}Vetted by {TEAM}</span>')
CARD = ('<aside class="post-author" aria-label="About the author">'
        f'<img class="pa-av" src="{IMG_PATH}" alt="{NAME}" width="72" height="72" loading="lazy" decoding="async">'
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
       '.post-meta .pm-au{display:inline-flex;align-items:center;gap:8px}'
       '.post-meta .pm-av{width:28px;height:28px;border-radius:50%;object-fit:cover;display:block;background:var(--color-gray-100,#e6e8eb)}'
       '.post-meta .pm-vet,.post-author .pa-vet{display:inline-flex;align-items:center;gap:6px}'
       '.post-meta .pm-vet svg,.post-author .pa-vet svg{width:16px;height:16px;flex:none;color:var(--acc,#CEAA32)}'
       '.post-author{display:grid;grid-template-columns:56px 1fr;gap:18px;align-items:start;margin:48px 0 32px;'
       'padding:26px 22px;background:var(--color-gray-5,#f3f4f6);border-top:3px solid var(--acc,#CEAA32)}'
       '.post-author .pa-av{width:56px;height:56px;border-radius:50%;object-fit:cover;display:block;background:var(--color-gray-100,#e6e8eb);'
       'box-shadow:0 0 0 3px var(--color-gray-5,#f3f4f6),0 0 0 4px var(--acc,#CEAA32)}'
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
       '.post-author .pa-av{width:72px;height:72px}.post-author .pa-name{font-size:26px}.post-author .pa-bio{font-size:17px}}'
       '</style>')


def person(site):
    return {'@type': 'Person', '@id': site + '#armash-peer', 'name': NAME, 'url': LI, 'sameAs': [LI],
            'image': site.rstrip('/') + IMG_PATH}


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
        return h  # already patched
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
img = os.path.join(root, IMG_PATH.lstrip('/'))
os.makedirs(os.path.dirname(img), exist_ok=True)
open(img, 'wb').write(base64.b64decode(IMG_B64))
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
