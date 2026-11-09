# explainer_patch.py: adds the CaseAuthority 1-minute animated explainer to each blog post page.
# Bundled from redesign/explainers/{people,explainer,specs}.py. Usage: python3 explainer_patch.py [public]
# Idempotent; exits non-zero if a target page is missing or has an unexpected structure.

# ===== people =====
# Flat animated people for the explainers. Each returns an inline SVG (~1KB).
SK = {'a': '#8d5a3b', 'b': '#f1c7a5', 'c': '#c98e64', 'd': '#e8b48f'}
CAST = {
    # attorney: charcoal suit, gold tie, short hair
    'attorney': dict(skin=SK['a'], hair='#1d1a17', hairstyle='short', top='#2b2b2e', shirt='#ffffff', tie='#CEAA32', pants='#1c1c1e'),
    # client: cream sweater, long hair
    'client': dict(skin=SK['b'], hair='#6b4a2e', hairstyle='long', top='#e9dcc2', shirt=None, tie=None, pants='#5c6470'),
    # intake manager: gold top, bun, headset
    'intake': dict(skin=SK['c'], hair='#2a1f18', hairstyle='bun', top='#CEAA32', shirt=None, tie=None, pants='#2b2b2e', headset=True),
    # partner: grey suit, curly hair
    'partner': dict(skin=SK['d'], hair='#3b2c22', hairstyle='curly', top='#6d6a66', shirt='#fff7e2', tie=None, pants='#2b2b2e'),
}
HAIR = {
    'short': '<path d="M41 47c0-14 9-22 19-22s19 8 19 21c-4-6-10-9-19-9s-15 3-19 10z" fill="{h}"/>',
    'long': '<path d="M40 52c-2-17 8-27 20-27s22 10 20 27v22c-3 2-6 2-8 0V52c-4-5-8-8-12-8s-8 3-12 8v22c-2 2-5 2-8 0z" fill="{h}"/>',
    'bun': '<circle cx="60" cy="24" r="8" fill="{h}"/><path d="M41 49c0-14 9-21 19-21s19 7 19 21c-6-6-12-9-19-9s-13 3-19 9z" fill="{h}"/>',
    'curly': '<g fill="{h}"><circle cx="46" cy="38" r="8"/><circle cx="56" cy="31" r="9"/><circle cx="68" cy="32" r="9"/><circle cx="76" cy="41" r="7"/><circle cx="43" cy="47" r="5"/></g>',
}
POSE = {'stand': -10, 'wave': -150, 'point': -78, 'phone': 158, 'cheer': -165}


def person(who='attorney', pose='stand', flip=False, cls=''):
    c = CAST[who]
    rot = POSE[pose]
    anim = {'wave': ' xp-wave', 'cheer': ' xp-wave'}.get(pose, '')
    tie = f'<path d="M58 80h4l2 22-4 5-4-5z" fill="{c["tie"]}"/>' if c.get('tie') else ''
    shirt = f'<path d="M51 78l9 20 9-20z" fill="{c["shirt"]}"/>' if c.get('shirt') else ''
    hs = '<path d="M40 50c0-14 9-22 20-22s20 8 20 22" fill="none" stroke="#0E0E0F" stroke-width="3"/><rect x="77" y="47" width="6" height="11" rx="3" fill="#0E0E0F"/><path d="M80 58c0 8-6 11-13 11" fill="none" stroke="#0E0E0F" stroke-width="2"/>' if c.get('headset') else ''
    phone = '<rect x="-5" y="50" width="11" height="19" rx="2.5" fill="#0E0E0F"/>' if pose == 'phone' else ''
    hair_back = HAIR[c['hairstyle']].format(h=c['hair']) if c['hairstyle'] == 'long' else ''
    hair_front = '' if c['hairstyle'] == 'long' else HAIR[c['hairstyle']].format(h=c['hair'])
    tf = ' transform="translate(160 0) scale(-1 1)"' if flip else ''
    return (
        f'<svg class="xperson{(" " + cls) if cls else ""}" viewBox="0 0 160 220" aria-hidden="true" focusable="false"><g{tf}><g class="xp-body">'
        f'<rect x="45" y="150" width="13" height="60" rx="6.5" fill="{c["pants"]}"/><rect x="62" y="150" width="13" height="60" rx="6.5" fill="{c["pants"]}"/>'
        f'<ellipse cx="50" cy="210" rx="10" ry="5" fill="#0E0E0F"/><ellipse cx="70" cy="210" rx="10" ry="5" fill="#0E0E0F"/>'
        f'<g transform="rotate(-8 38 86)"><rect x="32" y="82" width="12" height="54" rx="6" fill="{c["top"]}"/><circle cx="38" cy="138" r="6" fill="{c["skin"]}"/></g>'
        f'<path d="M34 96c0-11 7-18 17-18h18c10 0 17 7 17 18v60H34z" fill="{c["top"]}"/>{shirt}{tie}'
        f'<rect x="54" y="64" width="12" height="16" rx="5" fill="{c["skin"]}"/>{hair_back}'
        f'<g class="xp-head"><circle cx="60" cy="50" r="19" fill="{c["skin"]}"/>{hair_front}'
        f'<g class="xp-eyes" fill="#0E0E0F"><circle cx="53" cy="52" r="2"/><circle cx="67" cy="52" r="2"/></g>'
        f'<path class="xp-mouth" d="M55 60q5 4 10 0" fill="none" stroke="#0E0E0F" stroke-width="2" stroke-linecap="round"/>{hs}</g>'
        f'<g class="xp-arm{anim}" style="--r:{rot}deg"><rect x="76" y="82" width="12" height="54" rx="6" fill="{c["top"]}"/><circle cx="82" cy="138" r="6" fill="{c["skin"]}"/>'
        f'<g transform="translate(82 80)">{phone}</g></g>'
        f'</g></g></svg>')


PEOPLE_CSS = r"""
.xperson{display:block;overflow:visible}
.xperson .xp-arm{transform-box:view-box;transform-origin:82px 86px;transform:rotate(var(--r))}
.xperson .xp-eyes{transform-box:fill-box;transform-origin:center}
.xperson .xp-mouth{transform-box:fill-box;transform-origin:center}
.xs.act .xp-body{animation:xBob 2.6s ease-in-out infinite}
.xs.act .xp-eyes{animation:xBlink 3.4s steps(1) infinite}
.xs.act .xp-wave{animation:xWave 1.1s ease-in-out .4s 4}
.xs.act .xtalk .xp-mouth{animation:xTalk .32s ease-in-out 1.2s 12 alternate}
.xs.act .xp-head{animation:xNod 2.6s ease-in-out infinite;transform-box:fill-box;transform-origin:50% 100%}
@keyframes xBob{0%,100%{transform:none}50%{transform:translateY(-2px)}}
@keyframes xBlink{0%,92%,100%{transform:none}94%{transform:scaleY(.1)}}
@keyframes xWave{0%,100%{transform:rotate(var(--r))}50%{transform:rotate(calc(var(--r) + 25deg))}}
@keyframes xTalk{from{transform:none}to{transform:scaleY(2.2)}}
@keyframes xNod{0%,100%{transform:none}50%{transform:rotate(2deg)}}
@media (prefers-reduced-motion:reduce){.xs.act .xperson *{animation:none!important}}
"""

# ===== explainer =====
# CaseAuthority 1-minute animated explainer for blog posts.
# Pure HTML + CSS + a tiny JS player: no video file, no extra network requests.
# Usage: explainer.render(post_dict, spec) -> HTML string to place under the post hero.
from html import escape as E

MARK = '<svg viewBox="0 0 256 256" aria-hidden="true" focusable="false"><path fill="#CEAA32" d="M152 40 H192 V216 H152 V120 L104 216 H64 Z"/></svg>'
CHECK = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12.5l4.2 4.2L19 7" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'
PLAY = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5.5v13l11-6.5z" fill="currentColor"/></svg>'
CROSS = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 7l10 10M17 7L7 17" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"/></svg>'


def _d(i, base=0.0, step=0.18):
    return f'style="--d:{base + i * step:.2f}s"'


# ---------- visual motifs (reusable across every article) ----------
def v_phone(v):
    rows = ''.join(f'<div class="xr a-in" {_d(i, 1.6, .35)}><span>{E(r)}</span><i class="xb a-grow" {_d(i, 1.8, .35)}></i></div>' for i, r in enumerate(v.get('rows', [])))
    return (f'<div class="xv-phone"><div class="xph a-pop" {_d(0, .1)}><i class="xring"></i><i class="xring r2"></i>'
            f'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.6 10.8a15.1 15.1 0 006.6 6.6l2.2-2.2a1 1 0 011-.25 11.4 11.4 0 003.6.57 1 1 0 011 1V20a1 1 0 01-1 1A17 17 0 013 4a1 1 0 011-1h3.5a1 1 0 011 1c0 1.25.2 2.45.57 3.57a1 1 0 01-.25 1z" fill="currentColor"/></svg></div>'
            f'<div class="xcard a-up" {_d(0, 1.1)}><p class="xct">{E(v.get("title", ""))}</p>{rows}</div></div>')


def v_checklist(v):
    rows = ''.join(f'<div class="xr a-in" {_d(i, .5, .55)}><b class="xchk a-pop" {_d(i, .8, .55)}>{CHECK}</b><span>{E(r)}</span></div>' for i, r in enumerate(v['items']))
    return f'<div class="xcard xcl a-up" {_d(0, .1)}><p class="xct">{E(v.get("title", ""))}</p>{rows}</div>'


