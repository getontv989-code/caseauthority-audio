#!/usr/bin/env python3
"""WCAG 2.1 AA fixes for every CaseAuthority site (main sites and blogs), applied to built output.

  python3 a11y_patch.py public

Runs on the built public/ folder of all six projects (PI, criminal, divorce: main + blog), before
the split step. Idempotent. Fails the build (exit 1) if a page with a footer is left without the
Accessibility link, or if the statement page could not be made.

What it does, from the 2026-11-10 audit (axe-core on all 96 live URLs at 1366px and 390px, keyboard
walk, reduced-motion and animation checks):
  1. Explainer controls stay at full opacity (dimmed .xctl made the time text 1.6:1); time text,
     watermark and progress track meet 4.5:1 / 3:1.
  2. Visible keyboard focus ring on text inputs and the audio seek bar (footer email had none).
  3. Decorative looping motion stops within 5 seconds (pricing glow, caret, service-hero bob in
     site.js); prefers-reduced-motion turns all CSS motion off.
  4. The audio seek bar announces "x minutes y seconds of ..." instead of a raw number.
  5. Headings that skip a level (h1 -> h3) get aria-level so the outline has no gaps.
  6. Footer gets an "Accessibility" link next to "Privacy"; /accessibility is generated from the
     site's own privacy page (same header, footer, tags) and added to sitemap.xml.
"""
import os, re, sys

OUT = sys.argv[1].rstrip('/') + '/'
MARK = 'id="a11y-css"'
EMAIL = 'sales@seopersonalinjurylawyer.com'
PHONE = ('(838) 205-8892', 'tel:+18382058892')
DATE = '10 November 2026'

CSS = ('<style id="a11y-css">'
       '.xp .xctl{opacity:1!important}.xtime{color:#5f5f64!important}.xwm{color:#5f5f64!important}'
       '.xseg i{background:#949088!important}'
       'input:not([type=checkbox]):not([type=radio]):focus-visible,textarea:focus-visible,select:focus-visible'
       '{outline:2px solid currentColor!important;outline-offset:2px!important}'
       '.tier.feat::before{animation-duration:5s!important;animation-iteration-count:1!important;animation-fill-mode:forwards!important}'
       '.live-q .caret{animation-iteration-count:5!important}'
       '@media (prefers-reduced-motion:reduce){*,*::before,*::after{animation-duration:.01ms!important;'
       'animation-iteration-count:1!important;animation-delay:0s!important;transition-duration:.01ms!important;'
       'transition-delay:0s!important;scroll-behavior:auto!important}}'
       '</style>')

JS = ('<script id="a11y-js">(function(){'
      'function f(s){s=Math.max(0,Math.round(+s||0));var m=Math.floor(s/60),r=s%60;return m+(m===1?" minute ":" minutes ")+r+(r===1?" second":" seconds")}'
      'function u(r){r.setAttribute("aria-valuetext",f(r.value)+" of "+f(r.max))}'
      '[].forEach.call(document.querySelectorAll(".listen-bar"),function(r){u(r);["input","change","focus"].forEach(function(t){r.addEventListener(t,function(){u(r)})})});'
      '})()</script>')


def fix_headings(h):
    """Give headings that skip a level an aria-level that closes the gap (h1 then h3 -> level 2)."""
    out, pos, prev, shift_from, shift = [], 0, 0, None, 0
    for m in re.finditer(r'<h([1-6])\b([^>]*)>', h):
        lvl = int(m.group(1))
        attrs = m.group(2)
        if 'aria-level' in attrs:
            prev = int(re.search(r'aria-level="(\d)"', attrs).group(1))
            continue
        if shift_from is not None and lvl < shift_from:
            shift_from, shift = None, 0
        eff = lvl - shift
        if prev and eff > prev + 1:
            shift += eff - (prev + 1)
            shift_from = lvl if shift_from is None else shift_from
            eff = prev + 1
        if eff != lvl:
            out.append(h[pos:m.end() - 1] + ' aria-level="%d">' % eff)
            pos = m.end()
        prev = eff
    out.append(h[pos:])
    return ''.join(out)


