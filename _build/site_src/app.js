(function(){
  var root=document.documentElement;
  function store(k,v){try{if(v===undefined)return localStorage.getItem(k);localStorage.setItem(k,v)}catch(e){return null}}

  /* theme: diya (dark) mode */
  if(store('sa-mode')==='paper') root.setAttribute('data-theme','paper');
  document.addEventListener('click',function(e){
    var t=e.target.closest('[data-act]'); if(!t) return;
    var a=t.getAttribute('data-act');
    if(a==='theme'){var paper=root.getAttribute('data-theme')==='paper';
      if(paper){root.removeAttribute('data-theme');store('sa-mode','diya')}else{root.setAttribute('data-theme','paper');store('sa-mode','paper')}lbl();}
    if(a==='bigger'||a==='smaller'){var f=parseFloat(getComputedStyle(root).getPropertyValue('--fs'))||1;
      f=Math.min(1.6,Math.max(.8,f+(a==='bigger'?.1:-.1)));root.style.setProperty('--fs',f.toFixed(2));store('sa-fs',f.toFixed(2))}
    if(a==='layer'){var c=t.getAttribute('data-l');root.classList.toggle('no-'+c);t.classList.toggle('on');
      store('sa-hide-'+c,root.classList.contains('no-'+c)?'1':'0')}
  });
  function lbl(){var p=root.getAttribute('data-theme')==='paper';document.querySelectorAll('[data-lbl]').forEach(function(b){var t=p?'diya mode':'day mode';b.textContent=b.dataset.lbl==='cap'?t.charAt(0).toUpperCase()+t.slice(1):t;});}
  lbl();
  var fs=store('sa-fs'); if(fs) root.style.setProperty('--fs',fs);
  ['h','t','m'].forEach(function(c){ if(store('sa-hide-'+c)==='1'){root.classList.add('no-'+c);
    var b=document.querySelector('[data-l="'+c+'"]'); if(b) b.classList.remove('on');}});

  /* reveal */
  var io='IntersectionObserver' in window? new IntersectionObserver(function(es){es.forEach(function(x){if(x.isIntersecting){x.target.classList.add('in');io.unobserve(x.target)}})},{rootMargin:'0px 0px -8% 0px'}):null;
  document.querySelectorAll('.reveal').forEach(function(el){io?io.observe(el):el.classList.add('in')});

  /* home list: filter, search, peek */
  var list=document.getElementById('list');
  if(list){
    var rows=[].slice.call(list.querySelectorAll('.row')), kind='all', deity='all', q='';
    var empty=document.getElementById('empty');
    function apply(){var n=0;rows.forEach(function(r){
      var ok=(kind==='all'||r.dataset.kind===kind)&&(deity==='all'||r.dataset.deity===deity)&&(!q||r.dataset.search.indexOf(q)>-1);
      r.classList.toggle('hide',!ok); if(ok){n++; r.querySelector('.num').textContent=(n<10?'0':'')+n;}});
      empty.style.display=n?'none':'block';}
    document.querySelectorAll('[data-kind]').forEach(function(b){if(b.tagName!=='BUTTON')return;b.addEventListener('click',function(){
      kind=b.dataset.kind;document.querySelectorAll('button[data-kind]').forEach(function(x){x.classList.toggle('on',x===b)});apply();})});
    document.querySelectorAll('button[data-deity]').forEach(function(b){b.addEventListener('click',function(){
      deity=b.dataset.deity;document.querySelectorAll('button[data-deity]').forEach(function(x){x.classList.toggle('on',x===b)});apply();})});
    var s=document.getElementById('q'); if(s) s.addEventListener('input',function(){q=s.value.trim().toLowerCase();apply();});
    var hq=document.getElementById('hq');
    if(hq){hq.addEventListener('input',function(){s.value=hq.value;q=hq.value.trim().toLowerCase();apply();});
      hq.addEventListener('keydown',function(e){if(e.key==='Enter'){e.preventDefault();hq.blur();document.getElementById('collection').scrollIntoView({behavior:'smooth'});}});}
    if(location.hash==='#search'){setTimeout(function(){document.getElementById('collection').scrollIntoView();(matchMedia('(max-width:860px)').matches?s:(hq||s)).focus();},60);}
    var params=new URLSearchParams(location.search); if(params.get('k')){var kb=document.querySelector('button[data-kind="'+params.get('k')+'"]'); if(kb) kb.click();}
    var peek=document.getElementById('peek'), pimg=peek&&peek.querySelector('img');
    if(peek && matchMedia('(hover:hover)').matches){
      rows.forEach(function(r){var src=r.dataset.img; r.addEventListener('mouseenter',function(){if(!src)return;pimg.src=src;peek.classList.add('show')});
        r.addEventListener('mouseleave',function(){peek.classList.remove('show')});
        r.addEventListener('mousemove',function(e){peek.style.left=(e.clientX+130)+'px';peek.style.top=e.clientY+'px'});});
    }
  }

  /* today's suggestion */
  var td=document.getElementById('today');
  if(td){var map=JSON.parse(td.getAttribute('data-map'));var d=new Date().getDay();var x=map[d];
    td.innerHTML='It is '+x[0]+', the day of '+x[1]+'. Begin with <a href="'+x[3]+'">'+x[2]+'</a>.';}

  /* stippled diya: dots flow away from the cursor or finger like liquid, then settle back */
  var cv=document.getElementById('diya');
  if(cv && cv.getContext){
    var ctx=cv.getContext('2d'),W,H,dpr,pts=[],sparks=[],t0=performance.now(),running=false,G={};
    var reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
    var ptr={x:-9999,y:-9999,vx:0,vy:0,on:false,t:0};
    var bodyCol,flameCol,coreCol,glowCol,shadowCol;
    function colors(){var cs=getComputedStyle(root);var dark=root.getAttribute('data-theme')!=='paper';
      bodyCol=dark?'#E7B677':'#5C1E00';shadowCol=dark?'#7A4A22':'#B9805A';
      flameCol=cs.getPropertyValue('--accent').trim()||'#FF9A3C';coreCol=dark?'#FFE7A8':'#F2A81D';glowCol=dark?'rgba(255,165,60,.32)':'rgba(242,140,40,.18)';}
    function build(){
      dpr=Math.min(2,window.devicePixelRatio||1);var r=cv.getBoundingClientRect();W=Math.round(r.width);H=Math.round(r.height);if(!W||!H)return;
      cv.width=W*dpr;cv.height=H*dpr;
      var o=document.createElement('canvas');o.width=W;o.height=H;var g=o.getContext('2d',{willReadFrequently:true});
      var s=Math.min(W/500,H/470),cx=W/2-60*s,cy=H/2+30*s;g.fillStyle='#000';
      // bowl with a lip and a pinched spout
      g.beginPath();g.moveTo(cx-168*s,cy-6*s);g.bezierCurveTo(cx-160*s,cy+150*s,cx+110*s,cy+165*s,cx+168*s,cy+12*s);
      g.quadraticCurveTo(cx+205*s,cy-6*s,cx+236*s,cy-36*s);g.quadraticCurveTo(cx+212*s,cy-30*s,cx+186*s,cy-16*s);
      g.quadraticCurveTo(cx,cy-30*s,cx-168*s,cy-6*s);g.fill();
      // stem and foot
      g.beginPath();g.moveTo(cx-22*s,cy+118*s);g.lineTo(cx+22*s,cy+118*s);g.lineTo(cx+34*s,cy+160*s);g.lineTo(cx-34*s,cy+160*s);g.fill();
      g.beginPath();g.ellipse(cx,cy+164*s,76*s,13*s,0,0,Math.PI*2);g.fill();
      var dataB=g.getImageData(0,0,W,H).data;g.clearRect(0,0,W,H);
      // oil surface (an inner ellipse, slightly lighter) for depth
      g.beginPath();g.ellipse(cx+8*s,cy-8*s,150*s,15*s,-.03,0,Math.PI*2);g.fill();var dataO=g.getImageData(0,0,W,H).data;g.clearRect(0,0,W,H);
      // flame: teardrop sitting on the wick at the spout tip
      var fx=cx+232*s,fy=cy-44*s;g.beginPath();g.moveTo(fx-4*s,fy-178*s);
      g.bezierCurveTo(fx+30*s,fy-120*s,fx+52*s,fy-40*s,fx+30*s,fy-6*s);g.bezierCurveTo(fx+16*s,fy+12*s,fx-18*s,fy+12*s,fx-30*s,fy-6*s);
      g.bezierCurveTo(fx-50*s,fy-40*s,fx-36*s,fy-110*s,fx-4*s,fy-178*s);g.fill();var dataF=g.getImageData(0,0,W,H).data;
      pts=[];var step=Math.max(2.6,3.3*s);
      for(var y=0;y<H;y+=step)for(var x=0;x<W;x+=step){var i=(Math.round(y)*W+Math.round(x))*4;
        var jx=x+(Math.random()-.5)*step*.9,jy=y+(Math.random()-.5)*step*.9;
        if(dataF[i+3]>10){if(Math.random()<.92){var hot=(jy-(fy-178*s))/(190*s);var core=Math.abs(jx-fx)<(10+18*hot)*s&&hot>.45;
            pts.push({hx:jx,hy:jy,x:jx,y:jy,vx:0,vy:0,f:1,core:core,r:.55+Math.random()*1.05,a:.55+.45*Math.random(),ph:Math.random()*6.28,hot:hot})}}
        else if(dataB[i+3]>10){var shade=Math.min(1,Math.max(0,(jy-(cy-10*s))/(170*s)));var lit=1-Math.min(1,Math.hypot(jx-fx,jy-fy)/(420*s));
          var oil=dataO[i+3]>10;if(Math.random()<(oil?.5:.8-.25*shade))
          pts.push({hx:jx,hy:jy,x:jx,y:jy,vx:0,vy:0,f:0,oil:oil,r:(.6+Math.random()*.95)*(.75+.45*shade),a:(oil?.35:.45)+.5*Math.random()*(1-.4*shade)+.15*lit})}}
      sparks=[];for(var k=0;k<60;k++)sparks.push(spark(fx,fy,s,true));
      G={fx:fx,fy:fy,s:s,cx:cx,cy:cy};}
    function spark(fx,fy,s,init){return{x:fx+(Math.random()-.5)*30*s,y:init?fy-170*s-Math.random()*(fy-170*s):fy-160*s,vy:-(.25+Math.random()*.6)*s,vx:(Math.random()-.5)*.35*s,life:Math.random(),r:.6+Math.random()*1.2}}
    function draw(now){var t=(now-t0)/1000,s=G.s;ctx.setTransform(dpr,0,0,dpr,0,0);ctx.clearRect(0,0,W,H);
      var gx=G.fx,gy=G.fy-70*s,gr=Math.min(240*s,W-gx,gx,gy,H-gy);if(gr>10){var gl=ctx.createRadialGradient(gx,gy,0,gx,gy,gr);
        gl.addColorStop(0,glowCol);gl.addColorStop(1,'rgba(255,165,60,0)');ctx.fillStyle=gl;ctx.fillRect(gx-gr,gy-gr,gr*2,gr*2);}
      ctx.globalAlpha=.08;ctx.fillStyle=shadowCol;ctx.beginPath();ctx.ellipse(G.cx,G.cy+170*s,200*s,12*s,0,0,6.28);ctx.fill();
      var R=90*s,R2=R*R,pon=ptr.on&&now-ptr.t<1400;
      for(var i=0;i<pts.length;i++){var p=pts[i];
        var tx=p.hx,ty=p.hy;
        if(p.f){var lift=1-p.hot;tx+=(Math.sin(t*3.1+p.ph)*1.5+Math.sin(t*7.7+p.ph*2)*.6)*s*lift*1.8;ty-=Math.abs(Math.sin(t*4+p.ph))*1.6*s*lift;}
        if(pon){var dx=p.x-ptr.x,dy=p.y-ptr.y,d2=dx*dx+dy*dy;
          if(d2<R2){var d=Math.sqrt(d2)||1,f=(1-d/R);f=f*f*2.4;p.vx+=dx/d*f+ptr.vx*.06*f-dy/d*f*.35;p.vy+=dy/d*f+ptr.vy*.06*f+dx/d*f*.35;}}
        p.vx+=(tx-p.x)*.045;p.vy+=(ty-p.y)*.045;p.vx*=.86;p.vy*=.86;p.x+=p.vx;p.y+=p.vy;
        if(p.f){ctx.fillStyle=p.core?coreCol:flameCol;ctx.globalAlpha=p.a*(.8+.2*Math.sin(t*6+p.ph));}
        else{ctx.fillStyle=bodyCol;ctx.globalAlpha=p.a;}
        ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,6.28);ctx.fill();}
      ctx.fillStyle=coreCol;
      for(var j=0;j<sparks.length;j++){var q=sparks[j];q.x+=q.vx+Math.sin(t*1.3+j)*.15;q.y+=q.vy;q.life+=.003;
        ctx.globalAlpha=Math.max(0,1-q.life)*.75;ctx.beginPath();ctx.arc(q.x,q.y,q.r,0,6.28);ctx.fill();
        if(q.life>1||q.y<0){sparks[j]=spark(G.fx,G.fy,s,false);sparks[j].life=0}}
      ctx.globalAlpha=1;ptr.vx*=.8;ptr.vy*=.8;}
    function loop(now){draw(now);if(!document.hidden&&(!reduce||ptr.on))requestAnimationFrame(loop);else running=false;}
    function start(){if(running)return;running=true;requestAnimationFrame(loop);}
    function move(e){var r=cv.getBoundingClientRect();var x=e.clientX-r.left,y=e.clientY-r.top;
      if(ptr.on){ptr.vx=x-ptr.x;ptr.vy=y-ptr.y;}ptr.x=x;ptr.y=y;ptr.on=true;ptr.t=performance.now();start();}
    cv.addEventListener('pointermove',move);cv.addEventListener('pointerdown',move);
    cv.addEventListener('pointerleave',function(){ptr.on=false;ptr.x=ptr.y=-9999});
    colors();build();start();
    var rt;window.addEventListener('resize',function(){clearTimeout(rt);rt=setTimeout(function(){build();start();},150)});
    document.addEventListener('visibilitychange',function(){if(!document.hidden)start();});
    new MutationObserver(function(){colors();start();if(reduce)requestAnimationFrame(draw);}).observe(root,{attributes:true,attributeFilter:['data-theme']});
  }

  /* add to home screen */
  var modal=document.getElementById('install'),deferred=null;
  var standalone=matchMedia('(display-mode: standalone)').matches||navigator.standalone;
  if(standalone) document.querySelectorAll('[data-act="install"]').forEach(function(b){b.style.display='none'});
  window.addEventListener('beforeinstallprompt',function(e){e.preventDefault();deferred=e;document.querySelectorAll('.go-install').forEach(function(b){b.style.display='flex'})});
  function tab(w){document.querySelectorAll('[data-tab]').forEach(function(b){b.classList.toggle('on',b.dataset.tab===w)});
    document.querySelectorAll('.panel').forEach(function(p){p.classList.toggle('on',p.id==='p-'+w)});}
  document.addEventListener('click',function(e){var b=e.target.closest('[data-act],[data-tab],.go-install');if(!b)return;
    if(b.dataset.act==='install'&&modal){e.preventDefault();modal.classList.add('open');tab(/iphone|ipad|ipod|macintosh/i.test(navigator.userAgent)&&'ontouchend' in document||/iphone|ipad|ipod/i.test(navigator.userAgent)?'ios':'android');}
    if(b.dataset.act==='close'&&modal)modal.classList.remove('open');
    if(b.dataset.tab)tab(b.dataset.tab);
    if(b.classList.contains('go-install')&&deferred){deferred.prompt();deferred.userChoice.then(function(){deferred=null});}
  });
  if(modal)modal.addEventListener('click',function(e){if(e.target===modal)modal.classList.remove('open')});

  if('serviceWorker' in navigator){navigator.serviceWorker.register('/sw.js').catch(function(){});}
})();