def v_shrink(v):
    keep = ''.join(f'<div class="xr a-in" {_d(i, .5, .3)}><b class="xchk a-pop" {_d(i, .7, .3)}>{CHECK}</b><span>{E(r)}</span></div>' for i, r in enumerate(v['keep']))
    later = ''.join(f'<i class="xln a-in" {_d(i, 2.2, .12)}></i>' for i in range(v.get('later_rows', 7)))
    return (f'<div class="xv-shrink"><div class="xcard xback a-slide" {_d(0, 2.0)}><p class="xct">{E(v["later"])}</p>{later}</div>'
            f'<div class="xcard xfront a-up" {_d(0, .1)}><p class="xct">{E(v["title"])}</p>{keep}<p class="xtag a-in" {_d(0, 1.6)}>{E(v.get("tag", ""))}</p></div></div>')


def v_sources(v):
    items = v['items']
    mx = max(h for _, h in items)
    bars = ''.join(
        f'<div class="xbar{" top" if h == mx else ""}"><i class="a-rise" style="--h:{h}%;--d:{1.0 + i * .25:.2f}s"></i><span class="a-in" {_d(i, .3, .2)}>{E(n)}</span></div>'
        for i, (n, h) in enumerate(items))
    return (f'<div class="xcard xsrc a-up" {_d(0, .1)}><p class="xct">{E(v["title"])}</p><div class="xbars">{bars}</div>'
            f'<p class="xtag a-in" {_d(0, 2.6)}>{E(v.get("tag", ""))}</p></div>')


def v_race(v):
    (fa, fr), (sa, sr) = v['fast'], v['slow']
    return (f'<div class="xcard xrace a-up" {_d(0, .1)}>'
            f'<div class="xlane"><p>{E(fa)}</p><div class="xtrack"><i class="xdot fast"></i></div><b class="xres win a-pop" style="--d:1.9s">{CHECK}{E(fr)}</b></div>'
            f'<div class="xlane"><p>{E(sa)}</p><div class="xtrack"><i class="xdot slow"></i></div><b class="xres lose a-pop" style="--d:4.6s">{CROSS}{E(sr)}</b></div></div>')


def v_shield(v):
    chips = ''.join(f'<span class="xchip a-pop" {_d(i, 1.8, .35)}>{E(c)}</span>' for i, c in enumerate(v['chips']))
    return ('<div class="xv-shield"><svg class="xsh" viewBox="0 0 120 140" aria-hidden="true">'
            '<path class="a-draw" d="M60 8 L108 26 V66 C108 98 88 120 60 132 C32 120 12 98 12 66 V26 Z" fill="#fff7e2" stroke="#CEAA32" stroke-width="5" stroke-linejoin="round" pathLength="1"/>'
            '<path class="a-draw" style="--d:1s" d="M38 70 L54 86 L84 54" fill="none" stroke="#0E0E0F" stroke-width="8" stroke-linecap="round" stroke-linejoin="round" pathLength="1"/></svg>'
            f'<div class="xchips">{chips}</div></div>')


def v_search(v):
    rows = ''.join(
        f'<div class="xres1{" you" if you else ""} a-in" {_d(i, 1.9, .3)}><b>{E(n)}</b>{"<em>Top result</em>" if you else ""}<i></i></div>'
        for i, (n, you) in enumerate(v['results']))
    return (f'<div class="xcard xsearch a-up" {_d(0, .1)}><div class="xq"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="10.5" cy="10.5" r="6.5" fill="none" stroke="currentColor" stroke-width="2.4"/><path d="M15.5 15.5l5 5" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"/></svg>'
            f'<span class="xtype" style="--n:{len(v["q"])}">{E(v["q"])}</span></div>{rows}</div>')


def v_map(v):
    pins = ''.join(f'<i class="xpin a-drop" style="left:{x}%;top:{y}%;--d:{.5 + i * .3:.2f}s"><b>{i + 1}</b></i>' for i, (x, y) in enumerate([(30, 38), (62, 26), (74, 60)]))
    rows = ''.join(
        f'<div class="xmrow{" you" if i == 0 else ""} a-in" {_d(i, 1.6, .3)}><b>{i + 1}</b><span>{E(n)}</span><em>{"★" * 5}</em></div>'
        for i, n in enumerate(v['names']))
    return f'<div class="xcard xmap a-up" {_d(0, .1)}><div class="xtile">{pins}</div>{rows}</div>'


def v_stars(v):
    stars = ''.join(f'<i class="a-pop" {_d(i, .4, .2)}>★</i>' for i in range(5))
    bubs = ''.join(f'<p class="xrev a-up" {_d(i, 1.6, .6)}>{E(t)}</p>' for i, t in enumerate(v['reviews']))
    return f'<div class="xcard xstars a-up" {_d(0, .1)}><div class="xst">{stars}</div><p class="xtag a-in" {_d(0, 1.3)}>{E(v.get("tag", ""))}</p>{bubs}</div>'


def v_pages(v):
    cards = ''.join(f'<div class="xpg a-pop" {_d(i, .4, .25)}><i></i><b>{E(t)}</b><span>{E(c)}</span></div>' for i, (t, c) in enumerate(v['pages']))
    return f'<div class="xpages">{cards}</div>'


def v_timeline(v):
    pts = ''.join(
        f'<div class="xtm a-pop" style="left:{p}%;--d:{.6 + i * .7:.2f}s"><i></i><b>{E(t)}</b><span>{E(sub)}</span></div>'
        for i, (t, sub, p) in enumerate(v['points']))
    return (f'<div class="xcard xtl a-up" {_d(0, .1)}><p class="xct">{E(v.get("title", ""))}</p><div class="xline"><i class="a-grow" style="--d:.3s"></i>{pts}</div>'
            f'<p class="xtag a-in" {_d(0, 3.4)}>{E(v.get("tag", ""))}</p></div>')


def v_split(v):
    segs = ''.join(f'<i class="a-grow" style="flex:{w};--d:{.5 + i * .35:.2f}s;background:{c}"></i>' for i, (_, w, c) in enumerate(v['parts']))
    keys = ''.join(f'<span class="a-in" {_d(i, 1.6, .25)}><i style="background:{c}"></i>{E(n)}</span>' for i, (n, _, c) in enumerate(v['parts']))
    return (f'<div class="xcard xsplit a-up" {_d(0, .1)}><p class="xct">{E(v.get("title", ""))}</p><div class="xsbar">{segs}</div><div class="xkeys">{keys}</div>'
            f'<p class="xtag a-in" {_d(0, 2.8)}>{E(v.get("tag", ""))}</p></div>')


def v_compare(v):
    head = ''.join(f'<b>{E(h)}</b>' for h in v['cols'])
    rows = ''.join(
        f'<div class="xcmp a-in" {_d(i, .6, .45)}><span>{E(r)}</span>' + ''.join(f'<em class="{"ok" if ok else "no"} a-pop" {_d(i, .9, .45)}>{CHECK if ok else CROSS}</em>' for ok in oks) + '</div>'
        for i, (r, oks) in enumerate(v['rows']))
    return f'<div class="xcard xcompare a-up" {_d(0, .1)}><div class="xcmp xch"><span></span>{head}</div>{rows}</div>'


def v_chat(v):
    return (f'<div class="xcard xchat a-up" {_d(0, .1)}><p class="xct">{E(v.get("title", "AI assistant"))}</p>'
            f'<p class="xbq a-up" {_d(0, .5)}>{E(v["q"])}</p><p class="xba a-up" {_d(0, 1.6)}>{E(v["a"])}</p></div>')


MOTIFS = {'phone': v_phone, 'checklist': v_checklist, 'shrink': v_shrink, 'sources': v_sources, 'race': v_race, 'shield': v_shield, 'search': v_search, 'map': v_map, 'stars': v_stars, 'pages': v_pages, 'timeline': v_timeline, 'split': v_split, 'compare': v_compare, 'chat': v_chat}


# ---------- scenes ----------
def _scene(inner, dur, label, cls=''):
    return f'<div class="xs {cls}" data-d="{dur}" data-l="{E(label)}" aria-hidden="true">{inner}</div>'


ROTA = ['attorney', 'intake', 'client', 'partner']


def _crowd(a, b):
    return f'<span class="xcrowd l">{a}</span><span class="xcrowd r">{b}</span>'