def footer_link(h):
    if 'href="/accessibility"' in h:
        return h
    return re.sub(r'(<div class="ftr-bot">.*?<a href="/privacy-policy">Privacy</a>)',
                  r'\1 | <a href="/accessibility">Accessibility</a>', h, count=1, flags=re.S)


def statement(domain):
    secs = [
        ('Our commitment',
         '<p>CaseAuthority (Case Authority LLC) wants everyone to be able to use %s, including people who use a screen '
         'reader, a keyboard, zoom, voice control or other assistive technology. We use the Web Content Accessibility '
         'Guidelines (WCAG) 2.1 at Level AA as our target for the whole site, including the blog.</p>' % domain),
        ('Conformance status',
         '<p>We believe this website is <strong>partially conformant</strong> with WCAG 2.1 Level AA. Partially '
         'conformant means that some parts of the content may not fully meet the standard yet. We have not had the site '
         'audited or certified by an outside company, and we do not claim full conformance.</p>'),
        ('What we have done',
         '<ul class="a11y-ul"><li>A "Skip to content" link at the top of every page.</li>'
         '<li>Every link, button, menu and form can be used with a keyboard, with a visible focus outline. Escape closes '
         'the menus.</li>'
         '<li>Text and controls are checked for colour contrast.</li>'
         '<li>Form fields have labels, and form errors are announced.</li>'
         '<li>Pages use headings, landmarks and breadcrumbs so they are easy to move around with a screen reader.</li>'
         '<li>Images have text alternatives, and purely decorative graphics are hidden from screen readers.</li>'
         '<li>If your device is set to reduce motion, animations are turned off. Decorative moving graphics stop on '
         'their own within five seconds.</li>'
         '<li>The "Listen to this article" audio player and the 1-minute animated summaries on blog posts have labelled '
         'play, pause and seek controls that work with a keyboard.</li>'
         '<li>Pages work on small screens down to 320 pixels wide and when zoomed to 200%.</li></ul>'),
        ('Known limitations',
         '<ul class="a11y-ul"><li>The article audio uses a computer-generated voice. It reads the article that is on the same page, so the '
         'article text works as its transcript.</li>'
         '<li>The 1-minute animated summaries are visual summaries of the article. Everything they show is also in the '
         'article text on the same page.</li>'
         '<li>Some tools we use come from other companies, such as Google Tag Manager, Google Analytics and links to '
         'LinkedIn. We do not control how those work.</li></ul>'),
        ('How we test',
         '<p>We test the site ourselves. We run automated checks with axe-core on every page at desktop and mobile '
         'sizes, walk through pages with only a keyboard, and check the site with reduced motion turned on. The last '
         'check was on %s.</p>' % DATE),
        ('Feedback and help',
         '<p>If something on this site is hard to use, or you need any content in another format, please tell us. '
         'Email <a class="in" href="mailto:%s">%s</a> or call <a class="in" href="%s">%s</a>. Let us know the page '
         'address and what went wrong. We read every message, will reply, and will work on a fix.</p>'
         % (EMAIL, EMAIL, PHONE[1], PHONE[0])),
        ('About this statement',
         '<p>This statement was prepared on %s and last reviewed on %s. We will update it as we make changes to the '
         'site.</p>' % (DATE, DATE)),
    ]
    return secs


