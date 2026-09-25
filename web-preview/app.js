const state={
  screen:new URLSearchParams(location.search).get("screen")||localStorage.getItem("sp_screen")||"home",
  language:localStorage.getItem("sp_language")||"de",
  audience:localStorage.getItem("sp_audience")||"male",
  prayerStep:Number(localStorage.getItem("sp_prayer_step")||0),
  wuduStep:Number(localStorage.getItem("sp_wudu_step")||0),
  heading:0
};

const prayerSteps=[
 ["intention","Absicht"],["takbir","Takbīr"],["standing","Qiyām"],["bowing","Rukūʿ"],["upright","Aufrichten"],["sujud","Sujūd"],["sitting","Sitzen"],["second_sujud","2. Sujūd"],["standing","2. Rakʿah"],["bowing","2. Rukūʿ"],["upright","Aufrichten"],["sujud","2. Sujūd"],["second_sujud","2. Sujūd"],["final_sitting","Taschahhud"],["finger","Finger"],["salam_right","Salam rechts"],["salam_left","Salam links"]
];

const wuduSteps=[
 ["intention","Absicht"],["basmala","Basmala"],["hands","Hände"],["mouth","Mund"],["nose","Nase"],["face","Gesicht"],["rightarm","Rechter Arm"],["leftarm","Linker Arm"],["head","Kopf"],["ears","Ohren"],["neck","Nacken"],["rightfoot","Rechter Fuß"],["leftfoot","Linker Fuß"]
];

const prayerRows=[
 ["fajr","Fajr","05:31"],["sunrise","Sonnenaufgang","07:18"],["dhuhr","Dhuhr","13:24"],["asr","Asr","16:47"],["maghrib","Maghrib","19:29"],["isha","Isha","21:04"]
];

function t(de,tr){return state.language==="de"?de:tr}
function save(){
 localStorage.setItem("sp_screen",state.screen);
 localStorage.setItem("sp_language",state.language);
 localStorage.setItem("sp_audience",state.audience);
 localStorage.setItem("sp_prayer_step",state.prayerStep);
 localStorage.setItem("sp_wudu_step",state.wuduStep);
}
function asset(name){return "/public/assets/"+name}
function image(name,klass=""){
 const options=["svg","png","jpg","jpeg","webp"];
 const src=asset(name+"."+options[0]);
 const fallbacks=options.slice(1).map(ext=>asset(name+"."+ext));
 return `<img class="${klass}" src="${src}" data-fallbacks='${JSON.stringify(fallbacks)}' alt="">`;
}
function activateFallbacks(){
 document.querySelectorAll("img[data-fallbacks]").forEach(img=>{
   img.onerror=()=>{
     const list=JSON.parse(img.dataset.fallbacks||"[]");
     if(!list.length){img.style.visibility="hidden";return}
     img.src=list.shift();img.dataset.fallbacks=JSON.stringify(list);
   };
 });
}
function setScreen(screen){
 state.screen=screen;save();
 const u=new URL(location.href);u.searchParams.set("screen",screen);history.replaceState({},"",u);render();
}
window.setScreen=setScreen;