def render(post, spec):
    slug = post['slug'].split('/')[-1]
    scenes = []
    scenes.append(_scene(
        f'<div class="xintro"><span class="xmark a-pop">{MARK}</span><p class="xk a-in" {_d(0, .5)}>The 1-Minute Summary</p>'
        f'<p class="xh xbig a-up" {_d(0, .8)}>{E(spec["title"])}</p><p class="xd a-in" {_d(0, 1.5)}>{E(spec.get("sub", "The key points from this guide, in about a minute."))}</p></div>'
        + _crowd(person('attorney', 'wave', cls='a-up xtalk'), person('client', 'wave', flip=True, cls='a-up')),
        spec.get('intro_d', 5), 'Intro', 'xcenter'))
    n = 0
    for s in spec['scenes']:
        if s.get('kind') == 'answer':
            k = 'The Short Answer'
        else:
            n += 1
            k = f'{n:02d}'
        txt = (f'<div class="xtxt"><p class="xk a-in">{E(k)}</p><p class="xh a-up" {_d(0, .25)}>{E(s["h"])}</p>'
               f'<p class="xd a-up" {_d(0, .55)}>{E(s["p"])}</p></div>')
        who = s.get('who') or ROTA[len(scenes) % len(ROTA)]
        pose = s.get('pose') or ('stand' if who == 'intake' else 'point')
        talk = ' xtalk' if who == 'intake' or s.get('talk') else ''
        man = person(who, pose, flip=pose == 'point', cls='a-pop' + talk)
        vis = f'<div class="xvis"><div class="xwith">{MOTIFS[s["v"]["kind"]](s["v"])}<span class="xguy" style="--d:.6s">{man}</span></div></div>'
        scenes.append(_scene(txt + vis, s.get('d', 8), k if k[0].isdigit() else 'Answer'))
    c = spec['cta']
    scenes.append(_scene(
        f'<div class="xintro"><span class="xmark a-pop">{MARK}</span><p class="xh xbig a-up" {_d(0, .3)}>{E(c["h"])}</p>'
        f'<p class="xd a-in" {_d(0, .9)}>{E(c["p"])}</p><a class="xcta a-pop" style="--d:1.4s" href="{E(c["href"])}" data-xcta tabindex="-1">{E(c["btn"])}</a></div>'
        + _crowd(person('intake', 'cheer', cls='a-up xtalk'), person('partner', 'wave', flip=True, cls='a-up')),
        spec.get('cta_d', 7), 'Free audit', 'xcenter xend'))
    total = spec.get('intro_d', 5) + sum(s.get('d', 8) for s in spec['scenes']) + spec.get('cta_d', 7)
    mm = f'{total // 60}:{total % 60:02d}'
    poster = (f'<button class="xposter" type="button" data-xplay aria-label="Play the {mm} animated summary of this article">'
              f'<span class="xpk"><span class="xmark">{MARK}</span>The 1-Minute Summary</span>'
              f'<span class="xpt">{E(spec["title"])}</span>'
              f'<span class="xpb"><i>{PLAY}</i>Watch the summary <em>{mm}</em></span>'
              f'<span class="xpdeco" aria-hidden="true"><span class="xbub">{E(spec.get("bubble", "Here is the short version."))}</span>{person("attorney", "stand")}{person("client", "stand", flip=True)}</span></button>')
    bar = ('<div class="xctl"><button type="button" class="xbtn" data-xtoggle aria-label="Play">'
           '<svg class="i-play" viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5.5v13l11-6.5z" fill="currentColor"/></svg>'
           '<svg class="i-pause" viewBox="0 0 24 24" aria-hidden="true"><path d="M7 5h3.5v14H7zM13.5 5H17v14h-3.5z" fill="currentColor"/></svg>'
           '<svg class="i-replay" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 5V2L7 6l5 4V7a5 5 0 11-5 5H5a7 7 0 107-7z" fill="currentColor"/></svg></button>'
           '<div class="xsegs" role="group" aria-label="Jump to a point"></div><span class="xtime" aria-hidden="true">0:00</span></div>')
    return (f'<section class="xp" data-slug="{E(slug)}" aria-label="Animated 1-minute summary">'
            f'<div class="xstage">{poster}<span class="xwm" aria-hidden="true"><span class="xmark">{MARK}</span>CaseAuthority</span><div class="xscenes">{"".join(scenes)}</div></div>{bar}</section>')


