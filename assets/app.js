(function(){
  var root=document.documentElement;
  function store(k,v){try{if(v===undefined)return localStorage.getItem(k);localStorage.setItem(k,v)}catch(e){return null}}

  /* theme: diya (dark) mode */
  if(store('sa-theme')==='diya') root.setAttribute('data-theme','diya');
  document.addEventListener('click',function(e){
    var t=e.target.closest('[data-act]'); if(!t) return;
    var a=t.getAttribute('data-act');
    if(a==='theme'){var on=root.getAttribute('data-theme')==='diya';
      if(on){root.removeAttribute('data-theme');store('sa-theme','paper')}else{root.setAttribute('data-theme','diya');store('sa-theme','diya')}}
    if(a==='bigger'||a==='smaller'){var f=parseFloat(getComputedStyle(root).getPropertyValue('--fs'))||1;
      f=Math.min(1.6,Math.max(.8,f+(a==='bigger'?.1:-.1)));root.style.setProperty('--fs',f.toFixed(2));store('sa-fs',f.toFixed(2))}
    if(a==='layer'){var c=t.getAttribute('data-l');root.classList.toggle('no-'+c);t.classList.toggle('on');
      store('sa-hide-'+c,root.classList.contains('no-'+c)?'1':'0')}
  });
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

  /* diya drawn from the syllables of the aarti */
  var cv=document.getElementById('diya');
  if(cv && cv.getContext){
    var ctx=cv.getContext('2d'),W,H,dpr,pts=[],sparks=[],sprites={},t0=performance.now(),running=false;
    var reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
    var SYL=['ॐ','ज','य','ज','ग','दी','श','ह','रे','स्वा','मी','आ','र','ती','दी','प','शु','भ','क','रो','ति','रा','म','शि','व','श्री','गं','ॐ','ल','क्ष्मी','मा','ता'];
    var bodyCol,flameCol,glowCol;
    function sprite(txt,col,px){var c=document.createElement('canvas'),g=c.getContext('2d');var w=Math.ceil(px*2.2),h=Math.ceil(px*1.9);
      c.width=w*dpr;c.height=h*dpr;g.scale(dpr,dpr);g.font=px+"px 'Tiro Devanagari Hindi','Noto Serif Devanagari',serif";g.textAlign='center';g.textBaseline='middle';
      g.fillStyle=col;g.strokeStyle=col;g.lineWidth=Math.max(.35,px*.045);g.fillText(txt,w/2,h/2+px*.08);g.strokeText(txt,w/2,h/2+px*.08);c.w=w;c.h=h;return c;}
    function colors(){var cs=getComputedStyle(root);var dark=root.getAttribute('data-theme')==='diya';
      bodyCol=dark?'#E9B872':cs.getPropertyValue('--maroon').trim();flameCol=cs.getPropertyValue('--accent').trim();glowCol=cs.getPropertyValue('--flame').trim();
      if(W)makeSprites();}
    function makeSprites(){sprites={b:[],f:[],g:[]};var px=build.px||10;
      SYL.forEach(function(t){sprites.b.push(sprite(t,bodyCol,px));sprites.f.push(sprite(t,flameCol,px*1.05));sprites.g.push(sprite(t,glowCol,px*1.05));});}
    function build(){
      dpr=Math.min(2,window.devicePixelRatio||1);var r=cv.getBoundingClientRect();W=Math.round(r.width);H=Math.round(r.height);if(!W||!H)return;
      cv.width=W*dpr;cv.height=H*dpr;
      var o=document.createElement('canvas');o.width=W;o.height=H;var g=o.getContext('2d');var s=Math.min(W/500,H/460),cx=W/2-68*s,cy=H/2+20*s;
      g.fillStyle='#000';
      g.beginPath();g.moveTo(cx-160*s,cy);g.bezierCurveTo(cx-150*s,cy+185*s,cx+120*s,cy+185*s,cx+175*s,cy+10*s);
      g.quadraticCurveTo(cx+215*s,cy-12*s,cx+238*s,cy-40*s);g.quadraticCurveTo(cx+188*s,cy-14*s,cx+150*s,cy-4*s);
      g.lineTo(cx-160*s,cy);g.fill();
      g.beginPath();g.ellipse(cx,cy+172*s,64*s,12*s,0,0,Math.PI*2);g.fill();g.fillRect(cx-24*s,cy+120*s,48*s,52*s);
      var dataB=g.getImageData(0,0,W,H).data;g.clearRect(0,0,W,H);
      g.beginPath();var fx=cx+238*s,fy=cy-44*s;g.moveTo(fx,fy-185*s);g.bezierCurveTo(fx+62*s,fy-80*s,fx+44*s,fy+4*s,fx,fy+6*s);
      g.bezierCurveTo(fx-44*s,fy+4*s,fx-62*s,fy-80*s,fx,fy-185*s);g.fill();var dataF=g.getImageData(0,0,W,H).data;
      var step=Math.max(9,13*s);build.px=Math.max(8.5,step*.95);pts=[];var k=0;
      for(var y=step/2;y<H;y+=step*.86)for(var x=step/2;x<W;x+=step){var i=(Math.round(y)*W+Math.round(x))*4;
        if(dataB[i+3]>10){var shade=Math.min(1,Math.max(0,(y-cy)/(160*s)));pts.push({x:x,y:y,f:0,a:1-.45*shade,i:(k++)%SYL.length})}
        else if(dataF[i+3]>10){pts.push({x:x,y:y,f:1,a:.75+.25*Math.random(),ph:Math.random()*6.28,by:y,i:(k++)%SYL.length,hot:(y-(fy-185*s))/(191*s)})}}
      sparks=[];for(var q=0;q<46;q++)sparks.push(spark(fx,fy,s,true));
      build.fx=fx;build.fy=fy;build.s=s;build.cx=cx;build.cy=cy;makeSprites();}
    function spark(fx,fy,s,init){return{x:fx+(Math.random()-.5)*40*s,y:init?fy-200*s-Math.random()*(fy-200*s):fy-175*s,vy:-(.25+Math.random()*.6)*s,vx:(Math.random()-.5)*.35*s,life:Math.random(),r:.7+Math.random()*1.3}}
    function draw(now){var t=(now-t0)/1000,s=build.s;ctx.setTransform(dpr,0,0,dpr,0,0);ctx.clearRect(0,0,W,H);
      var gx=build.fx,gy=build.fy-80*s,gr=Math.min(250*s,W-gx,gx,gy,H-gy);var gl=ctx.createRadialGradient(gx,gy,0,gx,gy,Math.max(10,gr));
      gl.addColorStop(0,'rgba(255,170,60,'+(root.getAttribute('data-theme')==='diya'?.30:.16)+')');gl.addColorStop(1,'rgba(255,170,60,0)');
      ctx.fillStyle=gl;ctx.fillRect(0,0,W,H);
      for(var i=0;i<pts.length;i++){var p=pts[i],sp;
        if(p.f){var fl=Math.sin(t*3+p.ph)*1.6*s+Math.sin(t*7.3+p.ph*2)*.8*s;var lift=1-p.hot;sp=(p.hot<.55?sprites.g:sprites.f)[p.i];
          ctx.globalAlpha=p.a*(.75+.25*Math.sin(t*5+p.ph));ctx.drawImage(sp,p.x-sp.w/2+fl*lift*1.6,p.y-sp.h/2-Math.abs(fl)*lift,sp.w,sp.h);}
        else{sp=sprites.b[p.i];ctx.globalAlpha=p.a;ctx.drawImage(sp,p.x-sp.w/2,p.y-sp.h/2,sp.w,sp.h);}}
      ctx.fillStyle=glowCol;
      for(var j=0;j<sparks.length;j++){var q=sparks[j];if(!reduce){q.x+=q.vx+Math.sin(t*1.3+j)*.15;q.y+=q.vy;q.life+=.003;}
        ctx.globalAlpha=Math.max(0,1-q.life)*.8;ctx.beginPath();ctx.arc(q.x,q.y,q.r,0,6.28);ctx.fill();
        if(q.life>1||q.y<0){sparks[j]=spark(build.fx,build.fy,s,false);sparks[j].life=0}}
      ctx.globalAlpha=1;}
    function loop(now){draw(now);if(!reduce&&!document.hidden)requestAnimationFrame(loop);else running=false;}
    function start(){if(running&&!reduce)return;running=true;requestAnimationFrame(loop);}
    function go(){colors();build();start();}
    (document.fonts&&document.fonts.load?document.fonts.load("20px 'Tiro Devanagari Hindi'").then(go,go):go());
    var rt;window.addEventListener('resize',function(){clearTimeout(rt);rt=setTimeout(function(){build();start();},150)});
    document.addEventListener('visibilitychange',function(){if(!document.hidden)start();});
    new MutationObserver(function(){colors();start();}).observe(root,{attributes:true,attributeFilter:['data-theme']});
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
