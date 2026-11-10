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
import hashlib as _h
IMG_SRC = IMG_PATH + '?v=' + _h.sha1(base64.b64decode(IMG_B64)).hexdigest()[:10]  # cache-bust when the photo changes
OLD_BY = '<span>By the CaseAuthority team</span>'
LI_SVG = ('<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" focusable="false"><path d="M20.45 20.45h-3.55v-5.57c0-1.33-.03-3.04-1.85-3.04-1.86 0-2.14 1.45-2.14 2.94v5.67H9.35V9h3.41v1.56h.05c.48-.9 1.64-1.85 3.37-1.85 3.6 0 4.27 2.37 4.27 5.46v6.28zM5.34 7.43a2.06 2.06 0 1 1 0-4.13 2.06 2.06 0 0 1 0 4.13zM7.12 20.45H3.56V9h3.56v11.45zM22.22 0H1.77C.79 0 0 .77 0 1.73v20.54C0 23.23.79 24 1.77 24h20.45c.98 0 1.78-.77 1.78-1.73V1.73C24 .77 23.2 0 22.22 0z"/></svg>')
CHECK = ('<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" '
         'stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="M8 1.5 2.5 3.8v3.6c0 3.3 2.3 6 5.5 7.1 3.2-1.1 5.5-3.8 5.5-7.1V3.8z"/><path d="m5.6 8.1 1.7 1.7 3.2-3.4"/></svg>')
A = f'href="{LI}" target="_blank" rel="author noopener noreferrer"'
BYLINE = (f'<span class="pm-au"><img class="pm-av" src="{IMG_SRC}" alt="" width="28" height="28" decoding="async"><span>By <a {A}>{NAME}</a></span></span>'
          f'<span class="pm-vet">{CHECK}Vetted by {TEAM}</span>')
CARD = ('<aside class="post-author" aria-label="About the author">'
        f'<img class="pa-av" src="{IMG_SRC}" alt="{NAME}" width="72" height="72" loading="lazy" decoding="async">'
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
       # Desktop-only hero layout (Mash 2026-11-10): lead/meta/audio use the full content width and the
       # gaps between audio, explainer, summary box and article text are tighter. Mobile is unchanged.
       '@media (min-width:1024px){'
       '.phero .cs-hero{max-width:none}'
       '.phero .cs-hero .phero-lead{max-width:none}'
       '.phero .cs-hero .listen{max-width:none;margin-top:20px}'
       '.phero section.xp{margin-top:28px;padding-top:0;padding-bottom:0}'
       '.phero aside.aio{margin-top:28px}'
       'section.phero{padding-bottom:40px}'
       'section.sec.post-body{padding-top:48px}'
       '}'
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
