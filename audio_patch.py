#!/usr/bin/env python3
"""Add the 'Listen to this article' player and AudioObject schema to built blog posts.

Runs after build.py (before split.py). Reads audio/manifest.json:
  {"<slug>": {"file": "/blog/audio/<slug>.mp3", "seconds": 1081, "bytes": 4300000, "date": "2026-11-05"}}
For each slug, patches public/blog/<slug>.html:
  - a small player under the post meta line. No audio bytes load until the reader presses play
    (the <audio> element is only created on click, preload none).
  - "audio": AudioObject on the page's BlogPosting node.
Fails the build if a manifest slug has no page, or a patched page lacks the player or schema.
Usage: audio_patch.py [public_dir] [manifest]
"""
import json, os, re, sys

SITE = 'https://seopersonalinjurylawyer.com'

CSS = """<style id="listen-css">.listen{display:flex;align-items:center;gap:14px;margin-top:22px;padding:10px 16px 10px 10px;border:1px solid var(--color-gray-100,#e6e6ea);border-radius:999px;background:#fff;max-width:560px}
.listen-btn{flex:none;width:44px;height:44px;border-radius:50%;border:0;background:var(--color-gray-900,#14161c);color:#fff;display:grid;place-items:center;cursor:pointer;transition:transform .15s,background .15s}
.listen-btn:hover{background:var(--acc,#333)}.listen-btn:active{transform:scale(.94)}.listen-btn:focus-visible,.listen-rate:focus-visible,.listen-bar:focus-visible{outline:2px solid var(--acc,#333);outline-offset:2px}
.listen-btn svg{width:18px;height:18px;fill:currentColor}.listen .i-pause{display:none}.listen.playing .i-play{display:none}.listen.playing .i-pause{display:block}
.listen-body{flex:1;min-width:0;display:grid;gap:4px}.listen-k{font-weight:700;font-size:15px;line-height:1.2;color:var(--color-gray-900,#14161c)}
.listen-t{font-size:13px;color:var(--color-gray-600,#666c7a);font-variant-numeric:tabular-nums}
.listen-bar{width:100%;height:4px;margin:4px 0 2px;accent-color:var(--acc,#333);cursor:pointer}.listen-bar[hidden],.listen-rate[hidden]{display:none}
.listen-rate{flex:none;font:inherit;font-size:13px;font-weight:700;min-width:46px;padding:6px 10px;border-radius:999px;border:1px solid var(--color-gray-100,#e6e6ea);background:#fff;cursor:pointer;color:var(--color-gray-900,#14161c)}
@media (prefers-reduced-motion:reduce){.listen-btn{transition:none}}</style>"""

JS = """<script>(function(){var b=document.querySelector('.listen');if(!b)return;var btn=b.querySelector('.listen-btn'),bar=b.querySelector('.listen-bar'),t=b.querySelector('.listen-t'),r=b.querySelector('.listen-rate'),a=null,rates=[1,1.25,1.5,2,.75],ri=0,key='listen:'+b.dataset.src;
function f(s){s=Math.max(0,Math.floor(s||0));return Math.floor(s/60)+':'+('0'+s%60).slice(-2)}
function upd(){if(!a)return;var d=a.duration||+b.dataset.sec;bar.max=d;bar.value=a.currentTime;t.textContent=f(a.currentTime)+' / '+f(d);try{localStorage.setItem(key,a.currentTime)}catch(e){}}
function init(){a=new Audio();a.preload='none';a.src=b.dataset.src;bar.hidden=false;r.hidden=false;
var p=0;try{p=+localStorage.getItem(key)||0}catch(e){}if(p>5&&p<+b.dataset.sec-10){a.currentTime=p}
a.addEventListener('timeupdate',upd);a.addEventListener('play',function(){b.classList.add('playing');btn.setAttribute('aria-label','Pause narration')});
a.addEventListener('pause',function(){b.classList.remove('playing');btn.setAttribute('aria-label','Play narration')});
a.addEventListener('ended',function(){try{localStorage.removeItem(key)}catch(e){}});
a.addEventListener('error',function(){t.textContent='Audio unavailable right now'});
if(window.dataLayer)dataLayer.push({event:'article_listen',article:location.pathname})}
btn.addEventListener('click',function(){if(!a)init();a.paused?a.play():a.pause()});
bar.addEventListener('input',function(){if(a)a.currentTime=+bar.value});
r.addEventListener('click',function(){ri=(ri+1)%rates.length;r.textContent=rates[ri]+'x';if(a)a.playbackRate=rates[ri]})})()</script>"""