CSS = r""".xp{container:xp/inline-size}

.xpdeco{position:absolute;right:5%;bottom:0;display:flex;align-items:flex-end;gap:0;width:34%;max-width:360px}
.xpdeco .xperson{width:50%;height:auto}
.xbub{position:absolute;left:8%;top:-26%;background:#fff;border-radius:16px;padding:12px 16px;font-size:15px;font-weight:500;box-shadow:0 12px 30px -18px rgba(14,14,15,.3)}
.xbub::after{content:"";position:absolute;left:28px;bottom:-8px;border:8px solid transparent;border-bottom:0;border-top-color:#fff}
.xwith{position:relative;display:flex;align-items:flex-end;justify-content:center;gap:10px;width:100%;min-width:0}
.xwith>:first-child{flex:0 1 auto;min-width:0}
.xguy{flex:0 0 auto;width:clamp(76px,10cqw,118px)}
.xguy .xperson{width:100%;height:auto}
.xcrowd{position:absolute;bottom:-4px;width:clamp(64px,11cqw,140px)}
.xcrowd.l{left:7%}.xcrowd.r{right:7%}
.xcrowd .xperson{width:100%;height:auto}
.xp{--xg:#CEAA32;--xk:#0E0E0F;--xc:#F5F1EA;--xs:#fff7e2;--xi:#7a5f12;--xe:cubic-bezier(.16,1,.3,1);margin:40px 0 0;font-family:inherit}
.xstage{position:relative;aspect-ratio:16/9;border-radius:24px;overflow:hidden;background:var(--xc);color:var(--xk);isolation:isolate}
.xposter{all:unset;box-sizing:border-box;position:absolute;inset:0;z-index:3;display:flex;flex-direction:column;justify-content:center;gap:18px;padding:clamp(24px,6%,64px);cursor:pointer;background:var(--xc);transition:opacity .4s var(--xe)}
.xposter:focus-visible{outline:3px solid var(--xk);outline-offset:-6px;border-radius:24px}
.xp.on .xposter{opacity:0;pointer-events:none}
.xpk,.xk{display:inline-flex;align-items:center;gap:10px;font-size:13px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--xi)}
.xmark{display:inline-grid;place-items:center;width:30px;height:30px;border-radius:8px;background:var(--xk)}
.xmark svg{width:70%;height:70%}
.xpt{max-width:15ch;font-size:clamp(26px,4.6cqw,52px);line-height:1.04;font-weight:500;letter-spacing:-.03em}
.xpb{display:inline-flex;align-items:center;gap:12px;align-self:flex-start;background:var(--xk);color:#fff;border-radius:999px;padding:10px 22px 10px 10px;font-size:16px;font-weight:500;transition:transform .25s var(--xe)}
.xposter:hover .xpb{transform:translateY(-2px)}
.xpb i{display:grid;place-items:center;width:36px;height:36px;border-radius:50%;background:var(--xg);color:var(--xk)}
.xpb svg{width:18px;height:18px}
.xpb em{font-style:normal;color:#b8b8b8;font-variant-numeric:tabular-nums}
.xscenes{position:absolute;inset:0}
.xwm{position:absolute;left:18px;bottom:14px;z-index:2;display:flex;align-items:center;gap:7px;font-size:12px;font-weight:600;color:#8a8a90;opacity:0;transition:opacity .4s}
.xwm .xmark{width:18px;height:18px;border-radius:5px}
.xp.on .xwm{opacity:1}
.xp.on:has(.xs.xcenter.act) .xwm{opacity:0}
.xend .xmark{display:none}
.xs{position:absolute;inset:0;display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.15fr);align-items:center;gap:4%;padding:4% 5%;opacity:0;visibility:hidden;transition:opacity .45s var(--xe),visibility 0s .45s}
.xs.act{opacity:1;visibility:visible;transition:opacity .45s var(--xe)}
.xs.xcenter{grid-template-columns:1fr;justify-items:center;text-align:center}
.xtxt{display:grid;gap:14px}
.xintro{display:grid;justify-items:center;gap:16px;max-width:min(680px,58cqw)}
.xintro .xmark{width:56px;height:56px;border-radius:14px}
.xh{margin:0;font-size:clamp(20px,3.1cqw,38px);line-height:1.1;font-weight:500;letter-spacing:-.025em}
.xh.xbig{font-size:clamp(24px,4.2cqw,50px)}
.xs .xd{margin:0;font-size:clamp(14px,1.6cqw,19px);line-height:1.45;color:#45454a}
.xcta{display:inline-flex;align-items:center;background:var(--xk);color:#fff!important;text-decoration:none;border-radius:999px;padding:14px 24px;font-size:16px;font-weight:500;margin-top:6px}
.xcta:hover{background:#2a2a2d}
.xvis{display:grid;place-items:center;min-width:0;height:100%;max-height:100%}
.xcard{width:min(100%,360px);background:#fff;border-radius:18px;padding:20px;box-shadow:0 1px 0 rgba(14,14,15,.05),0 18px 40px -24px rgba(14,14,15,.25);display:grid;gap:10px}
.xct{margin:0 0 4px;font-size:12px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:#8a8a90}
.xr{display:flex;align-items:center;gap:12px;font-size:15px;font-weight:500;padding:10px 12px;border-radius:12px;background:#f7f6f3}
.xr span{flex:1;min-width:0}
.xchk{flex:none;display:grid;place-items:center;width:24px;height:24px;border-radius:50%;background:var(--xg);color:var(--xk)}
.xchk svg{width:15px;height:15px}
.xb{display:block;flex:none;width:38%;height:8px;border-radius:4px;background:var(--xg);transform-origin:left}
.xtag{margin:4px 0 0;font-size:13px;font-weight:600;color:var(--xi)}
.xv-phone{display:grid;justify-items:center;gap:18px;width:100%}
.xph{position:relative;display:grid;place-items:center;width:64px;height:64px;border-radius:50%;background:var(--xk);color:var(--xg)}
.xph svg{width:28px;height:28px}
.xring{position:absolute;inset:0;border-radius:50%;border:2px solid var(--xg);opacity:0}
.xs.act .xring{animation:xRing 1.6s ease-out .3s 3}
.xs.act .xring.r2{animation-delay:.8s}
.xv-shrink{position:relative;width:min(100%,380px);padding:0 0 22px}
.xv-shrink .xcard{position:absolute;width:78%}
.xv-shrink .xfront{position:relative;left:0;top:0;z-index:2}
.xback{right:0;top:34px;bottom:0;overflow:hidden;background:#fbfaf7;opacity:.95}
.xln{display:block;height:9px;border-radius:5px;background:#ebe8e1}
.xln:nth-of-type(odd){width:82%}
.xbars{display:flex;align-items:flex-end;gap:12px;height:150px;padding-top:8px}
.xbar{flex:1;display:flex;flex-direction:column;justify-content:flex-end;align-items:center;gap:8px;height:100%}
.xbar i{display:block;width:100%;height:var(--h);border-radius:10px 10px 4px 4px;background:#e6e1d6;transform-origin:bottom}
.xbar.top i{background:var(--xg)}
.xbar span{font-size:12px;font-weight:600;color:#5c5c62;text-align:center;line-height:1.15}
.xrace{gap:18px}
.xlane{display:grid;gap:8px}
.xlane p{margin:0;font-size:14px;font-weight:600}
.xtrack{position:relative;height:10px;border-radius:5px;background:#efece5}
.xdot{position:absolute;left:0;top:50%;width:18px;height:18px;margin-top:-9px;border-radius:50%;background:var(--xk)}
.xdot.fast{background:var(--xg);box-shadow:0 0 0 4px rgba(206,170,50,.25)}
.xs.act .xdot.fast{animation:xRun 1.2s var(--xe) .6s both}
.xs.act .xdot.slow{animation:xRun 3.8s linear .6s both}
.xres{justify-self:start;display:inline-flex;align-items:center;gap:6px;font-size:13px;font-weight:600;padding:5px 10px 5px 6px;border-radius:999px}
.xres svg{width:16px;height:16px}
.xres.win{background:var(--xs);color:var(--xi)}
.xres.lose{background:#f1f0ee;color:#6b6b70}
.xv-shield{display:grid;justify-items:center;gap:18px}
.xsh{width:120px;height:140px}
.xchips{display:flex;flex-wrap:wrap;justify-content:center;gap:8px}
.xchip{background:#fff;border-radius:999px;padding:8px 14px;font-size:14px;font-weight:600;box-shadow:0 1px 0 rgba(14,14,15,.06)}
.xs [class*="a-"]{opacity:0}
.xs .a-draw{opacity:1;stroke-dasharray:1;stroke-dashoffset:1}
.xs.act .a-up{animation:xUp .8s var(--xe) var(--d,0s) both}
.xs.act .a-in{animation:xIn .6s var(--xe) var(--d,0s) both}
.xs.act .a-pop{animation:xPop .55s cubic-bezier(.34,1.56,.64,1) var(--d,0s) both}
.xs.act .a-grow{animation:xGrow .9s var(--xe) var(--d,0s) both}
.xs.act .a-rise{animation:xRise 1s var(--xe) var(--d,0s) both}
.xs.act .a-slide{animation:xSlide .9s var(--xe) var(--d,0s) both}
.xs.act .a-draw{animation:xDraw 1.1s ease-in-out var(--d,0s) both}
.xq{display:flex;align-items:center;gap:10px;min-width:0;overflow:hidden;padding:10px 14px;border-radius:999px;border:1.5px solid #e4e0d6;font-size:15px;font-weight:500}
.xq svg{width:18px;height:18px;flex:none;color:#8a8a90}
.xtype{display:inline-block;flex:0 1 auto;min-width:0;overflow:hidden;white-space:nowrap;max-width:0;border-right:2px solid var(--xk)}
@media (prefers-reduced-motion:reduce){.xtype{max-width:none}}
.xs.act .xtype{animation:xType 1.4s steps(var(--n)) .5s both}
.xres1{display:flex;align-items:center;gap:8px;padding:9px 12px;border-radius:12px;background:#f7f6f3;font-size:14px}
.xres1 b{font-weight:600}.xres1 i{flex:1;height:7px;border-radius:4px;background:#e9e5dc;margin-left:6px}
.xres1.you{background:var(--xs);outline:2px solid var(--xg)}
.xres1 em,.xmrow em{font-style:normal}
.xres1 em{font-size:11px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:var(--xi);background:#fff;padding:2px 7px;border-radius:999px}
.xtile{position:relative;height:110px;border-radius:12px;overflow:hidden;background:linear-gradient(90deg,transparent 46%,#fff 46% 50%,transparent 50%),linear-gradient(0deg,transparent 56%,#fff 56% 61%,transparent 61%),linear-gradient(150deg,transparent 70%,#fff 70% 73%,transparent 73%),#e7eadc}
.xpin{position:absolute;display:grid;place-items:center;width:26px;height:26px;margin:-26px 0 0 -13px;border-radius:50% 50% 50% 0;transform:rotate(-45deg);background:var(--xk);color:#fff;font-size:12px;font-weight:700;font-style:normal}
.xpin b{transform:rotate(45deg)}
.xpin:first-child{background:var(--xg);color:var(--xk)}
.xmrow{display:flex;align-items:center;gap:10px;padding:8px 10px;border-radius:10px;font-size:14px}
.xmrow b{display:grid;place-items:center;width:22px;height:22px;border-radius:50%;background:#efece5;font-size:12px}
.xmrow span{flex:1;font-weight:500}.xmrow em{color:var(--xg);font-size:12px;letter-spacing:1px}
.xmrow.you{background:var(--xs)}.xmrow.you b{background:var(--xg)}
.xst{display:flex;gap:6px;font-size:38px;line-height:1;color:var(--xg)}
.xst i{font-style:normal}
.xrev{margin:0;background:#f7f6f3;border-radius:14px 14px 14px 4px;padding:10px 14px;font-size:14px;font-weight:500}
.xpages{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px;width:min(100%,380px)}
.xpg{background:#fff;border-radius:14px;padding:12px;display:grid;gap:4px;box-shadow:0 12px 30px -22px rgba(14,14,15,.35)}
.xpg i{display:block;height:34px;border-radius:8px;background:var(--xs);margin-bottom:4px}
.xpg b{font-size:14px;font-weight:600}.xpg span{font-size:12px;color:#6b6b70}
.xline{position:relative;height:96px;margin:6px 8px 0}
.xline>i{position:absolute;left:0;right:0;top:12px;height:4px;border-radius:2px;background:var(--xg);transform-origin:left}
.xtm{position:absolute;top:4px;display:grid;justify-items:center;text-align:center;translate:-50% 0;max-width:36%}
.xtm i{width:20px;height:20px;border-radius:50%;background:var(--xk);border:4px solid #fff;box-sizing:border-box}
.xtm b{font-size:13px;font-weight:600;margin-top:8px;line-height:1.2}
.xtm span{font-size:12px;line-height:1.25;color:#6b6b70}
.xtm:first-of-type{justify-items:start;text-align:left;translate:-10px 0}.xtm:last-of-type{justify-items:end;text-align:right;translate:calc(-100% + 10px) 0}
.xsbar{display:flex;gap:4px;height:44px}
.xsbar i{display:block;border-radius:8px;transform-origin:left}
.xkeys{display:flex;flex-wrap:wrap;gap:6px 14px;font-size:13px;font-weight:500}
.xkeys span{display:inline-flex;align-items:center;gap:6px}.xkeys i{width:10px;height:10px;border-radius:3px}
.xcmp{display:grid;grid-template-columns:1fr 54px 54px;align-items:center;gap:6px;padding:8px 10px;border-radius:10px;background:#f7f6f3;font-size:14px;font-weight:500}
.xch{background:none;padding-block:0}.xch b{text-align:center;font-size:12px;font-weight:700;color:#6b6b70}
.xcmp em{justify-self:center;display:grid;place-items:center;width:24px;height:24px;border-radius:50%}
.xcmp em svg{width:14px;height:14px}.xcmp em.ok{background:var(--xg);color:var(--xk)}.xcmp em.no{background:#e9e5dc;color:#6b6b70}
.xbq,.xba{margin:0;padding:11px 14px;font-size:14px;line-height:1.4;font-weight:500;max-width:88%}
.xbq{justify-self:end;background:var(--xk);color:#fff;border-radius:16px 16px 4px 16px}
.xba{background:var(--xs);border-radius:16px 16px 16px 4px}
.xs.act .a-drop{animation:xDrop .7s cubic-bezier(.34,1.56,.64,1) var(--d,0s) both}
@keyframes xType{from{max-width:0}to{max-width:100%}}
@keyframes xDrop{from{opacity:0;transform:translateY(-30px) rotate(-45deg)}to{opacity:1;transform:rotate(-45deg)}}
@keyframes xUp{from{opacity:0;transform:translateY(18px)}to{opacity:1;transform:none}}
@keyframes xIn{from{opacity:0}to{opacity:1}}
@keyframes xPop{from{opacity:0;transform:scale(.6)}to{opacity:1;transform:none}}
@keyframes xGrow{from{opacity:1;transform:scaleX(0)}to{opacity:1;transform:none}}
@keyframes xRise{from{opacity:1;transform:scaleY(0)}to{opacity:1;transform:none}}
@keyframes xSlide{from{opacity:0;transform:translate(-30%,0)}to{opacity:.95;transform:none}}
@keyframes xDraw{to{stroke-dashoffset:0}}
@keyframes xRing{from{opacity:.9;transform:scale(1)}to{opacity:0;transform:scale(1.9)}}
@keyframes xRun{from{left:0}to{left:calc(100% - 18px)}}
.xp.paused .xs *,.xp.paused .xs{animation-play-state:paused!important}
.xctl{display:flex;align-items:center;gap:14px;margin-top:12px;opacity:.35;transition:opacity .3s}
.xp.on .xctl{opacity:1}
.xbtn{flex:none;display:grid;place-items:center;width:40px;height:40px;border-radius:50%;border:0;background:var(--xk);color:#fff;cursor:pointer}
.xbtn svg{width:18px;height:18px;display:none}
.xp:not(.on) .i-play,.xp.paused:not(.done) .i-play,.xp.on:not(.paused):not(.done) .i-pause,.xp.done .i-replay{display:block}
.xsegs{flex:1;display:flex;gap:4px}
.xseg{all:unset;flex:var(--w);height:24px;display:flex;align-items:center;cursor:pointer}
.xseg i{display:block;width:100%;height:5px;border-radius:3px;background:#e4e0d6;overflow:hidden}
.xseg i::after{content:"";display:block;height:100%;width:calc(var(--f,0)*100%);background:var(--xk)}
.xseg:focus-visible i{outline:2px solid var(--xk);outline-offset:3px}
.xtime{flex:none;font-size:13px;font-weight:600;color:#6b6b70;font-variant-numeric:tabular-nums;min-width:34px;text-align:right}
@media (prefers-reduced-motion:reduce){.xs.act [class*="a-"]{animation:none!important;opacity:1;transform:none;stroke-dashoffset:0}.xs.act .xring,.xs.act .xdot{animation:none!important}.xs.act .xdot{left:calc(100% - 18px)}}
@container xp (max-width:819px){.xstage{aspect-ratio:4/3}.xs{grid-template-columns:minmax(0,1fr);grid-template-rows:auto auto;align-content:center;gap:16px;padding:22px 22px 26px}.xs .xvis{order:-1;height:auto}.xcard{padding:14px;gap:7px;border-radius:14px}.xr{padding:7px 10px;font-size:14px}.xbars{height:110px}.xst{font-size:28px;gap:4px}.xsh{width:84px;height:98px}.xph{display:none}.xwm{display:none}.xcmp{grid-template-columns:minmax(0,1fr) 40px 40px;font-size:13px}.xpages{gap:8px}.xpg{padding:9px}.xpg i{height:20px}.xtile{height:80px}.xres1 i{display:none}.xintro{max-width:100%;padding-bottom:calc(11cqw * 1.45)}.xpdeco{width:44%;right:3%}.xbub{display:none}.xpt{max-width:none}}
@container xp (max-width:559px){.xstage{aspect-ratio:3/5;border-radius:18px}.xs{padding:20px 16px 22px;gap:14px}.xguy{width:clamp(54px,16cqw,76px)}.xcrowd{width:clamp(56px,17cqw,80px)}.xcrowd.l{left:3%}.xcrowd.r{right:3%}.xintro{padding-bottom:calc(17cqw * 1.45)}.xpdeco{width:56%}.xst{font-size:24px}.xr{font-size:13.5px;gap:9px}.xchk{width:20px;height:20px}}
@container xp (max-width:319px){.xstage{aspect-ratio:1/2}.xs{padding:18px 12px 20px;gap:12px}.xguy{width:46px}.xwith{gap:4px}.xcard{padding:11px;gap:6px}.xr{font-size:12.5px;padding:6px 8px;gap:7px}.xh{font-size:19px}.xs .xd{font-size:13.5px}.xbars{gap:6px}.xbar span{font-size:10.5px}.xmrow{font-size:12.5px;gap:6px;padding:6px}.xmrow em{display:none}.xcmp{grid-template-columns:minmax(0,1fr) 28px 28px;font-size:12px;padding:6px}.xpg b{font-size:12.5px}.xres1{font-size:12.5px}.xres1 em{display:none}.xkeys{font-size:12px}.xlane p{font-size:12.5px}.xst{font-size:20px}}
"""