function nativeHeader(){
 const icon="feature_maghrib";
 return `<div class="native-header">
   ${image(icon,"phase-icon")}
   <div><div class="brand-title">SalahPath</div><div class="brand-sub">${t("Ein schöneres Leben mit Gebet","İbadetle Daha Güzel Bir Hayat")}</div></div>
   <div><div class="quote">„${t("Das Gebet ist den Gläubigen zu bestimmten Zeiten vorgeschrieben.","Namaz, müminlere vakitleri belli bir farzdır.")}“</div>
   <div class="quote-ref"><span>(An-Nisāʾ 4:103)</span>${image("feature_reminder")}</div></div>
 </div>`;
}
function nextPrayer(){
 return `<section class="card next-card">
   ${image("home_mosque","mosque")}
   <div class="next-head"><b>${t("Nächstes Gebet","Sıradaki Namaz")}</b><div class="date-stack"><b>25.09.2026</b><span>${t("Freitag","Cuma")}</span></div></div>
   <div class="next-main">${image("feature_maghrib")}<div><div class="prayer-name">Maghrib</div><div class="countdown">00:37:18</div></div></div>
   <div class="location-line">${image("feature_location")}<span>Mönchengladbach</span></div>
   <div class="sequence">${image("feature_maghrib")}<span class="num">3</span><span>Fard</span><span class="arrow">→</span><span class="num">2</span><span>Sunnah</span><span style="margin-left:auto">›</span></div>
   <div class="ayah-note">„${t("Das Gebet ist den Gläubigen zu bestimmten Zeiten vorgeschrieben.","Namaz, müminlere vakitleri belirlenmiş bir farzdır.")}“</div>
 </section>`;
}
function timesCard(){
 return `<section class="card times-card"><div class="section-head"><b>${t("Heutige Gebetszeiten","Bugün Namaz Vakitleri")}</b><span>${t("Details","Detaylar")}</span></div>
 ${prayerRows.map(([kind,label,time])=>`<div class="prayer-row ${kind==="maghrib"?"active":""}">${image("feature_"+kind)}<span class="label">${label}</span><span class="state">${kind==="maghrib"?t("Nächstes","Sıradaki"):""}</span><span class="time">${time}</span></div>`).join("")}
 </section>`;
}
function quickActions(){
 const items=[["times",t("Zeiten","Vakitler"),t("Heute","Bugün"),"settings"],["checkmark",t("Tracker","Takip"),t("Fortschritt","İlerleme"),"tracker"],["quran",t("Koran","Kur'an"),t("Lesen","Oku"),"quran"]];
 return `<div class="quick-grid">${items.map(([i,a,b,s])=>`<button class="quick-pill" onclick="setScreen('${s}')"><span class="icon-circle">${image("feature_"+i)}</span><b>${a}</b><span>${b}</span></button>`).join("")}</div>`;
}
function dailyDua(){
 return `<section class="card dua-card"><button class="dua-audio">◖))</button><div class="dua-top"><span class="leaf">❧</span><div><b>${t("Dua des Tages","Günün Duası")}</b><span>${t("Bitte um Rechtleitung","Hidayet duası")}</span></div></div>
 <div class="dua-ar">رَبِّ زِدْنِي عِلْمًا</div><div class="dua-meaning">${t("Mein Herr, mehre mich an Wissen.","Rabbim, ilmimi artır.")}</div><div class="dua-source">Quran 20:114</div></section>`;
}
function tracker(){
 const days=state.language==="de"?["Mo","Di","Mi","Do","Fr","Sa","So"]:["Pzt","Sal","Çar","Prş","Cum","Cts","Paz"];
 return `<button class="card tracker-card" style="width:100%;border-style:solid" onclick="setScreen('tracker')"><div><div class="tracker-title"><span class="check-dot">✓</span>${t("Gebets-Tracking","Namaz Takibi")}</div><div class="week">${days.map((d,i)=>`<div class="week-day ${i<4?"done":""}"><span>${d}</span><i>${i<4?"✓":i===4?"2":"·"}</i></div>`).join("")}</div></div><div class="tracker-sep"></div><div class="streak"><b>12</b><span>${t("Tage Serie","gün seri")}</span></div></button>`;
}
function dashboard(){
 const data=[
 ["quran",t("Quran","Kur'an"),t("Lesen & hören","Oku & Dinle"),"quran"],
 ["quran_audio",t("Quran-Audio","Kur'an Sesi"),t("Anhören","Dinle"),"quran"],
 ["fav",t("Juz & Favoriten","Cüz & Favoriler"),t("Lesezeichen","İşaretler"),"quran"],
 ["times",t("Gebetszeiten","Namaz Vakitleri"),t("Zeiten","Vakitler"),"settings"],
 ["prayer",t("Gebet\nlernen","Namaz\nÖğren"),t("Schritt für Schritt","Adım adım"),"prayer"],
 ["wudu",t("Wudu\nAnleitung","Abdest\nRehberi"),t("Grundlagen","Temel"),"wudu"],
 ["islamic_calendar",t("Islamischer\nKalender","İslami Takvim"),t("Ereignisse","Olaylar"),"more"],
 ["dhikr",t("Dua & Dhikr","Dua & Zikir"),t("Täglich","Günlük"),"more"],
 ["qibla",t("Qibla-Richtung","Kıble Yönü"),"Qibla","qibla"],
 ["islamic_knowledge",t("Islamwissen","İslami Bilgiler"),t("Wissen","Bilgi"),"more"],
 ["checkmark",t("Gebets-Tracker","Namaz Takibi"),t("Fortschritt","İlerleme"),"tracker"],
 ["settings",t("Einstellungen","Ayarlar"),t("Einstellungen","Ayarlar"),"settings"]
 ];
 return `<div class="dashboard">${data.map(([i,a,b,s])=>`<button class="dash-tile" onclick="setScreen('${s}')">${image("feature_"+i)}<b>${a}</b><span>${b}</span></button>`).join("")}</div>`;
}
function home(){
 return `<div class="home-root"><div class="home-stack">${nativeHeader()}${nextPrayer()}${timesCard()}${quickActions()}${dailyDua()}${tracker()}${dashboard()}<section class="card quote-strip"><span class="leaf">❧</span><div><b>„${t("Kleine Schritte führen zu großen Veränderungen.","Küçük adımlar, büyük değişimler getirir.")}“</b><span>${t("Kleine Schritte bringen große Veränderungen.","Küçük adımlar büyük değişim getirir.")}</span></div></section></div></div>`;
}
function navbar(title){return `<div class="navbar"><strong>${title}</strong></div>`}
function row(icon,title,sub,screen){
 return `<button class="list-row" onclick="${screen?`setScreen('${screen}')`:""}">${image("feature_"+icon)}<div class="grow"><b>${title}</b><span>${sub}</span></div><b>›</b></button>`;
}
function quran(){
 return `<div class="nav-page">${navbar(t("Koran","Kur'an"))}<div class="page-pad"><div class="list-card">${row("quran","1 · Al-Fātiḥa","7 Ayat","reader")}${row("quran","2 · Al-Baqara","286 Ayat","reader")}${row("fav",t("Favoriten","Favoriler"),t("Gespeicherte Stellen","Kaydedilen ayetler"))}${row("list","Juz","1–30")}</div></div></div>`;
}
function reader(){
 return `<div class="nav-page">${navbar("Al-Fātiḥa")}<div class="page-pad"><div class="reader"><div style="font-size:9px;color:var(--muted);font-weight:800;margin-bottom:12px">${t("Seite 1","Sayfa 1")}</div><div class="arabic">بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ<br>الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ<br>الرَّحْمَٰنِ الرَّحِيمِ<br>مَالِكِ يَوْمِ الدِّينِ<br>إِيَّاكَ نَعْبُدُ وَإِيَّاكَ نَسْتَعِينُ<br>اهْدِنَا الصِّرَاطَ الْمُسْتَقِيمَ</div></div></div></div>`;
}
function prayer(){
 const [pose,label]=prayerSteps[state.prayerStep];
 return `<div class="nav-page">${navbar(t("Gebet lernen","Namaz Öğren"))}<div class="page-pad"><div class="step-strip">${prayerSteps.map((s,i)=>`<button class="${i===state.prayerStep?"active":""}" data-prayer="${i}">${i+1}. ${s[1]}</button>`).join("")}</div><div class="stage">${image(state.audience+"_"+pose)}</div><div class="card" style="padding:8px 10px;font-size:10px"><b>${label}</b><br><span style="color:var(--muted)">${t("2. Rakʿah vollständig · Salam rechts → links","2. rekât tam · Selam sağ → sol")}</span></div></div></div>`;
}
function wudu(){
 const [pose,label]=wuduSteps[state.wuduStep];
 return `<div class="nav-page">${navbar(t("Abdest","Abdest"))}<div class="page-pad"><div class="step-strip">${wuduSteps.map((s,i)=>`<button class="${i===state.wuduStep?"active":""}" data-wudu="${i}">${i+1}. ${s[1]}</button>`).join("")}</div><div class="stage">${image("wudu_"+pose)}</div><div class="card" style="padding:8px 10px;font-size:10px"><b>${label}</b><br><span style="color:var(--muted)">${t("Rechter Arm vor linkem Arm · rechter Fuß vor linkem Fuß","Sağ kol soldan önce · sağ ayak soldan önce")}</span></div></div></div>`;
}
function qibla(){
 return `<div class="nav-page">${navbar(t("Qibla","Kıble"))}<div class="page-pad"><div class="card" style="padding:10px;text-align:center"><b>${t("Qibla-Richtung","Kıble Yönü")}</b><div style="font-size:9px;color:var(--muted);margin-top:2px">Mönchengladbach</div><div class="compass"><div class="north">N</div><div class="arrow" style="transform:translate(-50%,-100%) rotate(${state.heading}deg)"></div><div class="kaaba"></div></div><input id="heading" type="range" min="-180" max="180" value="${state.heading}" style="width:90%"></div></div></div>`;
}
function trackerPage(){
 const names=["Fajr","Dhuhr","Asr","Maghrib","Isha"];
 return `<div class="nav-page">${navbar(t("Gebets-Tracking","Namaz Takibi"))}<div class="page-pad"><div class="list-card">${names.map((n,i)=>`<label class="list-row"><span class="check-dot" style="background:${i<2?"var(--teal)":"var(--soft)"};color:${i<2?"#fff":"var(--muted)"}">${i<2?"✓":"○"}</span><div class="grow"><b>${n}</b><span>${i<2?t("markiert","tamamlandı"):t("offen","açık")}</span></div></label>`).join("")}</div></div></div>`;
}
function more(){
 return `<div class="nav-page">${navbar(t("Entdecken","Keşfet"))}<div class="page-pad"><div class="list-card">${row("prayer",t("Gebet lernen","Namaz Öğren"),t("Schritt für Schritt","Adım adım"),"prayer")}${row("wudu","Wudu",t("Schritt für Schritt","Adım adım"),"wudu")}${row("quran",t("Quran-Verzeichnis","Kur'an Dizini"),t("Suren · Seiten · Juz","Sûre · sayfa · cüz"),"quran")}${row("dhikr",t("Dua & Dhikr","Dua & Zikir"),t("Morgen & Abend","Sabah & Akşam"))}${row("qibla",t("Qibla","Kıble"),t("Richtung zur Kaaba","Kâbe yönü"),"qibla")}</div></div></div>`;
}
function settings(){
 return `<div class="nav-page">${navbar(t("Profil","Profil"))}<div class="page-pad"><div class="list-card">${row("profile",t("Gebetsdarstellung","Namaz görünümü"),state.audience==="male"?t("Mann","Erkek"):t("Frau","Kadın"))}${row("location",t("Standort","Konum"),"Mönchengladbach")}${row("reminder",t("Benachrichtigungen","Bildirimler"),t("Adhan & Erinnerungen","Ezan & hatırlatıcılar"))}${row("language",t("Sprache","Dil"),state.language==="de"?"Deutsch":"Türkçe")}${row("settings",t("Darstellung","Görünüm"),t("System","Sistem"))}</div></div></div>`;
}
function screen(){
 switch(state.screen){
  case"quran":return quran();case"reader":return reader();case"prayer":return prayer();case"wudu":return wudu();case"qibla":return qibla();case"tracker":return trackerPage();case"more":return more();case"settings":return settings();default:return home();
 }
}
function tabs(){
 const items=[
  ["home","home_active","home_inactive",t("Start","Ana Sayfa")],
  ["quran","quran_active","quran_inactive",t("Koran","Kur'an")],
  ["prayer","prayer_active","prayer_inactive",t("Gebet","Namaz")],
  ["more","discover","discover",t("Entdecken","Keşfet")],
  ["settings","profile","profile",t("Profil","Profil")]
 ];
 return `<nav class="tabs">${items.map(([key,on,off,label])=>`<button class="tab ${state.screen===key?"active":""}" data-screen="${key}"><span class="tab-icon">${image("feature_"+(state.screen===key?on:off))}</span><span>${label}</span><i class="dot"></i></button>`).join("")}</nav>`;
}
function render(){
 document.querySelector("#app").innerHTML=`<div class="preview-shell"><section class="phone"><div class="status"><span>9:41</span><span>●●● Wi-Fi 100%</span></div><div class="app-shell"><div class="screen">${screen()}</div>${tabs()}</div></section><aside class="reference-bar"><span class="ref-chip">IPA reference · v3.62 B78</span><h1>SalahPath Browser QA</h1><p>Aufbau und Inhalte orientieren sich am heutigen echten IPA-Stand statt an der alten Demo.</p><div class="control"><label>Screen</label><select id="screenSelect">${[["home","Start"],["quran","Koran"],["reader","Reader"],["prayer","Gebet"],["wudu","Abdest"],["qibla","Qibla"],["tracker","Tracker"],["more","Entdecken"],["settings","Profil"]].map(([v,l])=>`<option value="${v}" ${state.screen===v?"selected":""}>${l}</option>`).join("")}</select></div><div class="control"><label>Sprache</label><select id="language"><option value="de" ${state.language==="de"?"selected":""}>Deutsch</option><option value="tr" ${state.language==="tr"?"selected":""}>Türkçe</option></select></div><div class="control"><label>Gebetsdarstellung</label><select id="audience"><option value="male" ${state.audience==="male"?"selected":""}>Mann</option><option value="female" ${state.audience==="female"?"selected":""}>Frau</option></select></div><div class="control"><button id="reset">Zurücksetzen</button></div></aside></div>`;
 activateFallbacks();
 document.querySelectorAll("[data-screen]").forEach(el=>el.addEventListener("click",()=>setScreen(el.dataset.screen)));
 document.querySelector("#screenSelect").addEventListener("change",e=>setScreen(e.target.value));
 document.querySelector("#language").addEventListener("change",e=>{state.language=e.target.value;save();render()});
 document.querySelector("#audience").addEventListener("change",e=>{state.audience=e.target.value;save();render()});
 document.querySelector("#reset").addEventListener("click",()=>{localStorage.clear();location.href="/"});
 document.querySelectorAll("[data-prayer]").forEach(el=>el.addEventListener("click",()=>{state.prayerStep=Number(el.dataset.prayer);save();render()}));
 document.querySelectorAll("[data-wudu]").forEach(el=>el.addEventListener("click",()=>{state.wuduStep=Number(el.dataset.wudu);save();render()}));
 const h=document.querySelector("#heading");if(h)h.addEventListener("input",e=>{state.heading=Number(e.target.value);render()});
}
render();