ICON_PLAY = '<svg class="i-play" viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5.5v13l11-6.5z"/></svg>'
ICON_PAUSE = '<svg class="i-pause" viewBox="0 0 24 24" aria-hidden="true"><path d="M7 5h4v14H7zM13 5h4v14h-4z"/></svg>'


def iso(sec):
    m, s = divmod(int(sec), 60)
    return 'PT%dM%dS' % (m, s)


def player(a):
    mins = max(1, round(a['seconds'] / 60))
    return ('<div class="listen" data-src="%s" data-sec="%d">'
            '<button type="button" class="listen-btn" aria-label="Play narration">%s%s</button>'
            '<div class="listen-body"><span class="listen-k">Listen to this article</span>'
            '<input class="listen-bar" type="range" min="0" max="%d" step="1" value="0" aria-label="Seek narration" hidden>'
            '<span class="listen-t">%d min &middot; read by an AI voice</span></div>'
            '<button type="button" class="listen-rate" aria-label="Playback speed" hidden>1x</button></div>'
            % (a['file'], a['seconds'], ICON_PLAY, ICON_PAUSE, a['seconds'], mins))


def patch(html, slug, a):
    if 'class="listen"' in html:
        return html
    # 1) player right after the post meta line
    html, n = re.subn(r'(<p class="post-meta">.*?</p>)', lambda m: m.group(1) + player(a), html, count=1, flags=re.S)
    if n != 1:
        raise SystemExit('audio_patch: no post-meta in ' + slug)
    # 2) css in head, js before </body>
    html = html.replace('</head>', CSS + '</head>', 1).replace('</body>', JS + '</body>', 1)
    # 3) AudioObject on the BlogPosting node
    def add(m):
        data = json.loads(m.group(1))
        nodes = data.get('@graph', [data])
        bp = [x for x in nodes if x.get('@type') == 'BlogPosting']
        if not bp:
            raise SystemExit('audio_patch: no BlogPosting in ' + slug)
        bp = bp[0]
        bp['audio'] = {
            '@type': 'AudioObject',
            'name': 'Listen: ' + bp['headline'],
            'description': 'Audio version of this article, read by an AI voice.',
            'contentUrl': SITE + a['file'],
            'encodingFormat': 'audio/mpeg',
            'contentSize': '%.1f MB' % (a['bytes'] / 1e6),
            'duration': iso(a['seconds']),
            'uploadDate': a['date'],
            'inLanguage': 'en-US',
            'isAccessibleForFree': True,
        }
        return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False) + '</script>'
    html, n = re.subn(r'<script type="application/ld\+json">(\{.*?"BlogPosting".*?\})</script>', add, html, count=1, flags=re.S)
    if n != 1:
        raise SystemExit('audio_patch: no BlogPosting schema in ' + slug)
    return html


def main(pub='public', manifest='audio/manifest.json'):
    if not os.path.exists(manifest):
        print('audio_patch: no manifest, skipped'); return
    man = json.load(open(manifest))
    for slug, a in man.items():
        p = os.path.join(pub, 'blog', slug + '.html')
        if not os.path.exists(p):
            raise SystemExit('audio_patch: missing page for ' + slug)
        h = patch(open(p, encoding='utf-8').read(), slug, a)
        if h.count('class="listen"') != 1 or '"AudioObject"' not in h:
            raise SystemExit('audio_patch: check failed for ' + slug)
        open(p, 'w', encoding='utf-8').write(h)
    print('audio_patch: %d posts' % len(man))


if __name__ == '__main__':
    main(*sys.argv[1:])