JS = r"""
(function(){document.querySelectorAll('.xp').forEach(function(p){
var sc=[].slice.call(p.querySelectorAll('.xs')),D=sc.map(function(s){return +s.dataset.d*1000}),S=[],T=0,i,
segs=p.querySelector('.xsegs'),tm=p.querySelector('.xtime'),tg=p.querySelector('[data-xtoggle]'),cta=p.querySelector('[data-xcta]'),
t=0,cur=-1,run=false,last=0,raf=0,slug=p.dataset.slug,sent={};
for(i=0;i<D.length;i++){S.push(T);T+=D[i]}
function ev(n){if(sent[n])return;sent[n]=1;if(window.gtag)gtag('event',n,{post_slug:slug})}
function fmt(ms){var s=Math.round(ms/1000);return Math.floor(s/60)+':'+('0'+s%60).slice(-2)}
var sg=sc.map(function(s,k){var b=document.createElement('button');b.type='button';b.className='xseg';b.style.setProperty('--w',D[k]);
b.setAttribute('aria-label','Jump to '+s.dataset.l);b.innerHTML='<i></i>';b.onclick=function(){seek(S[k]);if(!run)play()};segs.appendChild(b);return b});
function show(k){if(k===cur)return;if(cur>-1){sc[cur].classList.remove('act');sc[cur].setAttribute('aria-hidden','true')}
cur=k;void sc[k].offsetWidth;sc[k].classList.add('act');sc[k].removeAttribute('aria-hidden');if(cta)cta.tabIndex=k===sc.length-1?0:-1}
function paint(){var k=0;while(k<S.length-1&&t>=S[k+1])k++;show(k);
sg.forEach(function(b,j){b.style.setProperty('--f',j<k?1:j>k?0:Math.min(1,(t-S[j])/D[j]))});tm.textContent=fmt(t)}
function tick(now){var dt=now-last;last=now;t=Math.min(T,t+dt);paint();
if(t>=T){run=false;p.classList.add('paused','done');tg.setAttribute('aria-label','Replay');ev('explainer_complete');return}
if(t>T/2)ev('explainer_half');raf=requestAnimationFrame(tick)}
function play(){if(t>=T)seek(0);p.classList.add('on');p.classList.remove('paused','done');run=true;tg.setAttribute('aria-label','Pause');
last=performance.now();cancelAnimationFrame(raf);raf=requestAnimationFrame(tick);ev('explainer_play')}
function pause(){if(!run)return;run=false;cancelAnimationFrame(raf);p.classList.add('paused');tg.setAttribute('aria-label','Play')}
function seek(ms){t=ms;cur=-1;sc.forEach(function(s){s.classList.remove('act');s.setAttribute('aria-hidden','true')});p.classList.remove('done');paint()}
p.querySelector('[data-xplay]').onclick=play;tg.onclick=function(){run?pause():play()};
if(cta)cta.addEventListener('click',function(){ev('explainer_cta')});
if('IntersectionObserver'in window)new IntersectionObserver(function(e){if(!e[0].isIntersecting)pause()},{threshold:.25}).observe(p);
document.addEventListener('visibilitychange',function(){if(document.hidden)pause()});
tm.textContent='0:00';
})})();
"""


def assets():
    return '<style>' + ' '.join(l.strip() for l in (CSS + PEOPLE_CSS).strip().splitlines()) + '</style>', '<script>' + JS.strip() + '</script>'

# ===== specs =====
# One explainer spec per published blog post, keyed by slug (the part after /blog/).
# Rules: Title Case headings, no em dashes, figures marked as examples unless they are the site's own case-study numbers.
G, K, B, S = '#CEAA32', '#0E0E0F', '#a8842a', '#d9d2c3'
CTA = lambda h, p: {'h': h, 'p': p, 'btn': 'Get my free audit', 'href': '/sales'}

