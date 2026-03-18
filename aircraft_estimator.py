<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Nashat Aldhoun — Aeronautical Engineer</title>
<meta name="description" content="Nashat Omar Aldhoun — Junior Aeronautical Engineer | Aircraft Structures | FEA | MRO | JUST Graduate">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,wght@0,300;0,400;0,500;0,600;1,400&family=DM+Serif+Display:ital@0;1&display=swap" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
<script>
const SUPA_URL = 'https://soxvbtenfnpokhrtlqmq.supabase.co';
const SUPA_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNveHZidGVuZm5wb2tocnRscW1xIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzM3Nzg3ODIsImV4cCI6MjA4OTM1NDc4Mn0.uHzbpngTq3TVASlFP359VHkLcSQ8fN0aE03Z0Ux1Xjw';
const EM = ['n','a','s','h','a','t','a','l','d','h','o','u','n','@','y','a','h','o','o','.','c','o','m'].join('');
const _supa = supabase.createClient(SUPA_URL, SUPA_KEY);
window.SB = {
  _supa,
  signIn:(e,p)=>_supa.auth.signInWithPassword({email:e,password:p}),
  signOut:()=>_supa.auth.signOut(),
  onAuth:(cb)=>{
    _supa.auth.getSession().then(({data:{session}})=>cb(session?.user||null));
    _supa.auth.onAuthStateChange((_,s)=>cb(s?.user||null));
  },
  insert:async(t,r)=>{
    const{data,error}=await _supa.from(t).insert(r).select().single();
    if(error){console.error('ERR:',error);throw new Error(error.message);}
    await window._refresh(t);return data;
  },
  update:async(t,id,r)=>{
    const{error}=await _supa.from(t).update(r).eq('id',id);
    if(error)console.error(error);
    await window._refresh(t);
  },
  delete:async(t,id)=>{
    const{error}=await _supa.from(t).delete().eq('id',id);
    if(error)console.error(error);
    await window._refresh(t);
  },
  upsert:async(t,r)=>{const{error}=await _supa.from(t).upsert(r);if(error)console.error(error);},
  listen:(t,cb)=>{
    _supa.from(t).select('*').order('created_at',{ascending:false}).then(({data})=>cb(data||[]));
    return _supa.channel('rt-'+t).on('postgres_changes',{event:'*',schema:'public',table:t},()=>{
      _supa.from(t).select('*').order('created_at',{ascending:false}).then(({data})=>cb(data||[]));
    }).subscribe();
  }
};
</script>
<style>
/* ══ RESET & BASE ══ */
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box;}
:root{
  --bg:#07090d;--sur:#0c0f16;--pan:#121720;--pan2:#181d28;
  --b:rgba(255,255,255,.052);--b2:rgba(255,255,255,.1);
  --wh:#f0ede6;--mu:#616878;--tx:#b0bcce;
  --go:#c8a86c;--go2:#e4c88a;--go3:rgba(200,168,108,.08);
  --bl:#4875c2;--bl2:#6a9eea;
  --gr:#389664;--re:#d14e4e;--pu:#8260d2;
  --sh:0 8px 40px rgba(0,0,0,.6);
  --sh2:0 2px 14px rgba(0,0,0,.35);
  --r:12px;
}
[data-theme="light"]{
  --bg:#f0ede8;--sur:#fff;--pan:#e9e6e0;--pan2:#e0ddd7;
  --b:rgba(0,0,0,.06);--b2:rgba(0,0,0,.11);
  --wh:#0e1115;--mu:#66717e;--tx:#334054;
  --sh:0 8px 40px rgba(0,0,0,.07);
  --sh2:0 2px 14px rgba(0,0,0,.06);
}
html{scroll-behavior:smooth;}
body{background:var(--bg);color:var(--tx);font-family:'DM Sans',sans-serif;line-height:1.65;overflow-x:hidden;transition:background .35s,color .35s;}
::-webkit-scrollbar{width:3px;}
::-webkit-scrollbar-thumb{background:linear-gradient(180deg,var(--bl),var(--go));border-radius:3px;}
::selection{background:rgba(200,168,108,.2);color:var(--wh);}

/* ══ LOADER ══ */
#loader{position:fixed;inset:0;background:var(--bg);z-index:9999;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:1.6rem;transition:opacity .7s;}
#loader.gone{opacity:0;pointer-events:none;}
.ld-logo{font-family:'DM Serif Display',serif;font-size:2.8rem;color:var(--wh);letter-spacing:-1px;}
.ld-logo span{color:var(--go);}
.ld-tag{font-size:.64rem;letter-spacing:4px;text-transform:uppercase;color:var(--mu);}
.ld-bar{width:72px;height:1.5px;background:var(--b2);border-radius:2px;overflow:hidden;}
.ld-fill{height:100%;background:linear-gradient(90deg,var(--bl),var(--go));width:0;animation:lfill 1.6s ease forwards;}
@keyframes lfill{to{width:100%;}}

/* ══ TOAST ══ */
.toast{position:fixed;bottom:2rem;left:50%;transform:translateX(-50%) translateY(100px);background:var(--pan2);border:1px solid var(--b2);color:var(--wh);border-radius:9px;padding:.6rem 1.3rem;font-size:.82rem;z-index:2000;transition:transform .38s cubic-bezier(.34,1.56,.64,1);box-shadow:var(--sh);white-space:nowrap;}
.toast.on{transform:translateX(-50%) translateY(0);}

/* ══ ADMIN ══ */
.admin-badge{display:none;background:var(--go3);border:1px solid rgba(200,168,108,.26);color:var(--go);font-size:.58rem;font-weight:700;padding:.16rem .5rem;border-radius:4px;letter-spacing:1.8px;}
.is-admin .admin-badge{display:inline-flex;}
.admin-only{display:none!important;}
.is-admin .admin-only{display:inline-flex!important;}
.admin-only-block{display:none!important;}
.is-admin .admin-only-block{display:block!important;}

