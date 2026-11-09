#!/usr/bin/env python3
"""Split a built sister site (public/) into the main project or the blog project.
  python3 sister_split.py <brand> main  -> everything except /blog; sitemap.xml becomes an index of
                                           sitemap-pages.xml + /blog/sitemap.xml (served by the blog project)
  python3 sister_split.py <brand> blog  -> only /blog/** and 404.html; the hashed CSS/JS the blog pages use are
                                           copied to /blog/_a/ so the blog never depends on the main build's file names
Fails (exit 1) if the result is missing anything it needs.
"""
import json, os, re, shutil, sys

brand, mode = sys.argv[1], sys.argv[2]
OUT = 'public/'
B = 'https://' + json.load(open('brands/%s/brand.json' % brand))['domain']
sm = open(OUT + 'sitemap.xml').read()
locs = re.findall(r'<loc>([^<]*)</loc>', sm)
is_blog = lambda u: u == B + '/blog' or u.startswith(B + '/blog/')
urlset = lambda us: ('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                     + ''.join('  <url><loc>%s</loc></url>\n' % u for u in us) + '</urlset>\n')
blog_urls = [u for u in locs if is_blog(u)]
if not blog_urls:
    sys.exit('sister_split: no blog URLs in sitemap')

if mode == 'main':
    shutil.rmtree(OUT + 'blog', ignore_errors=True)
    open(OUT + 'sitemap-pages.xml', 'w').write(urlset([u for u in locs if not is_blog(u)]))
    open(OUT + 'sitemap.xml', 'w').write(
        '<?xml version="1.0" encoding="UTF-8"?>\n<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        '  <sitemap><loc>%s/sitemap-pages.xml</loc></sitemap>\n  <sitemap><loc>%s/blog/sitemap.xml</loc></sitemap>\n</sitemapindex>\n' % (B, B))
    if os.path.exists(OUT + 'blog') or not os.path.exists(OUT + 'index.html'):
        sys.exit('sister_split: main output wrong')
elif mode == 'blog':
    keep = {'blog', '404.html'}
    assets = set()
    for root, _, files in os.walk(OUT + 'blog'):
        for f in files:
            if f.endswith('.html'):
                assets |= set(re.findall(r'(?:href|src)="/((?:site|home)\.[0-9a-f]{10}\.(?:css|js))"', open(os.path.join(root, f), encoding='utf-8').read()))
    assets |= set(re.findall(r'(?:href|src)="/((?:site|home)\.[0-9a-f]{10}\.(?:css|js))"', open(OUT + '404.html', encoding='utf-8').read()))
    if not assets:
        sys.exit('sister_split: no assets found')
    os.makedirs(OUT + 'blog/_a', exist_ok=True)
    for a in assets:
        shutil.copy(OUT + a, OUT + 'blog/_a/' + a)
    for name in os.listdir(OUT):
        if name not in keep:
            p = OUT + name
            shutil.rmtree(p) if os.path.isdir(p) else os.remove(p)
    pages = []
    for root, _, files in os.walk(OUT):
        for f in files:
            if f.endswith('.html'):
                p = os.path.join(root, f)
                h = open(p, encoding='utf-8').read()
                for a in assets:
                    h = h.replace('="/%s"' % a, '="/blog/_a/%s"' % a)
                open(p, 'w', encoding='utf-8').write(h)
                pages.append(p)
    open(OUT + 'blog/sitemap.xml', 'w').write(urlset(blog_urls))
    for u in blog_urls:
        p = OUT + ('blog/index.html' if u == B + '/blog' else u[len(B) + 1:] + '.html')
        if not os.path.exists(p):
            sys.exit('sister_split: missing page for ' + u)
        h = open(p, encoding='utf-8').read()
        if re.search(r'(?:href|src)="/(?:site|home)\.[0-9a-f]{10}\.', h) or '<link rel="canonical" href="%s"' % u not in h:
            sys.exit('sister_split: bad asset path or canonical in ' + p)
else:
    sys.exit('usage: sister_split.py <brand> main|blog')
print('sister_split: %s %s done, %d blog URLs' % (brand, mode, len(blog_urls)))