SPECS = {
'personal-injury-lead-generation': {
  'title': 'Personal Injury Lead Generation in 60 Seconds',
  'sub': 'Buying leads versus earning them, and what really decides signed cases.',
  'bubble': 'Leads are not cases. Here is why.',
  'scenes': [
    {'kind': 'answer', 'h': 'Leads Only Matter if They Sign',
     'p': 'You can buy leads, pay for them with ads, or earn them in Google and through referrals. Judge every source by signed cases.',
     'v': {'kind': 'phone', 'title': 'New injury inquiry', 'rows': ['Hurt in a car crash', 'Where did they find you?', 'Callback in minutes']}},
    {'h': 'Bought Leads Start Fast, Stop Fast', 'p': 'Purchased leads can fill a gap quickly, but they end the day you stop paying and are often shared.',
     'v': {'kind': 'compare', 'cols': ['Bought', 'Earned'], 'rows': [('Starts quickly', (True, False)), ('Only your firm', (False, True)), ('Keeps working', (False, True))]}},
    {'h': 'Shared Leads Turn Into a Race', 'p': 'When several firms get the same lead, the first helpful call usually wins the case.',
     'v': {'kind': 'race', 'fast': ('Called back in two minutes', 'Case signed'), 'slow': ('Called back tomorrow', 'Hired another firm')}},
    {'h': 'Ask Before You Buy', 'p': 'Get clear answers from any lead vendor before you pay for a single lead.',
     'v': {'kind': 'checklist', 'title': 'Questions for a lead vendor', 'items': ['Exclusive or shared?', 'Where do leads come from?', 'How is consent recorded?', 'What about bad leads?']}},
    {'h': 'Earned Leads Come Straight to You', 'p': 'Search, the Map Pack, reviews and referrals take longer, but nobody else is sold the same person.',
     'v': {'kind': 'search', 'q': 'car accident lawyer near me', 'results': [('Your Firm', True), ('Metro Injury Law', False), ('Smith Accident Attorneys', False)]}},
    {'h': 'Measure Cost per Signed Case', 'p': 'Record the source of every lead, then compare what each source cost with the cases it signed.',
     'v': {'kind': 'sources', 'title': 'Signed cases by source', 'items': [('Map Pack', 100), ('Referrals', 70), ('Paid search', 55), ('Bought leads', 30)], 'tag': 'Illustrative example'}},
    {'h': 'Check Your Bar Rules', 'p': 'Paying for leads is regulated, and rules vary by state.',
     'v': {'kind': 'shield', 'chips': ['State bar rules', 'No paid recommendations', 'Honest lead services']}},
  ],
  'cta': CTA('Want More Leads That Belong Only to Your Firm?', 'Get a free audit of where your firm stands in Google and the Map Pack.'),
},
'website-design-for-personal-injury-lawyers': {
  'title': 'Personal Injury Website Design in 60 Seconds',
  'sub': 'What turns an injury firm website into calls and signed cases.',
  'bubble': 'Here is what really matters.',
  'scenes': [
    {'kind': 'answer', 'h': 'Results Matter More Than Looks',
     'p': 'The best injury firm websites load fast on a phone, make calling easy and explain clearly what the firm handles and where.',
     'v': {'kind': 'phone', 'title': 'Your firm on a phone', 'rows': ['Tap to call', 'Free case review', 'Case types and cities']}},
    {'h': 'Design for the Phone First', 'p': 'Most injured people find a lawyer on their phone, often soon after an accident. The site has to work there first.',
     'v': {'kind': 'checklist', 'title': 'One-hand phone test', 'items': ['Loads in a moment', 'Phone number in view', 'Easy to read', 'Big tap targets']}},
    {'h': 'A Slow Site Loses Cases', 'p': 'Every extra second gives a stressed visitor a reason to go back and call the next firm.',
     'v': {'kind': 'race', 'fast': ('Page loads in a moment', 'Call to your firm'), 'slow': ('Page still loading', 'Called the next firm')}},
    {'h': 'One Page per Case Type and City', 'p': 'Clear pages help people and Google understand what you handle and where you work.',
     'v': {'kind': 'pages', 'pages': [('Car Accidents', 'Your main city'), ('Truck Accidents', 'Your main city'), ('Slip and Fall', 'Your main city'), ('Car Accidents', 'Nearby city')]}},
    {'h': 'Trust Comes From Real Proof', 'p': 'Real reviews, attorney profiles and honest facts build more trust than stock photos and slogans.',
     'v': {'kind': 'stars', 'tag': 'Real reviews from real clients', 'reviews': ['They explained everything clearly.', 'Easy to reach and always kind.']}},
    {'h': 'Judge It by Signed Cases', 'p': 'Track calls, forms and signed cases from the site, not just visits or how it looks.',
     'v': {'kind': 'compare', 'cols': ['Looks', 'Cases'], 'rows': [('Brings in calls', (False, True)), ('Ties to fees', (False, True)), ('Guides what to fix', (False, True))]}},
    {'h': 'Check Your Bar Rules', 'p': 'Your website is lawyer advertising, so results, reviews and awards need care.',
     'v': {'kind': 'shield', 'chips': ['State bar rules', 'Disclaimers', 'No promised results']}},
  ],
  'cta': CTA('Want to Know if Your Website Is Costing You Cases?', 'Get a free audit of how your site works on a phone and in Google.'),
},
'personal-injury-intake-form': {
  'title': 'Personal Injury Intake Forms in 60 Seconds',
  'sub': 'Five things every firm owner and intake manager should know.',
  'scenes': [
    {'kind': 'answer', 'h': 'Your Intake Form Decides Which Cases You Sign',
     'p': 'It records who called, gives you the facts to decide fast, and starts the relationship with someone who is hurt and calling other firms too.',
     'v': {'kind': 'phone', 'title': 'New inquiry', 'rows': ['Name and phone', 'Accident details', 'Next step booked']}},
    {'h': 'Ask the Deciding Questions First', 'p': 'Date, type of accident, injuries and fault tell you most of what you need in the first few minutes.',
     'v': {'kind': 'checklist', 'title': 'First few minutes', 'items': ['When did it happen?', 'What type of accident?', 'What injuries?', 'Who was at fault?']}},
    {'h': 'Keep the First Contact Short', 'p': 'Collect the essentials on the first call or web form. Save the long questionnaire for after you sign.',
     'v': {'kind': 'shrink', 'title': 'First contact', 'keep': ['Contact details', 'Accident basics', 'Callback time'], 'tag': 'About 5 minutes', 'later': 'After signing'}},
    {'h': 'Always Record the Lead Source', 'p': 'Without it, you cannot tell which marketing brings in signed cases.',
     'v': {'kind': 'sources', 'title': 'Where signed cases came from', 'items': [('Google search', 62), ('Map Pack', 100), ('Referral', 45), ('Other', 28)], 'tag': 'Illustrative example'}},
    {'h': 'Speed Beats Length', 'p': 'A short form followed up within minutes signs more cases than a perfect form followed up tomorrow.',
     'v': {'kind': 'race', 'fast': ('Short form, called back in minutes', 'Case signed'), 'slow': ('Perfect form, called back tomorrow', 'Hired another firm')}},
    {'h': 'Check Your Bar Rules', 'p': 'What you can ask, say and promise at intake is shaped by your state bar and privacy rules.',
     'v': {'kind': 'shield', 'chips': ['State bar rules', 'Privacy', 'No promised results']}},
  ],
  'cta': CTA('Want to See How Many Leads Reach Your Intake Team?', 'Get a free audit of where your firm stands in Google and the Map Pack.'),
},
'is-local-seo-worth-it-for-personal-injury-attorneys': {
  'title': 'Is Local SEO Worth It? The 60 Second Answer',
  'sub': 'What injury firm owners should weigh before they commit.',
  'scenes': [
    {'kind': 'answer', 'h': 'For Most Injury Firms, Yes',
     'p': 'Injured people search for a lawyer near them, often on a phone, and the firms in the Map Pack get a large share of those calls.',
     'v': {'kind': 'search', 'q': 'car accident lawyer near me', 'results': [('Your Firm', True), ('Smith Injury Law', False), ('Metro Accident Attorneys', False)]}},
    {'h': 'Usually Worth It for Injury Firms', 'p': 'People look for a personal injury lawyer near them, and local results get a large share of those searches.',
     'v': {'kind': 'map', 'names': ['Your Firm', 'Smith Injury Law', 'Metro Accident Attorneys']}},
    {'h': 'Think in Months, Not Weeks', 'p': 'Local SEO builds over time. Paid ads start faster but stop when the spending stops.',
     'v': {'kind': 'timeline', 'title': 'How local SEO builds', 'points': [('Month 1', 'Fix the basics', 0), ('Month 3', 'Early movement', 50), ('Month 6+', 'Steady calls', 100)], 'tag': 'Illustrative timeline'}},
    {'h': 'It Only Pays if Intake Works', 'p': 'More calls are only worth something if your team answers quickly and signs the right cases.',
     'v': {'kind': 'race', 'fast': ('Call answered in seconds', 'Case signed'), 'slow': ('Call goes to voicemail', 'Called the next firm')}},
    {'h': 'Measure Signed Cases, Not Rankings', 'p': 'Track calls and signed cases by lead source to judge whether it is paying off.',
     'v': {'kind': 'sources', 'title': 'Signed cases by source', 'items': [('Map Pack', 100), ('Organic', 70), ('Ads', 48), ('Referral', 36)], 'tag': 'Illustrative example'}},
    {'h': 'Some Firms Should Wait', 'p': 'No real local office, no room for more cases, or a need for cases this week all change the answer.',
     'v': {'kind': 'checklist', 'title': 'Check before you start', 'items': ['A real local office', 'Room for more cases', 'Time to let it build']}},
  ],
  'cta': CTA('Want to Know if Local SEO Is Worth It for Your Firm?', 'See where you stand today in Google and the Map Pack, for free.'),
},
'law-firm-marketing-plan': {
  'title': 'A Law Firm Marketing Plan in 60 Seconds',
  'sub': 'The five parts of a plan that actually brings in cases.',
  'scenes': [
    {'kind': 'answer', 'h': 'A Short Plan Built Around Signed Cases',
     'p': 'Set goals in cases, pick where to grow, choose a few channels, fix intake, and review the numbers every month.',
     'v': {'kind': 'checklist', 'title': 'Your one-page plan', 'items': ['Goals in signed cases', 'Case types and cities', 'Channels and budget', 'Monthly numbers']}},
    {'h': 'Start With Signed Cases', 'p': 'Set goals in cases and fees, then work back to calls and leads, not clicks and traffic.',
     'v': {'kind': 'sources', 'title': 'Work back from the goal', 'items': [('Signed cases', 30), ('Consults', 55), ('Calls', 80), ('Leads', 100)], 'tag': 'Illustrative example'}},
    {'h': 'Choose Where to Win', 'p': 'Pick the case types and cities that matter most instead of trying to rank for everything.',
     'v': {'kind': 'pages', 'pages': [('Car Accidents', 'Your main city'), ('Truck Accidents', 'Your main city'), ('Car Accidents', 'Nearby city'), ('Slip and Fall', 'Your main city')]}},
    {'h': 'Fewer Channels, Done Well', 'p': 'Two or three channels run properly beat six channels run halfway.',
     'v': {'kind': 'split', 'title': 'Example channel mix', 'parts': [('SEO and Map Pack', 5, G), ('Paid ads', 3, K), ('Referrals', 2, S)], 'tag': 'Illustrative example'}},
    {'h': 'Intake Is Part of Marketing', 'p': 'Missed calls and slow follow-up waste every dollar spent on getting found.',
     'v': {'kind': 'race', 'fast': ('Called back in minutes', 'Case signed'), 'slow': ('Missed call, no follow-up', 'Lead lost')}},
    {'h': 'Review It Every Quarter', 'p': 'A plan is only useful if you check it against real numbers and adjust.',
     'v': {'kind': 'timeline', 'title': 'Your review rhythm', 'points': [('Q1', 'Set goals', 0), ('Q2', 'Review and adjust', 50), ('Q4', 'Plan next year', 100)]}},
  ],
  'cta': CTA('Want a Starting Point for Your Plan?', 'Get a free audit so your plan starts from real numbers.'),
},
'how-to-compare-seo-proposals-for-personal-injury-law-firms': {
  'title': 'Comparing SEO Proposals in 60 Seconds',
  'sub': 'How to pick the right agency for your injury firm.',
  'scenes': [
    {'kind': 'answer', 'h': 'Put Every Proposal on One Scorecard',
     'p': 'Compare the work, who does it, the price, the contract, who owns the work and how results are reported.',
     'v': {'kind': 'compare', 'cols': ['A', 'B'], 'rows': [('Clear deliverables', (True, False)), ('Fair exit terms', (True, False)), ('You own the work', (True, True)), ('Reports signed cases', (True, False))]}},
    {'h': 'Compare Like With Like', 'p': 'Rewrite each proposal into the same few headings before you judge them.',
     'v': {'kind': 'checklist', 'title': 'Same headings for each', 'items': ['Work included', 'Who does it', 'Price and terms', 'Reporting']}},
    {'h': 'Clarity Beats Volume', 'p': 'A short proposal with clear deliverables is worth more than a long one full of jargon.',
     'v': {'kind': 'shrink', 'title': 'Clear proposal', 'keep': ['Pages to build', 'Profile work', 'Monthly report'], 'tag': 'Easy to check', 'later': '40 pages of jargon'}},
    {'h': 'Watch the Contract', 'p': 'Term length, exit terms and who owns your website and content matter as much as price.',
     'v': {'kind': 'shield', 'chips': ['Term length', 'Exit terms', 'You own the content']}},
    {'h': 'Ask About Exclusivity', 'p': 'Find out whether the agency will also work for a competing firm in your city.',
     'v': {'kind': 'map', 'names': ['Your Firm', 'Competitor A', 'Competitor B']}},
    {'h': 'Judge by Signed Cases', 'p': 'Pick the agency that will report on calls, intakes and signed cases, not just rankings.',
     'v': {'kind': 'sources', 'title': 'What a good report shows', 'items': [('Rankings', 40), ('Calls', 65), ('Intakes', 80), ('Signed cases', 100)], 'tag': 'Illustrative example'}},
  ],
  'cta': CTA('Not Sure Which Proposal to Pick?', 'Get a free second opinion on where your firm stands before you commit.'),
},
'how-much-should-a-law-firm-spend-on-marketing': {
  'title': 'Setting a Marketing Budget in 60 Seconds',
  'sub': 'How personal injury firms decide what to spend.',
  'scenes': [
    {'kind': 'answer', 'h': 'Start From Your Own Case Numbers',
     'p': 'Common ranges are a starting point. Your fee per case and the cases you want should set the budget.',
     'v': {'kind': 'checklist', 'title': 'Your budget inputs', 'items': ['Average fee per case', 'Cases you want', 'What a signed case can cost']}},
    {'h': 'Ranges Are a Starting Point', 'p': 'A share of revenue is a common rule of thumb, but your own case numbers should decide the budget.',
     'v': {'kind': 'split', 'title': 'Revenue and marketing', 'parts': [('Marketing', 1, G), ('Everything else', 9, S)], 'tag': 'Illustrative example'}},
    {'h': 'PI Usually Costs More', 'p': 'Personal injury is one of the most competitive areas in legal marketing, so budgets tend to run higher.',
     'v': {'kind': 'map', 'names': ['Your Firm', 'Big Billboard Firm', 'Regional Injury Group']}},
    {'h': 'Work Back From Cases', 'p': 'Decide how many signed cases you want, then what you can afford to pay for each one.',
     'v': {'kind': 'sources', 'title': 'Work back from the goal', 'items': [('Signed cases', 30), ('Consults', 55), ('Calls', 80), ('Leads', 100)], 'tag': 'Illustrative example'}},
    {'h': 'Mix Fast and Slow Channels', 'p': 'Ads bring calls quickly, while SEO and reviews build cases that keep coming.',
     'v': {'kind': 'split', 'title': 'Example mix', 'parts': [('Ads (fast)', 4, K), ('SEO and reviews (lasting)', 5, G), ('Referrals', 1, S)], 'tag': 'Illustrative example'}},
    {'h': 'Track Signed Cases', 'p': 'Judge every dollar by the cases and fees it brings in, not by clicks or traffic.',
     'v': {'kind': 'compare', 'cols': ['Clicks', 'Cases'], 'rows': [('Shows real return', (False, True)), ('Ties to fees', (False, True)), ('Guides the budget', (False, True))]}},
  ],
  'cta': CTA('Find Out Where Your Marketing Money Is Going', 'Get a free review of which channels can bring the most signed cases.'),
},
'seo-for-accident-claims': {
  'title': 'SEO for Accident Claims in 60 Seconds',
  'sub': 'How injury firms get found when it matters most.',
  'scenes': [
    {'kind': 'answer', 'h': 'Be Found When Accident Victims Search',
     'p': 'A strong Google Business Profile, a page per accident type and city, helpful answers, steady reviews and a fast site.',
     'v': {'kind': 'search', 'q': 'truck accident lawyer', 'results': [('Your Firm', True), ('Highway Injury Law', False), ('City Trial Lawyers', False)]}},
    {'h': 'Search Starts Early', 'p': 'Most accident victims look for answers on their phone long before they call a lawyer.',
     'v': {'kind': 'chat', 'title': 'Phone search', 'q': 'Who pays my medical bills after a car crash?', 'a': 'A clear answer from Your Firm, with a number to call.'}},
    {'h': 'Map Pack First', 'p': 'For local accident searches, the Google Map Pack is usually the first thing an injured person sees.',
     'v': {'kind': 'map', 'names': ['Your Firm', 'Highway Injury Law', 'City Trial Lawyers']}},
    {'h': 'One Page Per Accident Type', 'p': 'Car, truck, motorcycle and slip and fall claims each deserve their own page for each city you serve.',
     'v': {'kind': 'pages', 'pages': [('Car Accidents', 'Your city'), ('Truck Accidents', 'Your city'), ('Motorcycle Accidents', 'Your city'), ('Slip and Fall', 'Your city')]}},
    {'h': 'Answer the Claim Questions', 'p': 'Content about fault, deadlines, insurance and settlements feeds both Google and AI answers.',
     'v': {'kind': 'checklist', 'title': 'Questions to answer', 'items': ['Who was at fault?', 'How long do I have?', 'Will insurance pay?', 'What is my claim worth?']}},
    {'h': 'Measure Signed Cases', 'p': 'Rankings and traffic only matter if they turn into accident clients you sign.',
     'v': {'kind': 'sources', 'title': 'What really counts', 'items': [('Traffic', 40), ('Calls', 65), ('Consults', 80), ('Signed cases', 100)], 'tag': 'Illustrative example'}},
  ],
  'cta': CTA('Are You Showing Up When Accident Victims Search?', 'Get a free audit of your accident case rankings and Map Pack spot.'),
},
'personal-injury-marketing-ideas': {
  'title': 'Injury Marketing Ideas in 60 Seconds',
  'sub': 'What you can do yourself, and when to call an expert.',
  'scenes': [
    {'kind': 'answer', 'h': 'Simple Ideas You Can Run Yourself',
     'p': 'A complete Google profile, a review request to every client, a page per case type, and helpful answers.',
     'v': {'kind': 'checklist', 'title': 'Do it yourself', 'items': ['Weekly Google posts', 'Ask every client for a review', 'One page per case type', 'Answer client questions']}},
    {'h': 'Start With Google', 'p': 'Your Google Business Profile is free and drives more injury calls than any other single asset.',
     'v': {'kind': 'map', 'names': ['Your Firm', 'Downtown Injury Law', 'Accident Attorneys Group']}},
    {'h': 'Reviews Every Week', 'p': 'A steady flow of fresh reviews beats a burst of old ones.',
     'v': {'kind': 'stars', 'tag': 'A few new reviews every week', 'reviews': ['They called me back the same day.', 'Kind, clear and always available.']}},
    {'h': 'One Page Per Case', 'p': 'A page for each case type and city tells Google exactly where you should rank.',
     'v': {'kind': 'pages', 'pages': [('Car Accidents', 'Your city'), ('Dog Bites', 'Your city'), ('Truck Accidents', 'Nearby city'), ('Wrongful Death', 'Your city')]}},
    {'h': 'Answer Real Questions', 'p': 'Short articles and videos built around client questions feed both Google and AI search.',
     'v': {'kind': 'chat', 'title': 'AI assistant', 'q': 'What should I do after a car accident?', 'a': 'Here is a helpful guide from Your Firm.'}},
    {'h': 'Know Your Limit', 'p': 'Suspensions, filters and stalled rankings are where do-it-yourself marketing usually needs expert help.',
     'v': {'kind': 'shield', 'chips': ['Suspended listing', 'Filtered profile', 'Stalled rankings']}},
  ],
  'cta': CTA('Not Sure Which Ideas Will Work in Your Market?', 'Get a free audit that shows which ideas will help your firm first.'),
},
'how-to-get-personal-injury-clients': {
  'title': 'Getting More Injury Clients in 60 Seconds',
  'sub': 'The channels that actually sign cases.',
  'scenes': [
    {'kind': 'answer', 'h': 'Clients Come From Search, Ads and Referrals',
     'p': 'The fastest growing firms rank in the Map Pack, answer every call fast, and ask happy clients for reviews.',
     'v': {'kind': 'sources', 'title': 'Where injury clients come from', 'items': [('Google', 100), ('Ads', 55), ('Referrals', 45), ('AI search', 20)], 'tag': 'Illustrative example'}},
    {'h': 'Search First', 'p': 'Injured people search on Google when they are ready to hire, so the Map Pack and top results take most of the calls.',
     'v': {'kind': 'search', 'q': 'personal injury lawyer near me', 'results': [('Your Firm', True), ('Main Street Injury Law', False), ('Accident Law Center', False)]}},
    {'h': 'Ads for Speed', 'p': 'PPC and Local Services Ads buy visibility in days, but you pay for every click or lead.',
     'v': {'kind': 'timeline', 'title': 'Ads vs SEO', 'points': [('Day 1', 'Ads go live', 0), ('Month 3', 'SEO builds', 50), ('Month 6+', 'Calls keep coming', 100)], 'tag': 'Illustrative timeline'}},
    {'h': 'Referrals Compound', 'p': 'Past clients and other lawyers send the cheapest, best-qualified cases.',
     'v': {'kind': 'stars', 'tag': 'Happy clients send friends', 'reviews': ['I sent my brother to them too.', 'Best decision after my accident.']}},
    {'h': 'Intake Decides', 'p': 'The firm that answers first usually signs the client.',
     'v': {'kind': 'race', 'fast': ('Your firm answers first', 'Case signed'), 'slow': ('Another firm calls back later', 'Too late')}},
    {'h': 'One Measure', 'p': 'Compare every channel by cost per signed case and fees, not by leads or traffic.',
     'v': {'kind': 'compare', 'cols': ['Leads', 'Cases'], 'rows': [('Shows what works', (False, True)), ('Ties to fees', (False, True)), ('Fair across channels', (False, True))]}},
  ],
  'cta': CTA('Where Are Your Next Cases Coming From?', 'Get a free audit of the searches where clients find other firms.'),
},
'how-personal-injury-lawyers-rank-in-the-google-map-pack': {
  'title': 'Ranking in the Map Pack in 60 Seconds',
  'sub': 'How injury firms reach the top three on Google Maps.',
  'scenes': [
    {'kind': 'answer', 'h': 'Relevance, Prominence and Proximity',
     'p': 'The right category and pages, consistent listings and reviews, and a verified address close to the searcher.',
     'v': {'kind': 'map', 'names': ['Your Firm', 'Injury Law Partners', 'Accident Attorneys']}},
    {'h': 'Category First', 'p': 'Use "Personal injury attorney" as the primary Google Business Profile category.',
     'v': {'kind': 'checklist', 'title': 'Google Business Profile', 'items': ['Primary category set', 'Hours and phone', 'Photos and posts']}},
    {'h': 'Consistent Listings', 'p': 'Keep your name, address and phone the same on Avvo, Justia, FindLaw and every other directory.',
     'v': {'kind': 'compare', 'cols': ['Before', 'After'], 'rows': [('Avvo', (False, True)), ('Justia', (True, True)), ('FindLaw', (False, True))]}},
    {'h': 'Steady Reviews', 'p': 'Ask every satisfied client, steadily, and reply to every review.',
     'v': {'kind': 'stars', 'tag': 'Ask every happy client', 'reviews': ['They fought hard for my family.', 'Thank you for the kind words!']}},
    {'h': 'Focused Pages', 'p': 'Build one short landing page per case type and service area.',
     'v': {'kind': 'pages', 'pages': [('Car Accidents', 'Your city'), ('Truck Accidents', 'Your city'), ('Car Accidents', 'Nearby city'), ('Slip and Fall', 'Your city')]}},
    {'h': 'The Timeline', 'p': 'First appearances often come in 30 to 60 days, and the top 3 typically in 60 to 120 days.',
     'v': {'kind': 'timeline', 'title': 'Typical Map Pack timeline', 'points': [('Day 1', 'Profile fixed', 0), ('30 to 60 days', 'First appearances', 50), ('60 to 120 days', 'Top 3', 100)], 'tag': 'Typical results, not a guarantee'}},
  ],
  'cta': CTA('Where Does Your Firm Rank in the Map Pack Today?', 'Get a free audit of what it would take to reach the top 3.'),
},
'seo-roi-case-studies-personal-injury-attorneys': {
  'title': 'SEO ROI for Injury Firms in 60 Seconds',
  'sub': 'What the numbers from real case studies show.',
  'scenes': [
    {'kind': 'answer', 'h': 'Fees From Search, Minus the Cost of SEO',
     'p': 'SEO ROI is the fee revenue from cases signed through search, minus the SEO cost, divided by that cost.',
     'v': {'kind': 'split', 'title': 'How SEO ROI works', 'parts': [('Attributed fees', 8, G), ('SEO cost', 1, K)], 'tag': 'Measured over 12 months'}},
    {'h': 'The Formula', 'p': 'SEO ROI equals attributed fees minus SEO cost, divided by SEO cost, measured over 12 months.',
     'v': {'kind': 'checklist', 'title': 'What you need', 'items': ['Fees from search cases', 'What SEO cost', '12 months of data']}},
    {'h': 'Manhattan', 'p': 'Page 3 to #1 in the Map Pack in 118 days, 61% more qualified intakes and $3.2M in attributed fees.',
     'v': {'kind': 'timeline', 'title': 'Manhattan PI firm', 'points': [('Day 1', 'Page 3', 0), ('Day 118', '#1 Map Pack', 50), ('12 months', '$3.2M fees', 100)]}},
    {'h': 'Rosedale, New York', 'p': '#1 Map Pack average, 118% more qualified intakes and $5.2M in attributed fees over 12 months.',
     'v': {'kind': 'sources', 'title': 'Qualified intakes', 'items': [('Before', 46), ('After', 100)], 'tag': '+118% qualified intakes'}},
    {'h': 'A New York City Snapshot', 'p': 'Up 12 positions in 30 days to #1 in the Map Pack, with calls up 75% and 184 qualified leads.',
     'v': {'kind': 'map', 'names': ['Our Client', 'Competitor A', 'Competitor B']}},
    {'h': 'Measure Cases', 'p': 'Track calls and forms through intake to signed cases and fees, not traffic.',
     'v': {'kind': 'sources', 'title': 'Follow the lead through', 'items': [('Calls', 100), ('Intakes', 70), ('Signed', 45), ('Fees', 85)], 'tag': 'Illustrative example'}},
  ],
  'cta': CTA('What Could Search Be Worth to Your Firm?', 'Get a free audit and an estimate of the cases you are missing.'),
},
'why-seo-for-personal-injury-lawyers-matters': {
  'title': 'Why SEO Matters for Injury Lawyers',
  'sub': 'And how to judge an SEO proposal, in about a minute.',
  'scenes': [
    {'kind': 'answer', 'h': 'Injured People Search When Ready to Hire',
     'p': 'They usually call one of the first firms they see, and rankings keep producing calls without a per-click charge.',
     'v': {'kind': 'search', 'q': 'injury lawyer near me', 'results': [('Your Firm', True), ('Injury Law Group', False), ('Accident Lawyers', False)]}},
    {'h': 'Intent', 'p': 'People searching for an injury lawyer are ready to hire, often within hours.',
     'v': {'kind': 'race', 'fast': ('Search to first call', 'Within hours'), 'slow': ('Other marketing', 'Weeks or months')}},
    {'h': 'Position', 'p': 'The Map Pack and the first few organic results take most of the calls.',
     'v': {'kind': 'map', 'names': ['Your Firm', 'Injury Law Group', 'Accident Lawyers']}},
    {'h': 'Economics', 'p': 'Rankings keep producing calls without a per-click bill, so cost per case falls over time.',
     'v': {'kind': 'sources', 'title': 'Cost per signed case', 'items': [('Month 1', 100), ('Month 6', 60), ('Month 12', 35)], 'tag': 'Illustrative example'}},
    {'h': 'Mix', 'p': 'SEO works best alongside PPC and Local Services Ads, not instead of them.',
     'v': {'kind': 'split', 'title': 'Example mix', 'parts': [('SEO and Map Pack', 5, G), ('PPC', 3, K), ('Local Services Ads', 2, S)], 'tag': 'Illustrative example'}},
    {'h': 'Proposals', 'p': 'Judge an SEO proposal on exclusivity, deliverables, reporting on signed cases and real results.',
     'v': {'kind': 'compare', 'cols': ['A', 'B'], 'rows': [('Exclusive in your city', (True, False)), ('Clear deliverables', (True, False)), ('Reports signed cases', (True, False))]}},
  ],
  'cta': CTA('Is Your Firm Visible When Injured People Search?', 'Get a free audit of your Map Pack and organic rankings.'),
},
}