def make_page(domain):
    src = OUT + 'privacy-policy.html'
    if not os.path.isfile(src):
        sys.exit('a11y_patch: no privacy-policy.html to base the statement on')
    h = open(src, encoding='utf-8').read()
    base = 'https://' + domain
    url = base + '/accessibility'
    title = 'Accessibility Statement | CaseAuthority'
    desc = ('How CaseAuthority makes %s usable for everyone, our WCAG 2.1 AA target, known limitations and how to '
            'report a problem.' % domain)
    h = re.sub(r'<title>.*?</title>', '<title>%s</title>' % title, h, count=1, flags=re.S)
    for attr in ('name="description"', 'property="og:description"', 'name="twitter:description"'):
        h = re.sub(r'(<meta %s content=")[^"]*(")' % re.escape(attr), lambda m: m.group(1) + desc + m.group(2), h)
    for attr in ('property="og:title"', 'name="twitter:title"'):
        h = re.sub(r'(<meta %s content=")[^"]*(")' % re.escape(attr), lambda m: m.group(1) + title + m.group(2), h)
    h = h.replace(base + '/privacy-policy', url)
    ld = ('<script type="application/ld+json">{"@context":"https://schema.org","@graph":['
          '{"@type":"WebPage","@id":"%s#webpage","url":"%s","name":"Accessibility Statement","description":"%s",'
          '"dateModified":"2026-11-10","isPartOf":{"@type":"WebSite","url":"%s/","name":"CaseAuthority"},'
          '"publisher":{"@type":"Organization","name":"CaseAuthority","legalName":"Case Authority LLC","url":"%s/"}},'
          '{"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":"%s/"},'
          '{"@type":"ListItem","position":2,"name":"Accessibility","item":"%s"}]}]}</script>'
          % (url, url, desc, base, base, base, url))
    h = re.sub(r'<script type="application/ld\+json">.*?</script>', '', h, flags=re.S)
    h = h.replace('</head>', ld + '<style>.a11y-ul{margin:12px 0 0;padding-left:1.2em;display:grid;gap:8px;list-style:disc}.a11y-ul li{font-size:18px!important;line-height:1.6!important;letter-spacing:-.01em;color:var(--color-gray-800)!important}@media (min-width:1250px){.prose .a11y-ul li{font-size:20px!important}}@media (max-width:767px){.prose .a11y-ul li{font-size:17px!important}}</style></head>', 1)

    m = re.search(r'(<main\b[^>]*>)(.*?)(</main>)', h, re.S)
    inner = m.group(2)
    split = re.search(r'<script>\(function\(h\).*?</script>', inner, re.S)
    split = split.group(0) if split else ''
    crumbs = ('<nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a><span aria-hidden="true">/</span>'
              '<span aria-current="page">Accessibility statement</span></nav>')
    secs = statement(domain)
    if 'pp-hero' in inner:  # personal injury site layout
        toc = ''.join('<a href="#a11y-%d">%s</a>' % (i, t) for i, (t, _) in enumerate(secs))
        body = ''.join('<section class="pp-sec" id="a11y-%d"><h2 class="pp-h">%s</h2><div class="pp-body">%s</div></section>'
                       % (i, t, b) for i, (t, b) in enumerate(secs))
        new = ('\n  <section class="phero pp-hero" data-tint="#ffffff">\n    <div class="wrap">\n      ' + crumbs +
               '\n      <h1 class="t-h1">Accessibility statement</h1>' + split +
               '\n      <p class="pp-meta">Last reviewed %s · Report a problem: <a class="in" href="mailto:%s">%s</a></p>'
               % (DATE, EMAIL, EMAIL) +
               '\n      <aside class="answer" aria-label="Our commitment"><p class="answer-k"><i aria-hidden="true"></i>'
               'Our commitment</p><p class="answer-t">We want this website to work for everyone. We are working toward '
               'WCAG 2.1 Level AA and fix problems as soon as we find them.</p></aside>\n    </div>\n  </section>'
               '\n  <section class="sec pp-wrap" data-tint="#ffffff">\n    <div class="wrap pp-grid">\n      '
               '<nav class="pp-toc" aria-label="On this page"><p class="pp-toc-h">On this page</p>' + toc + '</nav>\n      '
               '<div class="pp-main">' + body + '</div>\n    </div>\n  </section>\n')
    else:  # sister site layout
        toc = ''.join('<a href="#a11y-%d">%s</a>' % (i, t) for i, (t, _) in enumerate(secs))
        body = ''.join('<h2 class="t-h3" id="a11y-%d" style="margin-top:32px">%s</h2>%s' % (i, t, b)
                       for i, (t, b) in enumerate(secs))
        new = ('\n  <section class="phero" data-tint="#ffffff">\n    <div class="wrap">\n      ' + crumbs +
               '\n      <div class="cs-hero"><h1 class="t-h1">Accessibility statement</h1>' + split +
               '<p class="t-lead phero-lead">We want this website to work for everyone. We are working toward WCAG 2.1 '
               'Level AA. Last reviewed %s.</p></div>\n    </div>\n  </section>' % DATE +
               '\n  <section class="sec" data-tint="#ffffff"><div class="wrap"><div class="sec-prose">'
               '<nav class="t-small" aria-label="On this page" style="display:grid;gap:8px;align-content:start">' + toc +
               '</nav><div class="prose">' + body + '</div></div></div></section>\n')
    h = h[:m.start(2)] + new + h[m.end(2):]
    open(OUT + 'accessibility.html', 'w', encoding='utf-8').write(h)

    sm = OUT + 'sitemap.xml'
    s = open(sm, encoding='utf-8').read()
    if base + '/accessibility</loc>' not in s:
        b = re.search(r'<url>(?:(?!</url>).)*?<loc>%s/privacy-policy</loc>.*?</url>' % re.escape(base), s, re.S)
        if not b:
            sys.exit('a11y_patch: privacy-policy not in sitemap.xml')
        ls = s.rfind('\n', 0, b.start()) + 1
        indent = s[ls:b.start()] if not s[ls:b.start()].strip() else ''
        add = b.group(0).replace(base + '/privacy-policy', base + '/accessibility')
        s = s[:b.end()] + ('\n' + indent if indent or s[b.end():b.end() + 1] == '\n' else '') + add + s[b.end():]
        open(sm, 'w', encoding='utf-8').write(s)


