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

  /* stippled diya */
  var cv=document.getElementById('diya');
  if(cv && cv.getContext){
    var ctx=cv.getContext('2d'),W,H,dpr,pts=[],sparks=[],ink,acc,t0=performance.now();
    var reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
    function colors(){var cs=getComputedStyle(root);ink=cs.getPropertyValue('--ink').trim();acc=cs.getPropertyValue('--flame').trim();}
    function build(){
      dpr=Math.min(2,window.devicePixelRatio||1);var r=cv.getBoundingClientRect();W=Math.round(r.width);H=Math.round(r.height);cv.width=W*dpr;cv.height=H*dpr;
      var o=document.createElement('canvas');o.width=W;o.height=H;var g=o.getContext('2d');var s=Math.min(W,H)/520,cx=W/2,cy=H*0.63;
      g.fillStyle='#000';
      // bowl
      g.beginPath();g.moveTo(cx-170*s,cy-8*s);g.bezierCurveTo(cx-160*s,cy+128*s,cx+160*s,cy+128*s,cx+170*s,cy-8*s);
      g.quadraticCurveTo(cx+205*s,cy-26*s,cx+228*s,cy-36*s);g.quadraticCurveTo(cx+170*s,cy+6*s,cx+150*s,cy-2*s);
      g.lineTo(cx-150*s,cy-2*s);g.quadraticCurveTo(cx-170*s,cy+0,cx-170*s,cy-8*s);g.fill();
      // foot
      g.beginPath();g.ellipse(cx,cy+112*s,74*s,14*s,0,0,Math.PI*2);g.fill();g.fillRect(cx-30*s,cy+84*s,60*s,28*s);
      var dataB=g.getImageData(0,0,W,H).data;g.clearRect(0,0,W,H);
      // flame
      g.beginPath();var fx=cx+214*s,fy=cy-40*s;g.moveTo(fx,fy-200*s);g.bezierCurveTo(fx+66*s,fy-90*s,fx+50*s,fy+6*s,fx,fy+8*s);
      g.bezierCurveTo(fx-50*s,fy+6*s,fx-66*s,fy-90*s,fx,fy-200*s);g.fill();var dataF=g.getImageData(0,0,W,H).data;
      pts=[];var step=Math.max(2.4,3.1*s);
      for(var y=0;y<H;y+=step)for(var x=0;x<W;x+=step){var i=(Math.round(y)*W+Math.round(x))*4;
        var jx=x+(Math.random()-.5)*step,jy=y+(Math.random()-.5)*step;
        if(dataB[i+3]>10 && Math.random()<.78){var shade=1-(y-(cy-30*s))/(130*s);pts.push({x:jx,y:jy,r:(.55+Math.random()*.9)*(.7+.5*(1-shade)),f:0,a:.35+.6*Math.random()})}
        else if(dataF[i+3]>10 && Math.random()<.9){pts.push({x:jx,y:jy,r:.5+Math.random()*1.1,f:1,a:.5+.5*Math.random(),ph:Math.random()*6.28,by:jy})}}
      sparks=[];for(var k=0;k<70;k++)sparks.push(spark(fx,fy,s,true));
      build.fx=fx;build.fy=fy;build.s=s;}
    function spark(fx,fy,s,init){return{x:fx+(Math.random()-.5)*40*s,y:init?fy-200*s-Math.random()*260*s:fy-170*s,vy:-(.25+Math.random()*.7)*s,vx:(Math.random()-.5)*.35*s,life:Math.random(),r:.6+Math.random()*1.2}}
    function frame(now){var t=(now-t0)/1000;ctx.setTransform(dpr,0,0,dpr,0,0);ctx.clearRect(0,0,W,H);
      // shadow
      var s=build.s;ctx.fillStyle=ink;ctx.globalAlpha=.06;ctx.beginPath();ctx.ellipse(W/2,H*0.63+128*s,190*s,13*s,0,0,6.28);ctx.fill();
      for(var i=0;i<pts.length;i++){var p=pts[i];ctx.globalAlpha=p.a;
        if(p.f){var fl=Math.sin(t*3+p.ph)*1.4*s+Math.sin(t*7.3+p.ph*2)*.7*s;var lift=(build.fy-p.by)/(200*s);
          ctx.fillStyle=acc;ctx.beginPath();ctx.arc(p.x+fl*lift*1.6,p.y-Math.abs(fl)*lift,p.r,0,6.28);ctx.fill();}
        else{ctx.fillStyle=ink;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,6.28);ctx.fill();}}
      for(var j=0;j<sparks.length;j++){var q=sparks[j];q.x+=q.vx+Math.sin(t*1.3+j)*.15;q.y+=q.vy;q.life+=.003;
        var a=Math.max(0,1-q.life);ctx.globalAlpha=a*.7;ctx.fillStyle=j%3?ink:acc;ctx.beginPath();ctx.arc(q.x,q.y,q.r,0,6.28);ctx.fill();
        if(q.life>1||q.y<0){sparks[j]=spark(build.fx,build.fy,build.s,false);sparks[j].life=0}}
      ctx.globalAlpha=1;if(!reduce)requestAnimationFrame(frame);}
    colors();build();requestAnimationFrame(frame);
    var rt;window.addEventListener('resize',function(){clearTimeout(rt);rt=setTimeout(build,150)});
    new MutationObserver(colors).observe(root,{attributes:true,attributeFilter:['data-theme']});
  }

  if('serviceWorker' in navigator){navigator.serviceWorker.register('/sw.js').catch(function(){});}
})();