# ---------- build step ----------
def main():
    import os, sys
    root = sys.argv[1] if len(sys.argv) > 1 else 'public'
    css, js = assets()
    css = css.replace('<style>', '<style id="xp-css">', 1)
    js = js.replace('<script>', '<script id="xp-js">', 1)
    done = skipped = 0
    for slug, spec in SPECS.items():
        path = os.path.join(root, 'blog', slug + '.html')
        if not os.path.exists(path):
            alt = os.path.join(root, 'blog', slug, 'index.html')
            if not os.path.exists(alt):
                sys.exit(f'explainer_patch: missing page for {slug}')
            path = alt
        h = open(path, encoding='utf-8').read()
        if 'id="xp-css"' in h:
            skipped += 1
            continue
        anchor = '<aside class="aio"'
        if h.count(anchor) != 1 or h.count('</head>') != 1 or h.count('</body>') != 1:
            sys.exit(f'explainer_patch: unexpected page structure in {path}')
        block = render({'slug': 'blog/' + slug}, spec)
        h = h.replace(anchor, block + anchor, 1).replace('</head>', css + '</head>', 1).replace('</body>', js + '</body>', 1)
        open(path, 'w', encoding='utf-8').write(h)
        done += 1
    print(f'explainer_patch: added {done}, already had {skipped}, total {len(SPECS)}')


if __name__ == '__main__':
    main()
