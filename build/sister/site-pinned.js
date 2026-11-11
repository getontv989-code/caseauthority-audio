(function(){
  var html=document.documentElement,hdr=document.querySelector('.hdr');
  function onScroll(){hdr.classList.toggle('dark',window.scrollY>40)}
  window.addEventListener('scroll',onScroll,{passive:true});onScroll();

  /* Mobile menu */
  var b=document.getElementById('burger'),m=document.getElementById('mnav'),c=document.getElementById('mclose');
  function setNav(open){m.hidden=!open;b.setAttribute('aria-expanded',String(open));document.body.style.overflow=open?'hidden':''}
  b.addEventListener('click',function(){setNav(true);c.focus()});
  c.addEventListener('click',function(){setNav(false);b.focus()});
  m.addEventListener('click',function(e){if(e.target.closest('a'))setNav(false)});

  /* Desktop dropdowns: hover/focus open via CSS; keep aria-expanded honest, Esc closes */
  document.querySelectorAll('.nav .dd').forEach(function(dd){
    var btn=dd.querySelector('button');
    function set(v){btn.setAttribute('aria-expanded',String(v));dd.classList.toggle('closed',!v)}
    dd.addEventListener('mouseenter',function(){set(true)});
    dd.addEventListener('mouseleave',function(){set(false)});
    dd.addEventListener('focusin',function(){set(true)});
    dd.addEventListener('focusout',function(e){if(!dd.contains(e.relatedTarget))set(false)});
    btn.addEventListener('click',function(){set(btn.getAttribute('aria-expanded')!=='true')});
  });
  document.addEventListener('keydown',function(e){
    if(e.key!=='Escape')return;
    if(!m.hidden){setNav(false);b.focus();return}
    var open=document.querySelector('.nav .dd button[aria-expanded="true"]');
    if(open){open.setAttribute('aria-expanded','false');open.closest('.dd').classList.add('closed');open.focus()}
  });


  /* Forms: validate, then POST to /api/contact (our own SMTP function) */
  var FAIL='Sorry, that didn’t send. Please try again, or email sales@seopersonalinjurylawyer.com.';
  function sendForm(f,ok,err,btn){
    var data={};[].forEach.call(f.elements,function(i){if(i.name&&i.type!=='submit')data[i.name]=i.value.trim()});
    if(!err.dataset.msg)err.dataset.msg=err.textContent;
    btn.disabled=true;f.setAttribute('aria-busy','true');
    return fetch('/api/contact',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)})
      .then(function(r){if(!r.ok)throw 0;ok.hidden=false;err.hidden=true;f.reset();return 'Sent. CaseAuthority has the details and will reply within one business day.'})
      .catch(function(){err.textContent=FAIL;err.hidden=false;ok.hidden=true;return 'Not sent: '+FAIL})
      .then(function(m){btn.disabled=false;f.removeAttribute('aria-busy');return m});
  }
  /* WebMCP: when an AI agent submits a form as a tool, hand it the outcome */
  function reply(e,p){if(e.agentInvoked&&e.respondWith)e.respondWith(Promise.resolve(p))}
  function bad(err){if(err.dataset.msg)err.textContent=err.dataset.msg}
  var af=document.getElementById('auditForm');
  if(af)af.addEventListener('submit',function(e){e.preventDefault();var ok=document.getElementById('formOk'),er=document.getElementById('formErr'),v=af.email.checkValidity()&&af.email.value;af.email.setAttribute('aria-invalid',String(!v));if(!v){bad(er);er.hidden=false;ok.hidden=true;af.email.focus();reply(e,'Not sent: a valid work email is required.');return}reply(e,sendForm(af,ok,er,af.querySelector('button[type=submit]')))});
  document.querySelectorAll('.lead-form').forEach(function(f){
    f.addEventListener('submit',function(e){
      e.preventDefault();
      var n=f.elements.name,em=f.elements.email,first=null,ok=f.querySelector('.ok'),er=f.querySelector('.err');
      [n,em].forEach(function(i){var v=i.value.trim()&&i.checkValidity();i.setAttribute('aria-invalid',String(!v));if(!v&&!first)first=i});
      if(first){bad(er);er.hidden=false;ok.hidden=true;first.focus();reply(e,'Not sent: a name and a valid email address are required.');return}
      reply(e,sendForm(f,ok,er,f.querySelector('button[type=submit]')));
    });
  });
  var pk=new URLSearchParams(location.search).get('package');
  if(pk){var mk=document.querySelector('.lead-form textarea');if(mk&&!mk.value)mk.value='Interested in the '+pk.charAt(0).toUpperCase()+pk.slice(1)+' package.'}

  /* ---------- Motion ---------- */
  function hideHeader(){var last=0;window.addEventListener('scroll',function(){var y=window.scrollY;if(!m.hidden)return;hdr.classList.toggle('hide',y>last&&y>480);last=y},{passive:true})}
  if(!window.gsap||!window.ScrollTrigger){html.classList.remove('m');return}
  gsap.registerPlugin(ScrollTrigger);
  var EXPO='expo.out';

  function split(el){
    if(el.dataset.split)return el.querySelectorAll('.wi');el.dataset.split='1';
    (function walk(node){[].slice.call(node.childNodes).forEach(function(n){
      if(n.nodeType===3){var frag=document.createDocumentFragment();n.textContent.split(/(\s+)/).forEach(function(t){
        if(!t)return;if(/^\s+$/.test(t)){frag.appendChild(document.createTextNode(t));return}
        var w=document.createElement('span');w.className='w';var i=document.createElement('span');i.className='wi';i.textContent=t;w.appendChild(i);frag.appendChild(w)});
        n.parentNode.replaceChild(frag,n)}
      else if(n.nodeType===1&&!n.classList.contains('w'))walk(n)})})(el);
    return el.querySelectorAll('.wi')}

  function counter(el,delay){
    var raw=el.textContent.trim();if(/→|–|\//.test(raw))return;
    var mt=raw.match(/^([^\d]*?)(\d[\d,]*(?:\.\d+)?)(.*)$/);if(!mt)return;
    var pre=mt[1],num=parseFloat(mt[2].replace(/,/g,'')),suf=mt[3],dec=(mt[2].split('.')[1]||'').length,rank=pre==='#';
    var o={v:rank?30:0};el.style.minWidth=el.offsetWidth+'px';
    gsap.to(o,{v:num,duration:rank?1.6:1.8,delay:delay||0,ease:rank?'power3.out':EXPO,
      onUpdate:function(){var v=dec?o.v.toFixed(dec):Math.round(o.v).toLocaleString('en-US');if(/^0\d/.test(mt[2]))v=String(v).padStart(mt[2].length,'0');el.textContent=pre+v+suf},
      onComplete:function(){el.textContent=raw}});
  }
  function countIn(els,trigger,stagger){
    els=gsap.utils.toArray(els);if(!els.length)return;
    ScrollTrigger.create({trigger:trigger||els[0],start:'top 85%',once:true,onEnter:function(){els.forEach(function(el,i){counter(el,i*(stagger||.08))})}});
  }

  /* Scroll-driven motion is only built once the reader engages (scroll, touch, key, click), so measuring every
     trigger never lands in the first seconds of page load. Hero motion runs straight away. */
  function engaged(fn){var ev=['scroll','wheel','touchstart','pointerdown','keydown'],done=0;
    function go(){if(done)return;done=1;ev.forEach(function(e){removeEventListener(e,go,true)});fn()}
    ev.forEach(function(e){addEventListener(e,go,{capture:true,passive:true})});if(window.scrollY>0||location.hash)go()}
  gsap.matchMedia().add({motion:'(prefers-reduced-motion: no-preference)',fine:'(hover: hover) and (pointer: fine)'},function(ctx){
    if(!ctx.conditions.motion){html.classList.remove('m');return}
    hideHeader();

    /* 1. Page hero: headline words rise, the render assembles, the short answer lands */
    var h1=document.querySelector('.phero h1');
    if(h1&&document.querySelector('.phero-copy')){
      var tl=gsap.timeline({defaults:{ease:EXPO}});
      tl.fromTo('.phero-art',{opacity:0,clipPath:'inset(10% 8% 0% 8%)'},{opacity:1,clipPath:'inset(0% 0% 0% 0%)',duration:1.3,ease:'expo.inOut'},0)
        .fromTo('.ha-bowl',{y:50,opacity:0},{y:0,opacity:1,duration:1.1},'<.3')
        .fromTo('.ha-orb',{scale:.6,opacity:0,svgOrigin:'280 222'},{scale:1,opacity:1,duration:1.1,ease:'back.out(1.5)'},'<.15')
        .fromTo('.ha-sh',{scale:.3,opacity:0,svgOrigin:'280 342'},{scale:1,opacity:.4,duration:.9},'<.1')
        .fromTo('.ha-pin',{y:-220},{y:0,duration:1.1,ease:'back.out(1.5)'},'<.1')
        .fromTo('.ha-f',{scale:.5,opacity:0,transformOrigin:'50% 50%'},{scale:1,opacity:1,duration:.9,stagger:.08,ease:'back.out(1.8)'},'<.1')
        .fromTo('.ha-badge',{scale:.7,opacity:0,transformOrigin:'0% 100%'},{scale:1,opacity:1,duration:.6,ease:'back.out(2)'},'<.25')
        .add(function(){
          gsap.to('.ha-pin',{y:-10,duration:2.6,ease:'sine.inOut',yoyo:true,repeat:-1});
          gsap.to('.ha-orb',{y:-8,duration:3.2,ease:'sine.inOut',yoyo:true,repeat:-1});
          gsap.utils.toArray('.ha-f').forEach(function(g,i){gsap.to(g,{y:i%2?10:-10,duration:2.4+i*.4,ease:'sine.inOut',yoyo:true,repeat:-1,delay:i*.2})});
        });
      if(ctx.conditions.fine){
        var art=document.querySelector('.phero-art'),fl=gsap.utils.toArray('.ha-f').map(function(g){var d=parseFloat(g.dataset.d)||1;return {d:d,x:gsap.quickTo(g,'x',{duration:.9,ease:'power3.out'})}});
        var ox=gsap.quickTo('.ha-orb','x',{duration:1.1,ease:'power3.out'});
        art.addEventListener('pointermove',function(e){var r=art.getBoundingClientRect(),nx=(e.clientX-r.left)/r.width-.5;fl.forEach(function(o){o.x(nx*-30*o.d)});ox(nx*12)});
        art.addEventListener('pointerleave',function(){fl.forEach(function(o){o.x(0)});ox(0)});
      }
    }

    engaged(function(){ctx.add(function(){
    /* 2. Section tint follows the reader */
    gsap.utils.toArray('main [data-tint]').forEach(function(s){
      ScrollTrigger.create({trigger:s,start:'top 55%',end:'bottom 55%',onToggle:function(self){if(self.isActive)gsap.to(document.body,{backgroundColor:s.dataset.tint,duration:.6,ease:'power2.out',overwrite:true})}});
    });

    /* 3. Headings rise word by word */
    gsap.utils.toArray('main section:not(.phero) h2.t-h2, footer h2').forEach(function(h){
      gsap.from(split(h),{yPercent:110,duration:1.05,ease:EXPO,stagger:.035,scrollTrigger:{trigger:h,start:'top 86%',once:true}});
    });
    gsap.utils.toArray('.sec-intro, .case-band .eyebrow, .cb-body').forEach(function(e){
      gsap.from(e,{opacity:0,y:12,duration:.9,ease:EXPO,scrollTrigger:{trigger:e,start:'top 88%',once:true}});
    });

    /* 4. Stats: rules draw, numbers count */
    if(document.querySelector('main .stats')){
      gsap.from('main .stat',{opacity:0,y:20,duration:1,ease:EXPO,stagger:.08,scrollTrigger:{trigger:'main .stats',start:'top 88%',once:true}});
      gsap.fromTo('main .stat',{'--s':0},{'--s':1,duration:1.1,ease:EXPO,stagger:.1,scrollTrigger:{trigger:'main .stats',start:'top 88%',once:true}});
      countIn('main .stat b','main .stats',.1);
    }

    /* 5. Content blocks arrive in sequence */
    [['.cards','.card',{y:28}],['.srows','.srow',{x:-24}],['.checks','li',{x:-16}],['.prose','p',{y:14}],['.rels','.rel',{y:20}],['.cmp-wrap','tr',{y:10}],['.study-toc','a',{y:10}],['.acc','details',{y:12}]].forEach(function(r){
      gsap.utils.toArray(r[0]).forEach(function(box){
        var items=box.querySelectorAll(r[1]);if(!items.length)return;
        gsap.from(items,Object.assign({opacity:0,duration:.9,ease:EXPO,stagger:.07,scrollTrigger:{trigger:box,start:'top 85%',once:true}},r[2]));
      });
    });
    gsap.utils.toArray('.srow .sn').forEach(function(n){countIn([n],n)});
    gsap.utils.toArray('.cdot').forEach(function(d){gsap.from(d,{scale:0,duration:.6,ease:'back.out(2.4)',scrollTrigger:{trigger:d,start:'top 88%',once:true}})});

    /* 6. Case band: metrics count once the band is in view */
    gsap.utils.toArray('.case-band').forEach(function(band){
      gsap.from(band.querySelectorAll('.cb-mets>div'),{opacity:0,y:24,duration:1,ease:EXPO,stagger:.08,scrollTrigger:{trigger:band,start:'top 75%',once:true}});
      countIn(band.querySelectorAll('.cb-mets b'),band,.1);
    });

    /* 7. Case studies: each study's results count as it arrives */
    gsap.utils.toArray('.study').forEach(function(st){
      var t=gsap.timeline({scrollTrigger:{trigger:st,start:'top 78%',once:true}});
      t.from(st.querySelectorAll('.study-meta>*, .study-h, .study-main>p'),{opacity:0,y:18,duration:.9,ease:EXPO,stagger:.06})
       .from(st.querySelectorAll('.kr-list li'),{opacity:0,y:20,duration:.9,ease:EXPO,stagger:.07},'<.2')
       .add(function(){st.querySelectorAll('.kr-list b').forEach(function(b,i){counter(b,i*.08)})},'<');
    });
    })});
  });
})();
/* FAQs: opening one closes the others in the same group */
document.addEventListener('toggle',function(e){var d=e.target;if(d.tagName!=='DETAILS'||!d.open||d.classList.contains('mgrp'))return;[].forEach.call(d.parentElement.children,function(o){if(o!==d&&o.tagName==='DETAILS'&&o.open)o.open=false})},true);
/* Article contents: highlight the section being read */
(function(){var links=document.querySelectorAll('.post-toc a');if(!links.length||!('IntersectionObserver' in window))return;
var map={};links.forEach(function(a){map[a.getAttribute('href').slice(1)]=a});
var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){links.forEach(function(a){a.classList.remove('on')});var a=map[e.target.id];if(a)a.classList.add('on')}})},{rootMargin:'-30% 0px -60% 0px'});
document.querySelectorAll('.post-sec[id]').forEach(function(s){io.observe(s)})})();
/* Smooth in-page jumps without CSS smooth scrolling, which throws off ScrollTrigger's measurements */
document.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('a[href^="#"]');if(!a)return;var id=a.getAttribute('href');if(id.length<2)return;var t=document.querySelector(id);if(!t)return;e.preventDefault();t.scrollIntoView({behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth'});history.replaceState(null,'',id)});