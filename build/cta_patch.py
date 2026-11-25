#!/usr/bin/env python3
"""Lead CTAs for every blog post (all CaseAuthority blogs).

usage: cta_patch.py <public dir> <brand: pi|criminal|divorce|estate>

Adds to each post page (pages with <article class="post">):
  1. Early in-article audit form (email + optional website) after section 1 or 2.
     Posts to /api/contact, so the lead email carries the article URL as Page.
  2. Mid-article "done for you" CTA at about 55% of the sections.
  3. Sticky mobile bar (under 1000px) that appears once the reader is past the
     early CTA, hides while another CTA or the footer form is on screen, and can
     be dismissed for the session.
  4. Desktop: the sidebar contents list scrolls inside itself so the sidebar
     CTA always stays on screen.
  5. Every /sales link in the article and sidebar gets ?from=<slug>&cta=<spot>,
     plus cta_click / generate_lead events in dataLayer (and gtag when present).
Fails the build if any post does not get all of it. Idempotent.
"""
import sys, os, re, html

PUB, BRAND = sys.argv[1], sys.argv[2]
NICHE = {'pi': 'personal injury', 'criminal': 'criminal defense', 'divorce': 'family law', 'estate': 'estate planning'}[BRAND]
PHONE_T, PHONE = '+18382058892', '(838) 205-8892'
MARK = 'data-ca-cta'

ARROW = '<svg width="14" height="14" viewBox="0 0 14 14" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true" focusable="false"><path d="M1 7h12M8 2l5 5-5 5"/></svg>'
TICK = '<svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true" focusable="false"><path d="M3 8.5l3 3 7-7"/></svg>'

CSS = """<style id="ca-cta-css">
.cax{margin:48px 0;padding:28px 26px 26px;border:1px solid var(--color-gray-200,#e4e4e7);border-top:3px solid var(--ca-black,#0E0E0F);background:#fff;box-shadow:0 30px 60px -34px rgba(14,14,15,.22);display:grid;gap:12px}
.cax.cax-mid{background:var(--ca-cream,#F5F1EA);border-color:#e6dfd2;border-top-color:var(--ca-gold,#CEAA32);box-shadow:none}
.cax .cax-k{margin:0;font-size:13px;font-weight:700;text-transform:uppercase;letter-spacing:.14em;color:#5c5c63}
.cax h3{margin:0;font-size:24px;line-height:1.2;letter-spacing:-.02em;font-weight:500;color:var(--ca-black,#0E0E0F)}
.cax p{margin:0;font-size:16px;line-height:1.55;color:#45454b}
.cax ul{list-style:none;margin:2px 0 0;padding:0;display:grid;gap:8px}
.cax li{display:flex;gap:10px;align-items:flex-start;font-size:16px;line-height:1.45;color:#2b2b30;margin:0}
.cax li svg{flex:none;margin-top:3px;color:#7a5f12}
.cax .cax-row{display:flex;flex-wrap:wrap;gap:14px 20px;align-items:center;margin-top:6px}
.cax .pill{background:var(--ca-black,#0E0E0F);color:#fff;text-decoration:none}
.cax .pill:hover{background:#2b2b30;color:#fff}
.cax .cax-tel{font-size:15px;color:var(--ca-black,#0E0E0F);text-decoration:underline;text-underline-offset:3px}
.cax .cax-fine{font-size:13px;color:#5c5c63}
.cax form{display:grid;gap:10px;margin-top:4px}
.cax .cax-f{display:grid;gap:10px;grid-template-columns:1fr}
.cax label{display:grid;gap:6px;font-size:14px;font-weight:600;color:#2b2b30}
.cax label span span{font-weight:400;color:#5c5c63}
.cax input{font:inherit;font-size:16px;padding:13px 14px;border:1px solid #8a8a92;border-radius:10px;background:#fff;color:#0E0E0F;width:100%;box-sizing:border-box}
.cax input[aria-invalid=true]{border-color:#b42318}
.cax button.pill{justify-content:center;width:100%}
.cax .cax-ok{color:#1d6b38;font-weight:600}
.cax .cax-err{color:#b42318}
.cax .cax-hp{position:absolute;left:-9999px;width:1px;height:1px;overflow:hidden}
.cax a:focus-visible,.cax input:focus-visible,.cax button:focus-visible,.caxbar a:focus-visible,.caxbar button:focus-visible{outline:3px solid #0E0E0F;outline-offset:2px}
@media (min-width:640px){.cax{padding:32px 32px 30px}.cax .cax-f{grid-template-columns:1fr 1fr}.cax button.pill{width:auto;justify-self:start}}
.caxbar{position:fixed;left:0;right:0;bottom:0;z-index:60;display:none;align-items:center;gap:12px;padding:10px 12px calc(10px + env(safe-area-inset-bottom)) 16px;background:#fff;border-top:1px solid var(--color-gray-200,#e4e4e7);box-shadow:0 -12px 30px -18px rgba(14,14,15,.35);transform:translateY(110%);transition:transform .25s ease}
.caxbar.on{transform:none}
.caxbar .caxbar-t{flex:1;min-width:0;margin:0;font-size:14px;line-height:1.3;color:#2b2b30}
.caxbar .caxbar-t b{display:block;font-size:15px;font-weight:600;color:#0E0E0F}
.caxbar .pill{flex:none;padding:12px 16px;font-size:15px;background:var(--ca-black,#0E0E0F);color:#fff;text-decoration:none}
.caxbar .caxbar-x{flex:none;width:44px;height:44px;display:grid;place-items:center;border:0;background:transparent;color:#45454b;cursor:pointer;border-radius:50%;padding:0}
@media (max-width:999px){.caxbar{display:flex}}
@media (prefers-reduced-motion:reduce){.caxbar{transition:none}}
@media (min-width:1000px){.post-aside .post-toc{max-height:max(140px,calc(100vh - 570px));overflow-y:auto;overscroll-behavior:contain}}
</style>"""