/* ══ NAV ══ */
nav{position:fixed;top:0;left:0;right:0;z-index:500;height:54px;display:flex;align-items:center;justify-content:space-between;padding:0 2rem;background:rgba(7,9,13,.9);backdrop-filter:blur(30px) saturate(1.5);border-bottom:1px solid var(--b);}
[data-theme="light"] nav{background:rgba(240,237,232,.93);}
.nav-logo{font-family:'DM Serif Display',serif;font-size:1.06rem;color:var(--wh);cursor:pointer;display:flex;align-items:center;gap:.52rem;letter-spacing:-.2px;}
.nav-logo .nl{color:var(--go);}
.nav-links{display:flex;gap:.04rem;}
.nav-links a{color:var(--mu);text-decoration:none;font-size:.76rem;font-weight:500;padding:.32rem .66rem;border-radius:6px;cursor:pointer;transition:color .2s;position:relative;}
.nav-links a::after{content:'';position:absolute;bottom:1px;left:.66rem;right:.66rem;height:1px;background:var(--go);transform:scaleX(0);transition:transform .25s cubic-bezier(.4,0,.2,1);}
.nav-links a:hover{color:var(--wh);}
.nav-links a.active{color:var(--wh);}
.nav-links a:hover::after,.nav-links a.active::after{transform:scaleX(1);}
.nav-r{display:flex;align-items:center;gap:.35rem;}
.icon-btn{background:none;border:1px solid var(--b2);color:var(--mu);border-radius:6px;padding:.26rem .55rem;cursor:pointer;font-size:.75rem;transition:all .2s;font-family:'DM Sans',sans-serif;line-height:1;}
.icon-btn:hover{color:var(--wh);border-color:var(--go);background:var(--go3);}
.hire-btn{background:linear-gradient(135deg,var(--go) 0%,var(--go2) 100%);color:#07090d;border:none;border-radius:6px;padding:.32rem .88rem;font-size:.76rem;font-weight:700;cursor:pointer;font-family:'DM Sans',sans-serif;transition:all .22s;letter-spacing:.2px;}
.hire-btn:hover{transform:translateY(-1px);box-shadow:0 4px 18px rgba(200,168,108,.3);}
.ham{display:none;background:none;border:1px solid var(--b2);color:var(--mu);border-radius:6px;padding:.26rem .5rem;cursor:pointer;font-size:.86rem;}
.mob{display:none;position:fixed;top:54px;left:0;right:0;background:var(--sur);border-bottom:1px solid var(--b);padding:.7rem 1.1rem;flex-direction:column;gap:.16rem;z-index:499;box-shadow:var(--sh);}
.mob.open{display:flex;}
.mob a,.mob button{color:var(--tx);font-size:.86rem;padding:.5rem .7rem;border-radius:7px;border:none;background:none;font-family:'DM Sans',sans-serif;cursor:pointer;text-align:left;text-decoration:none;transition:background .2s;display:block;}
.mob a:hover,.mob button:hover{background:var(--pan);}

/* ══ PAGES ══ */
.page{display:none;min-height:100vh;}
.page.active{display:block;animation:pageIn .42s ease;}
@keyframes pageIn{from{opacity:0;transform:translateY(10px);}to{opacity:1;transform:none;}}

/* ══ REVEAL ══ */
.rev{opacity:0;transform:translateY(22px);transition:opacity .58s ease,transform .58s ease;}
.rev.v{opacity:1;transform:none;}
.d1{transition-delay:.07s;}.d2{transition-delay:.14s;}.d3{transition-delay:.21s;}.d4{transition-delay:.28s;}

/* ══ BUTTONS ══ */
.btn{display:inline-flex;align-items:center;gap:.38rem;border-radius:8px;font-size:.85rem;font-weight:600;cursor:pointer;font-family:'DM Sans',sans-serif;text-decoration:none;border:none;transition:all .22s;padding:.6rem 1.38rem;}
.btn:active{transform:scale(.97);}
.btn-go{background:linear-gradient(135deg,var(--go),var(--go2));color:#07090d;}
.btn-go:hover{transform:translateY(-1px);box-shadow:0 4px 20px rgba(200,168,108,.28);}
.btn-gh{background:transparent;color:var(--tx);border:1px solid var(--b2);}
.btn-gh:hover{background:rgba(255,255,255,.05);border-color:var(--b2);}
.btn-sm{padding:.34rem .84rem;font-size:.74rem;}
.btn-xs{padding:.2rem .56rem;font-size:.68rem;}
.btn-del{background:transparent;color:var(--re);border:1px solid rgba(209,78,78,.16);border-radius:6px;padding:.2rem .58rem;font-size:.69rem;cursor:pointer;font-family:'DM Sans',sans-serif;transition:all .2s;display:inline-flex;align-items:center;gap:.2rem;}
.btn-del:hover{background:rgba(209,78,78,.08);border-color:var(--re);}

/* ══ SECTION ══ */
.section{padding:5.5rem 2rem 4rem;max-width:1080px;margin:0 auto;}
.eyebrow{display:inline-flex;align-items:center;gap:.42rem;font-size:.62rem;font-weight:700;letter-spacing:3.5px;color:var(--go);text-transform:uppercase;margin-bottom:.6rem;}
.eyebrow::before{content:'';width:10px;height:1px;background:var(--go);flex-shrink:0;}
.sec-t{font-family:'DM Serif Display',serif;font-size:clamp(1.6rem,3vw,2.3rem);color:var(--wh);line-height:1.1;margin-bottom:.45rem;letter-spacing:-.3px;}
.sec-s{color:var(--mu);font-size:.88rem;max-width:480px;margin-bottom:2.5rem;line-height:1.85;}
.sec-row{display:flex;justify-content:space-between;align-items:flex-end;flex-wrap:wrap;gap:1rem;margin-bottom:2.5rem;}

/* ══ FIELD ══ */
.field{width:100%;background:rgba(255,255,255,.033);border:1px solid var(--b);border-radius:8px;padding:.56rem .86rem;color:var(--tx);font-size:.83rem;font-family:'DM Sans',sans-serif;outline:none;transition:border-color .2s,box-shadow .2s;margin-bottom:.6rem;}
.field:focus{border-color:var(--bl);box-shadow:0 0 0 3px rgba(72,117,194,.1);}
textarea.field{min-height:78px;resize:vertical;}
select.field option{background:var(--pan);}
.flabel{display:block;font-size:.62rem;font-weight:700;letter-spacing:1.8px;text-transform:uppercase;color:var(--mu);margin-bottom:.3rem;}
.frow{display:grid;grid-template-columns:1fr 1fr;gap:.6rem;}

/* ══ HERO ══ */
.hero{min-height:100vh;display:grid;grid-template-columns:1fr 380px;align-items:center;padding:72px 2rem 3rem;gap:3rem;position:relative;overflow:hidden;}
.hbg{position:absolute;inset:0;pointer-events:none;overflow:hidden;}

/* Beautiful grid background */
.hgrid{position:absolute;inset:0;
  background-image:
    linear-gradient(rgba(72,117,194,.025) 1px,transparent 1px),
    linear-gradient(90deg,rgba(72,117,194,.025) 1px,transparent 1px);
  background-size:48px 48px;}
.hgrid2{position:absolute;inset:0;
  background-image:
    linear-gradient(rgba(200,168,108,.015) 1px,transparent 1px),
    linear-gradient(90deg,rgba(200,168,108,.015) 1px,transparent 1px);
  background-size:12px 12px;}

/* Glows */
.hglow-blue{position:absolute;right:8%;top:15%;width:600px;height:500px;background:radial-gradient(ellipse at center,rgba(72,117,194,.07) 0%,transparent 70%);pointer-events:none;}
.hglow-gold{position:absolute;left:-5%;bottom:10%;width:500px;height:400px;background:radial-gradient(ellipse at center,rgba(200,168,108,.04) 0%,transparent 70%);}

/* ══ AIRPLANE SVG ══ */
.airplane-wrapper{position:absolute;top:0;left:0;width:100%;height:100%;pointer-events:none;overflow:hidden;}
.airplane-path{position:absolute;}

/* Large background airplane - decorative */
.plane-bg{
  position:absolute;
  right:-60px;
  top:50%;
  transform:translateY(-50%);
  width:520px;
  opacity:.028;
  filter:blur(.5px);
}
[data-theme="light"] .plane-bg{opacity:.04;}

/* Flying small airplane animation */
.plane-fly{
  position:absolute;
  top:22%;
  left:-120px;
  animation:flyAcross 28s linear infinite;
  opacity:.09;
  filter:drop-shadow(0 0 8px rgba(200,168,108,.4));
}
@keyframes flyAcross{
  0%{left:-120px;top:22%;transform:rotate(-2deg);}
  25%{top:18%;transform:rotate(-1deg);}
  50%{top:22%;transform:rotate(-2deg);}
  75%{top:16%;transform:rotate(-1deg);}
  100%{left:110%;top:14%;transform:rotate(-3deg);}
}

/* Contrail / trail effect */
.contrail{
  position:absolute;
  top:22%;
  left:0;
  height:1px;
  background:linear-gradient(90deg,transparent,rgba(200,168,108,.08),transparent);
  width:0;
  animation:contrailGrow 28s linear infinite;
  pointer-events:none;
}
@keyframes contrailGrow{
  0%{width:0;left:-120px;top:22%;}
  100%{width:60%;left:50%;top:15%;}
}

.hero-l{position:relative;z-index:1;}
.status-pill{display:inline-flex;align-items:center;gap:.42rem;background:rgba(56,150,100,.08);border:1px solid rgba(56,150,100,.18);color:#4caf7d;font-size:.69rem;font-weight:600;padding:.24rem .82rem;border-radius:20px;margin-bottom:1.3rem;letter-spacing:.3px;}
.sdot{width:5.5px;height:5.5px;border-radius:50%;background:#4caf7d;animation:pulse 2.2s infinite;}
@keyframes pulse{0%,100%{box-shadow:0 0 0 0 rgba(56,150,100,.4);}60%{box-shadow:0 0 0 5px rgba(56,150,100,0);}}

.hero h1{font-family:'DM Serif Display',serif;font-size:clamp(2.2rem,4.5vw,3.6rem);line-height:1.05;color:var(--wh);margin-bottom:1rem;letter-spacing:-.5px;}
.hero h1 em{font-style:italic;background:linear-gradient(135deg,var(--go) 0%,var(--go2) 50%,var(--go) 100%);background-size:200% auto;-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;animation:shimmer 4s linear infinite;}
@keyframes shimmer{0%{background-position:0% center;}100%{background-position:200% center;}}
.hero h1 .sub{display:block;color:var(--tx);font-size:.66em;font-style:normal;margin-top:.1rem;opacity:.75;-webkit-text-fill-color:var(--tx);}

.hero-d{font-size:.94rem;color:var(--mu);line-height:1.85;margin-bottom:1.8rem;max-width:500px;}
.hero-d strong{color:var(--tx);font-weight:600;}

/* Email display */
.hero-email{display:inline-flex;align-items:center;gap:.62rem;background:var(--pan);border:1px solid var(--b);border-radius:9px;padding:.52rem .95rem;margin-bottom:1.8rem;transition:border-color .2s;}
.hero-email:hover{border-color:rgba(200,168,108,.25);}
.em-dot{width:6px;height:6px;border-radius:50%;background:var(--go);flex-shrink:0;opacity:.7;}
.em-val{font-size:.82rem;color:var(--go);font-weight:500;cursor:pointer;transition:color .2s;}
.em-val:hover{color:var(--go2);}
.em-copy{background:none;border:1px solid var(--b2);color:var(--mu);border-radius:5px;padding:.15rem .46rem;font-size:.68rem;cursor:pointer;font-family:'DM Sans',sans-serif;transition:all .2s;flex-shrink:0;}
.em-copy:hover{border-color:var(--go);color:var(--go);}

.hero-ctas{display:flex;gap:.62rem;flex-wrap:wrap;margin-bottom:2.2rem;}

.hmetrics{display:grid;grid-template-columns:repeat(3,1fr);gap:1px;background:var(--b);border:1px solid var(--b);border-radius:11px;overflow:hidden;}
.hm{background:var(--sur);padding:.95rem;text-align:center;}
.hm-n{font-family:'DM Serif Display',serif;font-size:1.65rem;color:var(--wh);line-height:1;}
.hm-n span{color:var(--go);font-size:1rem;}
.hm-l{font-size:.64rem;color:var(--mu);margin-top:.18rem;letter-spacing:.5px;}

/* ══ ID CARD ══ */
.idc{background:var(--sur);border:1px solid var(--b);border-radius:16px;overflow:hidden;box-shadow:var(--sh);animation:float 7s ease-in-out infinite;}
@keyframes float{0%,100%{transform:translateY(0);}50%{transform:translateY(-7px);}}
.idc-top{background:linear-gradient(150deg,#08162a 0%,#0f2240 50%,#0a1a38 100%);padding:2rem 1.6rem 1.6rem;text-align:center;position:relative;overflow:hidden;border-bottom:1px solid rgba(255,255,255,.05);}
.idc-grid{position:absolute;inset:0;background-image:linear-gradient(rgba(72,117,194,.06) 1px,transparent 1px),linear-gradient(90deg,rgba(72,117,194,.06) 1px,transparent 1px);background-size:18px 18px;pointer-events:none;}
.idc-stripe{position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,var(--bl) 0%,var(--go) 50%,var(--bl) 100%);animation:stripeMove 4s linear infinite;}
@keyframes stripeMove{0%{background-position:0% center;}100%{background-position:200% center;}}
.avatar{width:68px;height:68px;border-radius:50%;background:linear-gradient(135deg,var(--bl),var(--go));display:flex;align-items:center;justify-content:center;font-family:'DM Serif Display',serif;font-size:1.45rem;color:#07090d;margin:0 auto .72rem;position:relative;z-index:1;border:2.5px solid rgba(255,255,255,.1);overflow:hidden;background-size:cover;background-position:center;}
.idc-name{font-family:'DM Serif Display',serif;font-size:1.12rem;color:var(--wh);position:relative;z-index:1;letter-spacing:-.1px;}
.idc-role{font-size:.65rem;color:var(--go);letter-spacing:2.5px;text-transform:uppercase;margin-top:.18rem;position:relative;z-index:1;opacity:.85;}
.photo-btn{margin-top:.62rem;position:relative;z-index:1;background:rgba(255,255,255,.05);border:1px dashed rgba(255,255,255,.13);color:var(--mu);border-radius:5px;padding:.22rem .68rem;font-size:.65rem;cursor:pointer;font-family:'DM Sans',sans-serif;transition:all .2s;}
.photo-btn:hover{border-color:var(--go);color:var(--go);}
.idc-body{padding:.95rem 1.15rem;}
.idc-row{display:flex;align-items:center;gap:.68rem;padding:.48rem 0;border-bottom:1px solid var(--b);}
.idc-row:last-child{border-bottom:none;}
.idc-ic{width:26px;height:26px;border-radius:6px;display:flex;align-items:center;justify-content:center;font-size:.75rem;flex-shrink:0;}
.idc-key{font-size:.6rem;color:var(--mu);margin-bottom:.07rem;letter-spacing:.5px;text-transform:uppercase;}
.idc-val{color:var(--tx);font-weight:500;font-size:.79rem;}
.idc-foot{padding:.78rem 1.15rem;border-top:1px solid var(--b);display:flex;gap:.35rem;}
.idc-foot a{flex:1;display:flex;align-items:center;justify-content:center;gap:.3rem;padding:.38rem;border-radius:7px;border:1px solid var(--b);color:var(--mu);font-size:.69rem;text-decoration:none;transition:all .2s;background:var(--pan);}
.idc-foot a:hover{border-color:var(--go);color:var(--go);background:var(--go3);}

/* ══ CAROUSEL ══ */
.carousel-section{background:var(--sur);border-top:1px solid var(--b);border-bottom:1px solid var(--b);padding:2.5rem 0;overflow:hidden;}
.c-inner{max-width:1080px;margin:0 auto;padding:0 2rem;}
.c-head{display:flex;align-items:center;justify-content:space-between;margin-bottom:1.35rem;flex-wrap:wrap;gap:.75rem;}
.c-title{font-family:'DM Serif Display',serif;font-size:1.25rem;color:var(--wh);letter-spacing:-.2px;}
.c-controls{display:flex;align-items:center;gap:.65rem;}
.ctabs{display:flex;gap:.3rem;}
.ctab{background:var(--pan);border:1px solid var(--b);color:var(--mu);font-size:.74rem;font-weight:500;padding:.3rem .8rem;border-radius:20px;cursor:pointer;font-family:'DM Sans',sans-serif;transition:all .22s;letter-spacing:.2px;}
.ctab.on,.ctab:hover{background:var(--go3);border-color:rgba(200,168,108,.28);color:var(--go);}
.cnav{display:flex;gap:.3rem;}
.cnav-btn{background:var(--pan);border:1px solid var(--b);color:var(--mu);border-radius:7px;width:30px;height:30px;display:flex;align-items:center;justify-content:center;cursor:pointer;font-size:.82rem;transition:all .2s;}
.cnav-btn:hover{border-color:var(--go);color:var(--go);}
.c-slider{overflow:hidden;}
.c-track{display:flex;gap:1rem;transition:transform .52s cubic-bezier(.25,.46,.45,.94);will-change:transform;padding-bottom:.5rem;}
.ccard{min-width:255px;max-width:255px;background:var(--pan);border:1px solid var(--b);border-radius:var(--r);overflow:hidden;flex-shrink:0;transition:all .28s;cursor:pointer;position:relative;}
.ccard::after{content:'';position:absolute;inset:0;background:linear-gradient(135deg,rgba(255,255,255,.02),transparent);pointer-events:none;}
.ccard:hover{border-color:rgba(200,168,108,.28);transform:translateY(-5px);box-shadow:0 18px 48px rgba(0,0,0,.4);}
.ccard-img{height:125px;background:linear-gradient(135deg,#08162a,#0f2240);display:flex;align-items:center;justify-content:center;font-size:2.5rem;position:relative;overflow:hidden;}
.ccard-img-bg{position:absolute;inset:0;background-image:linear-gradient(rgba(72,117,194,.07) 1px,transparent 1px),linear-gradient(90deg,rgba(72,117,194,.07) 1px,transparent 1px);background-size:16px 16px;}
.ccard-img img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;}
.ccard-badge{position:absolute;top:.5rem;left:.5rem;background:rgba(7,9,13,.88);border:1px solid var(--b2);color:var(--tx);font-size:.58rem;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;padding:.12rem .42rem;border-radius:3px;z-index:2;}
.ccard-body{padding:.85rem;}
.ccard-title{font-weight:600;color:var(--wh);font-size:.84rem;margin-bottom:.25rem;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;letter-spacing:-.1px;}
.ccard-sub{font-size:.73rem;color:var(--mu);line-height:1.5;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;min-height:2.1rem;}
.ccard-foot{display:flex;justify-content:space-between;align-items:center;margin-top:.62rem;}
.ccard-date{font-size:.65rem;color:var(--mu);}
.ccard-btn{background:var(--go3);border:1px solid rgba(200,168,108,.2);color:var(--go);border-radius:5px;padding:.16rem .5rem;font-size:.67rem;font-family:'DM Sans',sans-serif;cursor:pointer;transition:all .2s;}
.ccard-btn:hover{background:var(--go);color:#07090d;}
.cdots{display:flex;justify-content:center;gap:.35rem;margin-top:1rem;}
.cdot{width:5px;height:5px;border-radius:50%;background:var(--b2);border:none;cursor:pointer;transition:all .3s;}
.cdot.on{width:18px;border-radius:3px;background:var(--go);}

/* ══ ABOUT ══ */
.about-grid{display:grid;grid-template-columns:1fr 1fr;gap:3.5rem;}
.ap{color:var(--mu);line-height:1.9;margin-bottom:.85rem;font-size:.91rem;}
.ap strong{color:var(--tx);font-weight:600;}
.sg{margin-top:1.3rem;}
.sg-l{font-size:.6rem;font-weight:700;letter-spacing:2.5px;text-transform:uppercase;color:var(--go);margin-bottom:.55rem;}
.chips{display:flex;flex-wrap:wrap;gap:.32rem;}
.chip{background:var(--pan);border:1px solid var(--b);color:var(--tx);font-size:.74rem;padding:.25rem .65rem;border-radius:6px;transition:all .22s;}
.chip:hover{border-color:rgba(200,168,108,.3);color:var(--go);transform:translateY(-1px);}
.tl-item{display:grid;grid-template-columns:82px 1fr;gap:1.1rem;padding:1.1rem 0;border-bottom:1px solid var(--b);}
.tl-item:last-child{border-bottom:none;}
.tl-date{font-size:.69rem;color:var(--mu);padding-top:.1rem;line-height:1.4;}
.tl-t{font-weight:600;color:var(--wh);font-size:.89rem;margin-bottom:.14rem;}
.tl-o{font-size:.76rem;color:var(--go);margin-bottom:.32rem;}
.tl-d{font-size:.79rem;color:var(--mu);line-height:1.65;}
.cv-box{background:var(--pan);border:1px solid rgba(200,168,108,.18);border-radius:var(--r);padding:1.15rem;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:1rem;margin-top:1.8rem;}
.cv-box h4{font-weight:600;color:var(--wh);font-size:.88rem;margin-bottom:.16rem;}
.cv-box p{font-size:.75rem;color:var(--mu);}

/* ══ WORKS ══ */
.wgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(278px,1fr));gap:1.2rem;}
.wcard{background:var(--pan);border:1px solid var(--b);border-radius:var(--r);overflow:hidden;transition:all .25s;cursor:pointer;}
.wcard:hover{border-color:rgba(200,168,108,.25);transform:translateY(-3px);box-shadow:0 14px 36px rgba(0,0,0,.35);}
.wthumb{height:150px;position:relative;overflow:hidden;background:#08162a;}
.wthumb img{width:100%;height:100%;object-fit:cover;display:none;}
.wthumb img.on{display:block;}
.wthumb-ph{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-size:2.9rem;}
.wthumb-bg{position:absolute;inset:0;background-image:linear-gradient(rgba(72,117,194,.07) 1px,transparent 1px),linear-gradient(90deg,rgba(72,117,194,.07) 1px,transparent 1px);background-size:16px 16px;}
.wcat{position:absolute;top:.6rem;left:.6rem;background:rgba(7,9,13,.88);border:1px solid var(--b2);color:var(--tx);font-size:.58rem;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;padding:.12rem .46rem;border-radius:3px;z-index:2;}
.wprice{position:absolute;top:.6rem;right:.6rem;background:var(--go3);border:1px solid rgba(200,168,108,.28);color:var(--go);font-size:.62rem;font-weight:700;padding:.12rem .46rem;border-radius:3px;z-index:2;}
.photo-ov{position:absolute;inset:0;background:rgba(0,0,0,.5);display:flex;align-items:center;justify-content:center;opacity:0;transition:opacity .2s;z-index:3;cursor:pointer;}
.wcard:hover .photo-ov{opacity:1;}
.photo-ov span{color:#fff;font-size:.7rem;background:rgba(200,168,108,.88);padding:.3rem .68rem;border-radius:5px;}
.wbody{padding:.95rem;}
.wtitle{font-weight:600;color:var(--wh);font-size:.88rem;margin-bottom:.28rem;line-height:1.3;letter-spacing:-.1px;}
.wdesc{font-size:.77rem;color:var(--mu);line-height:1.6;margin-bottom:.78rem;}
.wfoot{display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:.28rem;}
.wyear{font-size:.67rem;color:var(--mu);}

/* ══ POSTS ══ */
.posts-layout{display:grid;grid-template-columns:1fr 275px;gap:1.8rem;}
.pcompose{background:var(--pan);border:1px solid var(--b);border-radius:var(--r);padding:1.15rem;margin-bottom:1.35rem;display:none;}
.is-admin .pcompose{display:block;}
.pcompose-l{font-size:.61rem;font-weight:700;letter-spacing:2.5px;text-transform:uppercase;color:var(--go);margin-bottom:.85rem;}
.ptabs{display:flex;gap:0;border-bottom:1px solid var(--b);margin-bottom:.85rem;flex-wrap:wrap;}
.ptab{background:none;border:none;color:var(--mu);font-size:.72rem;font-family:'DM Sans',sans-serif;padding:.36rem .76rem;cursor:pointer;border-bottom:2px solid transparent;margin-bottom:-1px;transition:all .2s;}
.ptab.active,.ptab:hover{color:var(--go);border-bottom-color:var(--go);}
.ptype-panel{display:none;}.ptype-panel.active{display:block;}
.img-prev{width:100%;max-height:165px;object-fit:cover;border-radius:7px;margin-bottom:.6rem;display:none;}
.img-prev.on{display:block;}
.pfeed{display:grid;gap:.95rem;}
.pcard{background:var(--pan);border:1px solid var(--b);border-radius:var(--r);overflow:hidden;transition:border-color .22s;}
.pcard:hover{border-color:var(--b2);}
.pcard-head{display:flex;justify-content:space-between;align-items:flex-start;padding:.88rem .95rem .58rem;gap:.65rem;flex-wrap:wrap;}
.puser{display:flex;align-items:center;gap:.52rem;}
.pavatar{width:30px;height:30px;border-radius:50%;background:linear-gradient(135deg,var(--bl),var(--go));display:flex;align-items:center;justify-content:center;font-size:.74rem;font-weight:700;color:#07090d;flex-shrink:0;}
.pname{font-weight:600;color:var(--wh);font-size:.82rem;}
.pmeta{font-size:.66rem;color:var(--mu);}
.ptype-badge{font-size:.59rem;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;padding:.13rem .46rem;border-radius:3px;}
.t-article{background:rgba(72,117,194,.1);color:var(--bl2);}
.t-link{background:rgba(200,168,108,.1);color:var(--go);}
.t-video{background:rgba(209,78,78,.1);color:#ef8080;}
.t-doc{background:rgba(130,96,210,.1);color:var(--pu);}
.t-image{background:rgba(56,150,100,.1);color:#4caf7d;}
.pbody{padding:0 .95rem .82rem;}
.ptitle{font-family:'DM Serif Display',serif;font-size:.98rem;color:var(--wh);margin-bottom:.38rem;line-height:1.22;letter-spacing:-.1px;}
.ptext{font-size:.8rem;color:var(--mu);line-height:1.78;margin-bottom:.62rem;}
.ptext.col{display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden;}
.rm-btn{background:none;border:none;color:var(--go);font-size:.72rem;cursor:pointer;font-family:'DM Sans',sans-serif;padding:0;}
.rm-btn:hover{text-decoration:underline;}
.ptags{display:flex;flex-wrap:wrap;gap:.28rem;margin-bottom:.62rem;}
.ptag{background:rgba(72,117,194,.08);border:1px solid rgba(72,117,194,.16);color:var(--bl2);font-size:.64rem;padding:.13rem .45rem;border-radius:3px;cursor:pointer;}
.ptag:hover{background:rgba(72,117,194,.16);}
.pcard-img{width:100%;max-height:240px;object-fit:cover;display:block;}
.pcard-video{width:100%;aspect-ratio:16/9;border:none;display:block;}
.link-prev{margin:0 .95rem .78rem;background:var(--sur);border:1px solid var(--b);border-radius:9px;padding:.82rem;display:flex;gap:.65rem;align-items:flex-start;text-decoration:none;transition:border-color .2s;}
.link-prev:hover{border-color:var(--go);}
.lp-icon{width:36px;height:36px;border-radius:7px;background:var(--pan);display:flex;align-items:center;justify-content:center;font-size:1.05rem;flex-shrink:0;}
.lp-title{font-weight:600;color:var(--wh);font-size:.81rem;margin-bottom:.14rem;}
.lp-url{font-size:.68rem;color:var(--mu);}
.doc-card{margin:0 .95rem .78rem;background:var(--sur);border:1px solid var(--b);border-radius:9px;padding:.82rem;display:flex;gap:.65rem;align-items:center;text-decoration:none;transition:border-color .2s;}
.doc-card:hover{border-color:var(--pu);}
.doc-icon{width:36px;height:36px;border-radius:7px;background:rgba(130,96,210,.1);display:flex;align-items:center;justify-content:center;font-size:1.15rem;flex-shrink:0;}
.doc-name{font-weight:600;color:var(--wh);font-size:.81rem;margin-bottom:.14rem;}
.doc-sub{font-size:.67rem;color:var(--mu);}
.pfoot{display:flex;align-items:center;gap:.58rem;padding:.68rem .95rem;border-top:1px solid var(--b);flex-wrap:wrap;}
.pact{background:none;border:none;color:var(--mu);font-size:.71rem;cursor:pointer;font-family:'DM Sans',sans-serif;display:flex;align-items:center;gap:.22rem;padding:.2rem .46rem;border-radius:5px;transition:all .2s;}
.pact:hover{background:rgba(255,255,255,.05);color:var(--tx);}
.pact.liked{color:#e87461;}
.pcmt-section{display:none;padding:.68rem .95rem;border-top:1px solid var(--b);}
.pcmt-section.open{display:block;}
.pcmt-item{display:flex;gap:.48rem;margin-bottom:.48rem;}
.pcmt-av{width:22px;height:22px;border-radius:50%;background:rgba(72,117,194,.12);display:flex;align-items:center;justify-content:center;font-size:.6rem;color:var(--bl2);font-weight:700;flex-shrink:0;}
.pcmt-txt{font-size:.77rem;color:var(--mu);line-height:1.5;}
.pcmt-txt strong{color:var(--tx);}
.pcmt-row{display:flex;gap:.38rem;margin-top:.48rem;}
.pcmt-row input{flex:1;margin-bottom:0;font-size:.77rem;}
.psidebar{}
.scard{background:var(--pan);border:1px solid var(--b);border-radius:var(--r);padding:.95rem;margin-bottom:.95rem;}
.scard-t{font-size:.62rem;font-weight:700;letter-spacing:2.5px;text-transform:uppercase;color:var(--go);margin-bottom:.78rem;}
.tag-cloud{display:flex;flex-wrap:wrap;gap:.32rem;}
.ttag{background:var(--sur);border:1px solid var(--b);color:var(--tx);font-size:.7rem;padding:.24rem .56rem;border-radius:5px;cursor:pointer;transition:all .2s;}
.ttag:hover,.ttag.on{background:var(--go3);border-color:rgba(200,168,108,.26);color:var(--go);}

/* ══ JOURNEY ══ */
.journey-timeline{position:relative;padding-left:2rem;}
.journey-timeline::before{content:'';position:absolute;left:.42rem;top:0;bottom:0;width:1px;background:linear-gradient(180deg,transparent,var(--b) 10%,var(--b) 90%,transparent);}
.jitem{position:relative;margin-bottom:1.6rem;padding-left:1.35rem;}
.jdot{position:absolute;left:-1.58rem;top:.48rem;width:9px;height:9px;border-radius:50%;border:2px solid var(--go);background:var(--bg);z-index:1;transition:all .2s;}
.jitem:hover .jdot{transform:scale(1.3);}
.jdot.course{border-color:var(--bl2);}
.jdot.event{border-color:#4caf7d;}
.jcard{background:var(--pan);border:1px solid var(--b);border-radius:var(--r);padding:1.05rem;transition:all .22s;}
.jcard:hover{border-color:var(--b2);transform:translateX(3px);}
.jcard-top{display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:.42rem;margin-bottom:.42rem;}
.jtype-badge{font-size:.59rem;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;padding:.13rem .46rem;border-radius:3px;}
.jt-course{background:rgba(72,117,194,.1);color:var(--bl2);}
.jt-event{background:rgba(56,150,100,.1);color:#4caf7d;}
.jt-milestone{background:rgba(200,168,108,.1);color:var(--go);}
.jdate{font-size:.67rem;color:var(--mu);}
.jtitle{font-weight:600;color:var(--wh);font-size:.88rem;margin-bottom:.27rem;letter-spacing:-.1px;}
.jorg{font-size:.75rem;color:var(--go);margin-bottom:.32rem;}
.jdesc{font-size:.79rem;color:var(--mu);line-height:1.65;}
.jimg{width:100%;max-height:145px;object-fit:cover;border-radius:7px;margin-top:.68rem;display:none;}
.jimg.on{display:block;}
.jtabs{display:flex;gap:.32rem;flex-wrap:wrap;margin-bottom:1.35rem;}
.jtab{background:var(--pan);border:1px solid var(--b);color:var(--mu);font-size:.74rem;padding:.28rem .78rem;border-radius:20px;cursor:pointer;font-family:'DM Sans',sans-serif;transition:all .22s;}
.jtab:hover,.jtab.on{border-color:rgba(200,168,108,.28);color:var(--go);background:var(--go3);}

/* ══ DISCUSSION — محسّنة ومفصّلة ══ */
.disc-layout{display:grid;grid-template-columns:1fr 260px;gap:1.8rem;}
.disc-main{}
.disc-sidebar{}

/* Compose box */
.disc-compose{background:var(--pan);border:1px solid var(--b);border-radius:var(--r);padding:1.15rem;margin-bottom:1.5rem;}
.disc-compose-head{display:flex;align-items:center;gap:.55rem;margin-bottom:.9rem;}
.disc-compose-av{width:34px;height:34px;border-radius:50%;background:linear-gradient(135deg,var(--bl),var(--go));display:flex;align-items:center;justify-content:center;font-size:.8rem;font-weight:700;color:#07090d;flex-shrink:0;}
.disc-compose-label{font-size:.82rem;font-weight:600;color:var(--wh);}
.disc-compose-sub{font-size:.69rem;color:var(--mu);}

/* Topic cards */
.disc-feed{display:grid;gap:1rem;}
.dcard{background:var(--pan);border:1px solid var(--b);border-radius:var(--r);overflow:hidden;transition:all .22s;}
.dcard:hover{border-color:var(--b2);}

/* Admin topic header */
.dcard-admin-head{background:linear-gradient(135deg,rgba(8,22,42,.8),rgba(15,34,64,.6));padding:.95rem 1rem .75rem;border-bottom:1px solid rgba(255,255,255,.05);}
.dcard-topic-badge{display:inline-flex;align-items:center;gap:.3rem;font-size:.58rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:var(--go);margin-bottom:.4rem;}
.dcard-topic-badge::before{content:'';width:14px;height:1px;background:var(--go);}
.dcard-title{font-family:'DM Serif Display',serif;font-size:1.05rem;color:var(--wh);line-height:1.25;letter-spacing:-.1px;}

/* Author row */
.dcard-author{display:flex;align-items:center;gap:.55rem;padding:.75rem 1rem;border-bottom:1px solid var(--b);}
.dcard-av{width:30px;height:30px;border-radius:50%;background:linear-gradient(135deg,var(--bl),var(--go));display:flex;align-items:center;justify-content:center;font-size:.74rem;font-weight:700;color:#07090d;flex-shrink:0;}
.dcard-av-visitor{background:rgba(72,117,194,.12);color:var(--bl2);}
.dcard-aname{font-weight:600;font-size:.83rem;color:var(--wh);}
.dcard-aname.nashat{color:var(--go);}
.dcard-ameta{font-size:.67rem;color:var(--mu);}
.author-tag{display:inline-block;font-size:.56rem;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;background:var(--go3);border:1px solid rgba(200,168,108,.22);color:var(--go);padding:.08rem .38rem;border-radius:3px;margin-left:.38rem;}

/* Body */
.dcard-body{padding:.82rem 1rem;}
.dcard-text{font-size:.82rem;color:var(--mu);line-height:1.78;}

/* Actions row */
.dcard-actions{display:flex;align-items:center;gap:.52rem;padding:.65rem 1rem;border-top:1px solid var(--b);flex-wrap:wrap;}
.dact{background:none;border:none;color:var(--mu);font-size:.72rem;cursor:pointer;font-family:'DM Sans',sans-serif;display:flex;align-items:center;gap:.22rem;padding:.2rem .45rem;border-radius:5px;transition:all .2s;}
.dact:hover{background:rgba(255,255,255,.05);color:var(--tx);}
.dact.liked{color:#e87461;}
.dact-cmt{color:var(--bl2);}
.dact-cmt:hover{color:var(--bl2);background:rgba(72,117,194,.08);}
.dcard-meta{margin-left:auto;display:flex;align-items:center;gap:.45rem;}
.dcard-replies-count{font-size:.68rem;color:var(--mu);display:flex;align-items:center;gap:.22rem;}

/* Comments section */
.dcard-cmts{display:none;border-top:1px solid var(--b);background:rgba(0,0,0,.15);}
.dcard-cmts.open{display:block;}
.dcard-cmts-inner{padding:.78rem 1rem;}
.dcmt-list{display:grid;gap:.55rem;margin-bottom:.75rem;}
.dcmt{display:flex;gap:.5rem;align-items:flex-start;}
.dcmt-av{width:24px;height:24px;border-radius:50%;background:rgba(72,117,194,.1);display:flex;align-items:center;justify-content:center;font-size:.6rem;color:var(--bl2);font-weight:700;flex-shrink:0;margin-top:.1rem;}
.dcmt-bubble{background:var(--pan2);border:1px solid var(--b);border-radius:0 8px 8px 8px;padding:.5rem .72rem;flex:1;}
.dcmt-name{font-size:.7rem;font-weight:600;color:var(--tx);margin-bottom:.18rem;}
.dcmt-name .dcmt-time{font-weight:400;color:var(--mu);font-size:.64rem;margin-left:.38rem;}
.dcmt-text{font-size:.79rem;color:var(--mu);line-height:1.6;}

/* Comment input */
.dcmt-input-row{display:flex;gap:.4rem;align-items:flex-end;}
.dcmt-input-wrap{flex:1;}
.dcmt-name-in{margin-bottom:.32rem;}
.dcmt-text-in{margin-bottom:0;}
.dcmt-submit{align-self:flex-end;white-space:nowrap;}

/* Empty state */
.disc-empty{text-align:center;padding:3.5rem 2rem;color:var(--mu);}
.disc-empty-icon{font-size:2.8rem;margin-bottom:.85rem;opacity:.4;}
.disc-empty-title{font-size:.92rem;color:var(--tx);margin-bottom:.3rem;font-weight:600;}
.disc-empty-sub{font-size:.78rem;}

/* Sidebar */
.disc-sidebar-card{background:var(--pan);border:1px solid var(--b);border-radius:var(--r);padding:.95rem;margin-bottom:.95rem;}
.dsc-title{font-size:.62rem;font-weight:700;letter-spacing:2.5px;text-transform:uppercase;color:var(--go);margin-bottom:.78rem;}
.dsc-stat{display:flex;align-items:center;justify-content:space-between;padding:.42rem 0;border-bottom:1px solid var(--b);font-size:.8rem;}
.dsc-stat:last-child{border-bottom:none;}
.dsc-stat-label{color:var(--mu);}
.dsc-stat-val{color:var(--wh);font-weight:600;font-family:'DM Serif Display',serif;}
.dsc-guideline{display:flex;gap:.52rem;align-items:flex-start;padding:.42rem 0;border-bottom:1px solid var(--b);font-size:.77rem;color:var(--mu);}
.dsc-guideline:last-child{border-bottom:none;}
.dsc-guideline-icon{flex-shrink:0;font-size:.9rem;margin-top:.06rem;}

/* ══ CONTACT ══ */
.contact-grid{display:grid;grid-template-columns:1fr 1fr;gap:2.5rem;}
.ci-card{background:var(--pan);border:1px solid var(--b);border-radius:var(--r);padding:1.5rem;}
.ci-row{display:flex;align-items:center;gap:.82rem;padding:.68rem 0;border-bottom:1px solid var(--b);}
.ci-row:last-child{border-bottom:none;}
.ci-ic{width:30px;height:30px;border-radius:7px;display:flex;align-items:center;justify-content:center;font-size:.82rem;flex-shrink:0;}
.ci-key{font-size:.6rem;color:var(--mu);margin-bottom:.06rem;letter-spacing:.5px;text-transform:uppercase;}
.ci-val{color:var(--tx);font-size:.82rem;font-weight:500;}
.ci-val a{color:var(--go);text-decoration:none;}
.cf-card{background:var(--pan);border:1px solid var(--b);border-radius:var(--r);padding:1.5rem;}
.cf-card h3{font-family:'DM Serif Display',serif;font-size:1.12rem;color:var(--wh);margin-bottom:1.05rem;letter-spacing:-.1px;}

/* ══ SERVICES ══ */
.hire-hero{background:linear-gradient(150deg,#08162a 0%,#0f2240 60%,#081830 100%);border:1px solid rgba(72,117,194,.13);border-radius:18px;padding:3rem;text-align:center;margin-bottom:2.5rem;position:relative;overflow:hidden;}
.hh-grid{position:absolute;inset:0;background-image:linear-gradient(rgba(72,117,194,.05) 1px,transparent 1px),linear-gradient(90deg,rgba(72,117,194,.05) 1px,transparent 1px);background-size:24px 24px;pointer-events:none;}
.hh-stripe{position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,var(--bl),var(--go),var(--bl));z-index:1;}
.hire-hero>*{position:relative;z-index:1;}
.hire-hero h2{font-family:'DM Serif Display',serif;font-size:1.95rem;color:var(--wh);margin-bottom:.42rem;letter-spacing:-.3px;}
.hire-hero p{color:var(--mu);font-size:.89rem;margin-bottom:1.35rem;max-width:440px;margin-left:auto;margin-right:auto;line-height:1.82;}
.epill{display:inline-block;background:var(--go3);border:1px solid rgba(200,168,108,.2);color:var(--go);border-radius:7px;padding:.58rem 1.45rem;font-size:.85rem;font-weight:500;margin-bottom:1.15rem;cursor:pointer;transition:all .2s;}
.epill:hover{background:rgba(200,168,108,.14);}
.svc-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(228px,1fr));gap:1.15rem;margin-bottom:1.7rem;}
.svc-card{background:var(--pan);border:1px solid var(--b);border-radius:var(--r);padding:1.55rem;transition:all .25s;}
.svc-card:hover{border-color:rgba(200,168,108,.25);transform:translateY(-2px);}
.svc-icon{font-size:1.85rem;margin-bottom:.82rem;}
.svc-title{font-family:'DM Serif Display',serif;font-size:1.02rem;color:var(--wh);margin-bottom:.38rem;}
.svc-desc{font-size:.78rem;color:var(--mu);line-height:1.72;margin-bottom:.95rem;}
.svc-price{font-size:1.32rem;font-weight:700;color:var(--go);margin-bottom:.95rem;font-family:'DM Serif Display',serif;}
.csvc{background:var(--pan);border:1px solid rgba(56,150,100,.16);border-radius:9px;padding:.9rem 1.15rem;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:.62rem;margin-bottom:.62rem;}
.csvc h4{font-weight:600;color:var(--wh);font-size:.86rem;margin-bottom:.12rem;}
.csvc p{font-size:.74rem;color:var(--mu);}
.csvc-price{color:#4caf7d;font-weight:700;font-size:.88rem;}
.sup-card{background:var(--pan);border:1px solid rgba(200,168,108,.14);border-radius:var(--r);padding:2rem;text-align:center;margin-top:1.8rem;}
.sup-card h3{font-family:'DM Serif Display',serif;font-size:1.3rem;color:var(--wh);margin-bottom:.38rem;}
.sup-card p{color:var(--mu);font-size:.83rem;margin-bottom:1.15rem;line-height:1.82;}

/* ══ MODALS ══ */
.ov{display:none;position:fixed;inset:0;background:rgba(0,0,0,.78);z-index:600;align-items:center;justify-content:center;padding:1rem;backdrop-filter:blur(4px);}
.ov.open{display:flex;}
.modal{background:var(--sur);border:1px solid var(--b2);border-radius:15px;padding:1.75rem;width:100%;max-width:475px;max-height:90vh;overflow-y:auto;box-shadow:var(--sh);}
.mhd{display:flex;justify-content:space-between;align-items:center;margin-bottom:1.25rem;}
.mt{font-family:'DM Serif Display',serif;font-size:1.08rem;color:var(--wh);letter-spacing:-.1px;}
.mx{background:none;border:none;color:var(--mu);font-size:1.2rem;cursor:pointer;padding:.1rem;line-height:1;width:24px;height:24px;display:flex;align-items:center;justify-content:center;border-radius:4px;transition:all .2s;}
.mx:hover{color:var(--wh);background:rgba(255,255,255,.08);}
.mfr{display:grid;grid-template-columns:1fr 1fr;gap:.6rem;}
.macts{display:flex;gap:.62rem;justify-content:flex-end;margin-top:1.25rem;padding-top:.88rem;border-top:1px solid var(--b);}

/* Login */
#loginModal .modal{max-width:320px;text-align:center;}
.login-logo{font-family:'DM Serif Display',serif;font-size:1.9rem;color:var(--wh);margin-bottom:.22rem;}
.login-logo span{color:var(--go);}
.login-sub{font-size:.78rem;color:var(--mu);margin-bottom:1.35rem;}
.login-err{color:var(--re);font-size:.76rem;margin-top:.42rem;display:none;}
.login-err.show{display:block;}

/* FAB */
.fab{position:fixed;bottom:1.8rem;right:1.8rem;z-index:100;width:44px;height:44px;border-radius:50%;background:linear-gradient(135deg,var(--go),var(--go2));color:#07090d;border:none;font-size:1.3rem;cursor:pointer;box-shadow:0 6px 22px rgba(200,168,108,.3);transition:all .22s;display:none;align-items:center;justify-content:center;font-weight:700;}
.fab:hover{transform:scale(1.1);}

/* Footer */
footer{border-top:1px solid var(--b);padding:1.5rem 2rem;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:.9rem;}
.ft-brand{font-family:'DM Serif Display',serif;font-size:.9rem;color:var(--wh);}
.ft-brand span{color:var(--go);}
.ft-copy{font-size:.7rem;color:var(--mu);}

/* ══ ANIMATIONS ══ */
@keyframes fadeUp{from{opacity:0;transform:translateY(28px);}to{opacity:1;transform:none;}}
@keyframes glow{0%,100%{opacity:.6;}50%{opacity:1;}}

/* Gold gradient on section titles */
.sec-t{background:linear-gradient(135deg,var(--wh) 0%,rgba(240,237,230,1) 60%,var(--go2) 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;}
[data-theme="light"] .sec-t{background:var(--wh);-webkit-text-fill-color:var(--wh);}

/* Chip hover lift */
.chip{cursor:default;transition:all .22s;}
.chip:hover{transform:translateY(-2px);box-shadow:0 4px 14px rgba(0,0,0,.2);}

/* Smooth focus visible */
:focus-visible{outline:2px solid var(--go);outline-offset:2px;border-radius:4px;}

/* ══ RESPONSIVE ══ */
@media(max-width:920px){
  nav{padding:0 1.15rem;}
  .nav-links{display:none;}
  .ham{display:block;}
  .hero{grid-template-columns:1fr;padding:72px 1.5rem 3rem;gap:2.5rem;}
  .idc{max-width:320px;margin:0 auto;animation:none;}
  .section{padding:3.8rem 1.5rem 3rem;}
  .about-grid,.contact-grid{grid-template-columns:1fr;gap:2rem;}
  .posts-layout,.disc-layout{grid-template-columns:1fr;}
  .psidebar,.disc-sidebar{order:-1;}
  footer{padding:1.2rem 1.5rem;}
  .mfr,.frow{grid-template-columns:1fr;}
  .c-inner{padding:0 1.5rem;}
}
@media(max-width:560px){
  .hero h1{font-size:2rem;}
  .hire-hero{padding:2rem 1.2rem;}
  .ctabs{flex-wrap:wrap;}
  .ptabs{gap:.1rem;}
  .ptab{font-size:.69rem;padding:.32rem .58rem;}
}
</style>
</head>
<body>

<!-- LOADER -->
<div id="loader">
  <div class="ld-logo"><span>N.</span>Aldhoun</div>
  <div class="ld-tag">Aeronautical Engineer</div>
  <div class="ld-bar"><div class="ld-fill"></div></div>
</div>
<div class="toast" id="toast"></div>

<!-- NAV -->
<nav>
  <div class="nav-logo" onclick="showPage('home')">
    <span class="nl">N.</span>Aldhoun
    <span class="admin-badge">ADMIN</span>
  </div>
  <div class="nav-links">
    <a class="active" onclick="showPage('home',this)">Home</a>
    <a onclick="showPage('about',this)">About</a>
    <a onclick="showPage('works',this)">Projects</a>
    <a onclick="showPage('posts',this)">Posts</a>
    <a onclick="showPage('journey',this)">Journey</a>
    <a onclick="showPage('discuss',this)">Discussion</a>
  </div>
  <div class="nav-r">
    <button class="icon-btn" onclick="toggleTheme()">◐</button>
    <button class="icon-btn admin-only" onclick="doSignOut()">↪ Logout</button>
    <button class="icon-btn" id="loginNavBtn" onclick="openM('loginModal')" style="display:none;">🔐</button>
    <button class="hire-btn" onclick="showPage('services',null)">Hire Me ↗</button>
    <button class="ham" onclick="toggleMob()">☰</button>
  </div>
</nav>
<div class="mob" id="mobMenu">
  <a onclick="nav2('home')">Home</a>
  <a onclick="nav2('about')">About</a>
  <a onclick="nav2('works')">Projects</a>
  <a onclick="nav2('posts')">Posts</a>
  <a onclick="nav2('journey')">Journey</a>
  <a onclick="nav2('discuss')">Discussion</a>
  <a onclick="nav2('contact')">Contact</a>
  <button onclick="nav2('services')" style="background:linear-gradient(135deg,var(--go),var(--go2));color:#07090d;font-weight:700;border-radius:7px;margin-top:.3rem;">Hire Me ↗</button>
  <button class="admin-only" onclick="doSignOut()" style="color:var(--re);background:none;border:1px solid rgba(209,78,78,.2);border-radius:7px;margin-top:.3rem;">↪ Logout</button>
</div>

<!-- ══ HOME ══ -->
<div id="page-home" class="page active">
<div class="hero">
  <div class="hbg">
    <div class="hgrid"></div>
    <div class="hgrid2"></div>
    <div class="hglow-blue"></div>
    <div class="hglow-gold"></div>

    <!-- Large transparent background airplane -->
    <svg class="plane-bg" viewBox="0 0 800 300" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M790 150L520 10L480 150L520 165L500 290L370 185L280 200L0 150L280 100L370 115L500 10L520 135L480 150Z" fill="white"/>
      <path d="M480 150L520 135L790 150L520 165L480 150Z" fill="rgba(200,168,108,0.3)"/>
      <path d="M100 150L280 100L370 115" stroke="rgba(255,255,255,0.1)" stroke-width="1"/>
      <rect x="490" y="145" width="60" height="10" rx="2" fill="rgba(200,168,108,0.15)"/>
      <circle cx="500" cy="150" r="4" fill="rgba(200,168,108,0.3)"/>
    </svg>

    <!-- Animated flying airplane -->
    <div class="airplane-wrapper">
      <svg class="plane-fly" width="65" height="28" viewBox="0 0 65 28" fill="none">
        <path d="M0 14L52 0L65 14L52 17L57 28L42 20L32 22L0 14Z" fill="white"/>
        <path d="M52 17L65 14L52 14Z" fill="rgba(200,168,108,0.5)"/>
        <circle cx="52" cy="14" r="2" fill="rgba(200,168,108,0.6)"/>
        <path d="M20 14L32 22L42 20" stroke="rgba(200,168,108,0.3)" stroke-width="0.5"/>
      </svg>
      <div class="contrail"></div>
    </div>
  </div>

  <div class="hero-l rev">
    <div class="status-pill rev d1"><div class="sdot"></div>Open to Work — Junior / Entry Level</div>
    <h1>I engineer<br><em>aircraft structures</em><span class="sub">& simulate flight.</span></h1>
    <p class="hero-d rev d1"><strong>Nashat Omar Aldhoun</strong> — Junior Aeronautical Engineer from JUST. Specialized in Aircraft Structures, FEA, Modal Analysis & MRO. Trained at the Royal Jordanian Air Force.</p>

    <div class="hero-email rev d2" id="heroEmailBox">
      <div class="em-dot"></div>
      <span class="em-val" id="emVal" onclick="openMailto()"></span>
      <button class="em-copy" onclick="copyEmail()">Copy</button>
    </div>

    <div class="hero-ctas rev d2">
      <button class="btn btn-go" onclick="showPage('works',null)">View Projects →</button>
      <button class="btn btn-gh" onclick="showPage('contact',null)">Contact Me</button>
    </div>
    <div class="hmetrics rev d3">
      <div class="hm"><div class="hm-n" id="hm-w">3<span>+</span></div><div class="hm-l">Projects</div></div>
      <div class="hm"><div class="hm-n">8<span>wk</span></div><div class="hm-l">RJAF Training</div></div>
      <div class="hm"><div class="hm-n" id="hm-p">3<span>+</span></div><div class="hm-l">Posts</div></div>
    </div>
  </div>

  <div class="rev d1">
    <div class="idc">
      <div class="idc-top">
        <div class="idc-grid"></div>
        <div class="idc-stripe"></div>
        <div class="avatar" id="avatarEl">NA</div>
        <div class="idc-name">Nashat Omar Aldhoun</div>
        <div class="idc-role">Aeronautical Engineer</div>
        <button class="photo-btn admin-only" onclick="document.getElementById('photoIn').click()">+ Upload Photo</button>
        <input type="file" id="photoIn" accept="image/*" style="display:none" onchange="handleProfilePhoto(event)">
      </div>
      <div class="idc-body">
        <div class="idc-row">
          <div class="idc-ic" style="background:rgba(72,117,194,.1);">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="var(--bl2)" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
          </div>
          <div><div class="idc-key">Location</div><div class="idc-val">Irbid, Jordan</div></div>
        </div>
        <div class="idc-row">
          <div class="idc-ic" style="background:rgba(200,168,108,.1);">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="var(--go)" stroke-width="2"><path d="M22 10v6M2 10l10-5 10 5-10 5z"/><path d="M6 12v5c3 3 9 3 12 0v-5"/></svg>
          </div>
          <div><div class="idc-key">Education</div><div class="idc-val">B.Sc. Aero. Eng. — JUST '25</div></div>
        </div>
        <div class="idc-row">
          <div class="idc-ic" style="background:rgba(130,96,210,.1);">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="var(--pu)" stroke-width="2"><path d="M12 2L2 7l10 5 10-5-10-5z"/><path d="M2 17l10 5 10-5M2 12l10 5 10-5"/></svg>
          </div>
          <div><div class="idc-key">Training</div><div class="idc-val">RJAF Overhaul Dept.</div></div>
        </div>
        <div class="idc-row">
          <div class="idc-ic" style="background:rgba(56,150,100,.1);">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#4caf7d" stroke-width="2"><circle cx="12" cy="12" r="3"/><path d="M19.07 4.93a10 10 0 0 1 0 14.14M4.93 4.93a10 10 0 0 0 0 14.14"/></svg>
          </div>
          <div><div class="idc-key">Specialization</div><div class="idc-val">Structures · FEA · MRO</div></div>
        </div>
      </div>
      <div class="idc-foot">
        <a href="javascript:void(0)" onclick="openMailto()" id="idcEmailLink">
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>
          Email
        </a>
        <a href="https://www.linkedin.com/in/nashat-al-dhoun" target="_blank">
          <svg width="12" height="12" viewBox="0 0 24 24" fill="currentColor"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 0 1-2.063-2.065 2.064 2.064 0 1 1 2.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>
          LinkedIn
        </a>
        <a href="javascript:void(0)" onclick="downloadCV()">
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
          CV
        </a>
      </div>
    </div>
  </div>
</div>

<!-- CAROUSEL -->
<div class="carousel-section">
  <div class="c-inner">
    <div class="c-head">
      <div class="c-title">Highlights</div>
      <div class="c-controls">
        <div class="ctabs">
          <button class="ctab on" onclick="switchCarousel('works',this)">✈ Projects</button>
          <button class="ctab" onclick="switchCarousel('journey',this)">🗓 Journey</button>
          <button class="ctab" onclick="switchCarousel('posts',this)">📝 Posts</button>
        </div>
        <div class="cnav">
          <button class="cnav-btn" onclick="carouselPrev()">←</button>
          <button class="cnav-btn" onclick="carouselNext()">→</button>
        </div>
      </div>
    </div>
    <div class="c-slider">
      <div class="c-track" id="cTrack"></div>
    </div>
    <div class="cdots" id="cDots"></div>
  </div>
</div>
</div>

<!-- ══ ABOUT ══ -->
<div id="page-about" class="page">
<div class="section">
  <div class="rev"><div class="eyebrow">About Me</div><h2 class="sec-t">Engineer. Analyst.<br>Problem Solver.</h2></div>
  <div class="about-grid">
    <div class="rev">
      <p class="ap"><strong>Nashat Omar Aldhoun</strong> is a 2025 Aeronautical Engineering graduate from JUST with deep expertise in Aircraft Structures and MRO operations.</p>
      <p class="ap">His graduation project — <strong>Vibration Analysis on an Aircraft Wing</strong> — covered 3D modeling in Creo, modal analysis comparing Aluminum vs. CFRP in ANSYS, and CFD aerodynamic stability simulations with a validated notch-filter mitigation system.</p>
      <p class="ap">8-week training at the <strong>Royal Jordanian Air Force Overhaul Department</strong> gave him hands-on exposure to hydraulic systems, overhaul procedures, and aviation safety protocols.</p>
      <div class="sg"><div class="sg-l">Engineering Software</div><div class="chips"><span class="chip">Creo</span><span class="chip">ANSYS CFD</span><span class="chip">SolidWorks</span><span class="chip">MATLAB</span></div></div>
      <div class="sg"><div class="sg-l">Core Skills</div><div class="chips"><span class="chip">FEA</span><span class="chip">Modal Analysis</span><span class="chip">CFD Simulation</span><span class="chip">Aircraft MRO</span><span class="chip">Power BI</span><span class="chip">Structural Analysis</span></div></div>
      <div class="sg"><div class="sg-l">Languages</div><div class="chips"><span class="chip">Arabic — Native</span><span class="chip">English — B2</span></div></div>
      <div class="cv-box">
        <div>
          <h4>Curriculum Vitae</h4>
          <p>Download my full CV as PDF</p>
          <div style="margin-top:.42rem;font-size:.76rem;" id="aboutEmail"></div>
        </div>
        <button class="btn btn-go btn-sm" onclick="downloadCV()">⬇ Download CV</button>
      </div>
    </div>
    <div class="rev d1">
      <div class="eyebrow" style="margin-bottom:1.15rem;">Timeline</div>
      <div class="tl-item"><div class="tl-date">Sep–Oct<br>2025</div><div><div class="tl-t">Overhaul Dept. Trainee</div><div class="tl-o">Royal Jordanian Air Force</div><div class="tl-d">8-week intensive aircraft maintenance. Hydraulic systems, functional testing, aviation safety.</div></div></div>
      <div class="tl-item"><div class="tl-date">2021–2025</div><div><div class="tl-t">B.Sc. Aeronautical Engineering</div><div class="tl-o">JUST — Jordan</div><div class="tl-d">Graduation: Vibration Analysis on Aircraft Wing using ANSYS, Creo & CFD.</div></div></div>
      <div class="tl-item"><div class="tl-date">2026</div><div><div class="tl-t">Power BI Certification</div><div class="tl-o">Data Analysis & Visualization</div></div></div>
      <div class="tl-item"><div class="tl-date">2024</div><div><div class="tl-t">Employment Skills Training</div><div class="tl-o">Professional Development — 5 hrs</div></div></div>
    </div>
  </div>
</div>
</div>

<!-- ══ WORKS ══ -->
<div id="page-works" class="page">
<div class="section">
  <div class="sec-row rev">
    <div><div class="eyebrow">Portfolio</div><h2 class="sec-t">Projects & Works</h2><p class="sec-s" style="margin-bottom:0;">Click any project for full details.</p></div>
    <button class="btn btn-go btn-sm admin-only" onclick="openM('workModal')">+ Add Project</button>
  </div>
  <div class="wgrid rev" id="worksGrid"></div>
</div>
</div>

<!-- ══ POSTS ══ -->
<div id="page-posts" class="page">
<div class="section">
  <div class="sec-row rev">
    <div><div class="eyebrow">Knowledge Feed</div><h2 class="sec-t">Scientific Posts</h2><p class="sec-s" style="margin-bottom:0;">Articles, links, videos, documents, and images.</p></div>
    <button class="btn btn-go btn-sm admin-only" onclick="openM('postModal')">+ New Post</button>
  </div>
  <div class="posts-layout rev">
    <div>
      <div class="pcompose admin-only-block" id="postCompose">
        <div class="pcompose-l">Create New Post</div>
        <div class="ptabs">
          <button class="ptab active" onclick="switchPTab('article',this)">📝 Article</button>
          <button class="ptab" onclick="switchPTab('link',this)">🔗 Link</button>
          <button class="ptab" onclick="switchPTab('video',this)">▶ Video</button>
          <button class="ptab" onclick="switchPTab('doc',this)">📄 Doc</button>
          <button class="ptab" onclick="switchPTab('image',this)">🖼 Image</button>
        </div>
        <input type="hidden" id="pType" value="article">
        <input class="field" id="pTitle" placeholder="Post title">
        <textarea class="field" id="pContent" placeholder="Write here..."></textarea>
        <div class="ptype-panel active" id="pt-article"></div>
        <div class="ptype-panel" id="pt-link">
          <input class="field" id="pUrl" placeholder="https://...">
          <input class="field" id="pLinkTitle" placeholder="Link title">
          <input class="field" id="pLinkIcon" placeholder="🌐 Icon">
        </div>
        <div class="ptype-panel" id="pt-video">
          <input class="field" id="pVideoUrl" placeholder="YouTube URL">
        </div>
        <div class="ptype-panel" id="pt-doc">
          <input class="field" id="pDocName" placeholder="Document name">
          <input class="field" id="pDocUrl" placeholder="Document URL">
        </div>
        <div class="ptype-panel" id="pt-image">
          <input type="file" accept="image/*" id="pImgFile" class="field" onchange="prevPostImg(event)" style="padding:.5rem;">
          <img id="pImgPrev" class="img-prev" src="" alt="">
        </div>
        <input class="field" id="pTags" placeholder="Tags: CFD, Structures, MRO">
        <div style="display:flex;justify-content:flex-end;">
          <button class="btn btn-go btn-sm" onclick="savePost()">Publish →</button>
        </div>
      </div>
      <div id="postFeed"></div>
    </div>
    <div class="psidebar">
      <div class="scard"><div class="scard-t">Filter by Topic</div><div class="tag-cloud" id="tagCloud"></div><div style="font-size:.64rem;color:var(--mu);margin-top:.52rem;" id="filterCount"></div></div>
      <div class="scard"><div class="scard-t">Post Types</div><div style="display:grid;gap:.32rem;font-size:.75rem;color:var(--mu);line-height:1.6;">
        <span>📝 Article — Written content</span>
        <span>🔗 Link — Website preview</span>
        <span>▶ Video — YouTube embed</span>
        <span>📄 Document — PDF/file</span>
        <span>🖼 Image — Photo</span>
      </div></div>
    </div>
  </div>
</div>
</div>

<!-- ══ JOURNEY ══ -->
<div id="page-journey" class="page">
<div class="section">
  <div class="sec-row rev">
    <div>
      <div class="eyebrow">My Journey</div>
      <h2 class="sec-t">Courses, Events<br>& Milestones</h2>
      <p class="sec-s" style="margin-bottom:0;">A visual timeline of my academic life, courses, events, and key moments.</p>
    </div>
    <button class="btn btn-go btn-sm admin-only" onclick="openM('journeyModal')">+ Add Entry</button>
  </div>
  <div class="jtabs rev">
    <button class="jtab on" onclick="filterJourney('all',this)">All</button>
    <button class="jtab" onclick="filterJourney('milestone',this)">🏆 Milestones</button>
    <button class="jtab" onclick="filterJourney('course',this)">📚 Courses</button>
    <button class="jtab" onclick="filterJourney('event',this)">🎤 Events</button>
  </div>
  <div class="journey-timeline rev" id="journeyTimeline"></div>
</div>
</div>

<!-- ══ DISCUSSION — محسّنة ══ -->
<div id="page-discuss" class="page">
<div class="section">
  <div class="sec-row rev">
    <div>
      <div class="eyebrow">Community</div>
      <h2 class="sec-t">Open Discussion</h2>
      <p class="sec-s" style="margin-bottom:0;">Explore topics posted by Nashat and join the conversation.</p>
    </div>
    <button class="btn btn-go btn-sm admin-only" onclick="openM('discussModal')">+ New Topic</button>
  </div>

  <div class="disc-layout rev">
    <div class="disc-main">
      <!-- Admin compose inline -->
      <div class="disc-compose admin-only-block">
        <div class="disc-compose-head">
          <div class="disc-compose-av">NA</div>
          <div>
            <div class="disc-compose-label">Start a Discussion</div>
            <div class="disc-compose-sub">Share a topic, question, or idea with your audience</div>
          </div>
        </div>
        <input class="field" id="dTitle" placeholder="Topic title...">
        <textarea class="field" id="dText" placeholder="Write your discussion post..." style="min-height:88px;"></textarea>
        <div style="display:flex;justify-content:flex-end;">
          <button class="btn btn-go btn-sm" onclick="addDiscussPost()">Publish Topic →</button>
        </div>
      </div>
      <div class="disc-feed" id="cmtsList"></div>
    </div>

    <div class="disc-sidebar">
      <div class="disc-sidebar-card">
        <div class="dsc-title">Discussion Stats</div>
        <div class="dsc-stat"><span class="dsc-stat-label">Topics</span><span class="dsc-stat-val" id="discTopicCount">0</span></div>
        <div class="dsc-stat"><span class="dsc-stat-label">Comments</span><span class="dsc-stat-val" id="discCmtCount">0</span></div>
        <div class="dsc-stat"><span class="dsc-stat-label">Likes</span><span class="dsc-stat-val" id="discLikeCount">0</span></div>
      </div>
      <div class="disc-sidebar-card">
        <div class="dsc-title">Guidelines</div>
        <div class="dsc-guideline"><span class="dsc-guideline-icon">✈</span><span>Keep discussions aerospace-related or academic</span></div>
        <div class="dsc-guideline"><span class="dsc-guideline-icon">💬</span><span>Feel free to ask questions or share ideas</span></div>
        <div class="dsc-guideline"><span class="dsc-guideline-icon">🤝</span><span>Be respectful and constructive</span></div>
        <div class="dsc-guideline"><span class="dsc-guideline-icon">📌</span><span>New topics are posted by Nashat only</span></div>
      </div>
    </div>
  </div>
</div>
</div>

<!-- ══ CONTACT ══ -->
<div id="page-contact" class="page">
<div class="section">
  <div class="rev"><div class="eyebrow">Get In Touch</div><h2 class="sec-t">Contact Me</h2><p class="sec-s">Whether it's a job opportunity, collaboration, or just a question.</p></div>
  <div class="contact-grid rev">
    <div>
      <div class="ci-card">
        <div class="ci-row"><div class="ci-ic" style="background:rgba(200,168,108,.1);"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="var(--go)" stroke-width="2"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg></div><div><div class="ci-key">Email</div><div class="ci-val" id="contactEmail"></div></div></div>
        <div class="ci-row"><div class="ci-ic" style="background:rgba(72,117,194,.1);"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="var(--bl2)" stroke-width="2"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07A19.5 19.5 0 0 1 4.36 14a19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 3.11 3h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L7.91 10.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 17.92z"/></svg></div><div><div class="ci-key">Phone / WhatsApp</div><div class="ci-val">+962 776 763 628</div></div></div>
        <div class="ci-row"><div class="ci-ic" style="background:rgba(209,78,78,.1);"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="var(--re)" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg></div><div><div class="ci-key">Location</div><div class="ci-val">Irbid, Jordan</div></div></div>
        <div class="ci-row"><div class="ci-ic" style="background:rgba(130,96,210,.1);"><svg width="13" height="13" viewBox="0 0 24 24" fill="currentColor" style="color:var(--pu)"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 0 1-2.063-2.065 2.064 2.064 0 1 1 2.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg></div><div><div class="ci-key">LinkedIn</div><div class="ci-val"><a href="https://www.linkedin.com/in/nashat-al-dhoun" target="_blank">Nashat Al Dhoun</a></div></div></div>
        <div class="ci-row"><div class="ci-ic" style="background:rgba(56,150,100,.1);"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#4caf7d" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg></div><div><div class="ci-key">Status</div><div class="ci-val" style="color:#4caf7d;">Open to work — Junior roles</div></div></div>
      </div>
    </div>
    <div class="cf-card rev d1">
      <h3>Send a Message</h3>
      <div class="frow">
        <div><label class="flabel">Your Name</label><input class="field" id="cf-name" placeholder="John Doe" style="margin-bottom:0;"></div>
        <div><label class="flabel">Email</label><input class="field" id="cf-email" placeholder="email@co.com" style="margin-bottom:0;"></div>
      </div><br>
      <label class="flabel">Subject</label>
      <select class="field" id="cf-subj"><option>Job Opportunity</option><option>Project Collaboration</option><option>Service Inquiry</option><option>Academic Discussion</option><option>Other</option></select>
      <label class="flabel">Message</label>
      <textarea class="field" id="cf-msg" style="min-height:108px;" placeholder="Write your message..."></textarea>
      <button class="btn btn-go" style="width:100%;" onclick="sendContact()">Send Message →</button>
    </div>
  </div>
</div>
</div>

<!-- ══ SERVICES ══ -->
<div id="page-services" class="page">
<div class="section">
  <div class="hire-hero rev">
    <div class="hh-grid"></div><div class="hh-stripe"></div>
    <div class="eyebrow" style="justify-content:center;margin-bottom:.62rem;">Available for Work</div>
    <h2>Work With Nashat</h2>
    <p>Need structural analysis, 3D modeling, or engineering reports? Let's collaborate.</p>
    <div class="epill" id="svcEmailPill" onclick="copyEmail()"></div><br>
    <a class="btn btn-go" id="svcEmailLink">Send Inquiry →</a>
  </div>
  <div class="svc-grid rev">
    <div class="svc-card"><div class="svc-icon">🔧</div><div class="svc-title">Structural Analysis</div><div class="svc-desc">FEA & Modal Analysis using ANSYS or SolidWorks. Full reports with charts.</div><div class="svc-price">From $50</div><a class="btn btn-go btn-sm" id="svc1Link">Request →</a></div>
    <div class="svc-card"><div class="svc-icon">📐</div><div class="svc-title">3D Modeling</div><div class="svc-desc">Aircraft & mechanical modeling using Creo or SolidWorks.</div><div class="svc-price">From $30</div><a class="btn btn-go btn-sm" id="svc2Link">Request →</a></div>
    <div class="svc-card"><div class="svc-icon">📊</div><div class="svc-title">Data Reports</div><div class="svc-desc">Engineering data visualization with Power BI dashboards.</div><div class="svc-price">From $20</div><a class="btn btn-go btn-sm" id="svc3Link">Request →</a></div>
  </div>
  <div class="sec-row rev" style="margin-bottom:.95rem;">
    <div class="eyebrow">Custom Services</div>
    <button class="btn btn-gh btn-sm admin-only" onclick="openM('svcModal')">+ Add Service</button>
  </div>
  <div id="customSvcs" class="rev"></div>
  <div class="sup-card rev">
    <h3>☕ Support My Work</h3>
    <p>If my content or tools helped you, consider supporting via PayPal or bank transfer.</p>
    <div class="epill" id="supEmailPill" onclick="copyEmail()" style="margin-bottom:1rem;"></div><br>
    <button class="btn btn-go btn-sm" onclick="openM('donateModal')">Send a Coffee</button>
  </div>
</div>
</div>

<!-- ══ MODALS ══ -->

<!-- LOGIN -->
<div class="ov" id="loginModal">
<div class="modal" style="max-width:310px;text-align:center;">
  <div class="login-logo"><span>N.</span>Aldhoun</div>
  <div class="login-sub">Admin access only</div>
  <input class="field" id="loginEmail" type="email" placeholder="your@email.com">
  <input class="field" id="loginPass" type="password" placeholder="Password" style="margin-bottom:.25rem;">
  <div class="login-err" id="loginErr">Wrong email or password.</div>
  <div class="macts" style="justify-content:center;margin-top:.88rem;border-top:none;padding-top:0;">
    <button class="btn btn-gh btn-sm" onclick="closeM('loginModal')">Cancel</button>
    <button class="btn btn-go btn-sm" onclick="doLogin()">Sign In</button>
  </div>
</div>
</div>

<!-- WORK -->
<div class="ov" id="workModal">
<div class="modal">
  <div class="mhd"><div class="mt">Add / Edit Project</div><button class="mx" onclick="closeM('workModal')">×</button></div>
  <input type="hidden" id="ewId">
  <div class="mfr">
    <div><label class="flabel">Title</label><input class="field" id="wT" placeholder="Project name" style="margin-bottom:0;"></div>
    <div><label class="flabel">Emoji</label><input class="field" id="wE" placeholder="✈" style="margin-bottom:0;"></div>
  </div><br>
  <label class="flabel">Category</label>
  <select class="field" id="wC"><option>Simulation</option><option>3D Modeling</option><option>MRO</option><option>Data Analysis</option><option>Research</option><option>Design</option><option>Other</option></select>
  <label class="flabel">Description</label>
  <textarea class="field" id="wD" placeholder="Describe the project, tools, and outcomes..."></textarea>
  <div class="mfr">
    <div><label class="flabel">Year</label><input class="field" id="wY" placeholder="2025" style="margin-bottom:0;"></div>
    <div><label class="flabel">Price</label><input class="field" id="wP" placeholder="$50" style="margin-bottom:0;"></div>
  </div><br>
  <label class="flabel">Link (optional)</label>
  <input class="field" id="wL" placeholder="https://..." style="margin-bottom:0;">
  <div class="macts">
    <button class="btn btn-gh btn-sm" onclick="closeM('workModal')">Cancel</button>
    <button class="btn btn-go btn-sm" onclick="saveWork()">Save</button>
  </div>
</div>
</div>

<!-- PROJECT DETAIL -->
<div class="ov" id="pdModal">
<div class="modal" style="max-width:560px;">
  <div class="mhd"><div class="mt" id="pd-t"></div><button class="mx" onclick="closeM('pdModal')">×</button></div>
  <div style="height:165px;background:linear-gradient(135deg,#08162a,#0f2240);border-radius:10px;margin-bottom:1.05rem;display:flex;align-items:center;justify-content:center;font-size:3.8rem;position:relative;overflow:hidden;">
    <div style="position:absolute;inset:0;background-image:linear-gradient(rgba(72,117,194,.07) 1px,transparent 1px),linear-gradient(90deg,rgba(72,117,194,.07) 1px,transparent 1px);background-size:16px 16px;"></div>
    <img id="pd-img" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;display:none;" src="" alt="">
    <span id="pd-em" style="position:relative;z-index:1;"></span>
  </div>
  <div id="pd-meta" style="display:flex;gap:.42rem;flex-wrap:wrap;margin-bottom:.82rem;"></div>
  <div id="pd-desc" style="font-size:.85rem;color:var(--mu);line-height:1.85;margin-bottom:1.05rem;"></div>
  <div id="pd-link"></div>
</div>
</div>

<!-- POST MODAL -->
<div class="ov" id="postModal">
<div class="modal" style="max-width:510px;">
  <div class="mhd"><div class="mt">New Post</div><button class="mx" onclick="closeM('postModal')">×</button></div>
  <input type="hidden" id="mPType" value="article">
  <div class="ptabs" id="modalPTabs">
    <button class="ptab active" onclick="switchModalPTab('article',this)">📝 Article</button>
    <button class="ptab" onclick="switchModalPTab('link',this)">🔗 Link</button>
    <button class="ptab" onclick="switchModalPTab('video',this)">▶ Video</button>
    <button class="ptab" onclick="switchModalPTab('doc',this)">📄 Doc</button>
    <button class="ptab" onclick="switchModalPTab('image',this)">🖼 Image</button>
  </div>
  <label class="flabel">Title</label><input class="field" id="mPTitle" placeholder="Post title">
  <label class="flabel">Content</label><textarea class="field" id="mPContent" placeholder="Write here..."></textarea>
  <div class="ptype-panel active" id="mpt-article"></div>
  <div class="ptype-panel" id="mpt-link">
    <input class="field" id="mPUrl" placeholder="https://...">
    <input class="field" id="mPLinkTitle" placeholder="Link title">
    <input class="field" id="mPLinkIcon" placeholder="🌐">
  </div>
  <div class="ptype-panel" id="mpt-video">
    <input class="field" id="mPVideoUrl" placeholder="YouTube URL">
  </div>
  <div class="ptype-panel" id="mpt-doc">
    <input class="field" id="mPDocName" placeholder="Document name">
    <input class="field" id="mPDocUrl" placeholder="Document URL">
  </div>
  <div class="ptype-panel" id="mpt-image">
    <input type="file" accept="image/*" id="mPImgFile" class="field" onchange="prevModalImg(event)" style="padding:.5rem;">
    <img id="mPImgPrev" class="img-prev" src="" alt="">
  </div>
  <label class="flabel">Tags</label>
  <input class="field" id="mPTags" placeholder="CFD, Structures, MRO" style="margin-bottom:0;">
  <div class="macts">
    <button class="btn btn-gh btn-sm" onclick="closeM('postModal')">Cancel</button>
    <button class="btn btn-go btn-sm" onclick="savePostModal()">Publish</button>
  </div>
</div>
</div>

<!-- JOURNEY -->
<div class="ov" id="journeyModal">
<div class="modal">
  <div class="mhd"><div class="mt">Add Journey Entry</div><button class="mx" onclick="closeM('journeyModal')">×</button></div>
  <label class="flabel">Type</label>
  <select class="field" id="jType"><option value="milestone">🏆 Milestone</option><option value="course">📚 Course</option><option value="event">🎤 Event</option></select>
  <div class="mfr">
    <div><label class="flabel">Title</label><input class="field" id="jTitle" placeholder="e.g. Graduated JUST" style="margin-bottom:0;"></div>
    <div><label class="flabel">Date</label><input class="field" id="jDate" placeholder="2025-07" style="margin-bottom:0;"></div>
  </div><br>
  <label class="flabel">Organization</label>
  <input class="field" id="jOrg" placeholder="e.g. JUST, RJAF, Online">
  <label class="flabel">Description</label>
  <textarea class="field" id="jDesc" placeholder="What did you learn or achieve?" style="min-height:72px;"></textarea>
  <label class="flabel">Image (optional)</label>
  <input type="file" accept="image/*" id="jImgFile" class="field" onchange="prevJourneyImg(event)" style="padding:.5rem;">
  <img id="jImgPrev" class="img-prev" src="" alt="">
  <div class="macts">
    <button class="btn btn-gh btn-sm" onclick="closeM('journeyModal')">Cancel</button>
    <button class="btn btn-go btn-sm" onclick="saveJourney()">Save</button>
  </div>
</div>
</div>

<!-- DISCUSS MODAL -->
<div class="ov" id="discussModal">
<div class="modal">
  <div class="mhd"><div class="mt">New Discussion Topic</div><button class="mx" onclick="closeM('discussModal')">×</button></div>
  <label class="flabel">Title</label>
  <input class="field" id="dmTitle" placeholder="What's the topic?">
  <label class="flabel">Content</label>
  <textarea class="field" id="dmText" style="min-height:95px;" placeholder="Share your thoughts, questions, or insights..."></textarea>
  <div class="macts">
    <button class="btn btn-gh btn-sm" onclick="closeM('discussModal')">Cancel</button>
    <button class="btn btn-go btn-sm" onclick="addDiscussPost()">Publish →</button>
  </div>
</div>
</div>

<!-- SERVICE -->
<div class="ov" id="svcModal">
<div class="modal">
  <div class="mhd"><div class="mt">Add Custom Service</div><button class="mx" onclick="closeM('svcModal')">×</button></div>
  <label class="flabel">Name</label><input class="field" id="sN" placeholder="e.g. CFD Consulting">
  <label class="flabel">Description</label><textarea class="field" id="sD" style="min-height:62px;" placeholder="What do you offer?"></textarea>
  <label class="flabel">Price</label><input class="field" id="sP" placeholder="$40 / project">
  <div class="macts">
    <button class="btn btn-gh btn-sm" onclick="closeM('svcModal')">Cancel</button>
    <button class="btn btn-go btn-sm" onclick="saveSvc()">Add</button>
  </div>
</div>
</div>

<!-- DONATE -->
<div class="ov" id="donateModal">
<div class="modal" style="text-align:center;">
  <div class="mhd"><div class="mt">☕ Support Nashat</div><button class="mx" onclick="closeM('donateModal')">×</button></div>
  <p style="color:var(--mu);font-size:.83rem;margin-bottom:1.25rem;line-height:1.78;">Thank you for your support! Contact via email to complete via PayPal or bank transfer.</p>
  <div class="epill" id="donateEmailPill" onclick="copyEmail()"></div>
  <div class="macts" style="justify-content:center;margin-top:1.25rem;"><button class="btn btn-gh btn-sm" onclick="closeM('donateModal')">Close</button></div>
</div>
</div>

<button class="fab" id="fab">+</button>
<footer>
  <div class="ft-brand"><span>N.</span>Aldhoun — Aeronautical Engineer</div>
  <div class="ft-copy">Irbid, Jordan · <span id="footerEmail" style="cursor:pointer;color:var(--go);transition:color .2s;" onclick="copyEmail()" onmouseenter="this.style.color='var(--go2)'" onmouseleave="this.style.color='var(--go)'"></span></div>
</footer>

<script>
// ══ STATE ══
let isAdmin=false;
let works=[],posts=[],journey=[],comments=[],customSvcs=[];
let activeTag='',activeJType='all';
let cType='works',cIdx=0,cAuto;

// ══ REFRESH — instant update after any DB change ══
window._refresh = async function(t){
  const{data}=await _supa.from(t).select('*').order('created_at',{ascending:false});
  if(!data) return;
  if(t==='works'){
    works=data.map(r=>({id:r.id,title:r.title||'',emoji:r.emoji||'📁',cat:r.cat||'',desc:r.description||'',year:r.year||'',link:r.link||'',price:r.price||'',photo:r.photo||''}));
    renderWorks();renderCarousel();updateStats();
  }else if(t==='posts'){
    posts=data.map(r=>({id:r.id,type:r.type||'article',title:r.title||'',content:r.content||'',tags:Array.isArray(r.tags)?r.tags:[],date:r.date||'',likes:r.likes||0,liked:false,comments:Array.isArray(r.comments)?r.comments:[],url:r.url||'',linkTitle:r.link_title||'',linkIcon:r.link_icon||'🌐',videoId:r.video_id||'',docName:r.doc_name||'',docUrl:r.doc_url||'',imgData:r.img_data||''}));
    renderPosts(activeTag);renderCarousel();updateStats();
  }else if(t==='journey'){
    journey=data.map(r=>({id:r.id,type:r.type||'milestone',title:r.title||'',org:r.org||'',date:r.date||'',desc:r.description||'',img:r.img||''})).reverse();
    renderJourney(activeJType);renderCarousel();
  }else if(t==='comments'){
    comments=data.map(r=>({id:r.id,isAdminPost:r.is_admin_post,name:r.name||'Visitor',title:r.title||'',text:r.body||r.text||'',time:r.time||'',date:r.date||'',likes:r.likes||0,liked:false,replies:Array.isArray(r.replies)?r.replies:[],showReps:false}));
    renderCmts();updateDiscStats();
  }
};

// ══ EMAIL ══
function setupEmails(){
  // Build email from array — never stored as plain text in HTML
  const e=EM;
  const els=['emVal','aboutEmail','contactEmail','svcEmailPill','supEmailPill','donateEmailPill','footerEmail'];
  els.forEach(id=>{const el=document.getElementById(id);if(el)el.textContent=e;});
  const ce=document.getElementById('contactEmail');
  if(ce)ce.innerHTML=`<a href="mailto:${e}" style="color:var(--go);text-decoration:none;">${e}</a>`;
  // Links
  [['svcEmailLink','Work Inquiry'],['svc1Link','Structural Analysis'],['svc2Link','3D Modeling'],['svc3Link','Data Report']].forEach(([id,subj])=>{
    const el=document.getElementById(id);if(el)el.href=`mailto:${e}?subject=${encodeURIComponent(subj)}`;
  });
}
function openMailto(){window.location.href=`mailto:${EM}`;}
function copyEmail(){
  navigator.clipboard.writeText(EM)
    .then(()=>toast('✓ Email copied!'))
    .catch(()=>{const t=document.createElement('textarea');t.value=EM;document.body.appendChild(t);t.select();document.execCommand('copy');document.body.removeChild(t);toast('✓ Email copied!');});
}

// ══ THEME ══
function toggleTheme(){const t=document.documentElement.getAttribute('data-theme');document.documentElement.setAttribute('data-theme',t==='light'?'':'light');localStorage.setItem('theme',t==='light'?'':'light');}
(()=>{const t=localStorage.getItem('theme');if(t)document.documentElement.setAttribute('data-theme',t);})();

// ══ LOADER ══
window.addEventListener('load',()=>{
  setTimeout(()=>{document.getElementById('loader').classList.add('gone');trigRev();},1200);
  setTimeout(()=>document.getElementById('loader').classList.add('gone'),3500);
});

// ══ AUTH ══
function initApp(){
  loadLocalData();renderAll();setupEmails();
  if(!window.SB){document.getElementById('loginNavBtn').style.display='inline-flex';return;}
  SB.onAuth(user=>{
    isAdmin=!!user;
    document.body.classList.toggle('is-admin',isAdmin);
    document.getElementById('loginNavBtn').style.display=isAdmin?'none':'inline-flex';
    if(isAdmin) toast('✓ Welcome back, Nashat!');
    startListeners();
  });
  setTimeout(()=>{if(!isAdmin)document.getElementById('loginNavBtn').style.display='inline-flex';},2200);
}
async function doLogin(){
  const email=document.getElementById('loginEmail').value.trim();
  const pass=document.getElementById('loginPass').value;
  const err=document.getElementById('loginErr');
  err.classList.remove('show');
  if(!email||!pass){err.classList.add('show');return;}
  try{const{error}=await SB.signIn(email,pass);if(error)throw error;closeM('loginModal');toast('✓ Signed in!');}
  catch(e){err.classList.add('show');}
}
async function doSignOut(){await SB.signOut();isAdmin=false;document.body.classList.remove('is-admin');toast('Signed out');}

// ══ LISTENERS ══
function startListeners(){
  SB.listen('works',data=>{works=data.map(r=>({id:r.id,title:r.title||'',emoji:r.emoji||'📁',cat:r.cat||'',desc:r.description||'',year:r.year||'',link:r.link||'',price:r.price||'',photo:r.photo||''}));renderWorks();renderCarousel();updateStats();});
  SB.listen('posts',data=>{posts=data.map(r=>({id:r.id,type:r.type||'article',title:r.title||'',content:r.content||'',tags:Array.isArray(r.tags)?r.tags:[],date:r.date||'',likes:r.likes||0,liked:false,comments:Array.isArray(r.comments)?r.comments:[],url:r.url||'',linkTitle:r.link_title||'',linkIcon:r.link_icon||'🌐',videoId:r.video_id||'',docName:r.doc_name||'',docUrl:r.doc_url||'',imgData:r.img_data||''}));renderPosts(activeTag);renderCarousel();updateStats();});
  SB.listen('journey',data=>{journey=data.map(r=>({id:r.id,type:r.type||'milestone',title:r.title||'',org:r.org||'',date:r.date||'',desc:r.description||'',img:r.img||''})).reverse();renderJourney(activeJType);renderCarousel();});
  SB.listen('comments',data=>{comments=data.map(r=>({id:r.id,isAdminPost:r.is_admin_post,name:r.name||'Visitor',title:r.title||'',text:r.body||r.text||'',time:r.time||'',date:r.date||'',likes:r.likes||0,liked:false,replies:Array.isArray(r.replies)?r.replies:[],showReps:false}));renderCmts();updateDiscStats();});
}

// ══ LOCAL DATA ══
function loadLocalData(){
  if(!works.length) works=[
    {id:'w1',title:'Vibration Analysis on Aircraft Wing',emoji:'✈',cat:'Simulation',photo:'',desc:'Modal analysis comparing Aluminum vs. CFRP using ANSYS. CFD simulation for aerodynamic stability and validated notch-filter mitigation system.',year:'2025',link:'',price:''},
    {id:'w2',title:'Hydraulic Pump Systems Study',emoji:'⚙',cat:'MRO',photo:'',desc:'Hands-on inspection and functional testing of hydraulic pump systems during 8-week RJAF Overhaul Workshop training.',year:'2025',link:'',price:''},
    {id:'w3',title:'CFD Aerodynamic Stability Model',emoji:'🛩',cat:'Simulation',photo:'',desc:'CFD simulation to investigate aerodynamic stability of aircraft wing profiles using ANSYS.',year:'2025',link:'',price:''}
  ];
  if(!posts.length) posts=[
    {id:'p1',type:'article',title:'Aluminum vs CFRP: What My Research Found',content:'During my graduation project at JUST, I performed an in-depth modal analysis comparing aluminum alloys to CFRP on a full aircraft wing model. CFRP offers significantly higher natural frequencies and better resonance resistance.',tags:['Structures','CFRP','FEA'],date:'2025-12-01',likes:0,liked:false,comments:[],url:'',linkTitle:'',linkIcon:'',videoId:'',docName:'',docUrl:'',imgData:''},
    {id:'p2',type:'article',title:'What I Learned at the Royal Jordanian Air Force',content:'My 8-week training at the RJAF Overhaul Department was one of the most transformative experiences. Working directly with aircraft components gave me ground-level understanding.',tags:['MRO','Career','RJAF'],date:'2025-10-15',likes:0,liked:false,comments:[],url:'',linkTitle:'',linkIcon:'',videoId:'',docName:'',docUrl:'',imgData:''}
  ];
  if(!journey.length) journey=[
    {id:'j1',type:'milestone',title:'Graduated — B.Sc. Aeronautical Engineering',org:'JUST, Jordan',date:'2025-07',desc:"Graduated with a Bachelor's degree in Aeronautical Engineering from Jordan University of Science and Technology.",img:''},
    {id:'j2',type:'milestone',title:'RJAF Overhaul Department Training',org:'Royal Jordanian Air Force',date:'2025-09',desc:'Completed 8-week aircraft maintenance training at the RJAF Overhaul Workshop.',img:''},
    {id:'j3',type:'course',title:'Power BI Data Visualization',org:'Online — Microsoft',date:'2026-01',desc:'Completed a Power BI course covering data analysis and visualization techniques.',img:''}
  ];
}

// ══ NAV ══
function toggleMob(){document.getElementById('mobMenu').classList.toggle('open');}
function nav2(p){showPage(p,null);document.getElementById('mobMenu').classList.remove('open');}
function showPage(name,el){
  document.querySelectorAll('.page').forEach(p=>p.classList.remove('active'));
  document.querySelectorAll('.nav-links a').forEach(a=>a.classList.remove('active'));
  document.getElementById('page-'+name).classList.add('active');
  if(el)el.classList.add('active');
  const fab=document.getElementById('fab');
  const fm={works:()=>openM('workModal'),posts:()=>openM('postModal'),journey:()=>openM('journeyModal'),discuss:()=>openM('discussModal')};
  if(isAdmin&&fm[name]){fab.style.display='flex';fab.onclick=fm[name];}else fab.style.display='none';
  document.getElementById('mobMenu').classList.remove('open');
  window.scrollTo({top:0,behavior:'smooth'});
  setTimeout(trigRev,60);
}

// ══ REVEAL ══
function trigRev(){document.querySelectorAll('.rev:not(.v)').forEach(el=>{if(el.getBoundingClientRect().top<window.innerHeight-50)el.classList.add('v');});}
window.addEventListener('scroll',trigRev,{passive:true});

// ══ MODALS ══
function openM(id){
  if(['workModal','postModal','journeyModal','svcModal','discussModal'].includes(id)&&!isAdmin){toast('⚠ Admin only');return;}
  document.getElementById(id).classList.add('open');
}
function closeM(id){document.getElementById(id).classList.remove('open');}
document.querySelectorAll('.ov').forEach(o=>o.addEventListener('click',e=>{if(e.target===o)o.classList.remove('open');}));

// ══ TOAST ══
function toast(m){const t=document.getElementById('toast');t.textContent=m;t.classList.add('on');setTimeout(()=>t.classList.remove('on'),2800);}

// ══ PROFILE PHOTO ══
function handleProfilePhoto(e){
  const f=e.target.files[0];if(!f)return;
  const r=new FileReader();r.onload=async ev=>{
    const av=document.getElementById('avatarEl');
    av.style.backgroundImage=`url(${ev.target.result})`;av.style.backgroundSize='cover';av.style.backgroundPosition='center';av.textContent='';
    await SB._supa.from('settings').upsert({key:'profile_photo',value:ev.target.result});
    localStorage.setItem('pp',ev.target.result);toast('✓ Photo saved!');
  };r.readAsDataURL(f);
}
async function loadProfilePhoto(){
  try{
    const{data}=await SB._supa.from('settings').select('value').eq('key','profile_photo').single();
    if(data?.value){const av=document.getElementById('avatarEl');av.style.backgroundImage=`url(${data.value})`;av.style.backgroundSize='cover';av.style.backgroundPosition='center';av.textContent='';}
  }catch(e){const p=localStorage.getItem('pp');if(p){const av=document.getElementById('avatarEl');av.style.backgroundImage=`url(${p})`;av.style.backgroundSize='cover';av.textContent='';}}
}
(()=>{const p=localStorage.getItem('pp');if(p){const av=document.getElementById('avatarEl');av.style.backgroundImage=`url(${p})`;av.style.backgroundSize='cover';av.textContent='';}})();

// ══ CAROUSEL ══
function switchCarousel(type,btn){
  cType=type;cIdx=0;
  document.querySelectorAll('.ctab').forEach(t=>t.classList.remove('on'));
  if(btn)btn.classList.add('on');
  renderCarousel();resetCarouselAuto();
}
function renderCarousel(){
  const track=document.getElementById('cTrack');
  const dots=document.getElementById('cDots');
  if(!track)return;
  let items=[];
  if(cType==='works') items=works.map(w=>({emoji:w.emoji||'✈',photo:w.photo||'',badge:w.cat,title:w.title,sub:w.desc,date:w.year,fn:()=>openPD(w.id)}));
  else if(cType==='journey') items=journey.map(j=>({emoji:j.type==='milestone'?'🏆':j.type==='course'?'📚':'🎤',photo:j.img||'',badge:j.type,title:j.title,sub:j.desc||j.org,date:j.date,fn:null}));
  else items=posts.map(p=>({emoji:p.type==='video'?'▶':p.type==='link'?'🔗':p.type==='doc'?'📄':'📝',photo:p.imgData||'',badge:p.type,title:p.title,sub:p.content,date:p.date,fn:()=>showPage('posts',null)}));
  if(!items.length){track.innerHTML='<div style="padding:2rem;color:var(--mu);font-size:.84rem;">No items yet.</div>';dots.innerHTML='';return;}
  track.innerHTML=items.map((item,i)=>`
    <div class="ccard" onclick="cClick(${i})">
      <div class="ccard-img">
        <div class="ccard-img-bg"></div>
        ${item.photo?`<img src="${item.photo}" alt="">`:`<span style="position:relative;z-index:1;">${item.emoji}</span>`}
        <div class="ccard-badge">${item.badge}</div>
      </div>
      <div class="ccard-body">
        <div class="ccard-title">${item.title}</div>
        <div class="ccard-sub">${item.sub||''}</div>
        <div class="ccard-foot">
          <span class="ccard-date">${item.date||''}</span>
          <button class="ccard-btn">View →</button>
        </div>
      </div>
    </div>`).join('');
  dots.innerHTML=items.map((_,i)=>`<button class="cdot${i===cIdx?' on':''}" onclick="goCarousel(${i})"></button>`).join('');
  goCarousel(cIdx,false);
}
function cClick(i){
  const items=cType==='works'?works:cType==='journey'?journey:posts;
  if(cType==='works')openPD(items[i]?.id);
  else if(cType==='posts')showPage('posts',null);
}
function goCarousel(idx){
  const track=document.getElementById('cTrack');if(!track)return;
  const cards=track.querySelectorAll('.ccard');if(!cards.length)return;
  cIdx=Math.max(0,Math.min(idx,cards.length-1));
  const cardW=cards[0].offsetWidth+16;
  track.style.transform=`translateX(${-(cIdx*cardW)}px)`;
  document.querySelectorAll('.cdot').forEach((d,i)=>d.classList.toggle('on',i===cIdx));
}
function carouselNext(){const track=document.getElementById('cTrack');if(!track)return;const total=track.querySelectorAll('.ccard').length;goCarousel(cIdx>=total-1?0:cIdx+1);resetCarouselAuto();}
function carouselPrev(){goCarousel(cIdx<=0?0:cIdx-1);resetCarouselAuto();}
function startCarouselAuto(){cAuto=setInterval(carouselNext,4000);}
function resetCarouselAuto(){clearInterval(cAuto);startCarouselAuto();}

// ══ CV ══
function downloadCV(){
  const cv=`<!DOCTYPE html><html><head><meta charset="UTF-8"><title>Nashat Aldhoun CV</title>
<style>*{margin:0;padding:0;box-sizing:border-box;}body{font-family:'Segoe UI',sans-serif;color:#0f1115;padding:2.5cm 2cm;font-size:10.5pt;line-height:1.5;}
h1{font-size:22pt;letter-spacing:-.5px;margin-bottom:2pt;}
.role{font-size:10pt;color:#4875c2;font-weight:600;letter-spacing:1px;text-transform:uppercase;margin-bottom:7pt;}
.contact{font-size:8.5pt;color:#677080;margin-bottom:14pt;border-bottom:1px solid #e5e7eb;padding-bottom:9pt;}
h2{font-size:11.5pt;color:#08162a;margin:14pt 0 5pt;border-left:3pt solid #c8a86c;padding-left:7pt;}
.item{margin-bottom:8pt;}.ih{display:flex;justify-content:space-between;}
.it{font-weight:600;font-size:10pt;}.io{color:#4875c2;font-size:9pt;margin:1pt 0;}
.id{font-size:9pt;color:#677080;margin-top:2pt;}
.date{font-size:8.5pt;color:#9ca3af;white-space:nowrap;}
ul{padding-left:13pt;margin-top:2pt;}li{margin-bottom:1.5pt;font-size:8.5pt;color:#677080;}
.sg{display:grid;grid-template-columns:1fr 1fr;gap:7pt;margin-top:3pt;}
.sl{font-size:7.5pt;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:#c8a86c;margin-bottom:2pt;}
.sv{font-size:9pt;color:#334054;}
.footer{margin-top:18pt;text-align:center;font-size:7.5pt;color:#d1d5db;border-top:1px solid #f3f4f6;padding-top:7pt;}
</style></head><body>
<h1>Nashat Omar Aldhoun</h1>
<div class="role">Junior Aeronautical Engineer</div>
<div class="contact">Irbid, Jordan &nbsp;|&nbsp; +962 776 763 628 &nbsp;|&nbsp; nashataldhoun@yahoo.com &nbsp;|&nbsp; linkedin.com/in/nashat-al-dhoun</div>
<h2>Summary</h2>
<div class="item"><div class="id">Highly motivated Junior Aeronautical Engineer and 2025 JUST graduate. Specialized in Aircraft Structures, FEA, and MRO. Trained at the Royal Jordanian Air Force. Proficient in ANSYS, SolidWorks, Creo, and MATLAB.</div></div>
<h2>Experience</h2>
<div class="item"><div class="ih"><div><div class="it">Aircraft Maintenance Trainee</div><div class="io">Royal Jordanian Air Force — Overhaul Department</div></div><div class="date">Sep–Oct 2025</div></div>
<ul><li>8-week intensive training in aircraft maintenance and overhaul procedures</li><li>Hands-on inspection and functional testing of hydraulic pump systems</li><li>Applied aviation safety protocols under licensed engineers supervision</li></ul></div>
<h2>Education</h2>
<div class="item"><div class="ih"><div><div class="it">B.Sc. Aeronautical Engineering</div><div class="io">Jordan University of Science and Technology (JUST)</div></div><div class="date">2021–2025</div></div>
<div class="id">Graduation Project: Vibration Analysis on Aircraft Wing — Modal analysis (Al vs CFRP), CFD simulation, notch-filter mitigation.</div></div>
<h2>Projects</h2>
<div class="item"><div class="it">Vibration Analysis on Aircraft Wing — JUST 2025</div>
<ul><li>3D modeling of full aircraft wing in Creo Parametric</li><li>Modal analysis in ANSYS comparing Aluminum Alloys vs. CFRP composites</li><li>CFD simulation for aerodynamic stability analysis</li><li>Designed and validated notch-filter vibration mitigation system</li></ul></div>
<h2>Skills</h2>
<div class="sg">
<div><div class="sl">Engineering Software</div><div class="sv">Creo · ANSYS (FEA & CFD) · SolidWorks · MATLAB</div></div>
<div><div class="sl">Core Competencies</div><div class="sv">FEA · Modal Analysis · CFD · MRO · Structural Analysis</div></div>
<div style="margin-top:5pt"><div class="sl">Data & Office</div><div class="sv">Power BI · Microsoft Office</div></div>
<div style="margin-top:5pt"><div class="sl">Languages</div><div class="sv">Arabic (Native) · English (B2)</div></div>
</div>
<h2>Certifications</h2>
<div class="item"><div class="ih"><div class="it">Power BI — Data Analysis & Visualization</div><div class="date">2026</div></div></div>
<div class="item"><div class="ih"><div class="it">Employment Skills Training (5hrs)</div><div class="date">2024</div></div></div>
<div class="footer">Nashat Omar Aldhoun · nashataldhoun@yahoo.com · +962 776 763 628 · Irbid, Jordan</div>
</body></html>`;
  const w=window.open('','_blank');w.document.write(cv);w.document.close();
  w.onload=()=>setTimeout(()=>w.print(),500);
  toast('✓ Choose "Save as PDF" in the print dialog');
}

// ══ WORKS ══
function renderWorks(){
  const g=document.getElementById('worksGrid');if(!g)return;
  if(!works.length){g.innerHTML='<div style="text-align:center;padding:4rem;color:var(--mu);grid-column:1/-1;"><div style="font-size:2.8rem;margin-bottom:.85rem;opacity:.35;">✈</div><p style="font-size:.88rem;">No projects yet.</p></div>';return;}
  g.innerHTML=works.map(w=>`
    <div class="wcard" onclick="openPD('${w.id}')">
      <div class="wthumb">
        <img src="${w.photo||''}" class="${w.photo?'on':''}" alt="">
        <div class="wthumb-ph" ${w.photo?'style="display:none"':''}><div class="wthumb-bg"></div><span style="position:relative;z-index:1;">${w.emoji||'📁'}</span></div>
        <div class="wcat">${w.cat}</div>
        ${w.price?`<div class="wprice">${w.price}</div>`:''}
        <div class="photo-ov" style="display:${isAdmin?'flex':'none'}" onclick="event.stopPropagation();document.getElementById('wph-${w.id}').click()">
          <span>📷 Upload Photo</span>
          <input type="file" id="wph-${w.id}" accept="image/*" style="display:none" onchange="workPhoto('${w.id}',event)">
        </div>
      </div>
      <div class="wbody">
        <div class="wtitle">${w.title}</div>
        <div class="wdesc">${(w.desc||'').substring(0,105)}${(w.desc||'').length>105?'…':''}</div>
        <div class="wfoot">
          <div class="wyear">${w.year}${w.link?` · <a href="${w.link}" target="_blank" onclick="event.stopPropagation()" style="color:var(--bl2);font-size:.67rem;">View ↗</a>`:''}</div>
          <div style="display:flex;gap:.28rem;">
            <button class="btn btn-gh btn-xs" style="display:${isAdmin?'inline-flex':'none'}" onclick="event.stopPropagation();editWork('${w.id}')">Edit</button>
            <button class="btn-del" style="display:${isAdmin?'inline-flex':'none'}" onclick="event.stopPropagation();delWork('${w.id}')">🗑</button>
          </div>
        </div>
      </div>
    </div>`).join('');
}
function workPhoto(id,e){
  const f=e.target.files[0];if(!f)return;
  const r=new FileReader();r.onload=async ev=>{await SB.update('works',id,{photo:ev.target.result});toast('✓ Photo saved!');};r.readAsDataURL(f);
}
function openPD(id){
  const w=works.find(x=>x.id===id);if(!w)return;
  document.getElementById('pd-t').textContent=w.title;
  const img=document.getElementById('pd-img'),em=document.getElementById('pd-em');
  if(w.photo){img.src=w.photo;img.style.display='block';em.style.display='none';}
  else{img.style.display='none';em.style.display='block';em.textContent=w.emoji||'📁';}
  document.getElementById('pd-meta').innerHTML=`<span style="background:var(--pan);border:1px solid var(--b);color:var(--tx);font-size:.69rem;padding:.2rem .52rem;border-radius:4px;">${w.cat}</span><span style="background:var(--pan);border:1px solid var(--b);color:var(--tx);font-size:.69rem;padding:.2rem .52rem;border-radius:4px;">${w.year}</span>${w.price?`<span style="background:var(--go3);border:1px solid rgba(200,168,108,.24);color:var(--go);font-size:.69rem;padding:.2rem .52rem;border-radius:4px;">${w.price}</span>`:''}`;
  document.getElementById('pd-desc').textContent=w.desc||'';
  document.getElementById('pd-link').innerHTML=w.link?`<a class="btn btn-gh btn-sm" href="${w.link}" target="_blank" style="display:inline-flex;text-decoration:none;">View Project ↗</a>`:'';
  openM('pdModal');
}
async function saveWork(){
  if(!isAdmin)return;
  const id=document.getElementById('ewId').value;
  const w={title:document.getElementById('wT').value||'Untitled',emoji:document.getElementById('wE').value||'📁',cat:document.getElementById('wC').value,description:document.getElementById('wD').value,year:document.getElementById('wY').value||'2025',link:document.getElementById('wL').value,price:document.getElementById('wP').value};
  try{if(id){await SB.update('works',id,w);}else{await SB.insert('works',w);}closeM('workModal');clearWForm();toast('✓ Saved!');}
  catch(e){toast('⚠ Error: '+e.message);}
}
function editWork(id){
  const w=works.find(x=>x.id===id);if(!w)return;
  document.getElementById('ewId').value=id;document.getElementById('wT').value=w.title;document.getElementById('wE').value=w.emoji;document.getElementById('wC').value=w.cat;document.getElementById('wD').value=w.desc;document.getElementById('wY').value=w.year;document.getElementById('wL').value=w.link;document.getElementById('wP').value=w.price;
  openM('workModal');
}
async function delWork(id){if(!isAdmin||!confirm('Delete this project?'))return;try{await SB.delete('works',id);toast('Deleted');}catch(e){toast('⚠ '+e.message);}}
function clearWForm(){['ewId','wT','wE','wY','wL','wP'].forEach(i=>document.getElementById(i).value='');document.getElementById('wD').value='';}

// ══ POSTS ══
function switchPTab(type,btn){
  document.getElementById('pType').value=type;
  document.querySelectorAll('#postCompose .ptab').forEach(t=>t.classList.remove('active'));btn.classList.add('active');
  document.querySelectorAll('#postCompose .ptype-panel').forEach(p=>p.classList.remove('active'));
  document.getElementById('pt-'+type).classList.add('active');
}
function switchModalPTab(type,btn){
  document.getElementById('mPType').value=type;
  document.querySelectorAll('#modalPTabs .ptab').forEach(t=>t.classList.remove('active'));btn.classList.add('active');
  document.querySelectorAll('#postModal .ptype-panel').forEach(p=>p.classList.remove('active'));
  document.getElementById('mpt-'+type).classList.add('active');
}
function prevPostImg(e){const f=e.target.files[0];if(!f)return;const r=new FileReader();r.onload=ev=>{const p=document.getElementById('pImgPrev');p.src=ev.target.result;p.classList.add('on');};r.readAsDataURL(f);}
function prevModalImg(e){const f=e.target.files[0];if(!f)return;const r=new FileReader();r.onload=ev=>{const p=document.getElementById('mPImgPrev');p.src=ev.target.result;p.classList.add('on');};r.readAsDataURL(f);}
function getYTId(url){const m=url.match(/(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([a-zA-Z0-9_-]{11})/);return m?m[1]:url.trim().substring(0,11);}

async function savePost(){
  if(!isAdmin){toast('⚠ Admin only');return;}
  const type=document.getElementById('pType').value;
  const imgPrev=document.getElementById('pImgPrev');
  const row={type,title:document.getElementById('pTitle').value||'Untitled',content:document.getElementById('pContent').value,
    tags:document.getElementById('pTags').value.split(',').map(t=>t.trim()).filter(Boolean),
    date:new Date().toISOString().split('T')[0],likes:0,comments:[],
    url:document.getElementById('pUrl')?.value||'',link_title:document.getElementById('pLinkTitle')?.value||'',
    link_icon:document.getElementById('pLinkIcon')?.value||'🌐',
    video_id:type==='video'?getYTId(document.getElementById('pVideoUrl')?.value||''):'',
    doc_name:document.getElementById('pDocName')?.value||'',doc_url:document.getElementById('pDocUrl')?.value||'',
    img_data:type==='image'&&imgPrev&&imgPrev.classList.contains('on')?imgPrev.src:''};
  try{
    await SB.insert('posts',row);
    ['pTitle','pContent','pTags'].forEach(i=>document.getElementById(i).value='');
    toast('✓ Published!');
  }catch(e){toast('⚠ '+e.message);}
}
async function savePostModal(){
  if(!isAdmin){toast('⚠ Admin only');return;}
  const type=document.getElementById('mPType').value;
  const imgPrev=document.getElementById('mPImgPrev');
  const row={type,title:document.getElementById('mPTitle').value||'Untitled',content:document.getElementById('mPContent').value,
    tags:document.getElementById('mPTags').value.split(',').map(t=>t.trim()).filter(Boolean),
    date:new Date().toISOString().split('T')[0],likes:0,comments:[],
    url:document.getElementById('mPUrl')?.value||'',link_title:document.getElementById('mPLinkTitle')?.value||'',
    link_icon:document.getElementById('mPLinkIcon')?.value||'🌐',
    video_id:type==='video'?getYTId(document.getElementById('mPVideoUrl')?.value||''):'',
    doc_name:document.getElementById('mPDocName')?.value||'',doc_url:document.getElementById('mPDocUrl')?.value||'',
    img_data:type==='image'&&imgPrev&&imgPrev.classList.contains('on')?imgPrev.src:''};
  try{await SB.insert('posts',row);closeM('postModal');toast('✓ Published!');}
  catch(e){toast('⚠ '+e.message);}
}

function renderPosts(filterTag){
  const feed=document.getElementById('postFeed');if(!feed)return;
  let filtered=filterTag?posts.filter(p=>p.tags&&p.tags.includes(filterTag)):posts;
  document.getElementById('filterCount').innerHTML=filterTag?`Showing ${filtered.length} for <strong style="color:var(--go)">#${filterTag}</strong> — <button onclick="filterPosts('',null)" style="background:none;border:none;color:var(--mu);cursor:pointer;font-size:.64rem;font-family:'DM Sans',sans-serif;">Clear ×</button>`:'';
  if(!filtered.length){feed.innerHTML='<div style="text-align:center;padding:4rem;color:var(--mu);"><div style="font-size:2.6rem;margin-bottom:.82rem;opacity:.35;">📝</div><p style="font-size:.86rem;">No posts yet.</p></div>';return;}
  const tl={article:'t-article',link:'t-link',video:'t-video',doc:'t-doc',image:'t-image'};
  const tn={article:'Article',link:'Link',video:'Video',doc:'Document',image:'Image'};
  feed.innerHTML=filtered.map(p=>{
    let media='';
    if(p.type==='image'&&p.imgData) media=`<img class="pcard-img" src="${p.imgData}" alt="">`;
    else if(p.type==='video'&&p.videoId) media=`<iframe class="pcard-video" src="https://www.youtube.com/embed/${p.videoId}" allowfullscreen></iframe>`;
    else if(p.type==='link'&&p.url) media=`<a class="link-prev" href="${p.url}" target="_blank"><div class="lp-icon">${p.linkIcon||'🌐'}</div><div><div class="lp-title">${p.linkTitle||p.url}</div><div class="lp-url">${p.url}</div></div></a>`;
    else if(p.type==='doc'&&p.docName) media=`<a class="doc-card" href="${p.docUrl||'#'}" target="_blank"><div class="doc-icon">📄</div><div><div class="doc-name">${p.docName}</div><div class="doc-sub">Click to view</div></div></a>`;
    const isLong=(p.content||'').length>220;
    return `<div class="pcard">
      <div class="pcard-head">
        <div class="puser"><div class="pavatar">NA</div><div><div class="pname">Nashat Aldhoun</div><div class="pmeta">${p.date||''}${p.tags?.length?' · '+p.tags[0]:''}</div></div></div>
        <div style="display:flex;align-items:center;gap:.42rem;">
          <span class="ptype-badge ${tl[p.type]||''}">${tn[p.type]||p.type}</span>
          <button class="btn-del" style="display:${isAdmin?'inline-flex':'none'}" onclick="delPost('${p.id}')">🗑</button>
        </div>
      </div>
      <div class="pbody">
        <div class="ptitle">${p.title}</div>
        <div class="ptext${isLong?' col':''}" id="ptxt-${p.id}">${(p.content||'').replace(/\n/g,'<br>')}</div>
        ${isLong?`<button class="rm-btn" onclick="togglePost('${p.id}',this)">Read more →</button>`:''}
        ${p.tags?.length?`<div class="ptags">${p.tags.map(t=>`<span class="ptag" onclick="filterPosts('${t}',this)">#${t}</span>`).join('')}</div>`:''}
      </div>
      ${media}
      <div class="pfoot">
        <button class="pact${p.liked?' liked':''}" onclick="likePost('${p.id}')">♥ ${p.likes||0}</button>
        <button class="pact" onclick="togglePCmt('${p.id}')">💬 ${(p.comments||[]).length}</button>
      </div>
      <div class="pcmt-section" id="pcmt-${p.id}">
        ${(p.comments||[]).map(c=>`<div class="pcmt-item"><div class="pcmt-av">${(c.name||'V')[0]}</div><div class="pcmt-txt"><strong>${c.name||'Visitor'}:</strong> ${c.text}</div></div>`).join('')}
        <div class="pcmt-row">
          <input class="field" id="pcin-${p.id}" placeholder="Add a comment..." style="margin-bottom:0;font-size:.77rem;">
          <button class="btn btn-go btn-xs" onclick="addPostCmt('${p.id}')">Post</button>
        </div>
      </div>
    </div>`;
  }).join('');
  renderTagCloud();
}
function togglePost(id,btn){const el=document.getElementById('ptxt-'+id);el.classList.toggle('col');btn.textContent=el.classList.contains('col')?'Read more →':'Show less ↑';}
function togglePCmt(id){document.getElementById('pcmt-'+id).classList.toggle('open');}
async function likePost(id){const p=posts.find(x=>x.id===id);if(!p)return;p.liked=!p.liked;p.likes=(p.likes||0)+(p.liked?1:-1);try{await SB.update('posts',id,{likes:p.likes});}catch(e){}renderPosts(activeTag);}
async function delPost(id){if(!isAdmin||!confirm('Delete post?'))return;try{await SB.delete('posts',id);toast('Deleted');}catch(e){toast('⚠ '+e.message);}}
async function addPostCmt(id){
  const input=document.getElementById('pcin-'+id);const text=input.value.trim();if(!text)return;
  const name=prompt('Your name (optional):','')||'Visitor';
  const p=posts.find(x=>x.id===id);if(!p)return;
  if(!p.comments)p.comments=[];p.comments.push({name,text,time:new Date().toLocaleTimeString('en',{hour:'2-digit',minute:'2-digit'})});
  try{await SB.update('posts',id,{comments:p.comments});input.value='';toast('✓ Comment added!');}catch(e){toast('⚠ '+e.message);}
}
function filterPosts(tag,el){activeTag=tag;document.querySelectorAll('.ttag').forEach(t=>t.classList.remove('on'));if(el)el.classList.add('on');renderPosts(tag);}
function renderTagCloud(){
  const tc=document.getElementById('tagCloud');if(!tc)return;
  const allTags=[...new Set(posts.flatMap(p=>p.tags||[]))];
  tc.innerHTML=allTags.map(t=>`<span class="ttag${activeTag===t?' on':''}" onclick="filterPosts('${t}',this)">${t}</span>`).join('');
  if(!allTags.length)tc.innerHTML='<span style="font-size:.73rem;color:var(--mu);">No tags yet</span>';
}

// ══ JOURNEY ══
function prevJourneyImg(e){const f=e.target.files[0];if(!f)return;const r=new FileReader();r.onload=ev=>{const p=document.getElementById('jImgPrev');p.src=ev.target.result;p.classList.add('on');};r.readAsDataURL(f);}
async function saveJourney(){
  if(!isAdmin)return;
  const imgPrev=document.getElementById('jImgPrev');
  const row={type:document.getElementById('jType').value,title:document.getElementById('jTitle').value||'Untitled',org:document.getElementById('jOrg').value,date:document.getElementById('jDate').value||new Date().toISOString().split('T')[0].substring(0,7),description:document.getElementById('jDesc').value,img:imgPrev.classList.contains('on')?imgPrev.src:''};
  try{await SB.insert('journey',row);closeM('journeyModal');['jTitle','jOrg','jDate','jDesc'].forEach(i=>document.getElementById(i).value='');const pi=document.getElementById('jImgPrev');pi.src='';pi.classList.remove('on');toast('✓ Entry saved!');}
  catch(e){toast('⚠ '+e.message);}
}
function filterJourney(type,btn){activeJType=type;document.querySelectorAll('.jtab').forEach(t=>t.classList.remove('on'));if(btn)btn.classList.add('on');renderJourney(type);}
function renderJourney(filter){
  const tl=document.getElementById('journeyTimeline');if(!tl)return;
  const filtered=filter==='all'?journey:journey.filter(j=>j.type===filter);
  if(!filtered.length){tl.innerHTML='<div style="text-align:center;padding:4rem;color:var(--mu);"><div style="font-size:2.6rem;margin-bottom:.82rem;opacity:.35;">🗓</div><p style="font-size:.86rem;">No entries yet.</p></div>';return;}
  const tb={milestone:'jt-milestone',course:'jt-course',event:'jt-event'};
  const tn={milestone:'Milestone',course:'Course',event:'Event'};
  tl.innerHTML=filtered.map(j=>`
    <div class="jitem">
      <div class="jdot ${j.type}"></div>
      <div class="jcard">
        <div class="jcard-top">
          <div style="flex:1;">
            <span class="jtype-badge ${tb[j.type]||''}">${tn[j.type]||j.type}</span>
            <div class="jtitle" style="margin-top:.32rem;">${j.title}</div>
            ${j.org?`<div class="jorg">${j.org}</div>`:''}
            ${j.desc?`<div class="jdesc">${j.desc}</div>`:''}
            ${j.img?`<img class="jimg on" src="${j.img}" alt="">`:''}
          </div>
          <div style="display:flex;flex-direction:column;align-items:flex-end;gap:.32rem;flex-shrink:0;">
            <span class="jdate">${j.date||''}</span>
            <button class="btn-del" style="display:${isAdmin?'inline-flex':'none'}" onclick="delJourney('${j.id}')">🗑</button>
          </div>
        </div>
      </div>
    </div>`).join('');
}
async function delJourney(id){if(!isAdmin||!confirm('Delete entry?'))return;try{await SB.delete('journey',id);toast('Deleted');}catch(e){toast('⚠ '+e.message);}}

// ══ DISCUSSION — محسّنة ══
async function addDiscussPost(){
  if(!isAdmin){toast('⚠ Admin only');return;}
  const title=(document.getElementById('dmTitle')?.value||document.getElementById('dTitle')?.value||'').trim();
  const text=(document.getElementById('dmText')?.value||document.getElementById('dText')?.value||'').trim();
  if(!text){toast('⚠ Write something first');return;}
  try{
    await SB.insert('comments',{is_admin_post:true,name:'Nashat',title,body:text,time:new Date().toLocaleTimeString('en',{hour:'2-digit',minute:'2-digit'}),date:new Date().toISOString().split('T')[0],likes:0,replies:[]});
    ['dmTitle','dmText','dTitle','dText'].forEach(id=>{const el=document.getElementById(id);if(el)el.value='';});
    closeM('discussModal');toast('✓ Topic published!');
  }catch(e){toast('⚠ '+e.message);}
}

async function addReplyToTopic(id){
  const nameEl=document.getElementById('rn-'+id);
  const input=document.getElementById('ri-'+id);
  const text=input.value.trim();if(!text)return;
  const name=(nameEl?.value||'').trim()||'Visitor';
  const c=comments.find(x=>x.id===id);if(!c)return;
  if(!c.replies)c.replies=[];
  c.replies.push({name,text,time:new Date().toLocaleTimeString('en',{hour:'2-digit',minute:'2-digit'})});
  try{await SB.update('comments',id,{replies:c.replies});if(nameEl)nameEl.value='';input.value='';toast('✓ Comment added!');}
  catch(e){toast('⚠ '+e.message);}
}

function updateDiscStats(){
  const topics=comments.filter(c=>c.isAdminPost).length;
  const allReplies=comments.reduce((s,c)=>s+(c.replies?.length||0),0);
  const allLikes=comments.reduce((s,c)=>s+(c.likes||0),0);
  const tc=document.getElementById('discTopicCount');
  const cc=document.getElementById('discCmtCount');
  const lc=document.getElementById('discLikeCount');
  if(tc)tc.textContent=topics;
  if(cc)cc.textContent=allReplies;
  if(lc)lc.textContent=allLikes;
}

function renderCmts(){
  const l=document.getElementById('cmtsList');if(!l)return;
  updateDiscStats();
  if(!comments.length){
    l.innerHTML=`<div class="disc-empty">
      <div class="disc-empty-icon">💬</div>
      <div class="disc-empty-title">No discussions yet</div>
      <div class="disc-empty-sub">Nashat will start a discussion soon. Check back later!</div>
    </div>`;return;
  }
  l.innerHTML=comments.map(c=>{
    const isN=c.isAdminPost||c.name==='Nashat';
    const totalLikes=c.likes||0;
    const repliesCount=(c.replies||[]).length;
    return `<div class="dcard">
      ${isN?`<div class="dcard-admin-head">
        <div class="dcard-topic-badge">Discussion Topic</div>
        <div class="dcard-title">${c.title||'Untitled Topic'}</div>
      </div>`:''}
      <div class="dcard-author">
        <div class="dcard-av ${isN?'':'dcard-av-visitor'}">${isN?'NA':(c.name||'V')[0].toUpperCase()}</div>
        <div style="flex:1;">
          <div class="dcard-aname ${isN?'nashat':''}">${isN?'Nashat Aldhoun':c.name||'Visitor'}${isN?'<span class="author-tag">AUTHOR</span>':''}</div>
          <div class="dcard-ameta">${c.date||''} ${c.time?'· '+c.time:''}</div>
        </div>
        <button class="btn-del" style="display:${isAdmin?'inline-flex':'none'}" onclick="delCmt('${c.id}')">🗑</button>
      </div>
      <div class="dcard-body">
        <div class="dcard-text">${c.text}</div>
      </div>
      <div class="dcard-actions">
        <button class="dact${c.liked?' liked':''}" onclick="likeCmt('${c.id}')">
          <svg width="13" height="13" viewBox="0 0 24 24" fill="${c.liked?'currentColor':'none'}" stroke="currentColor" stroke-width="2"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>
          ${totalLikes} ${totalLikes===1?'like':'likes'}
        </button>
        <button class="dact dact-cmt" onclick="toggleRep('${c.id}')">
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
          ${repliesCount} ${repliesCount===1?'comment':'comments'}
        </button>
        <div class="dcard-meta">
          <span style="font-size:.66rem;color:var(--mu);">${isN?'📌 Official Post':''}</span>
        </div>
      </div>
      <div class="dcard-cmts${c.showReps?' open':''}" id="rblock-${c.id}">
        <div class="dcard-cmts-inner">
          <div class="dcmt-list" id="dcl-${c.id}">
            ${(c.replies||[]).length?
              (c.replies||[]).map(r=>`
                <div class="dcmt">
                  <div class="dcmt-av">${(r.name||'V')[0]}</div>
                  <div class="dcmt-bubble">
                    <div class="dcmt-name">${r.name||'Visitor'}<span class="dcmt-time">${r.time||''}</span></div>
                    <div class="dcmt-text">${r.text}</div>
                  </div>
                </div>`).join('')
              :`<div style="font-size:.78rem;color:var(--mu);text-align:center;padding:.6rem 0;">Be the first to comment!</div>`
            }
          </div>
          <div class="dcmt-input-row">
            <div class="dcmt-input-wrap">
              <input class="field dcmt-name-in" type="text" id="rn-${c.id}" placeholder="Your name (optional)" style="margin-bottom:.28rem;font-size:.77rem;">
              <input class="field dcmt-text-in" type="text" id="ri-${c.id}" placeholder="Write a comment..." style="margin-bottom:0;font-size:.77rem;">
            </div>
            <button class="btn btn-go btn-xs dcmt-submit" onclick="addReplyToTopic('${c.id}')">Post</button>
          </div>
        </div>
      </div>
    </div>`;
  }).join('');
}

async function likeCmt(id){
  const c=comments.find(x=>x.id===id);if(!c)return;
  c.liked=!c.liked;c.likes=(c.likes||0)+(c.liked?1:-1);
  try{await SB.update('comments',id,{likes:c.likes});}catch(e){}renderCmts();
}
function toggleRep(id){const c=comments.find(x=>x.id===id);if(c){c.showReps=!c.showReps;renderCmts();}}
async function delCmt(id){if(!isAdmin||!confirm('Delete this topic?'))return;try{await SB.delete('comments',id);toast('Deleted');}catch(e){toast('⚠ '+e.message);}}

// ══ CONTACT ══
function sendContact(){
  const name=document.getElementById('cf-name').value;
  const email=document.getElementById('cf-email').value;
  const subj=document.getElementById('cf-subj').value;
  const msg=document.getElementById('cf-msg').value;
  if(!name||!email||!msg){toast('⚠ Please fill all fields');return;}
  window.location.href=`mailto:${EM}?subject=${encodeURIComponent(subj+' — from '+name)}&body=${encodeURIComponent('From: '+name+'\nEmail: '+email+'\n\n'+msg)}`;
  toast('✓ Opening email client...');
}

// ══ SERVICES ══
function saveSvc(){
  if(!isAdmin)return;
  customSvcs.push({id:'s'+Date.now(),name:document.getElementById('sN').value||'Service',desc:document.getElementById('sD').value,price:document.getElementById('sP').value||'TBD'});
  closeM('svcModal');['sN','sD','sP'].forEach(i=>document.getElementById(i).value='');
  renderSvcs();toast('✓ Service added!');
}
function renderSvcs(){
  const c=document.getElementById('customSvcs');if(!c)return;
  c.innerHTML=customSvcs.map(s=>`<div class="csvc"><div><h4>${s.name}</h4><p>${s.desc}</p></div><div style="display:flex;gap:.48rem;align-items:center;"><span class="csvc-price">${s.price}</span><button class="btn-del" style="display:${isAdmin?'inline-flex':'none'}" onclick="delSvc('${s.id}')">🗑</button></div></div>`).join('');
}
function delSvc(id){if(!isAdmin)return;customSvcs=customSvcs.filter(s=>s.id!==id);renderSvcs();}

// ══ STATS ══
function updateStats(){
  const hw=document.getElementById('hm-w');const hp=document.getElementById('hm-p');
  if(hw)hw.innerHTML=works.length+'<span>+</span>';
  if(hp)hp.innerHTML=posts.length+'<span>+</span>';
}

// ══ RENDER ALL ══
function renderAll(){renderWorks();renderPosts(activeTag);renderJourney(activeJType);renderCmts();renderSvcs();updateStats();renderCarousel();}

// ══ INIT ══
loadLocalData();
renderAll();
setupEmails();
initApp();
startCarouselAuto();
loadProfilePhoto();
setTimeout(trigRev,200);
</script>
</body>
</html>
