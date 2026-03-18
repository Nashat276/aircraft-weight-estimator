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
.hgrid{position:absolute;inset:0;background-image:linear-gradient(rgba(72,117,194,.025) 1px,transparent 1px),linear-gradient(90deg,rgba(72,117,194,.025) 1px,transparent 1px);background-size:48px 48px;}
.hgrid2{position:absolute;inset:0;background-image:linear-gradient(rgba(200,168,108,.015) 1px,transparent 1px),linear-gradient(90deg,rgba(200,168,108,.015) 1px,transparent 1px);background-size:12px 12px;}
.hglow-blue{position:absolute;right:8%;top:15%;width:600px;height:500px;background:radial-gradient(ellipse at center,rgba(72,117,194,.07) 0%,transparent 70%);pointer-events:none;}
.hglow-gold{position:absolute;left:-5%;bottom:10%;width:500px;height:400px;background:radial-gradient(ellipse at center,rgba(200,168,108,.04) 0%,transparent 70%);}
.stars-wrap{position:absolute;inset:0;pointer-events:none;overflow:hidden;}
.star{position:absolute;border-radius:50%;background:#fff;animation:twinkle var(--dur,3s) ease-in-out infinite;opacity:0;}
@keyframes twinkle{0%,100%{opacity:0;transform:scale(.4);}50%{opacity:var(--op,.5);transform:scale(1.2);}}
.plane-bg{position:absolute;right:-40px;top:50%;transform:translateY(-50%);width:500px;opacity:.025;pointer-events:none;filter:blur(.3px);}
[data-theme="light"] .plane-bg{opacity:.04;}
.airplane-wrapper{position:absolute;top:0;left:0;width:100%;height:100%;pointer-events:none;overflow:hidden;}
.plane-fly{position:absolute;top:22%;left:-130px;animation:flyAcross 26s linear infinite;opacity:.08;filter:drop-shadow(0 0 8px rgba(200,168,108,.5));}
@keyframes flyAcross{
  0%{left:-130px;top:22%;transform:rotate(-1.5deg);}
  30%{top:18%;transform:rotate(-1deg);}
  60%{top:22%;transform:rotate(-2deg);}
  100%{left:112%;top:13%;transform:rotate(-3deg);}
}
.contrail{position:absolute;top:22%;left:0;height:1px;background:linear-gradient(90deg,transparent,rgba(200,168,108,.07),transparent);pointer-events:none;width:0;animation:contrailGrow 26s linear infinite;}
@keyframes contrailGrow{0%{width:0;left:0;opacity:0;}10%{opacity:1;}90%{opacity:.4;}100%{width:55%;left:45%;opacity:0;}}

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
.wcard{background:linear-gradient(145deg,#0b1220 0%,#0f1828 100%);border:1px solid rgba(72,117,194,.16);border-radius:14px;overflow:hidden;transition:all .28s;cursor:pointer;position:relative;}
.wcard:hover{border-color:rgba(200,168,108,.32);transform:translateY(-4px);box-shadow:0 16px 42px rgba(0,0,0,.45);}
.wthumb{height:190px;position:relative;overflow:hidden;background:linear-gradient(135deg,#08162a,#0d1f3c);}
.wthumb img{width:100%;height:100%;object-fit:cover;display:none;}
.wthumb img.on{display:block;}
.wthumb-ph{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-size:2.9rem;}
.wthumb-bg{position:absolute;inset:0;background-image:linear-gradient(rgba(72,117,194,.07) 1px,transparent 1px),linear-gradient(90deg,rgba(72,117,194,.07) 1px,transparent 1px);background-size:18px 18px;}
.wcat{position:absolute;top:.7rem;left:.7rem;background:rgba(7,9,13,.88);border:1px solid rgba(200,168,108,.22);color:var(--go);font-size:.58rem;font-weight:700;letter-spacing:1.8px;text-transform:uppercase;padding:.14rem .52rem;border-radius:4px;z-index:2;backdrop-filter:blur(4px);}
.wprice{position:absolute;top:.6rem;right:.6rem;background:var(--go3);border:1px solid rgba(200,168,108,.28);color:var(--go);font-size:.62rem;font-weight:700;padding:.12rem .46rem;border-radius:3px;z-index:2;}
.photo-ov{position:absolute;inset:0;background:rgba(0,0,0,.5);display:flex;align-items:center;justify-content:center;opacity:0;transition:opacity .2s;z-index:3;cursor:pointer;}
.wcard:hover .photo-ov{opacity:1;}
.photo-ov span{color:#fff;font-size:.7rem;background:rgba(200,168,108,.88);padding:.3rem .68rem;border-radius:5px;}
.wbody{padding:1rem 1.1rem 1rem;}
.wtitle{font-family:'DM Serif Display',serif;font-weight:400;color:var(--wh);font-size:1.05rem;margin-bottom:.32rem;line-height:1.22;letter-spacing:-.15px;}
.wdesc{font-size:.8rem;color:var(--tx);line-height:1.72;margin-bottom:.82rem;opacity:.85;}
.wfoot{display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:.28rem;}
.wyear{font-size:.67rem;color:var(--mu);}

/* ══ POSTS - NEW PROFESSIONAL DESIGN ══ */
.posts-layout{display:grid;grid-template-columns:1fr 275px;gap:1.8rem;}

/* ── NEW: Composer Box ── */
.pcompose{
  background:var(--sur);
  border:1px solid var(--b);
  border-radius:16px;
  overflow:hidden;
  margin-bottom:1.5rem;
  display:none;
}
.is-admin .pcompose{display:block;}

.pcompose-header{
  padding:1rem 1.25rem .85rem;
  border-bottom:1px solid var(--b);
  display:flex;align-items:center;justify-content:space-between;
}
.pcompose-header h3{font-family:'DM Serif Display',serif;font-size:1.05rem;color:var(--wh);}
.pcompose-header p{font-size:.72rem;color:var(--mu);margin-top:.1rem;}

/* Type tabs */
.ptabs{display:flex;gap:0;border-bottom:1px solid var(--b);overflow-x:auto;scrollbar-width:none;}
.ptabs::-webkit-scrollbar{display:none;}
.ptab{background:none;border:none;color:var(--mu);font-size:.73rem;font-family:'DM Sans',sans-serif;padding:.42rem .82rem;cursor:pointer;border-bottom:2px solid transparent;margin-bottom:-1px;transition:all .2s;white-space:nowrap;}
.ptab.active,.ptab:hover{color:var(--go);border-bottom-color:var(--go);}

.pcompose-body{padding:1rem 1.25rem 1.1rem;display:flex;flex-direction:column;gap:.7rem;}
.pcompose-field{display:flex;flex-direction:column;gap:.28rem;}
.pcompose-flabel{font-size:.6rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:var(--mu);}

/* Image upload zone */
.img-upload-zone{
  position:relative;
  border:1.5px dashed rgba(72,117,194,.25);
  border-radius:10px;
  background:rgba(72,117,194,.03);
  overflow:hidden;
  cursor:pointer;
  transition:all .2s;
  min-height:110px;
  display:flex;align-items:center;justify-content:center;
}
.img-upload-zone:hover{border-color:rgba(200,168,108,.4);background:rgba(200,168,108,.03);}
.img-upload-zone.has-img{border-style:solid;border-color:rgba(200,168,108,.25);min-height:0;}
.img-upload-ph{text-align:center;padding:.8rem;}
.img-upload-ph-icon{font-size:1.6rem;margin-bottom:.3rem;opacity:.4;}
.img-upload-ph-text{font-size:.75rem;color:var(--mu);}
.img-upload-ph-sub{font-size:.65rem;color:var(--mu);opacity:.6;margin-top:.15rem;}
.img-upload-preview{width:100%;max-height:200px;object-fit:cover;display:block;}

/* Overlay buttons on image */
.img-overlay-btns{
  position:absolute;top:8px;right:8px;
  display:flex;gap:4px;
  opacity:0;transition:opacity .18s;
}
.img-upload-zone.has-img:hover .img-overlay-btns{opacity:1;}
.img-ov-btn{
  width:28px;height:28px;border-radius:6px;border:none;
  cursor:pointer;display:flex;align-items:center;justify-content:center;
  font-size:.8rem;font-family:'DM Sans',sans-serif;
  transition:all .15s;
}
.img-ov-btn.change{background:rgba(7,9,13,.75);color:#fff;backdrop-filter:blur(4px);}
.img-ov-btn.change:hover{background:var(--bl);}
.img-ov-btn.remove{background:rgba(209,78,78,.85);color:#fff;backdrop-filter:blur(4px);}
.img-ov-btn.remove:hover{background:var(--re);}

/* Tags input */
.tags-wrap{
  display:flex;flex-wrap:wrap;gap:4px;
  padding:.42rem .72rem;
  border:1px solid var(--b);border-radius:8px;
  background:rgba(255,255,255,.033);
  cursor:text;min-height:36px;align-items:center;
  transition:border-color .2s;
}
.tags-wrap:focus-within{border-color:var(--bl);}
.tag-pill{
  display:inline-flex;align-items:center;gap:3px;
  background:rgba(72,117,194,.12);
  border:1px solid rgba(72,117,194,.22);
  color:var(--bl2);font-size:.68rem;
  padding:.15rem .52rem;border-radius:20px;
}
.tag-pill-x{background:none;border:none;cursor:pointer;color:var(--bl2);font-size:.8rem;line-height:1;padding:0;opacity:.7;}
.tag-pill-x:hover{opacity:1;}
.tags-in{
  border:none;background:transparent;outline:none;
  font-size:.76rem;color:var(--tx);
  font-family:'DM Sans',sans-serif;
  min-width:80px;flex:1;
}

.pcompose-footer{
  padding:.82rem 1.25rem;
  border-top:1px solid var(--b);
  display:flex;align-items:center;justify-content:space-between;
}
.ptype-panel{display:none;}
.ptype-panel.active{display:flex;flex-direction:column;gap:.7rem;}
.char-count{font-size:.68rem;color:var(--mu);}

/* ══ POST CARD - NEW PROFESSIONAL ══ */
.pfeed{display:grid;gap:1rem;}

.pcard{
  background:var(--sur);
  border:1px solid var(--b);
  border-radius:14px;
  overflow:hidden;
  cursor:pointer;
  transition:all .28s;
  position:relative;
}
.pcard:hover{
  border-color:rgba(200,168,108,.22);
  transform:translateY(-2px);
  box-shadow:0 12px 36px rgba(0,0,0,.35);
}

/* Card with cover image — horizontal layout on large, vertical on small */
.pcard-inner{display:flex;flex-direction:column;}
.pcard.has-cover .pcard-inner{flex-direction:row;}

.pcard-cover{
  width:220px;flex-shrink:0;
  position:relative;overflow:hidden;
  background:linear-gradient(135deg,#08162a,#0d1f3c);
  min-height:160px;
}
.pcard.has-cover .pcard-cover{display:block;}
.pcard:not(.has-cover) .pcard-cover{display:none;}
.pcard-cover img{width:100%;height:100%;object-fit:cover;display:block;}
.pcard-cover-ph{
  position:absolute;inset:0;
  display:flex;align-items:center;justify-content:center;
  font-size:2.2rem;
}
.pcard-cover-ph-bg{
  position:absolute;inset:0;
  background-image:linear-gradient(rgba(72,117,194,.06) 1px,transparent 1px),
    linear-gradient(90deg,rgba(72,117,194,.06) 1px,transparent 1px);
  background-size:16px 16px;
}
.pcard-cover-type{
  position:absolute;bottom:.55rem;left:.55rem;
  background:rgba(7,9,13,.85);
  border:1px solid var(--b2);
  color:var(--tx);font-size:.55rem;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;
  padding:.1rem .38rem;border-radius:3px;
  backdrop-filter:blur(4px);
}

.pcard-main{flex:1;display:flex;flex-direction:column;padding:1rem 1.1rem .85rem;min-width:0;}

.pcard-top{display:flex;align-items:center;gap:.52rem;margin-bottom:.72rem;}
.pcard-av{
  width:30px;height:30px;border-radius:50%;
  background:linear-gradient(135deg,var(--bl),var(--go));
  display:flex;align-items:center;justify-content:center;
  font-size:.7rem;font-weight:700;color:#07090d;
  flex-shrink:0;overflow:hidden;background-size:cover;background-position:center;
}
.pcard-author{font-size:.79rem;font-weight:600;color:var(--wh);}
.pcard-date{font-size:.66rem;color:var(--mu);}
.pcard-badge{
  margin-left:auto;
  font-size:.58rem;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;
  padding:.15rem .48rem;border-radius:3px;
}
.pcard-rt{font-size:.63rem;color:var(--mu);display:flex;align-items:center;gap:.18rem;}

.pcard-title{
  font-family:'DM Serif Display',serif;
  font-size:1.08rem;color:var(--wh);
  line-height:1.25;letter-spacing:-.1px;
  margin-bottom:.4rem;
}
.pcard-excerpt{
  font-size:.8rem;color:var(--mu);line-height:1.72;
  display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden;
  margin-bottom:.7rem;flex:1;
}
.pcard-tags{display:flex;flex-wrap:wrap;gap:.28rem;margin-bottom:.7rem;}
.pcard-tag{
  background:rgba(72,117,194,.08);
  border:1px solid rgba(72,117,194,.15);
  color:var(--bl2);font-size:.62rem;
  padding:.12rem .44rem;border-radius:3px;
}
.pcard-foot{
  display:flex;align-items:center;gap:.52rem;
  padding:.62rem 0 0;
  border-top:1px solid var(--b);
  margin-top:auto;
}
.pact{
  background:none;border:none;color:var(--mu);
  font-size:.71rem;cursor:pointer;font-family:'DM Sans',sans-serif;
  display:flex;align-items:center;gap:.2rem;
  padding:.18rem .42rem;border-radius:5px;transition:all .2s;
}
.pact:hover{background:rgba(255,255,255,.05);color:var(--tx);}
.pact.liked{color:#e87461;}
.pcard-read{
  margin-left:auto;
  font-size:.68rem;color:var(--mu);
  display:flex;align-items:center;gap:.2rem;opacity:.65;
}

/* Type badge colors */
.t-article{background:rgba(72,117,194,.1);color:var(--bl2);}
.t-link{background:rgba(200,168,108,.1);color:var(--go);}
.t-video{background:rgba(209,78,78,.1);color:#ef8080;}
.t-doc{background:rgba(130,96,210,.1);color:var(--pu);}
.t-image{background:rgba(56,150,100,.1);color:#4caf7d;}
.t-tool{background:rgba(200,168,108,.1);color:var(--go);}

/* Inline media in post */
.pcard-video{width:100%;aspect-ratio:16/9;border:none;display:block;}
.link-prev{
  background:var(--pan);border:1px solid var(--b);border-radius:9px;
  padding:.72rem .88rem;display:flex;gap:.58rem;align-items:flex-start;
  text-decoration:none;transition:border-color .2s;margin:.2rem 0 .6rem;
}
.link-prev:hover{border-color:var(--go);}
.lp-icon{width:32px;height:32px;border-radius:7px;background:var(--pan2);display:flex;align-items:center;justify-content:center;font-size:.95rem;flex-shrink:0;}
.lp-title{font-weight:600;color:var(--wh);font-size:.79rem;margin-bottom:.1rem;}
.lp-url{font-size:.65rem;color:var(--mu);}

/* Tool card special style */
.pcard-tool{
  background:linear-gradient(135deg,#07111f 0%,#0d1e3a 45%,#091626 100%);
  border:1px solid rgba(72,117,194,.22);
  border-radius:14px;overflow:hidden;transition:all .28s;cursor:pointer;
}
.pcard-tool:hover{border-color:rgba(200,168,108,.3);transform:translateY(-3px);box-shadow:0 14px 40px rgba(0,0,0,.45);}
.pcard-tool-bg{position:absolute;inset:0;background-image:linear-gradient(rgba(72,117,194,.05) 1px,transparent 1px),linear-gradient(90deg,rgba(72,117,194,.05) 1px,transparent 1px);background-size:20px 20px;pointer-events:none;}
.tool-badge{display:inline-flex;align-items:center;gap:.35rem;font-size:.58rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:var(--go);margin-bottom:.45rem;}
.tool-badge::before{content:'';width:12px;height:1px;background:var(--go);}
.tool-chips{display:flex;flex-wrap:wrap;gap:.3rem;margin-top:.75rem;}
.tool-chip{background:rgba(72,117,194,.1);border:1px solid rgba(72,117,194,.18);color:var(--bl2);font-size:.65rem;padding:.12rem .46rem;border-radius:4px;}

/* ══ SIDEBAR ══ */
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
.jcard{background:linear-gradient(145deg,#0b1220 0%,#0f1828 100%);border:1px solid rgba(72,117,194,.14);border-radius:var(--r);padding:1.05rem;transition:all .25s;position:relative;overflow:hidden;cursor:pointer;}
.jcard::before{content:'';position:absolute;inset:0;pointer-events:none;background-image:linear-gradient(rgba(72,117,194,.035) 1px,transparent 1px),linear-gradient(90deg,rgba(72,117,194,.035) 1px,transparent 1px);background-size:18px 18px;}
.jcard:hover{border-color:rgba(200,168,108,.28);transform:translateX(4px);box-shadow:0 6px 24px rgba(0,0,0,.3);}
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

/* ══ DISCUSSION ══ */
.disc-layout{display:grid;grid-template-columns:1fr 260px;gap:1.8rem;}
.disc-compose{background:var(--pan);border:1px solid var(--b);border-radius:var(--r);padding:1.15rem;margin-bottom:1.5rem;}
.disc-compose-head{display:flex;align-items:center;gap:.55rem;margin-bottom:.9rem;}
.disc-compose-av{width:34px;height:34px;border-radius:50%;background:linear-gradient(135deg,var(--bl),var(--go));display:flex;align-items:center;justify-content:center;font-size:.8rem;font-weight:700;color:#07090d;flex-shrink:0;}
.disc-compose-label{font-size:.82rem;font-weight:600;color:var(--wh);}
.disc-compose-sub{font-size:.69rem;color:var(--mu);}
.disc-feed{display:grid;gap:1rem;}
.dcard{background:linear-gradient(145deg,#0b1220 0%,#0f1828 100%);border:1px solid rgba(72,117,194,.14);border-radius:var(--r);overflow:hidden;transition:all .28s;position:relative;cursor:pointer;}
.dcard::before{content:'';position:absolute;inset:0;pointer-events:none;z-index:0;background-image:linear-gradient(rgba(72,117,194,.03) 1px,transparent 1px),linear-gradient(90deg,rgba(72,117,194,.03) 1px,transparent 1px);background-size:18px 18px;}
.dcard>*{position:relative;z-index:1;}
.dcard:hover{border-color:rgba(200,168,108,.28);box-shadow:0 8px 28px rgba(0,0,0,.32);}
.dcard-admin-head{background:linear-gradient(135deg,rgba(8,22,55,.95),rgba(12,28,64,.85));padding:.95rem 1rem .75rem;border-bottom:1px solid rgba(72,117,194,.15);}
.dcard-topic-badge{display:inline-flex;align-items:center;gap:.3rem;font-size:.58rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:var(--go);margin-bottom:.4rem;}
.dcard-topic-badge::before{content:'';width:14px;height:1px;background:var(--go);}
.dcard-title{font-family:'DM Serif Display',serif;font-size:1.05rem;color:var(--wh);line-height:1.25;letter-spacing:-.1px;}
.dcard-author{display:flex;align-items:center;gap:.55rem;padding:.75rem 1rem;border-bottom:1px solid var(--b);}
.dcard-av{width:30px;height:30px;border-radius:50%;background:linear-gradient(135deg,var(--bl),var(--go));display:flex;align-items:center;justify-content:center;font-size:.74rem;font-weight:700;color:#07090d;flex-shrink:0;}
.dcard-av-visitor{background:rgba(72,117,194,.12);color:var(--bl2);}
.dcard-aname{font-weight:600;font-size:.83rem;color:var(--wh);}
.dcard-aname.nashat{color:var(--go);}
.dcard-ameta{font-size:.67rem;color:var(--mu);}
.author-tag{display:inline-block;font-size:.56rem;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;background:var(--go3);border:1px solid rgba(200,168,108,.22);color:var(--go);padding:.08rem .38rem;border-radius:3px;margin-left:.38rem;}
.dcard-body{padding:.82rem 1rem;}
.dcard-text{font-size:.82rem;color:var(--mu);line-height:1.78;}
.dcard-actions{display:flex;align-items:center;gap:.52rem;padding:.65rem 1rem;border-top:1px solid var(--b);flex-wrap:wrap;}
.dact{background:none;border:none;color:var(--mu);font-size:.72rem;cursor:pointer;font-family:'DM Sans',sans-serif;display:flex;align-items:center;gap:.22rem;padding:.2rem .45rem;border-radius:5px;transition:all .2s;}
.dact:hover{background:rgba(255,255,255,.05);color:var(--tx);}
.dact.liked{color:#e87461;}
.dact-cmt{color:var(--bl2);}
.dact-cmt:hover{color:var(--bl2);background:rgba(72,117,194,.08);}
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

/* ══ CERTIFICATIONS ══ */
.cert-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:1rem;margin-top:1.5rem;}
.cert-card{background:var(--pan);border:1px solid var(--b);border-radius:var(--r);padding:1rem 1.15rem;display:flex;gap:.85rem;align-items:flex-start;transition:all .25s;cursor:default;}
.cert-card:hover{border-color:rgba(200,168,108,.25);transform:translateY(-2px);}
.cert-icon{width:38px;height:38px;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:1.2rem;flex-shrink:0;}
.cert-name{font-weight:600;color:var(--wh);font-size:.84rem;margin-bottom:.16rem;}
.cert-org{font-size:.72rem;color:var(--go);margin-bottom:.1rem;}
.cert-year{font-size:.66rem;color:var(--mu);}

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

/* ══ READER MODAL ══ */
.reader-ov{position:fixed;inset:0;z-index:800;background:rgba(0,0,0,0);display:none;align-items:flex-start;justify-content:center;overflow-y:auto;padding:0;transition:background .35s;}
.reader-ov.open{display:flex;background:rgba(4,5,8,.92);backdrop-filter:blur(8px);}
.reader-modal{background:var(--sur);width:100%;max-width:720px;min-height:100vh;margin:0 auto;position:relative;animation:readerIn .38s cubic-bezier(.16,1,.3,1);box-shadow:0 0 80px rgba(0,0,0,.6);}
@keyframes readerIn{from{opacity:0;transform:translateY(32px);}to{opacity:1;transform:none;}}
.reader-progress{position:fixed;top:0;left:0;height:2.5px;background:linear-gradient(90deg,var(--bl),var(--go));width:0;z-index:900;transition:width .1s;border-radius:0 2px 2px 0;}
.reader-topbar{position:sticky;top:0;z-index:10;display:flex;align-items:center;justify-content:space-between;padding:.75rem 1.5rem;background:rgba(12,15,22,.92);backdrop-filter:blur(20px);border-bottom:1px solid var(--b);}
.reader-nav-btn{background:none;border:1px solid var(--b);color:var(--mu);border-radius:8px;padding:.32rem .72rem;cursor:pointer;font-size:.76rem;font-family:'DM Sans',sans-serif;transition:all .2s;display:flex;align-items:center;gap:.32rem;}
.reader-nav-btn:hover{border-color:var(--go);color:var(--wh);}
.reader-nav-center{font-family:'DM Serif Display',serif;font-size:.82rem;color:var(--mu);letter-spacing:.02em;}
.reader-cover{width:100%;aspect-ratio:21/9;object-fit:cover;display:block;}
.reader-cover-placeholder{width:100%;height:220px;background:linear-gradient(135deg,#08162a,#0f2240);display:flex;align-items:center;justify-content:center;font-size:4rem;position:relative;overflow:hidden;}
.reader-cover-placeholder::after{content:'';position:absolute;inset:0;background-image:linear-gradient(rgba(72,117,194,.06) 1px,transparent 1px),linear-gradient(90deg,rgba(72,117,194,.06) 1px,transparent 1px);background-size:20px 20px;}
.reader-body{padding:2.8rem 3.5rem 4rem;max-width:680px;margin:0 auto;}
@media(max-width:600px){.reader-body{padding:1.8rem 1.4rem 3rem;}}
.reader-meta-row{display:flex;align-items:center;gap:.55rem;margin-bottom:1.2rem;flex-wrap:wrap;}
.reader-type-badge{font-size:.6rem;font-weight:700;letter-spacing:1.8px;text-transform:uppercase;padding:.18rem .56rem;border-radius:4px;}
.reader-date{font-size:.75rem;color:var(--mu);}
.reader-read-time{font-size:.72rem;color:var(--mu);background:var(--pan);border:1px solid var(--b);padding:.12rem .5rem;border-radius:20px;}
.reader-title{font-family:'DM Serif Display',serif;font-size:clamp(1.65rem,3.5vw,2.4rem);color:var(--wh);line-height:1.12;letter-spacing:-.4px;margin-bottom:1rem;}
.reader-author-row{display:flex;align-items:center;gap:.75rem;padding:1rem 0;border-top:1px solid var(--b);border-bottom:1px solid var(--b);margin-bottom:2rem;}
.reader-av{width:42px;height:42px;border-radius:50%;background:linear-gradient(135deg,var(--bl),var(--go));display:flex;align-items:center;justify-content:center;font-family:'DM Serif Display',serif;font-size:.95rem;color:#07090d;flex-shrink:0;overflow:hidden;background-size:cover;background-position:center;}
.reader-author-name{font-weight:600;color:var(--wh);font-size:.88rem;}
.reader-author-role{font-size:.72rem;color:var(--go);}
.reader-content{font-size:1.08rem;color:var(--tx);line-height:1.88;letter-spacing:.01em;}
.reader-content p{margin-bottom:1.4rem;}
.reader-content strong{color:var(--wh);font-weight:600;}
.reader-content em{color:var(--go2);font-style:italic;}
.reader-content a{color:var(--bl2);text-decoration:underline;text-decoration-color:rgba(106,158,234,.3);}
.reader-content .first-para::first-letter{font-family:'DM Serif Display',serif;font-size:3.4rem;line-height:.82;float:left;margin:0 .12em -.05em 0;color:var(--go);font-weight:400;}
.reader-quote{border-left:3px solid var(--go);margin:2rem 0;padding:.8rem 1.4rem;background:var(--pan);border-radius:0 8px 8px 0;font-family:'DM Serif Display',serif;font-size:1.15rem;color:var(--wh);line-height:1.55;font-style:italic;}
.reader-tags{display:flex;flex-wrap:wrap;gap:.35rem;margin:2rem 0 1.5rem;}
.reader-tag{background:rgba(72,117,194,.08);border:1px solid rgba(72,117,194,.18);color:var(--bl2);font-size:.72rem;padding:.2rem .58rem;border-radius:4px;cursor:pointer;}
.reader-divider{display:flex;align-items:center;gap:.6rem;justify-content:center;margin:2.2rem 0;}
.reader-divider span{width:4px;height:4px;border-radius:50%;background:var(--mu);opacity:.5;}
.reader-action-bar{position:sticky;bottom:0;background:rgba(12,15,22,.95);backdrop-filter:blur(20px);border-top:1px solid var(--b);padding:.75rem 1.5rem;display:flex;align-items:center;gap:.75rem;}
.reader-act{background:none;border:1px solid var(--b);color:var(--mu);border-radius:8px;padding:.36rem .82rem;cursor:pointer;font-size:.8rem;font-family:'DM Sans',sans-serif;display:flex;align-items:center;gap:.3rem;transition:all .2s;}
.reader-act:hover,.reader-act.active{border-color:var(--go);color:var(--go);background:var(--go3);}
.reader-act.liked{color:#e87461;border-color:#e87461;background:rgba(232,116,97,.08);}
.reader-share{margin-left:auto;background:var(--go3);border:1px solid rgba(200,168,108,.22);color:var(--go);border-radius:8px;padding:.36rem .88rem;cursor:pointer;font-size:.8rem;font-family:'DM Sans',sans-serif;font-weight:600;transition:all .2s;}
.reader-share:hover{background:rgba(200,168,108,.16);}
.reader-cmts{padding:1.5rem 3.5rem 2rem;border-top:1px solid var(--b);}
@media(max-width:600px){.reader-cmts{padding:1.2rem 1.4rem;}}
.reader-cmts-title{font-family:'DM Serif Display',serif;font-size:1.1rem;color:var(--wh);margin-bottom:1.2rem;}
.reader-cmt-item{display:flex;gap:.6rem;margin-bottom:1rem;}
.reader-cmt-av{width:28px;height:28px;border-radius:50%;background:rgba(72,117,194,.15);display:flex;align-items:center;justify-content:center;font-size:.68rem;font-weight:700;color:var(--bl2);flex-shrink:0;margin-top:.08rem;}
.reader-cmt-bubble{background:var(--pan);border:1px solid var(--b);border-radius:0 10px 10px 10px;padding:.58rem .85rem;flex:1;}
.reader-cmt-name{font-size:.75rem;font-weight:600;color:var(--wh);margin-bottom:.2rem;}
.reader-cmt-time{font-size:.64rem;color:var(--mu);font-weight:400;margin-left:.3rem;}
.reader-cmt-text{font-size:.82rem;color:var(--mu);line-height:1.6;}
.reader-cmt-input-row{display:flex;gap:.5rem;margin-top:1rem;align-items:flex-end;}
.reader-cmt-input-row input{flex:1;margin-bottom:0;}

/* ══ RADAR ══ */
.radar-wrap{position:relative;width:100%;max-width:340px;margin:0 auto;}
.radar-label{font-size:.66rem;font-weight:600;fill:var(--tx);font-family:'DM Sans',sans-serif;}
.radar-polygon{fill:rgba(72,117,194,.15);stroke:var(--bl2);stroke-width:1.5;transition:all .4s;}
.radar-grid{fill:none;stroke:rgba(255,255,255,.06);stroke-width:.8;}
.radar-axis{stroke:rgba(255,255,255,.08);stroke-width:.8;}
.radar-dot{fill:var(--go);stroke:var(--pan);stroke-width:2;cursor:pointer;transition:r .2s;}
.radar-dot:hover{r:6;}
.radar-tooltip{position:absolute;background:var(--pan2);border:1px solid var(--b2);border-radius:7px;padding:.32rem .68rem;font-size:.72rem;color:var(--wh);pointer-events:none;opacity:0;transition:opacity .18s;white-space:nowrap;font-family:'DM Sans',sans-serif;z-index:10;}

/* ══ ANIM CARD ══ */
.anim-card{opacity:0;transform:translateY(24px) scale(.98);transition:opacity .55s cubic-bezier(.16,1,.3,1),transform .55s cubic-bezier(.16,1,.3,1);}
.anim-card.in{opacity:1;transform:none;}
.sec-t{background:linear-gradient(135deg,var(--wh) 0%,rgba(240,237,230,1) 55%,var(--go2) 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;}
[data-theme="light"] .sec-t{background:none;-webkit-text-fill-color:var(--wh);}
:focus-visible{outline:2px solid var(--go);outline-offset:2px;border-radius:4px;}

/* Login */
#loginModal .modal{max-width:320px;text-align:center;}
.login-logo{font-family:'DM Serif Display',serif;font-size:1.9rem;color:var(--wh);margin-bottom:.22rem;}
.login-logo span{color:var(--go);}
.login-sub{font-size:.78rem;color:var(--mu);margin-bottom:1.35rem;}
.login-err{color:var(--re);font-size:.76rem;margin-top:.42rem;display:none;}
.login-err.show{display:block;}
.fab{position:fixed;bottom:1.8rem;right:1.8rem;z-index:100;width:44px;height:44px;border-radius:50%;background:linear-gradient(135deg,var(--go),var(--go2));color:#07090d;border:none;font-size:1.3rem;cursor:pointer;box-shadow:0 6px 22px rgba(200,168,108,.3);transition:all .22s;display:none;align-items:center;justify-content:center;font-weight:700;}
.fab:hover{transform:scale(1.1);}

footer{border-top:1px solid var(--b);padding:1.5rem 2rem;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:.9rem;}
.ft-brand{font-family:'DM Serif Display',serif;font-size:.9rem;color:var(--wh);}
.ft-brand span{color:var(--go);}
.ft-copy{font-size:.7rem;color:var(--mu);}

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
  .pcard.has-cover .pcard-inner{flex-direction:column;}
  .pcard.has-cover .pcard-cover{width:100%;height:180px;}
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
    <div class="stars-wrap" id="starsWrap"></div>
    <svg class="plane-bg" viewBox="0 0 800 300" fill="none">
      <path d="M790 150L520 10L480 150L520 165L500 290L370 185L280 200L0 150L280 100L370 115L500 10L520 135L480 150Z" fill="white"/>
      <path d="M480 150L520 135L790 150L520 165L480 150Z" fill="rgba(200,168,108,0.3)"/>
    </svg>
    <div class="airplane-wrapper">
      <svg class="plane-fly" width="68" height="30" viewBox="0 0 68 30" fill="none">
        <path d="M0 15L54 0L68 15L54 18L59 30L44 21L34 23L0 15Z" fill="white"/>
        <path d="M54 18L68 15L54 15Z" fill="rgba(200,168,108,0.55)"/>
        <circle cx="54" cy="15" r="2.5" fill="rgba(200,168,108,0.7)"/>
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
    <div class="hmetrics rev d3" id="statsRow">
      <div class="hm"><div class="hm-n"><span class="stat-num" data-target="3" id="hm-w">0</span><span>+</span></div><div class="hm-l">Projects</div></div>
      <div class="hm"><div class="hm-n"><span class="stat-num" data-target="8">0</span><span>wk</span></div><div class="hm-l">RJAF Training</div></div>
      <div class="hm"><div class="hm-n"><span class="stat-num" data-target="4">0</span><span></span></div><div class="hm-l">CAD & Sim Tools</div></div>
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
          <div class="idc-ic" style="background:rgba(72,117,194,.1);"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="var(--bl2)" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg></div>
          <div><div class="idc-key">Location</div><div class="idc-val">Irbid, Jordan</div></div>
        </div>
        <div class="idc-row">
          <div class="idc-ic" style="background:rgba(200,168,108,.1);"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="var(--go)" stroke-width="2"><path d="M22 10v6M2 10l10-5 10 5-10 5z"/><path d="M6 12v5c3 3 9 3 12 0v-5"/></svg></div>
          <div><div class="idc-key">Education</div><div class="idc-val">B.Sc. Aero. Eng. — JUST '25</div></div>
        </div>
        <div class="idc-row">
          <div class="idc-ic" style="background:rgba(130,96,210,.1);"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="var(--pu)" stroke-width="2"><path d="M12 2L2 7l10 5 10-5-10-5z"/><path d="M2 17l10 5 10-5M2 12l10 5 10-5"/></svg></div>
          <div><div class="idc-key">Training</div><div class="idc-val">RJAF Overhaul Dept.</div></div>
        </div>
        <div class="idc-row">
          <div class="idc-ic" style="background:rgba(56,150,100,.1);"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#4caf7d" stroke-width="2"><circle cx="12" cy="12" r="3"/><path d="M19.07 4.93a10 10 0 0 1 0 14.14M4.93 4.93a10 10 0 0 0 0 14.14"/></svg></div>
          <div><div class="idc-key">Specialization</div><div class="idc-val">Structures · FEA · MRO</div></div>
        </div>
      </div>
      <div class="idc-foot">
        <a href="javascript:void(0)" onclick="openMailto()">
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
    <div class="c-slider"><div class="c-track" id="cTrack"></div></div>
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
      <div class="sg" style="margin-top:1.6rem;">
        <div class="sg-l" style="margin-bottom:.75rem;">Technical Proficiency</div>
        <div class="radar-wrap" id="radarWrap">
          <div class="radar-tooltip" id="radarTip"></div>
          <svg id="radarSvg" viewBox="0 0 280 260" width="100%" style="overflow:visible;"></svg>
        </div>
      </div>
      <div class="cv-box">
        <div><h4>Curriculum Vitae</h4><p>Download my full CV as PDF</p><div style="margin-top:.42rem;font-size:.76rem;" id="aboutEmail"></div></div>
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
  <div class="rev" style="margin-top:2.8rem;">
    <div class="eyebrow">Credentials</div>
    <h3 style="font-family:'DM Serif Display',serif;font-size:1.35rem;color:var(--wh);margin-bottom:.3rem;letter-spacing:-.2px;">Certifications & Training</h3>
    <p style="font-size:.84rem;color:var(--mu);margin-bottom:0;">Official credentials and professional development.</p>
    <div class="cert-grid">
      <div class="cert-card"><div class="cert-icon" style="background:rgba(72,117,194,.12);">🎓</div><div><div class="cert-name">B.Sc. Aeronautical Engineering</div><div class="cert-org">Jordan University of Science & Technology</div><div class="cert-year">2021 – 2025 · Irbid, Jordan</div></div></div>
      <div class="cert-card"><div class="cert-icon" style="background:rgba(56,150,100,.1);">✈</div><div><div class="cert-name">Aircraft Maintenance Training</div><div class="cert-org">Royal Jordanian Air Force — Overhaul Dept.</div><div class="cert-year">Sep – Oct 2025 · 8 Weeks Intensive</div></div></div>
      <div class="cert-card"><div class="cert-icon" style="background:rgba(200,168,108,.1);">📊</div><div><div class="cert-name">Power BI — Data Analysis & Visualization</div><div class="cert-org">Microsoft Power BI</div><div class="cert-year">2026 · 3 Hours</div></div></div>
      <div class="cert-card"><div class="cert-icon" style="background:rgba(130,96,210,.1);">🤝</div><div><div class="cert-name">We Are Community Leaders</div><div class="cert-org">University Leadership Program</div><div class="cert-year">2019</div></div></div>
      <div class="cert-card"><div class="cert-icon" style="background:rgba(56,150,100,.1);">💼</div><div><div class="cert-name">Employment Skills Training</div><div class="cert-org">Professional Development</div><div class="cert-year">2024 · 5 Hours</div></div></div>
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
      <!-- ═══ NEW PROFESSIONAL COMPOSER ═══ -->
      <div class="pcompose admin-only-block" id="postCompose">
        <div class="pcompose-header">
          <div>
            <h3>New Post</h3>
            <p>Share your knowledge with the world</p>
          </div>
        </div>
        <div class="ptabs" id="composeTabs">
          <button class="ptab active" onclick="switchPTab('article',this)">📝 Article</button>
          <button class="ptab" onclick="switchPTab('link',this)">🔗 Link</button>
          <button class="ptab" onclick="switchPTab('video',this)">▶ Video</button>
          <button class="ptab" onclick="switchPTab('doc',this)">📄 Doc</button>
          <button class="ptab" onclick="switchPTab('image',this)">🖼 Image</button>
          <button class="ptab" onclick="switchPTab('tool',this)">⚙ Tool</button>
        </div>
        <div class="pcompose-body">
          <input type="hidden" id="pType" value="article">
          <div class="pcompose-field">
            <span class="pcompose-flabel">Title</span>
            <input class="field" id="pTitle" placeholder="Give your post a compelling title…" style="margin-bottom:0;" oninput="updateCharCount()">
          </div>
          <div class="pcompose-field">
            <span class="pcompose-flabel">Content</span>
            <textarea class="field" id="pContent" placeholder="Write your content here…" style="min-height:100px;margin-bottom:0;" oninput="updateCharCount()"></textarea>
          </div>

          <!-- Article panel (empty, just title+content) -->
          <div class="ptype-panel active" id="pt-article"></div>

          <!-- Link panel -->
          <div class="ptype-panel" id="pt-link">
            <div class="pcompose-field">
              <span class="pcompose-flabel">URL</span>
              <input class="field" id="pUrl" placeholder="https://…" style="margin-bottom:0;">
            </div>
            <div class="frow">
              <div><span class="pcompose-flabel">Link title</span><input class="field" id="pLinkTitle" placeholder="Page title" style="margin-bottom:0;"></div>
              <div><span class="pcompose-flabel">Icon</span><input class="field" id="pLinkIcon" placeholder="🌐" style="margin-bottom:0;text-align:center;"></div>
            </div>
          </div>

          <!-- Video panel -->
          <div class="ptype-panel" id="pt-video">
            <div class="pcompose-field">
              <span class="pcompose-flabel">YouTube URL</span>
              <input class="field" id="pVideoUrl" placeholder="https://youtube.com/watch?v=…" style="margin-bottom:0;">
            </div>
          </div>

          <!-- Doc panel -->
          <div class="ptype-panel" id="pt-doc">
            <div class="frow">
              <div><span class="pcompose-flabel">Document name</span><input class="field" id="pDocName" placeholder="FEA Report 2025.pdf" style="margin-bottom:0;"></div>
              <div><span class="pcompose-flabel">Document URL</span><input class="field" id="pDocUrl" placeholder="https://…" style="margin-bottom:0;"></div>
            </div>
          </div>

          <!-- Tool panel -->
          <div class="ptype-panel" id="pt-tool">
            <div class="pcompose-field">
              <span class="pcompose-flabel">Tool URL</span>
              <input class="field" id="pToolUrl" placeholder="https://aerosizer.streamlit.app" style="margin-bottom:0;">
            </div>
            <div class="frow">
              <div><span class="pcompose-flabel">Stack</span><input class="field" id="pToolStack" placeholder="Python, Streamlit…" style="margin-bottom:0;"></div>
              <div><span class="pcompose-flabel">Icon</span><input class="field" id="pToolIcon" placeholder="⚙" style="margin-bottom:0;text-align:center;"></div>
            </div>
          </div>

          <!-- Image panel — NEW with delete button -->
          <div class="ptype-panel" id="pt-image">
            <div class="pcompose-field">
              <span class="pcompose-flabel">Cover Image</span>
              <div class="img-upload-zone" id="composeImgZone" onclick="document.getElementById('pImgFile').click()">
                <div class="img-upload-ph" id="composeImgPh">
                  <div class="img-upload-ph-icon">📷</div>
                  <div class="img-upload-ph-text">Click to upload an image</div>
                  <div class="img-upload-ph-sub">PNG, JPG, GIF up to 10MB</div>
                </div>
                <img id="pImgPrev" class="img-upload-preview" src="" alt="" style="display:none;">
                <!-- Overlay buttons: change + delete -->
                <div class="img-overlay-btns">
                  <button class="img-ov-btn change" title="Change image" onclick="event.stopPropagation();document.getElementById('pImgFile').click()">✎</button>
                  <button class="img-ov-btn remove" title="Remove image" onclick="event.stopPropagation();removeComposeImg()">✕</button>
                </div>
              </div>
              <input type="file" id="pImgFile" accept="image/*" style="display:none" onchange="prevPostImg(event)">
            </div>
          </div>

          <!-- Tags -->
          <div class="pcompose-field">
            <span class="pcompose-flabel">Tags</span>
            <div class="tags-wrap" id="composeTags" onclick="document.getElementById('composeTagIn').focus()">
              <input class="tags-in" id="composeTagIn" placeholder="Add tag + Enter…" onkeydown="handleComposeTag(event)">
            </div>
          </div>
        </div>
        <div class="pcompose-footer">
          <span class="char-count" id="charCount">0 / 1200 characters</span>
          <button class="btn btn-go btn-sm" onclick="savePost()">Publish →</button>
        </div>
      </div>
      <!-- END COMPOSER -->

      <div id="postFeed" class="pfeed"></div>
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

<!-- ══ DISCUSSION ══ -->
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
      <div class="disc-compose admin-only-block">
        <div class="disc-compose-head">
          <div class="disc-compose-av" id="discComposeAv">NA</div>
          <div>
            <div class="disc-compose-label">Start a Discussion</div>
            <div class="disc-compose-sub">Share a topic, question, or idea</div>
          </div>
        </div>
        <input class="field" id="dTitle" placeholder="Topic title…">
        <textarea class="field" id="dText" placeholder="Write your discussion post…" style="min-height:88px;"></textarea>
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
      <textarea class="field" id="cf-msg" style="min-height:108px;" placeholder="Write your message…"></textarea>
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

<div class="ov" id="workModal">
<div class="modal" style="max-width:520px;">
  <div class="mhd"><div class="mt">Add / Edit Project</div><button class="mx" onclick="closeM('workModal')">×</button></div>
  <input type="hidden" id="ewId">
  <label class="flabel">Cover Image</label>
  <div id="wCoverArea" onclick="document.getElementById('wImgFile').click()" style="height:140px;border-radius:10px;border:1.5px dashed rgba(72,117,194,.3);background:linear-gradient(135deg,#08162a,#0f2240);display:flex;align-items:center;justify-content:center;cursor:pointer;position:relative;overflow:hidden;margin-bottom:.85rem;transition:border-color .2s;">
    <div id="wCoverPh" style="text-align:center;color:var(--mu);"><div style="font-size:1.8rem;margin-bottom:.3rem;">📷</div><div style="font-size:.75rem;">Click to upload cover image</div></div>
    <img id="wImgPrev" src="" alt="" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;display:none;">
  </div>
  <input type="file" id="wImgFile" accept="image/*" style="display:none" onchange="prevWorkImg(event)">
  <div class="mfr">
    <div style="flex:2"><label class="flabel">Title *</label><input class="field" id="wT" placeholder="Project title" style="margin-bottom:0;"></div>
    <div style="flex:0 0 70px"><label class="flabel">Icon</label><input class="field" id="wE" placeholder="✈" style="margin-bottom:0;text-align:center;font-size:1.2rem;"></div>
  </div><br>
  <div class="mfr">
    <div><label class="flabel">Category</label><select class="field" id="wC" style="margin-bottom:0;"><option>Simulation</option><option>3D Modeling</option><option>Structures</option><option>MRO</option><option>CFD</option><option>Data Analysis</option><option>Research</option><option>Design</option><option>Tool</option><option>Other</option></select></div>
    <div><label class="flabel">Year</label><input class="field" id="wY" placeholder="2025" style="margin-bottom:0;"></div>
  </div><br>
  <label class="flabel">Description *</label>
  <textarea class="field" id="wD" placeholder="Describe the project…" style="min-height:110px;"></textarea>
  <label class="flabel">Technologies / Tags</label>
  <input class="field" id="wTags" placeholder="ANSYS, Creo, CFD…" style="margin-bottom:.65rem;">
  <div class="mfr">
    <div><label class="flabel">Link (optional)</label><input class="field" id="wL" placeholder="https://…" style="margin-bottom:0;"></div>
    <div><label class="flabel">Price</label><input class="field" id="wP" placeholder="Free" style="margin-bottom:0;"></div>
  </div>
  <div class="macts">
    <button class="btn btn-gh btn-sm" onclick="closeM('workModal')">Cancel</button>
    <button class="btn btn-go btn-sm" onclick="saveWork()">Save Project</button>
  </div>
</div>
</div>

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

<!-- Post Modal (for + button) -->
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
    <button class="ptab" onclick="switchModalPTab('tool',this)">⚙ Tool</button>
  </div>
  <label class="flabel">Title</label><input class="field" id="mPTitle" placeholder="Post title">
  <label class="flabel">Content</label><textarea class="field" id="mPContent" placeholder="Write here…"></textarea>
  <div class="ptype-panel active" id="mpt-article"></div>
  <div class="ptype-panel" id="mpt-link">
    <input class="field" id="mPUrl" placeholder="https://…">
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
  <div class="ptype-panel" id="mpt-tool">
    <input class="field" id="mPToolUrl" placeholder="Tool URL">
    <div class="frow">
      <input class="field" id="mPToolStack" placeholder="Stack: Python, Streamlit…" style="margin-bottom:0;">
      <input class="field" id="mPToolIcon" placeholder="Icon emoji ⚙" style="margin-bottom:0;">
    </div>
  </div>
  <div class="ptype-panel" id="mpt-image">
    <!-- Modal image upload with delete button -->
    <div class="img-upload-zone" id="modalImgZone" onclick="document.getElementById('mPImgFile').click()" style="min-height:90px;margin-bottom:.6rem;">
      <div class="img-upload-ph" id="modalImgPh">
        <div class="img-upload-ph-icon">📷</div>
        <div class="img-upload-ph-text">Click to upload an image</div>
      </div>
      <img id="mPImgPrev" class="img-upload-preview" src="" alt="" style="display:none;">
      <div class="img-overlay-btns">
        <button class="img-ov-btn change" title="Change" onclick="event.stopPropagation();document.getElementById('mPImgFile').click()">✎</button>
        <button class="img-ov-btn remove" title="Remove" onclick="event.stopPropagation();removeModalImg()">✕</button>
      </div>
    </div>
    <input type="file" accept="image/*" id="mPImgFile" style="display:none" onchange="prevModalImg(event)">
  </div>
  <label class="flabel">Tags</label>
  <input class="field" id="mPTags" placeholder="CFD, Structures, MRO" style="margin-bottom:0;">
  <div class="macts">
    <button class="btn btn-gh btn-sm" onclick="closeM('postModal')">Cancel</button>
    <button class="btn btn-go btn-sm" onclick="savePostModal()">Publish</button>
  </div>
</div>
</div>

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
  <div class="img-upload-zone" id="journeyImgZone" onclick="document.getElementById('jImgFile').click()" style="min-height:80px;margin-bottom:.6rem;">
    <div class="img-upload-ph" id="journeyImgPh">
      <div class="img-upload-ph-icon">📷</div>
      <div class="img-upload-ph-text">Click to add a photo</div>
    </div>
    <img id="jImgPrev" class="img-upload-preview" src="" alt="" style="display:none;max-height:140px;">
    <div class="img-overlay-btns">
      <button class="img-ov-btn change" title="Change" onclick="event.stopPropagation();document.getElementById('jImgFile').click()">✎</button>
      <button class="img-ov-btn remove" title="Remove" onclick="event.stopPropagation();removeJourneyImg()">✕</button>
    </div>
  </div>
  <input type="file" accept="image/*" id="jImgFile" style="display:none" onchange="prevJourneyImg(event)">
  <div class="macts">
    <button class="btn btn-gh btn-sm" onclick="closeM('journeyModal')">Cancel</button>
    <button class="btn btn-go btn-sm" onclick="saveJourney()">Save</button>
  </div>
</div>
</div>

<div class="ov" id="discussModal">
<div class="modal">
  <div class="mhd"><div class="mt">New Discussion Topic</div><button class="mx" onclick="closeM('discussModal')">×</button></div>
  <label class="flabel">Title</label>
  <input class="field" id="dmTitle" placeholder="What's the topic?">
  <label class="flabel">Content</label>
  <textarea class="field" id="dmText" style="min-height:95px;" placeholder="Share your thoughts…"></textarea>
  <div class="macts">
    <button class="btn btn-gh btn-sm" onclick="closeM('discussModal')">Cancel</button>
    <button class="btn btn-go btn-sm" onclick="addDiscussPost()">Publish →</button>
  </div>
</div>
</div>

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

<div class="ov" id="donateModal">
<div class="modal" style="text-align:center;">
  <div class="mhd"><div class="mt">☕ Support Nashat</div><button class="mx" onclick="closeM('donateModal')">×</button></div>
  <p style="color:var(--mu);font-size:.83rem;margin-bottom:1.25rem;line-height:1.78;">Thank you for your support! Contact via email to complete via PayPal or bank transfer.</p>
  <div class="epill" id="donateEmailPill" onclick="copyEmail()"></div>
  <div class="macts" style="justify-content:center;margin-top:1.25rem;"><button class="btn btn-gh btn-sm" onclick="closeM('donateModal')">Close</button></div>
</div>
</div>

<!-- ══ READER MODAL ══ -->
<div class="reader-ov" id="readerOv" onclick="readerClickOut(event)">
  <div class="reader-modal" id="readerModal">
    <div class="reader-progress" id="readerProgress"></div>
    <div class="reader-topbar">
      <button class="reader-nav-btn" onclick="closeReader()">
        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="15 18 9 12 15 6"/></svg>
        Back
      </button>
      <div class="reader-nav-center" id="readerNavTitle"></div>
      <div style="width:60px"></div>
    </div>
    <div id="readerContent"></div>
    <div class="reader-action-bar" id="readerActionBar"></div>
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
let composeTags=[];

// ══ REFRESH ══
window._refresh=async function(t){
  const{data}=await _supa.from(t).select('*').order('created_at',{ascending:false});
  if(!data)return;
  if(t==='works'){
    works=data.map(r=>({id:r.id,title:r.title||'',emoji:r.emoji||'📁',cat:r.cat||'',desc:r.description||'',year:r.year||'',link:r.link||'',price:r.price||'',photo:r.photo||'',tagsText:r.tags_text||''}));
    renderWorks();renderCarousel();updateStats();
  }else if(t==='posts'){
    posts=data.map(r=>({id:r.id,type:r.type||'article',title:r.title||'',content:r.content||'',tags:Array.isArray(r.tags)?r.tags:[],date:r.date||'',likes:r.likes||0,liked:false,comments:Array.isArray(r.comments)?r.comments:[],url:r.url||'',linkTitle:r.link_title||'',linkIcon:r.link_icon||'🌐',videoId:r.video_id||'',docName:r.doc_name||'',docUrl:r.doc_url||'',imgData:r.img_data||'',toolUrl:r.tool_url||'',toolStack:r.tool_stack||'',toolIcon:r.tool_icon||'⚙'}));
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
  const e=EM;
  ['emVal','aboutEmail','contactEmail','svcEmailPill','supEmailPill','donateEmailPill','footerEmail'].forEach(id=>{const el=document.getElementById(id);if(el)el.textContent=e;});
  const ce=document.getElementById('contactEmail');
  if(ce)ce.innerHTML=`<a href="mailto:${e}" style="color:var(--go);text-decoration:none;">${e}</a>`;
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
    if(isAdmin)toast('✓ Welcome back, Nashat!');
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
  SB.listen('works',data=>{works=data.map(r=>({id:r.id,title:r.title||'',emoji:r.emoji||'📁',cat:r.cat||'',desc:r.description||'',year:r.year||'',link:r.link||'',price:r.price||'',photo:r.photo||'',tagsText:r.tags_text||''}));renderWorks();renderCarousel();updateStats();});
  SB.listen('posts',data=>{posts=data.map(r=>({id:r.id,type:r.type||'article',title:r.title||'',content:r.content||'',tags:Array.isArray(r.tags)?r.tags:[],date:r.date||'',likes:r.likes||0,liked:false,comments:Array.isArray(r.comments)?r.comments:[],url:r.url||'',linkTitle:r.link_title||'',linkIcon:r.link_icon||'🌐',videoId:r.video_id||'',docName:r.doc_name||'',docUrl:r.doc_url||'',imgData:r.img_data||'',toolUrl:r.tool_url||'',toolStack:r.tool_stack||'',toolIcon:r.tool_icon||'⚙'}));renderPosts(activeTag);renderCarousel();updateStats();});
  SB.listen('journey',data=>{journey=data.map(r=>({id:r.id,type:r.type||'milestone',title:r.title||'',org:r.org||'',date:r.date||'',desc:r.description||'',img:r.img||''})).reverse();renderJourney(activeJType);renderCarousel();});
  SB.listen('comments',data=>{comments=data.map(r=>({id:r.id,isAdminPost:r.is_admin_post,name:r.name||'Visitor',title:r.title||'',text:r.body||r.text||'',time:r.time||'',date:r.date||'',likes:r.likes||0,liked:false,replies:Array.isArray(r.replies)?r.replies:[],showReps:false}));renderCmts();updateDiscStats();});
}

// ══ LOCAL DATA ══
function loadLocalData(){
  if(!works.length)works=[
    {id:'w1',title:'Vibration Analysis on Aircraft Wing',emoji:'✈',cat:'Simulation',photo:'',desc:'Modal analysis comparing Aluminum vs. CFRP using ANSYS. CFD simulation for aerodynamic stability and validated notch-filter mitigation system.',year:'2025',link:'',price:'',tagsText:'ANSYS,Creo,CFD,Modal Analysis'},
    {id:'w2',title:'Hydraulic Pump Systems Study',emoji:'⚙',cat:'MRO',photo:'',desc:'Hands-on inspection and functional testing of hydraulic pump systems during 8-week RJAF Overhaul Workshop training.',year:'2025',link:'',price:'',tagsText:'MRO,Hydraulics,RJAF'},
    {id:'w3',title:'CFD Aerodynamic Stability Model',emoji:'🛩',cat:'Simulation',photo:'',desc:'CFD simulation to investigate aerodynamic stability of aircraft wing profiles using ANSYS.',year:'2025',link:'',price:'',tagsText:'ANSYS,CFD,Aerodynamics'}
  ];
  if(!posts.length)posts=[
    {id:'p1',type:'article',title:'Aluminum vs CFRP: What My Research Found',content:'During my graduation project at JUST, I performed an in-depth modal analysis comparing aluminum alloys to CFRP on a full aircraft wing model. CFRP offers significantly higher natural frequencies and better resonance resistance.',tags:['Structures','CFRP','FEA'],date:'2025-12-01',likes:0,liked:false,comments:[],url:'',linkTitle:'',linkIcon:'',videoId:'',docName:'',docUrl:'',imgData:'',toolUrl:'',toolStack:'',toolIcon:'⚙'},
    {id:'p2',type:'article',title:'What I Learned at the Royal Jordanian Air Force',content:'My 8-week training at the RJAF Overhaul Department was one of the most transformative experiences. Working directly with aircraft components gave me ground-level understanding of MRO operations.',tags:['MRO','Career','RJAF'],date:'2025-10-15',likes:0,liked:false,comments:[],url:'',linkTitle:'',linkIcon:'',videoId:'',docName:'',docUrl:'',imgData:'',toolUrl:'',toolStack:'',toolIcon:'⚙'}
  ];
  if(!journey.length)journey=[
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
  setTimeout(()=>{trigRev();observeCards();},60);
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
    applyProfilePhoto(ev.target.result);
    await SB._supa.from('settings').upsert({key:'profile_photo',value:ev.target.result});
    localStorage.setItem('pp',ev.target.result);toast('✓ Photo saved!');
  };r.readAsDataURL(f);
}
function applyProfilePhoto(src){
  ['avatarEl','discComposeAv'].forEach(id=>{
    const el=document.getElementById(id);if(!el)return;
    el.style.backgroundImage=`url(${src})`;el.style.backgroundSize='cover';el.style.backgroundPosition='center';el.textContent='';
  });
}
async function loadProfilePhoto(){
  try{const{data}=await SB._supa.from('settings').select('value').eq('key','profile_photo').single();if(data?.value)applyProfilePhoto(data.value);}
  catch(e){const p=localStorage.getItem('pp');if(p)applyProfilePhoto(p);}
}
(()=>{const p=localStorage.getItem('pp');if(p){['avatarEl','discComposeAv'].forEach(id=>{const el=document.getElementById(id);if(el){el.style.backgroundImage=`url(${p})`;el.style.backgroundSize='cover';el.style.backgroundPosition='center';el.textContent='';}});}})();

// ══ STARS ══
(()=>{
  const wrap=document.getElementById('starsWrap');if(!wrap)return;
  for(let i=0;i<65;i++){
    const s=document.createElement('div');s.className='star';
    s.style.left=Math.random()*100+'%';s.style.top=Math.random()*100+'%';
    const sz=Math.random()>.85?3:Math.random()>.6?2:1.5;
    s.style.width=sz+'px';s.style.height=sz+'px';
    s.style.setProperty('--dur',(2+Math.random()*4)+'s');
    s.style.setProperty('--op',(0.2+Math.random()*0.55));
    s.style.animationDelay=(Math.random()*7)+'s';
    wrap.appendChild(s);
  }
})();

// ══ CARD OBSERVER ══
const _cObs=new IntersectionObserver(entries=>{entries.forEach(e=>{if(e.isIntersecting)e.target.classList.add('in');});},{threshold:0.08});
function observeCards(){document.querySelectorAll('.anim-card:not(.in)').forEach((el,i)=>{if(!el.dataset.obs){el.dataset.obs='1';el.style.transitionDelay=(i%6)*.08+'s';_cObs.observe(el);}});}

// ══ CAROUSEL ══
function switchCarousel(type,btn){cType=type;cIdx=0;document.querySelectorAll('.ctab').forEach(t=>t.classList.remove('on'));if(btn)btn.classList.add('on');renderCarousel();resetCarouselAuto();}
function renderCarousel(){
  const track=document.getElementById('cTrack');const dots=document.getElementById('cDots');if(!track)return;
  let items=[];
  if(cType==='works')items=works.map(w=>({emoji:w.emoji||'✈',photo:w.photo||'',badge:w.cat,title:w.title,sub:w.desc,date:w.year,fn:()=>openPD(w.id)}));
  else if(cType==='journey')items=journey.map(j=>({emoji:j.type==='milestone'?'🏆':j.type==='course'?'📚':'🎤',photo:j.img||'',badge:j.type,title:j.title,sub:j.desc||j.org,date:j.date,fn:null}));
  else items=posts.map(p=>({emoji:p.type==='video'?'▶':p.type==='link'?'🔗':p.type==='doc'?'📄':'📝',photo:p.imgData||'',badge:p.type,title:p.title,sub:p.content,date:p.date,fn:()=>openPostReader(p.id)}));
  if(!items.length){track.innerHTML='<div style="padding:2rem;color:var(--mu);font-size:.84rem;">No items yet.</div>';dots.innerHTML='';return;}
  track.innerHTML=items.map((item,i)=>`<div class="ccard" onclick="cClick(${i})"><div class="ccard-img"><div class="ccard-img-bg"></div>${item.photo?`<img src="${item.photo}" alt="">`:`<span style="position:relative;z-index:1;">${item.emoji}</span>`}<div class="ccard-badge">${item.badge}</div></div><div class="ccard-body"><div class="ccard-title">${item.title}</div><div class="ccard-sub">${item.sub||''}</div><div class="ccard-foot"><span class="ccard-date">${item.date||''}</span><button class="ccard-btn">View →</button></div></div></div>`).join('');
  dots.innerHTML=items.map((_,i)=>`<button class="cdot${i===cIdx?' on':''}" onclick="goCarousel(${i})"></button>`).join('');
  goCarousel(cIdx,false);
}
function cClick(i){if(cType==='works')openPD(works[i]?.id);else if(cType==='posts'){const p=posts[i];if(p)openPostReader(p.id);}}
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
  const cv=`<!DOCTYPE html><html><head><meta charset="UTF-8"><title>Nashat Aldhoun CV</title><style>*{margin:0;padding:0;box-sizing:border-box;}body{font-family:'Segoe UI',sans-serif;color:#0f1115;padding:2.5cm 2cm;font-size:10.5pt;line-height:1.5;}h1{font-size:22pt;letter-spacing:-.5px;margin-bottom:2pt;}.role{font-size:10pt;color:#4875c2;font-weight:600;letter-spacing:1px;text-transform:uppercase;margin-bottom:7pt;}.contact{font-size:8.5pt;color:#677080;margin-bottom:14pt;border-bottom:1px solid #e5e7eb;padding-bottom:9pt;}h2{font-size:11.5pt;color:#08162a;margin:14pt 0 5pt;border-left:3pt solid #c8a86c;padding-left:7pt;}.item{margin-bottom:8pt;}.ih{display:flex;justify-content:space-between;}.it{font-weight:600;font-size:10pt;}.io{color:#4875c2;font-size:9pt;margin:1pt 0;}.id{font-size:9pt;color:#677080;margin-top:2pt;}.date{font-size:8.5pt;color:#9ca3af;white-space:nowrap;}ul{padding-left:13pt;margin-top:2pt;}li{margin-bottom:1.5pt;font-size:8.5pt;color:#677080;}.sg{display:grid;grid-template-columns:1fr 1fr;gap:7pt;margin-top:3pt;}.sl{font-size:7.5pt;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:#c8a86c;margin-bottom:2pt;}.sv{font-size:9pt;color:#334054;}.footer{margin-top:18pt;text-align:center;font-size:7.5pt;color:#d1d5db;border-top:1px solid #f3f4f6;padding-top:7pt;}</style></head><body><h1>Nashat Omar Aldhoun</h1><div class="role">Junior Aeronautical Engineer</div><div class="contact">Irbid, Jordan &nbsp;|&nbsp; +962 776 763 628 &nbsp;|&nbsp; nashataldhoun@yahoo.com &nbsp;|&nbsp; linkedin.com/in/nashat-al-dhoun</div><h2>Summary</h2><div class="item"><div class="id">Highly motivated Junior Aeronautical Engineer and 2025 JUST graduate. Specialized in Aircraft Structures, FEA, and MRO. Trained at the Royal Jordanian Air Force. Proficient in ANSYS, SolidWorks, Creo, and MATLAB.</div></div><h2>Experience</h2><div class="item"><div class="ih"><div><div class="it">Aircraft Maintenance Trainee</div><div class="io">Royal Jordanian Air Force — Overhaul Department</div></div><div class="date">Sep–Oct 2025</div></div><ul><li>8-week intensive training in aircraft maintenance and overhaul procedures</li><li>Hands-on inspection and functional testing of hydraulic pump systems</li><li>Applied aviation safety protocols under licensed engineers supervision</li></ul></div><h2>Education</h2><div class="item"><div class="ih"><div><div class="it">B.Sc. Aeronautical Engineering</div><div class="io">Jordan University of Science and Technology (JUST)</div></div><div class="date">2021–2025</div></div><div class="id">Graduation Project: Vibration Analysis on Aircraft Wing — Modal analysis (Al vs CFRP), CFD simulation, notch-filter mitigation.</div></div><h2>Projects</h2><div class="item"><div class="it">Vibration Analysis on Aircraft Wing — JUST 2025</div><ul><li>3D modeling of full aircraft wing in Creo Parametric</li><li>Modal analysis in ANSYS comparing Aluminum Alloys vs. CFRP composites</li><li>CFD simulation for aerodynamic stability analysis</li><li>Designed and validated notch-filter vibration mitigation system</li></ul></div><h2>Skills</h2><div class="sg"><div><div class="sl">Engineering Software</div><div class="sv">Creo · ANSYS (FEA & CFD) · SolidWorks · MATLAB</div></div><div><div class="sl">Core Competencies</div><div class="sv">FEA · Modal Analysis · CFD · MRO · Structural Analysis</div></div><div style="margin-top:5pt"><div class="sl">Data & Office</div><div class="sv">Power BI · Microsoft Office</div></div><div style="margin-top:5pt"><div class="sl">Languages</div><div class="sv">Arabic (Native) · English (B2)</div></div></div><h2>Certifications</h2><div class="item"><div class="ih"><div class="it">Power BI — Data Analysis & Visualization</div><div class="date">2026</div></div></div><div class="item"><div class="ih"><div class="it">Employment Skills Training (5hrs)</div><div class="date">2024</div></div></div><div class="footer">Nashat Omar Aldhoun · nashataldhoun@yahoo.com · +962 776 763 628 · Irbid, Jordan</div></body></html>`;
  const w=window.open('','_blank');w.document.write(cv);w.document.close();
  w.onload=()=>setTimeout(()=>w.print(),500);
  toast('✓ Choose "Save as PDF" in the print dialog');
}

// ══ WORKS ══
function renderWorks(){
  const g=document.getElementById('worksGrid');if(!g)return;
  if(!works.length){g.innerHTML='<div style="text-align:center;padding:4rem;color:var(--mu);grid-column:1/-1;"><div style="font-size:2.8rem;margin-bottom:.85rem;opacity:.35;">✈</div><p style="font-size:.88rem;">No projects yet.</p></div>';return;}
  g.innerHTML=works.map(w=>{
    const descPreview=(w.desc||'').substring(0,110)+(w.desc&&w.desc.length>110?'…':'');
    return `<div class="wcard anim-card" onclick="openPD('${w.id}')">
      <div class="wthumb">
        <img src="${w.photo||''}" class="${w.photo?'on':''}" alt="">
        <div class="wthumb-ph" ${w.photo?'style="display:none"':''}><div class="wthumb-bg"></div><span style="position:relative;z-index:1;font-size:2.8rem;">${w.emoji||'📁'}</span></div>
        <div class="wcat">${w.cat||'Project'}</div>
        ${w.price?`<div class="wprice">${w.price}</div>`:''}
        <div class="photo-ov" style="display:${isAdmin?'flex':'none'}" onclick="event.stopPropagation();document.getElementById('wph-${w.id}').click()">
          <span>📷 Upload Photo</span>
          <input type="file" id="wph-${w.id}" accept="image/*" style="display:none" onchange="workPhoto('${w.id}',event)">
        </div>
      </div>
      <div class="wbody">
        <div class="wtitle">${w.title||'Untitled Project'}</div>
        ${descPreview?`<div class="wdesc">${descPreview}</div>`:'<div class="wdesc" style="color:var(--mu);font-style:italic;font-size:.75rem;">No description yet.</div>'}
        <div class="wfoot">
          <div style="display:flex;align-items:center;gap:.45rem;flex-wrap:wrap;">
            <span class="wyear">${w.year||'2025'}</span>
            ${w.link?`<a href="${w.link}" target="_blank" onclick="event.stopPropagation()" style="color:var(--bl2);font-size:.68rem;text-decoration:none;">View ↗</a>`:''}
          </div>
          <div style="display:flex;gap:.28rem;">
            <button class="btn btn-gh btn-xs" style="display:${isAdmin?'inline-flex':'none'}" onclick="event.stopPropagation();editWork('${w.id}')">Edit</button>
            <button class="btn-del" style="display:${isAdmin?'inline-flex':'none'}" onclick="event.stopPropagation();delWork('${w.id}')">🗑</button>
          </div>
        </div>
      </div>
    </div>`;
  }).join('');
  setTimeout(observeCards,30);
}
function workPhoto(id,e){const f=e.target.files[0];if(!f)return;const r=new FileReader();r.onload=async ev=>{await SB.update('works',id,{photo:ev.target.result});toast('✓ Photo saved!');};r.readAsDataURL(f);}
function openPD(id){
  const w=works.find(x=>x.id===id);if(!w)return;
  document.getElementById('pd-t').textContent=w.title;
  const img=document.getElementById('pd-img'),em=document.getElementById('pd-em');
  if(w.photo){img.src=w.photo;img.style.display='block';em.style.display='none';}
  else{img.style.display='none';em.style.display='block';em.textContent=w.emoji||'📁';}
  const metaBadge=(txt)=>`<span style="background:var(--pan);border:1px solid var(--b);color:var(--tx);font-size:.69rem;padding:.22rem .58rem;border-radius:5px;">${txt}</span>`;
  document.getElementById('pd-meta').innerHTML=metaBadge(w.cat)+metaBadge(w.year)+(w.price?`<span style="background:var(--go3);border:1px solid rgba(200,168,108,.24);color:var(--go);font-size:.69rem;padding:.22rem .58rem;border-radius:5px;">${w.price}</span>`:'');
  const rawDesc=w.desc||'';
  const descLines=rawDesc.length?rawDesc.split('\n').filter(Boolean):[];
  document.getElementById('pd-desc').innerHTML=descLines.length?descLines.map(p=>'<p style="margin-bottom:.85rem;color:var(--tx);font-size:.86rem;line-height:1.82;">'+p+'</p>').join(''):'<p style="color:var(--mu);font-style:italic;">No description yet.</p>';
  document.getElementById('pd-link').innerHTML=w.link?`<a class="btn btn-go btn-sm" href="${w.link}" target="_blank" style="display:inline-flex;text-decoration:none;">View Project ↗</a>`:'';
  openM('pdModal');
}
function prevWorkImg(e){
  const f=e.target.files[0];if(!f)return;
  const r=new FileReader();
  r.onload=ev=>{const pi=document.getElementById('wImgPrev');const ph=document.getElementById('wCoverPh');if(pi){pi.src=ev.target.result;pi.style.display='block';}if(ph)ph.style.display='none';};
  r.readAsDataURL(f);
}
async function saveWork(){
  if(!isAdmin)return;
  const id=document.getElementById('ewId').value;
  const wImgEl=document.getElementById('wImgPrev');
  const wImgData=wImgEl&&wImgEl.style.display!=='none'?wImgEl.src:'';
  const w={title:document.getElementById('wT').value||'Untitled',emoji:document.getElementById('wE').value||'📁',cat:document.getElementById('wC').value,description:document.getElementById('wD').value,year:document.getElementById('wY').value||'2025',link:document.getElementById('wL').value,price:document.getElementById('wP').value,tags_text:document.getElementById('wTags')?.value||''};
  if(wImgData)w.photo=wImgData;
  try{if(id){await SB.update('works',id,w);}else{await SB.insert('works',w);}closeM('workModal');clearWForm();toast('✓ Saved!');}
  catch(e){toast('⚠ Error: '+e.message);}
}
function editWork(id){
  const w=works.find(x=>x.id===id);if(!w)return;
  document.getElementById('ewId').value=id;
  document.getElementById('wT').value=w.title;
  document.getElementById('wE').value=w.emoji;
  document.getElementById('wC').value=w.cat;
  document.getElementById('wD').value=w.desc;
  document.getElementById('wY').value=w.year;
  document.getElementById('wL').value=w.link;
  document.getElementById('wP').value=w.price;
  if(document.getElementById('wTags'))document.getElementById('wTags').value=w.tagsText||'';
  if(w.photo){const pi=document.getElementById('wImgPrev');const ph=document.getElementById('wCoverPh');if(pi){pi.src=w.photo;pi.style.display='block';}if(ph)ph.style.display='none';}
  openM('workModal');
}
async function delWork(id){if(!isAdmin||!confirm('Delete this project?'))return;try{await SB.delete('works',id);toast('Deleted');}catch(e){toast('⚠ '+e.message);}}
function clearWForm(){['ewId','wT','wE','wY','wL','wP'].forEach(i=>document.getElementById(i).value='');document.getElementById('wD').value='';}

// ══ POSTS — NEW COMPOSER ══

// Image upload helpers with zone state
function _applyImgToZone(zoneId,phId,prevId,src){
  const zone=document.getElementById(zoneId);
  const ph=document.getElementById(phId);
  const prev=document.getElementById(prevId);
  if(zone)zone.classList.add('has-img');
  if(ph)ph.style.display='none';
  if(prev){prev.src=src;prev.style.display='block';}
}
function _clearImgZone(zoneId,phId,prevId,fileId){
  const zone=document.getElementById(zoneId);
  const ph=document.getElementById(phId);
  const prev=document.getElementById(prevId);
  const fi=document.getElementById(fileId);
  if(zone)zone.classList.remove('has-img');
  if(ph)ph.style.display='';
  if(prev){prev.src='';prev.style.display='none';}
  if(fi)fi.value='';
}

function prevPostImg(e){
  const f=e.target.files[0];if(!f)return;
  const r=new FileReader();
  r.onload=ev=>_applyImgToZone('composeImgZone','composeImgPh','pImgPrev',ev.target.result);
  r.readAsDataURL(f);
}
function removeComposeImg(){_clearImgZone('composeImgZone','composeImgPh','pImgPrev','pImgFile');}

function prevModalImg(e){
  const f=e.target.files[0];if(!f)return;
  const r=new FileReader();
  r.onload=ev=>_applyImgToZone('modalImgZone','modalImgPh','mPImgPrev',ev.target.result);
  r.readAsDataURL(f);
}
function removeModalImg(){_clearImgZone('modalImgZone','modalImgPh','mPImgPrev','mPImgFile');}

// Compose tags
function handleComposeTag(e){
  if(e.key==='Enter'||e.key===','){
    e.preventDefault();
    const val=e.target.value.trim().replace(/,$/,'');
    if(val&&!composeTags.includes(val)&&composeTags.length<8){
      composeTags.push(val);
      renderComposeTags();
    }
    e.target.value='';
  }
}
function renderComposeTags(){
  const wrap=document.getElementById('composeTags');
  const input=document.getElementById('composeTagIn');
  wrap.querySelectorAll('.tag-pill').forEach(c=>c.remove());
  composeTags.forEach((t,i)=>{
    const pill=document.createElement('span');
    pill.className='tag-pill';
    pill.innerHTML=t+`<button class="tag-pill-x" onclick="removeComposeTag(${i})">×</button>`;
    wrap.insertBefore(pill,input);
  });
}
function removeComposeTag(i){composeTags.splice(i,1);renderComposeTags();}

function updateCharCount(){
  const content=document.getElementById('pContent')?.value||'';
  const el=document.getElementById('charCount');
  if(el)el.textContent=content.length+' / 1200 characters';
}

function switchPTab(type,btn){
  document.getElementById('pType').value=type;
  document.querySelectorAll('#composeTabs .ptab').forEach(t=>t.classList.remove('active'));btn.classList.add('active');
  document.querySelectorAll('#postCompose .ptype-panel').forEach(p=>p.classList.remove('active'));
  document.getElementById('pt-'+type).classList.add('active');
}
function switchModalPTab(type,btn){
  document.getElementById('mPType').value=type;
  document.querySelectorAll('#modalPTabs .ptab').forEach(t=>t.classList.remove('active'));btn.classList.add('active');
  document.querySelectorAll('#postModal .ptype-panel').forEach(p=>p.classList.remove('active'));
  document.getElementById('mpt-'+type).classList.add('active');
}

function getYTId(url){const m=url.match(/(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([a-zA-Z0-9_-]{11})/);return m?m[1]:url.trim().substring(0,11);}

async function savePost(){
  if(!isAdmin){toast('⚠ Admin only');return;}
  const type=document.getElementById('pType').value;
  const imgPrev=document.getElementById('pImgPrev');
  const row={
    type,
    title:document.getElementById('pTitle').value||'Untitled',
    content:document.getElementById('pContent').value,
    tags:composeTags.slice(),
    date:new Date().toISOString().split('T')[0],
    likes:0,comments:[],
    url:document.getElementById('pUrl')?.value||'',
    link_title:document.getElementById('pLinkTitle')?.value||'',
    link_icon:document.getElementById('pLinkIcon')?.value||'🌐',
    video_id:type==='video'?getYTId(document.getElementById('pVideoUrl')?.value||''):'',
    doc_name:document.getElementById('pDocName')?.value||'',
    doc_url:document.getElementById('pDocUrl')?.value||'',
    img_data:imgPrev&&imgPrev.style.display!=='none'?imgPrev.src:'',
    tool_url:document.getElementById('pToolUrl')?.value||'',
    tool_stack:document.getElementById('pToolStack')?.value||'',
    tool_icon:document.getElementById('pToolIcon')?.value||'⚙'
  };
  try{
    await SB.insert('posts',row);
    ['pTitle','pContent'].forEach(i=>document.getElementById(i).value='');
    composeTags=[];renderComposeTags();
    removeComposeImg();
    updateCharCount();
    toast('✓ Published!');
  }catch(e){toast('⚠ '+e.message);}
}

async function savePostModal(){
  if(!isAdmin){toast('⚠ Admin only');return;}
  const type=document.getElementById('mPType').value;
  const imgPrev=document.getElementById('mPImgPrev');
  const row={
    type,
    title:document.getElementById('mPTitle').value||'Untitled',
    content:document.getElementById('mPContent').value,
    tags:document.getElementById('mPTags').value.split(',').map(t=>t.trim()).filter(Boolean),
    date:new Date().toISOString().split('T')[0],likes:0,comments:[],
    url:document.getElementById('mPUrl')?.value||'',
    link_title:document.getElementById('mPLinkTitle')?.value||'',
    link_icon:document.getElementById('mPLinkIcon')?.value||'🌐',
    video_id:type==='video'?getYTId(document.getElementById('mPVideoUrl')?.value||''):'',
    doc_name:document.getElementById('mPDocName')?.value||'',
    doc_url:document.getElementById('mPDocUrl')?.value||'',
    img_data:imgPrev&&imgPrev.style.display!=='none'?imgPrev.src:'',
    tool_url:document.getElementById('mPToolUrl')?.value||'',
    tool_stack:document.getElementById('mPToolStack')?.value||'',
    tool_icon:document.getElementById('mPToolIcon')?.value||'⚙'
  };
  try{await SB.insert('posts',row);closeM('postModal');toast('✓ Published!');}
  catch(e){toast('⚠ '+e.message);}
}

function readTime(txt){const w=(txt||'').split(' ').filter(Boolean).length;return Math.max(1,Math.round(w/200));}

// ══ NEW PROFESSIONAL POST RENDER ══
function renderPosts(filterTag){
  const feed=document.getElementById('postFeed');if(!feed)return;
  let filtered=filterTag?posts.filter(p=>p.tags&&p.tags.includes(filterTag)):posts;
  document.getElementById('filterCount').innerHTML=filterTag?`Showing ${filtered.length} for <strong style="color:var(--go)">#${filterTag}</strong> — <button onclick="filterPosts('',null)" style="background:none;border:none;color:var(--mu);cursor:pointer;font-size:.64rem;font-family:'DM Sans',sans-serif;">Clear ×</button>`:'';
  if(!filtered.length){feed.innerHTML='<div style="text-align:center;padding:4rem;color:var(--mu);"><div style="font-size:2.6rem;margin-bottom:.82rem;opacity:.35;">📝</div><p style="font-size:.86rem;">No posts yet.</p></div>';return;}
  const tl={article:'t-article',link:'t-link',video:'t-video',doc:'t-doc',image:'t-image',tool:'t-tool'};
  const tn={article:'Article',link:'Link',video:'Video',doc:'Document',image:'Image',tool:'Tool'};
  const pp=localStorage.getItem('pp');
  const avStyle=pp?`style="background-image:url(${pp});background-size:cover;background-position:center;"`:'';
  const avText=pp?'':'NA';

  feed.innerHTML=filtered.map(p=>{
    const rt=readTime(p.content);
    const preview=(p.content||'').substring(0,160)+(p.content&&p.content.length>160?'…':'');
    const hasCover=!!(p.imgData||(p.type==='video'&&p.videoId));

    // ── Tool card ──
    if(p.type==='tool'){
      const stack=(p.toolStack||'').split(',').map(s=>s.trim()).filter(Boolean);
      return `<div class="pcard-tool anim-card" onclick="openPostReader('${p.id}')" style="position:relative;padding:1.2rem 1.3rem .9rem;">
        <div class="pcard-tool-bg"></div>
        <div style="position:relative;z-index:1;">
          <div class="tool-badge">${p.toolIcon||'⚙'} Engineering Tool</div>
          <div style="font-family:'DM Serif Display',serif;font-size:1.18rem;color:var(--wh);margin-bottom:.35rem;letter-spacing:-.15px;">${p.title}</div>
          <div style="font-size:.82rem;color:var(--tx);line-height:1.7;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;">${preview}</div>
          <div class="tool-chips">${stack.map(s=>`<span class="tool-chip">${s}</span>`).join('')}</div>
        </div>
        <div style="padding:.65rem 0 0;border-top:1px solid rgba(255,255,255,.06);margin-top:.75rem;display:flex;align-items:center;justify-content:space-between;position:relative;z-index:1;">
          <div style="display:flex;gap:.5rem;align-items:center;">
            <button class="pact${p.liked?' liked':''}" onclick="event.stopPropagation();likePost('${p.id}')">♥ ${p.likes||0}</button>
            <button class="pact" onclick="event.stopPropagation();openPostReader('${p.id}',true)">💬 ${(p.comments||[]).length}</button>
          </div>
          <div style="display:flex;align-items:center;gap:.5rem;">
            ${p.toolUrl?`<a href="${p.toolUrl}" target="_blank" onclick="event.stopPropagation()" class="btn btn-go btn-xs" style="text-decoration:none;">Launch ↗</a>`:''}
            <button class="btn-del" style="display:${isAdmin?'inline-flex':'none'}" onclick="event.stopPropagation();delPost('${p.id}')">🗑</button>
          </div>
        </div>
      </div>`;
    }

    // Cover HTML for image/video
    let coverHtml='';
    if(p.imgData){
      coverHtml=`<div class="pcard-cover"><img src="${p.imgData}" alt=""><div class="pcard-cover-type">${tn[p.type]||p.type}</div></div>`;
    }else if(p.type==='video'&&p.videoId){
      coverHtml=`<div class="pcard-cover"><div class="pcard-cover-ph"><div class="pcard-cover-ph-bg"></div><span style="position:relative;z-index:1;font-size:2rem;">▶</span></div><div class="pcard-cover-type">Video</div></div>`;
    }

    return `<div class="pcard anim-card${hasCover?' has-cover':''}" onclick="openPostReader('${p.id}')">
      <div class="pcard-inner">
        ${coverHtml}
        <div class="pcard-main">
          <div class="pcard-top">
            <div class="pcard-av" ${avStyle}>${avText}</div>
            <div>
              <div class="pcard-author">Nashat Aldhoun</div>
              <div class="pcard-date">${p.date||''}</div>
            </div>
            <span class="pcard-badge ${tl[p.type]||''}">${tn[p.type]||p.type}</span>
            <span class="pcard-rt">⏱ ${rt} min</span>
            <button class="btn-del" style="display:${isAdmin?'inline-flex':'none'};margin-left:.2rem;" onclick="event.stopPropagation();delPost('${p.id}')">🗑</button>
          </div>
          <div class="pcard-title">${p.title}</div>
          <div class="pcard-excerpt">${preview}</div>
          ${p.tags?.length?`<div class="pcard-tags">${p.tags.map(t=>`<span class="pcard-tag" onclick="event.stopPropagation();filterPosts('${t}',this)">#${t}</span>`).join('')}</div>`:''}
          <div class="pcard-foot">
            <button class="pact${p.liked?' liked':''}" onclick="event.stopPropagation();likePost('${p.id}')">♥ ${p.likes||0}</button>
            <button class="pact" onclick="event.stopPropagation();openPostReader('${p.id}',true)">💬 ${(p.comments||[]).length}</button>
            <span class="pcard-read">Read full <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"/></svg></span>
          </div>
        </div>
      </div>
    </div>`;
  }).join('');

  renderTagCloud();
  setTimeout(observeCards,30);
}

async function likePost(id){const p=posts.find(x=>x.id===id);if(!p)return;p.liked=!p.liked;p.likes=(p.likes||0)+(p.liked?1:-1);try{await SB.update('posts',id,{likes:p.likes});}catch(e){}renderPosts(activeTag);}
async function delPost(id){if(!isAdmin||!confirm('Delete post?'))return;try{await SB.delete('posts',id);toast('Deleted');}catch(e){toast('⚠ '+e.message);}}
function filterPosts(tag,el){activeTag=tag;document.querySelectorAll('.ttag').forEach(t=>t.classList.remove('on'));if(el)el.classList.add('on');renderPosts(tag);}
function renderTagCloud(){
  const tc=document.getElementById('tagCloud');if(!tc)return;
  const allTags=[...new Set(posts.flatMap(p=>p.tags||[]))];
  tc.innerHTML=allTags.map(t=>`<span class="ttag${activeTag===t?' on':''}" onclick="filterPosts('${t}',this)">${t}</span>`).join('');
  if(!allTags.length)tc.innerHTML='<span style="font-size:.73rem;color:var(--mu);">No tags yet</span>';
}

// ══ JOURNEY ══
function prevJourneyImg(e){
  const f=e.target.files[0];if(!f)return;
  const r=new FileReader();
  r.onload=ev=>_applyImgToZone('journeyImgZone','journeyImgPh','jImgPrev',ev.target.result);
  r.readAsDataURL(f);
}
function removeJourneyImg(){_clearImgZone('journeyImgZone','journeyImgPh','jImgPrev','jImgFile');}

async function saveJourney(){
  if(!isAdmin)return;
  const imgPrev=document.getElementById('jImgPrev');
  const row={
    type:document.getElementById('jType').value,
    title:document.getElementById('jTitle').value||'Untitled',
    org:document.getElementById('jOrg').value,
    date:document.getElementById('jDate').value||new Date().toISOString().split('T')[0].substring(0,7),
    description:document.getElementById('jDesc').value,
    img:imgPrev&&imgPrev.style.display!=='none'?imgPrev.src:''
  };
  try{
    await SB.insert('journey',row);closeM('journeyModal');
    ['jTitle','jOrg','jDate','jDesc'].forEach(i=>document.getElementById(i).value='');
    removeJourneyImg();
    toast('✓ Entry saved!');
  }catch(e){toast('⚠ '+e.message);}
}
function filterJourney(type,btn){activeJType=type;document.querySelectorAll('.jtab').forEach(t=>t.classList.remove('on'));if(btn)btn.classList.add('on');renderJourney(type);}
function renderJourney(filter){
  const tl=document.getElementById('journeyTimeline');if(!tl)return;
  const filtered=filter==='all'?journey:journey.filter(j=>j.type===filter);
  if(!filtered.length){tl.innerHTML='<div style="text-align:center;padding:4rem;color:var(--mu);"><div style="font-size:2.6rem;margin-bottom:.82rem;opacity:.35;">🗓</div><p style="font-size:.86rem;">No entries yet.</p></div>';return;}
  const tb={milestone:'jt-milestone',course:'jt-course',event:'jt-event'};
  const tn={milestone:'Milestone',course:'Course',event:'Event'};
  tl.innerHTML=filtered.map(j=>`
    <div class="jitem anim-card">
      <div class="jdot ${j.type}"></div>
      <div class="jcard" onclick="openJourneyReader('${j.id}')">
        <div class="jcard-top">
          <div style="flex:1;">
            <div style="display:flex;align-items:center;gap:.45rem;margin-bottom:.32rem;">
              <span class="jtype-badge ${tb[j.type]||''}">${tn[j.type]||j.type}</span>
              ${j.org?`<span style="font-size:.7rem;color:var(--go);font-weight:500;">${j.org}</span>`:''}
            </div>
            <div class="jtitle">${j.title}</div>
            ${j.desc?`<div class="jdesc" style="margin-top:.25rem;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;">${j.desc}</div>`:''}
            ${j.img?`<img class="jimg on" src="${j.img}" alt="" style="margin-top:.55rem;">`:''}
          </div>
          <div style="display:flex;flex-direction:column;align-items:flex-end;gap:.32rem;flex-shrink:0;">
            <span class="jdate">${j.date||''}</span>
            <span style="font-size:.66rem;color:var(--mu);display:flex;align-items:center;gap:.2rem;">Details<svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"/></svg></span>
            <button class="btn-del" style="display:${isAdmin?'inline-flex':'none'}" onclick="event.stopPropagation();delJourney('${j.id}')">🗑</button>
          </div>
        </div>
      </div>
    </div>`).join('');
  setTimeout(observeCards,30);
}
async function delJourney(id){if(!isAdmin||!confirm('Delete entry?'))return;try{await SB.delete('journey',id);toast('Deleted');}catch(e){toast('⚠ '+e.message);}}

// ══ DISCUSSION ══
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
  const nameEl=document.getElementById('rn-'+id);const input=document.getElementById('ri-'+id);
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
  const tc=document.getElementById('discTopicCount');const cc=document.getElementById('discCmtCount');const lc=document.getElementById('discLikeCount');
  if(tc)tc.textContent=topics;if(cc)cc.textContent=allReplies;if(lc)lc.textContent=allLikes;
}
function renderCmts(){
  const l=document.getElementById('cmtsList');if(!l)return;
  updateDiscStats();
  if(!comments.length){l.innerHTML=`<div style="text-align:center;padding:3.5rem 2rem;color:var(--mu);"><div style="font-size:2.8rem;margin-bottom:.85rem;opacity:.4;">💬</div><div style="font-size:.92rem;color:var(--tx);margin-bottom:.3rem;font-weight:600;">No discussions yet</div><div style="font-size:.78rem;">Nashat will start a discussion soon.</div></div>`;return;}
  const pp=localStorage.getItem('pp');
  l.innerHTML=comments.map(c=>{
    const isN=c.isAdminPost||c.name==='Nashat';
    const avStyle=isN&&pp?`style="background-image:url(${pp});background-size:cover;background-position:center;"`:'' ;
    const avText=isN&&pp?'':(isN?'NA':(c.name||'V')[0].toUpperCase());
    return `<div class="dcard anim-card" onclick="openDiscReader('${c.id}')">
      ${isN?`<div class="dcard-admin-head"><div class="dcard-topic-badge">Discussion Topic</div><div class="dcard-title">${c.title||'Untitled Topic'}</div></div>`:''}
      <div class="dcard-author">
        <div class="dcard-av ${isN?'':'dcard-av-visitor'}" ${avStyle}>${avText}</div>
        <div style="flex:1;"><div class="dcard-aname ${isN?'nashat':''}">${isN?'Nashat Aldhoun':c.name||'Visitor'}${isN?'<span class="author-tag">AUTHOR</span>':''}</div><div class="dcard-ameta">${c.date||''} ${c.time?'· '+c.time:''}</div></div>
        <button class="btn-del" style="display:${isAdmin?'inline-flex':'none'}" onclick="event.stopPropagation();delCmt('${c.id}')">🗑</button>
      </div>
      <div class="dcard-body"><div class="dcard-text" style="display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden;">${c.text}</div></div>
      <div class="dcard-actions">
        <button class="dact${c.liked?' liked':''}" onclick="event.stopPropagation();likeCmt('${c.id}')">
          <svg width="13" height="13" viewBox="0 0 24 24" fill="${c.liked?'currentColor':'none'}" stroke="currentColor" stroke-width="2"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>
          ${c.likes||0}
        </button>
        <button class="dact dact-cmt" onclick="event.stopPropagation();openDiscReader('${c.id}',true)">
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
          ${(c.replies||[]).length}
        </button>
        <span style="margin-left:auto;font-size:.68rem;color:var(--mu);display:flex;align-items:center;gap:.22rem;">Read full<svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"/></svg></span>
      </div>
    </div>`;
  }).join('');
  setTimeout(observeCards,30);
}
async function likeCmt(id){const c=comments.find(x=>x.id===id);if(!c)return;c.liked=!c.liked;c.likes=(c.likes||0)+(c.liked?1:-1);try{await SB.update('comments',id,{likes:c.likes});}catch(e){}renderCmts();}
async function delCmt(id){if(!isAdmin||!confirm('Delete this topic?'))return;try{await SB.delete('comments',id);toast('Deleted');}catch(e){toast('⚠ '+e.message);}}

// ══ CONTACT ══
function sendContact(){
  const name=document.getElementById('cf-name').value;
  const email=document.getElementById('cf-email').value;
  const subj=document.getElementById('cf-subj').value;
  const msg=document.getElementById('cf-msg').value;
  if(!name||!email||!msg){toast('⚠ Please fill all fields');return;}
  window.location.href=`mailto:${EM}?subject=${encodeURIComponent(subj+' — from '+name)}&body=${encodeURIComponent('From: '+name+'\nEmail: '+email+'\n\n'+msg)}`;
  toast('✓ Opening email client…');
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
  const hw=document.getElementById('hm-w');if(hw)hw.innerHTML=works.length+'<span>+</span>';
}

// ══ RENDER ALL ══
function renderAll(){renderWorks();renderPosts(activeTag);renderJourney(activeJType);renderCmts();renderSvcs();updateStats();renderCarousel();}

// ══ READER SYSTEM ══
function openPostReader(id,scrollToCmts=false){
  const p=posts.find(x=>x.id===id);if(!p)return;
  const tl={article:'t-article',link:'t-link',video:'t-video',doc:'t-doc',image:'t-image',tool:'t-tool'};
  const tn={article:'Article',link:'Link',video:'Video',doc:'Document',image:'Image',tool:'Tool'};
  const pp=localStorage.getItem('pp');
  const avatarStyle=pp?`style="background-image:url(${pp});background-size:cover;background-position:center;"`:'' ;
  const avatarText=pp?'':'NA';
  const rt=readTime(p.content);
  let cover='';
  if(p.imgData)cover=`<img class="reader-cover" src="${p.imgData}" alt="">`;
  else if(p.type==='tool')cover=`<div class="reader-cover-placeholder"><span style="position:relative;z-index:1;font-size:3.2rem;">${p.toolIcon||'⚙'}</span></div>`;
  else cover=`<div class="reader-cover-placeholder"><span style="position:relative;z-index:1;font-size:3.8rem;">${p.type==='video'?'▶':p.type==='link'?'🔗':p.type==='doc'?'📄':'📝'}</span></div>`;
  const paras=(p.content||'').split('\n').filter(Boolean);
  let bodyHtml=paras.map((par,i)=>`<p class="${i===0?'first-para':''}">${par}</p>`).join('');
  let mediaHtml='';
  if(p.type==='video'&&p.videoId)mediaHtml=`<iframe style="width:100%;aspect-ratio:16/9;border:none;border-radius:10px;margin:1.5rem 0;" src="https://www.youtube.com/embed/${p.videoId}" allowfullscreen></iframe>`;
  else if(p.type==='link'&&p.url)mediaHtml=`<a href="${p.url}" target="_blank" class="link-prev" style="margin:1.5rem 0;display:flex;"><div class="lp-icon">${p.linkIcon||'🌐'}</div><div><div class="lp-title">${p.linkTitle||p.url}</div><div class="lp-url">${p.url}</div></div></a>`;
  const cmtsHtml=`<div class="reader-cmts" id="readerCmtsSection"><div class="reader-cmts-title">Comments (${(p.comments||[]).length})</div>${(p.comments||[]).map(c=>`<div class="reader-cmt-item"><div class="reader-cmt-av">${(c.name||'V')[0]}</div><div class="reader-cmt-bubble"><div class="reader-cmt-name">${c.name||'Visitor'}<span class="reader-cmt-time">${c.time||''}</span></div><div class="reader-cmt-text">${c.text}</div></div></div>`).join('')}<div class="reader-cmt-input-row" style="padding:0 0 1rem;"><div class="reader-av" ${avatarStyle} style="width:32px;height:32px;font-size:.75rem;flex-shrink:0;">${avatarText}</div><input class="field" id="readerCmtIn" placeholder="Add a comment…" style="margin-bottom:0;font-size:.82rem;"><button class="btn btn-go btn-xs" onclick="submitReaderCmt('${p.id}')">Post</button></div></div>`;
  document.getElementById('readerNavTitle').textContent=p.title.substring(0,38)+(p.title.length>38?'…':'');
  document.getElementById('readerContent').innerHTML=`${cover}<div class="reader-body"><div class="reader-meta-row"><span class="pcard-badge ${tl[p.type]||''} reader-type-badge">${tn[p.type]||p.type}</span><span class="reader-date">${p.date||''}</span><span class="reader-read-time">⏱ ${rt} min read</span></div><h1 class="reader-title">${p.title}</h1><div class="reader-author-row"><div class="reader-av" ${avatarStyle}>${avatarText}</div><div><div class="reader-author-name">Nashat Omar Aldhoun</div><div class="reader-author-role">Aeronautical Engineer · JUST '25</div></div></div><div class="reader-content">${bodyHtml}${mediaHtml}</div>${p.tags?.length?`<div class="reader-tags">${p.tags.map(t=>`<span class="reader-tag">#${t}</span>`).join('')}</div>`:''}<div class="reader-divider"><span></span><span></span><span></span></div></div>${cmtsHtml}`;
  const toolLaunchBtn=p.type==='tool'&&p.toolUrl?`<a href="${p.toolUrl}" target="_blank" class="reader-share" style="text-decoration:none;margin-right:auto;">Launch Tool ↗</a>`:'';
  document.getElementById('readerActionBar').innerHTML=`${toolLaunchBtn}<button class="reader-act${p.liked?' liked':''}" onclick="readerLikePost('${p.id}')"><svg width="14" height="14" viewBox="0 0 24 24" fill="${p.liked?'currentColor':'none'}" stroke="currentColor" stroke-width="2"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>${p.likes||0} likes</button><button class="reader-act" onclick="document.getElementById('readerCmtsSection').scrollIntoView({behavior:'smooth'})"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>${(p.comments||[]).length} comments</button><button class="reader-share" onclick="copyReaderLink()">Share ↗</button>`;
  openReaderOv();
  if(scrollToCmts)setTimeout(()=>document.getElementById('readerCmtsSection')?.scrollIntoView({behavior:'smooth'}),400);
}

function openJourneyReader(id){
  const j=journey.find(x=>x.id===id);if(!j)return;
  const tb={milestone:'jt-milestone',course:'jt-course',event:'jt-event'};
  const tn={milestone:'Milestone',course:'Course',event:'Event'};
  const paras=(j.desc||'').split('\n').filter(Boolean);
  let bodyHtml=paras.map((par,i)=>`<p class="${i===0?'first-para':''}">${par}</p>`).join('')||`<p style="color:var(--mu);font-style:italic;">No description added yet.</p>`;
  document.getElementById('readerNavTitle').textContent=j.title.substring(0,38)+(j.title.length>38?'…':'');
  document.getElementById('readerContent').innerHTML=`${j.img?`<img class="reader-cover" src="${j.img}" alt="">`:`<div class="reader-cover-placeholder"><span style="position:relative;z-index:1;font-size:3.8rem;">${j.type==='milestone'?'🏆':j.type==='course'?'📚':'🎤'}</span></div>`}<div style="background:linear-gradient(135deg,#08162a,#0f2240);padding:2rem 3.5rem 1.5rem;position:relative;overflow:hidden;border-bottom:1px solid rgba(255,255,255,.06);"><div style="position:absolute;inset:0;background-image:linear-gradient(rgba(72,117,194,.07) 1px,transparent 1px),linear-gradient(90deg,rgba(72,117,194,.07) 1px,transparent 1px);background-size:20px 20px;pointer-events:none;"></div><span class="jtype-badge ${tb[j.type]||''}" style="position:relative;z-index:1;display:inline-flex;margin-bottom:.65rem;">${tn[j.type]||j.type}</span><h1 class="reader-title" style="font-size:clamp(1.4rem,3vw,2rem);margin-bottom:.3rem;position:relative;z-index:1;">${j.title}</h1>${j.org?`<div style="font-size:.88rem;color:var(--go);font-weight:500;position:relative;z-index:1;">${j.org}</div>`:''}${j.date?`<div style="font-size:.75rem;color:var(--mu);margin-top:.22rem;position:relative;z-index:1;">${j.date}</div>`:''}</div><div class="reader-body"><div class="reader-content">${bodyHtml}</div><div class="reader-divider"><span></span><span></span><span></span></div></div>`;
  document.getElementById('readerActionBar').innerHTML=`<button class="reader-act" onclick="closeReader()">← Back to Journey</button>${isAdmin?`<button class="btn-del" onclick="closeReader();delJourney('${j.id}')">🗑 Delete</button>`:''}<button class="reader-share" style="margin-left:auto;" onclick="copyReaderLink()">Share ↗</button>`;
  openReaderOv();
}

function openDiscReader(id,scrollToCmts=false){
  const c=comments.find(x=>x.id===id);if(!c)return;
  const isN=c.isAdminPost||c.name==='Nashat';
  const pp=localStorage.getItem('pp');
  const avStyle=isN&&pp?`style="background-image:url(${pp});background-size:cover;background-position:center;"`:'' ;
  const avText=isN&&pp?'':(isN?'NA':(c.name||'V')[0].toUpperCase());
  const rt=readTime(c.text);
  const paras=(c.text||'').split('\n').filter(Boolean);
  let bodyHtml=paras.map((par,i)=>`<p class="${i===0?'first-para':''}">${par}</p>`).join('');
  const repliesHtml=`<div class="reader-cmts" id="readerCmtsSection"><div class="reader-cmts-title">Replies (${(c.replies||[]).length})</div>${(c.replies||[]).map(r=>`<div class="reader-cmt-item"><div class="reader-cmt-av">${(r.name||'V')[0]}</div><div class="reader-cmt-bubble"><div class="reader-cmt-name">${r.name||'Visitor'}<span class="reader-cmt-time">${r.time||''}</span></div><div class="reader-cmt-text">${r.text}</div></div></div>`).join('')}<div class="reader-cmt-input-row" style="padding:0 0 1rem;"><input class="field" id="readerDiscNameIn" placeholder="Your name…" style="margin-bottom:0;font-size:.78rem;max-width:130px;"><input class="field" id="readerDiscIn" placeholder="Write a reply…" style="margin-bottom:0;font-size:.82rem;"><button class="btn btn-go btn-xs" onclick="submitDiscReaderReply('${c.id}')">Reply</button></div></div>`;
  document.getElementById('readerNavTitle').textContent=(c.title||c.text||'').substring(0,38);
  document.getElementById('readerContent').innerHTML=`<div style="background:linear-gradient(135deg,rgba(8,22,42,.95),rgba(15,34,64,.8));padding:2rem 3.5rem 1.5rem;border-bottom:1px solid rgba(255,255,255,.06);"><div style="font-size:.58rem;font-weight:700;letter-spacing:2.5px;text-transform:uppercase;color:var(--go);display:flex;align-items:center;gap:.4rem;margin-bottom:.5rem;"><span style="display:inline-block;width:14px;height:1px;background:var(--go);"></span>Discussion Topic</div><h1 class="reader-title" style="font-size:clamp(1.4rem,3vw,2.1rem);">${c.title||'Discussion'}</h1></div><div class="reader-body"><div class="reader-author-row"><div class="reader-av" ${avStyle}>${avText}</div><div><div class="reader-author-name" style="${isN?'color:var(--go)':''}">${isN?'Nashat Aldhoun':c.name||'Visitor'}${isN?'&nbsp;<span class="author-tag">AUTHOR</span>':''}</div><div class="reader-author-role" style="color:var(--mu)">${c.date||''} ${c.time?'· '+c.time:''}</div></div><span style="margin-left:auto;font-size:.7rem;color:var(--mu);">⏱ ${rt} min read</span></div><div class="reader-content">${bodyHtml}</div><div class="reader-divider"><span></span><span></span><span></span></div></div>${repliesHtml}`;
  document.getElementById('readerActionBar').innerHTML=`<button class="reader-act${c.liked?' liked':''}" onclick="readerLikeCmt('${c.id}')"><svg width="14" height="14" viewBox="0 0 24 24" fill="${c.liked?'currentColor':'none'}" stroke="currentColor" stroke-width="2"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>${c.likes||0} likes</button><button class="reader-act" onclick="document.getElementById('readerCmtsSection').scrollIntoView({behavior:'smooth'})"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>${(c.replies||[]).length} replies</button>${isAdmin?`<button class="btn-del" onclick="closeReader();delCmt('${c.id}')">🗑</button>`:''}<button class="reader-share" style="margin-left:auto;" onclick="copyReaderLink()">Share ↗</button>`;
  openReaderOv();
  if(scrollToCmts)setTimeout(()=>document.getElementById('readerCmtsSection')?.scrollIntoView({behavior:'smooth'}),400);
}

function openReaderOv(){
  const ov=document.getElementById('readerOv');ov.classList.add('open');ov.scrollTop=0;document.body.style.overflow='hidden';
  const modal=document.getElementById('readerModal');const bar=document.getElementById('readerProgress');
  ov.onscroll=()=>{const scrolled=ov.scrollTop;const total=modal.scrollHeight-ov.clientHeight;bar.style.width=(total>0?(scrolled/total*100):0)+'%';};
}
function closeReader(){document.getElementById('readerOv').classList.remove('open');document.body.style.overflow='';document.getElementById('readerProgress').style.width='0';}
function readerClickOut(e){if(e.target===document.getElementById('readerOv'))closeReader();}
function copyReaderLink(){navigator.clipboard.writeText(window.location.href).then(()=>toast('✓ Link copied!'));}
async function readerLikePost(id){const p=posts.find(x=>x.id===id);if(!p)return;p.liked=!p.liked;p.likes=(p.likes||0)+(p.liked?1:-1);try{await SB.update('posts',id,{likes:p.likes});}catch(e){}openPostReader(id);}
async function readerLikeCmt(id){const c=comments.find(x=>x.id===id);if(!c)return;c.liked=!c.liked;c.likes=(c.likes||0)+(c.liked?1:-1);try{await SB.update('comments',id,{likes:c.likes});}catch(e){}openDiscReader(id);}
async function submitReaderCmt(postId){
  const input=document.getElementById('readerCmtIn');const text=(input?.value||'').trim();if(!text)return;
  const name=prompt('Your name (optional):','')||'Visitor';
  const p=posts.find(x=>x.id===postId);if(!p)return;
  if(!p.comments)p.comments=[];
  p.comments.push({name,text,time:new Date().toLocaleTimeString('en',{hour:'2-digit',minute:'2-digit'})});
  try{await SB.update('posts',postId,{comments:p.comments});toast('✓ Comment added!');openPostReader(postId,true);}
  catch(e){toast('⚠ '+e.message);}
}
async function submitDiscReaderReply(cmtId){
  const nameIn=document.getElementById('readerDiscNameIn');const textIn=document.getElementById('readerDiscIn');
  const text=(textIn?.value||'').trim();if(!text)return;
  const name=(nameIn?.value||'').trim()||'Visitor';
  const c=comments.find(x=>x.id===cmtId);if(!c)return;
  if(!c.replies)c.replies=[];
  c.replies.push({name,text,time:new Date().toLocaleTimeString('en',{hour:'2-digit',minute:'2-digit'})});
  try{await SB.update('comments',cmtId,{replies:c.replies});toast('✓ Reply added!');openDiscReader(cmtId,true);}
  catch(e){toast('⚠ '+e.message);}
}
document.addEventListener('keydown',e=>{if(e.key==='Escape')closeReader();});

// ══ RADAR ══
function drawRadar(){
  const svg=document.getElementById('radarSvg');if(!svg)return;svg.innerHTML='';
  const skills=[{label:'ANSYS / FEA',val:85},{label:'Creo / 3D',val:80},{label:'SolidWorks',val:72},{label:'MATLAB',val:65},{label:'CFD Sim.',val:78},{label:'Aircraft MRO',val:88},{label:'Power BI',val:70},{label:'Structures',val:90}];
  const N=skills.length,cx=140,cy=130,R=95,levels=5;
  for(let l=1;l<=levels;l++){const r=(R/levels)*l;const pts=skills.map((_,i)=>{const a=(Math.PI*2/N)*i-Math.PI/2;return`${cx+r*Math.cos(a)},${cy+r*Math.sin(a)}`;}).join(' ');const poly=document.createElementNS('http://www.w3.org/2000/svg','polygon');poly.setAttribute('points',pts);poly.setAttribute('class','radar-grid');svg.appendChild(poly);}
  skills.forEach((_,i)=>{const a=(Math.PI*2/N)*i-Math.PI/2;const line=document.createElementNS('http://www.w3.org/2000/svg','line');line.setAttribute('x1',cx);line.setAttribute('y1',cy);line.setAttribute('x2',cx+R*Math.cos(a));line.setAttribute('y2',cy+R*Math.sin(a));line.setAttribute('class','radar-axis');svg.appendChild(line);});
  const pts=skills.map((s,i)=>{const a=(Math.PI*2/N)*i-Math.PI/2;const r=R*(s.val/100);return`${cx+r*Math.cos(a)},${cy+r*Math.sin(a)}`;}).join(' ');
  const poly=document.createElementNS('http://www.w3.org/2000/svg','polygon');poly.setAttribute('points',pts);poly.setAttribute('class','radar-polygon');svg.appendChild(poly);
  const tip=document.getElementById('radarTip');const wrap=document.getElementById('radarWrap');
  skills.forEach((s,i)=>{
    const a=(Math.PI*2/N)*i-Math.PI/2;const r=R*(s.val/100);
    const dx=cx+r*Math.cos(a),dy=cy+r*Math.sin(a);const lx=cx+(R+22)*Math.cos(a),ly=cy+(R+22)*Math.sin(a);
    const circle=document.createElementNS('http://www.w3.org/2000/svg','circle');circle.setAttribute('cx',dx);circle.setAttribute('cy',dy);circle.setAttribute('r','4');circle.setAttribute('class','radar-dot');
    circle.onmouseenter=(e)=>{if(!tip||!wrap)return;const wr=wrap.getBoundingClientRect();const er=e.target.getBoundingClientRect();tip.textContent=s.label+' — '+s.val+'%';tip.style.opacity='1';tip.style.left=(er.left-wr.left+8)+'px';tip.style.top=(er.top-wr.top-28)+'px';};
    circle.onmouseleave=()=>{if(tip)tip.style.opacity='0';};
    svg.appendChild(circle);
    const text=document.createElementNS('http://www.w3.org/2000/svg','text');text.setAttribute('x',lx);text.setAttribute('y',ly+4);text.setAttribute('text-anchor',Math.cos(a)>0.1?'start':Math.cos(a)<-0.1?'end':'middle');text.setAttribute('class','radar-label');text.textContent=s.label;svg.appendChild(text);
  });
}

// ══ STATS COUNTER ══
function animateCounters(){
  document.querySelectorAll('.stat-num[data-target]').forEach(el=>{
    const target=parseInt(el.dataset.target);let current=0;
    const step=Math.max(1,Math.ceil(target/25));
    const interval=setInterval(()=>{current=Math.min(current+step,target);el.textContent=current;if(current>=target)clearInterval(interval);},55);
  });
}
let countersRan=false;
const _counterObs=new IntersectionObserver(entries=>{entries.forEach(e=>{if(e.isIntersecting&&!countersRan){countersRan=true;animateCounters();}});},{threshold:0.5});
const _statsRow=document.getElementById('statsRow');if(_statsRow)_counterObs.observe(_statsRow);
const _radarObs=new IntersectionObserver(entries=>{entries.forEach(e=>{if(e.isIntersecting){drawRadar();_radarObs.disconnect();}});},{threshold:0.1});
const _radarEl=document.getElementById('radarWrap');if(_radarEl)_radarObs.observe(_radarEl);

// ══ INIT ══
loadLocalData();
renderAll();
setupEmails();
initApp();
startCarouselAuto();
loadProfilePhoto();
setTimeout(()=>{trigRev();observeCards();},200);
</script>
</body>
</html>