JS = """<script id="ca-cta-js">(function(){var d=document,w=window,dl=w.dataLayer=w.dataLayer||[],slug=(location.pathname.split('/').filter(Boolean).pop()||'blog');
function ev(n,p){var o={event:n,page_slug:slug};for(var k in p)o[k]=p[k];dl.push(o);if(typeof w.gtag==='function'){var g={page_slug:slug};for(var k2 in p)g[k2]=p[k2];w.gtag('event',n,g)}}
d.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('[data-cta]');if(a)ev('cta_click',{cta_position:a.getAttribute('data-cta'),link_url:a.getAttribute('href')||''})});
var f=d.getElementById('caxForm');if(f)f.addEventListener('submit',function(e){e.preventDefault();var em=f.elements.email,ws=f.elements.website,ok=f.querySelector('.cax-ok'),er=f.querySelector('.cax-err'),b=f.querySelector('button');var v=em.value.trim()&&em.checkValidity();em.setAttribute('aria-invalid',String(!v));if(!v){er.textContent='Enter your work email, e.g. partner@yourfirm.com';er.hidden=false;ok.hidden=true;em.focus();return}
b.disabled=true;f.setAttribute('aria-busy','true');fetch('/api/contact',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({form:'Blog audit (in-article)',email:em.value.trim(),website:ws.value.trim(),message:'Requested from the article: '+slug,company_site:f.elements.company_site.value})}).then(function(r){if(!r.ok)throw 0;ok.hidden=false;er.hidden=true;f.reset();ev('generate_lead',{form_location:'blog_inline'})}).catch(function(){er.textContent='Sorry, that did not send. Please try again, or email sales@seopersonalinjurylawyer.com.';er.hidden=false;ok.hidden=true}).then(function(){b.disabled=false;f.removeAttribute('aria-busy')})});
var bar=d.getElementById('caxBar');if(!bar||!('IntersectionObserver' in w))return;var off=false;try{off=sessionStorage.getItem('caxBarOff')==='1'}catch(_){}if(off){bar.remove();return}
var first=d.querySelector('.cax'),seen=0,past=false;function upd(){var on=past&&seen===0;bar.classList.toggle('on',on);bar.setAttribute('aria-hidden',String(!on));[].forEach.call(bar.querySelectorAll('a,button'),function(x){x.tabIndex=on?0:-1})}
var zones=[].slice.call(d.querySelectorAll('.cax,.post-cta,#auditForm,.ftr-main'));var vis=new Set();var io=new IntersectionObserver(function(es){es.forEach(function(x){if(x.isIntersecting)vis.add(x.target);else vis.delete(x.target)});seen=vis.size;upd()});zones.forEach(function(z){io.observe(z)});
function sc(){var r=first?first.getBoundingClientRect().bottom:0;past=first?r<0:w.scrollY>600;upd()}w.addEventListener('scroll',sc,{passive:true});sc();
bar.querySelector('.caxbar-x').addEventListener('click',function(){bar.remove();try{sessionStorage.setItem('caxBarOff','1')}catch(_){}ev('cta_dismiss',{cta_position:'sticky'})})})();</script>"""


def early(slug):
    return (f'<aside class="cax cax-early" {MARK}="early" aria-labelledby="caxH1">'
            f'<p class="cax-k">Free SEO audit</p>'
            f'<h3 id="caxH1">Is Your {NICHE.title()} Firm Showing Up When Clients Search?</h3>'
            f'<p>Tell us where to send it. A senior strategist will check where your site ranks on Google and in AI answers, what is holding it back, and the first fixes worth making.</p>'
            f'<form id="caxForm" action="/api/contact" method="post" novalidate>'
            f'<div class="cax-hp" aria-hidden="true"><label>Leave this empty<input name="company_site" tabindex="-1" autocomplete="off"></label></div>'
            f'<div class="cax-f"><label for="caxEmail">Work email<input id="caxEmail" name="email" type="email" autocomplete="email" placeholder="partner@yourfirm.com" required aria-describedby="caxErr"></label>'
            f'<label for="caxSite"><span class="cax-l">Firm website <span>(optional)</span></span><input id="caxSite" name="website" type="text" inputmode="url" autocomplete="url" placeholder="yourfirm.com"></label></div>'
            f'<button class="pill" type="submit" data-cta="early-form">Send my free audit {ARROW}</button>'
            f'<p class="cax-ok" role="status" aria-live="polite" hidden>Thanks! A senior strategist will reply within one business day.</p>'
            f'<p class="cax-err" id="caxErr" role="alert" hidden></p>'
            f'<p class="cax-fine">Free for qualified law firms. Confidential. No sales pressure.</p>'
            f'</form></aside>')


