#!/usr/bin/env python3
"""External source links on every blog post (all CaseAuthority blogs).
Reads a JSON map {slug: {"edits": [{"old","new"}], "links": [{"text","url","title"}]}}.
- edits: small wording fixes, applied to every occurrence in the page (article, FAQ, schema).
- links: the first occurrence of "text" inside <article class="post"> is wrapped in an external link,
  and every linked source is listed in a short "Sources" block at the end of the article.
Fails the build if an edit or link text is not found, or if any post has no sources entry
(every new post needs about 3 verified external sources in the map before it can publish).
Usage: sources_patch.py public sources.json"""
import html, json, os, re, sys

root, mp = sys.argv[1], json.load(open(sys.argv[2], encoding='utf-8'))
CSS = ('<style id="post-sources-css">'
       '.post a.src{text-decoration:underline;text-decoration-color:var(--acc,#CEAA32);text-underline-offset:3px}'
       '.post-sources{margin-top:40px;padding-top:20px;border-top:1px solid var(--color-gray-100,#e6e8eb)}'
       '.post-sources h2{font-size:20px;margin:0 0 10px}'
       '.post-sources ol{margin:0;padding-left:20px;font-size:15px;line-height:1.55;color:var(--color-gray-700,#4e5361)}'
       '.post-sources li{margin:4px 0}.post-sources a{overflow-wrap:anywhere}'
       '</style>')


def slug_of(h):
    m = re.search(r'<link rel="canonical" href="([^"]+)"', h)
    return m.group(1).rstrip('/').rsplit('/', 1)[-1] if m else None


def outside_tags(seg, text):
    """index of text in seg where it is not inside a tag or an existing <a>."""
    i = 0
    while True:
        i = seg.find(text, i)
        if i < 0:
            return -1
        before = seg[:i]
        in_tag = before.rfind('<') > before.rfind('>')
        in_a = before.rfind('<a ') > before.rfind('</a>')
        if not in_tag and not in_a:
            return i
        i += 1


def patch(h, cfg, p, errs):
    for e in cfg.get('edits', []):
        if e['old'] not in h:
            errs.append(f'{p}: edit text not found: {e["old"][:60]}'); continue
        h = h.replace(e['old'], e['new'])
    a0 = h.find('<article class="post"'); a1 = h.find('</article>', a0)
    art = h[a0:a1]
    srcs = []
    for l in cfg['links']:
        i = outside_tags(art, l['text'])
        if i < 0:
            errs.append(f'{p}: link text not found: {l["text"][:60]}'); continue
        a = (f'<a class="in src" href="{html.escape(l["url"])}" target="_blank" rel="noopener">'
             f'{l["text"]}</a>')
        art = art[:i] + a + art[i + len(l['text']):]
        if l['url'] not in [s['url'] for s in srcs]:
            srcs.append(l)
    items = ''.join(f'<li><a class="in src" href="{html.escape(s["url"])}" target="_blank" rel="noopener">'
                    f'{html.escape(s["title"])}</a></li>' for s in srcs)
    block = f'<div class="post-sources" id="sources"><h2>Sources</h2><ol>{items}</ol></div>'
    at = art.find('<aside class="post-author"')
    if at < 0:
        at = art.find('<div class="post-cta')
    if at < 0:
        at = len(art)
    art = art[:at] + block + art[at:]
    h = h[:a0] + art + h[a1:]
    return h.replace('</head>', CSS + '</head>', 1)


done, errs, seen = 0, [], set()
for d, _, fs in os.walk(root):
    for f in fs:
        if not f.endswith('.html'):
            continue
        p = os.path.join(d, f)
        h = open(p, encoding='utf-8').read()
        if '"BlogPosting"' not in h or '<article class="post"' not in h:
            continue
        if 'id="post-sources-css"' in h:
            continue
        s = slug_of(h)
        if s not in mp:
            errs.append(f'{p}: no sources entry for "{s}" (add about 3 verified external sources)'); continue
        seen.add(s)
        n = len(errs)
        h = patch(h, mp[s], p, errs)
        if len(errs) == n:
            open(p, 'w', encoding='utf-8').write(h); done += 1
if errs or not done:
    print('sources_patch failed:', *errs[:40], sep='\n  '); sys.exit(1)
print(f'sources_patch: {done} posts have external source links ({len(seen)} slugs)')