def patch_sitejs():
    p = OUT + 'site.js'
    if not os.path.isfile(p):
        return
    s = open(p, encoding='utf-8').read()
    t = (s.replace("gsap.to('.ha-pin',{y:-10,duration:2.6,ease:'sine.inOut',yoyo:true,repeat:-1})",
                   "gsap.to('.ha-pin',{y:-10,duration:2.2,ease:'sine.inOut',yoyo:true,repeat:1})")
          .replace("gsap.to('.ha-orb',{y:-8,duration:3.2,ease:'sine.inOut',yoyo:true,repeat:-1})",
                   "gsap.to('.ha-orb',{y:-8,duration:2.3,ease:'sine.inOut',yoyo:true,repeat:1})")
          .replace("duration:2.4+i*.4,ease:'sine.inOut',yoyo:true,repeat:-1",
                   "duration:2+i*.1,ease:'sine.inOut',yoyo:true,repeat:1"))
    if 'repeat:-1' in t:
        sys.exit('a11y_patch: site.js still has an endless animation')
    if t != s:
        open(p, 'w', encoding='utf-8').write(t)


def main():
    idx = open(OUT + 'index.html', encoding='utf-8').read() if os.path.isfile(OUT + 'index.html') else ''
    dom = re.search(r'<link rel="canonical" href="https://([^/"]+)', idx)
    if not dom:
        sys.exit('a11y_patch: cannot read the site domain from index.html')
    domain = dom.group(1)
    if not os.path.isfile(OUT + 'accessibility.html'):
        make_page(domain)
    patch_sitejs()
    n = bad = 0
    for root, _, files in os.walk(OUT):
        for f in files:
            if not f.endswith('.html'):
                continue
            p = os.path.join(root, f)
            h = open(p, encoding='utf-8').read()
            o = h
            if MARK not in h:
                # some minified pages (PI home) omit </head> and </body>
                if '</head>' in h:
                    h = h.replace('</head>', CSS + '</head>', 1)
                else:
                    for tag in ('<body', '<header', '<main'):
                        if tag in h:
                            h = h.replace(tag, CSS + tag, 1)
                            break
            if 'id="a11y-js"' not in h:
                h = h.replace('</body>', JS + '</body>', 1) if '</body>' in h else h.rstrip('\n') + JS + '\n'
            if MARK not in h or 'id="a11y-js"' not in h:
                print('a11y_patch: could not add CSS/JS to', p)
                bad += 1
            h = fix_headings(h)
            h = footer_link(h)
            if '</footer>' in h and 'href="/accessibility"' not in h:
                print('a11y_patch: no Accessibility footer link in', p)
                bad += 1
            if h != o:
                open(p, 'w', encoding='utf-8').write(h)
                n += 1
    if bad:
        sys.exit(1)
    print('a11y_patch: %s, %d pages patched' % (domain, n))


main()