def mid(slug):
    return (f'<aside class="cax cax-mid" {MARK}="mid" aria-labelledby="caxH2">'
            f'<p class="cax-k">Done for you</p>'
            f'<h3 id="caxH2">Want This Handled for Your Firm?</h3>'
            f'<p>Our team puts SEO like this into practice for {NICHE} firms. Start with a free audit and you get:</p>'
            f'<ul><li>{TICK}A clear picture of where your firm ranks today</li>'
            f'<li>{TICK}The gaps your competitors are using to win the click</li>'
            f'<li>{TICK}A plan you can act on, even if you never hire us</li></ul>'
            f'<div class="cax-row"><a href="/sales?from={slug}&amp;cta=mid" class="pill" data-cta="mid">Get my free SEO plan {ARROW}</a>'
            f'<a href="tel:{PHONE_T}" class="cax-tel" data-cta="mid-call">Or call {PHONE}</a></div>'
            f'</aside>')


def bar(slug):
    return (f'<div class="caxbar" id="caxBar" {MARK}="sticky" role="region" aria-label="Free SEO audit" aria-hidden="true">'
            f'<p class="caxbar-t"><b>Free {NICHE} SEO audit</b>Reply within one business day</p>'
            f'<a href="/sales?from={slug}&amp;cta=sticky" class="pill" data-cta="sticky" tabindex="-1">Get my audit</a>'
            f'<button class="caxbar-x" type="button" aria-label="Dismiss the free audit bar" tabindex="-1"><svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true" focusable="false"><path d="M3 3l10 10M13 3L3 13"/></svg></button>'
            f'</div>')


def tag_sales(seg, slug, spot):
    """Add ?from=&cta= to plain /sales links inside a segment."""
    return re.sub(r'<a href="/sales"( class="([^"]*)")?',
                  lambda m: f'<a href="/sales?from={slug}&amp;cta={spot}"{m.group(1) or ""} data-cta="{spot}"', seg)


def patch(path):
    h = open(path, encoding='utf-8').read()
    if '<article class="post">' not in h:
        return None
    if MARK in h:
        return 'skip'
    slug = os.path.basename(os.path.dirname(path)) if os.path.basename(path) == 'index.html' else os.path.splitext(os.path.basename(path))[0]
    a0 = h.index('<article class="post">')
    a1 = h.index('</article>', a0)
    art = h[a0:a1]
    starts = [m.start() for m in re.finditer(r'<div class="post-sec"', art)]
    n = len(starts)
    if n < 4:
        raise SystemExit(f'cta_patch: {path} has only {n} sections')
    e_after = 2 if n >= 9 else 1
    m_after = max(e_after + 2, round(n * 0.55))
    if m_after >= n:
        m_after = n - 1
    # insert from the back so earlier offsets stay valid
    art = art[:starts[m_after]] + mid(slug) + art[starts[m_after]:]
    art = art[:starts[e_after]] + early(slug) + art[starts[e_after]:]
    art = tag_sales(art, slug, 'end')
    h = h[:a0] + art + h[a1:]
    # sidebar
    s0 = h.find('<aside class="post-aside"')
    if s0 != -1:
        s1 = h.index('</aside>', s0)
        h = h[:s0] + tag_sales(h[s0:s1], slug, 'sidebar') + h[s1:]
    # explainer end card
    h = h.replace('<a class="xcta a-pop" style="--d:1.4s" href="/sales"', f'<a class="xcta a-pop" style="--d:1.4s" href="/sales?from={slug}&amp;cta=explainer"')
    h = h.replace('</head>', CSS + '</head>', 1)
    i = h.rindex('</body>')
    h = h[:i] + bar(slug) + JS + h[i:]
    for need in ('cax-early', 'cax-mid', 'caxBar', 'ca-cta-css', 'ca-cta-js'):
        if h.count(need) < 1:
            raise SystemExit(f'cta_patch: {need} missing in {path}')
    if '—' in early(slug) + mid(slug) + bar(slug):
        raise SystemExit('cta_patch: em dash in CTA copy')
    open(path, 'w', encoding='utf-8').write(h)
    return 'ok'


done = 0
for root, _, files in os.walk(os.path.join(PUB, 'blog')):
    for fn in files:
        if fn.endswith('.html'):
            r = patch(os.path.join(root, fn))
            if r in ('ok', 'skip'):
                done += 1
if done == 0:
    raise SystemExit('cta_patch: no blog posts patched')
print(f'cta_patch: {done} posts ({BRAND})')
