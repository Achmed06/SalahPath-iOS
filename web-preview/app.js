const state = {
  screen: new URLSearchParams(location.search).get("screen") || localStorage.getItem("sp_screen") || "home",
  language: localStorage.getItem("sp_language") || "de",
  audience: localStorage.getItem("sp_audience") || "male",
  prayerStep: Number(localStorage.getItem("sp_prayer_step") || 0),
  wuduStep: Number(localStorage.getItem("sp_wudu_step") || 0),
  heading: 0
};

const prayerSteps = [
  ["intention","Absicht"], ["takbir","Takbīr"], ["standing","Stehen"], ["bowing","Rukūʿ"],
  ["upright","Aufrichten"], ["sujud","Sujūd"], ["sitting","Sitzen"], ["second_sujud","2. Sujūd"],
  ["standing","2. Rakʿah"], ["bowing","2. Rukūʿ"], ["sujud","2. Sujūd"], ["final_sitting","Taschahhud"],
  ["finger","Finger"], ["salam_right","Salam rechts"], ["salam_left","Salam links"]
];

const wuduSteps = [
  ["intention","Absicht"], ["basmala","Basmala"], ["hands","Hände"], ["mouth","Mund"], ["nose","Nase"],
  ["face","Gesicht"], ["rightarm","Rechter Arm"], ["leftarm","Linker Arm"], ["head","Kopf"],
  ["ears","Ohren"], ["neck","Nacken"], ["rightfoot","Rechter Fuß"], ["leftfoot","Linker Fuß"]
];

function t(de, tr) { return state.language === "de" ? de : tr; }
function save() {
  localStorage.setItem("sp_screen", state.screen);
  localStorage.setItem("sp_language", state.language);
  localStorage.setItem("sp_audience", state.audience);
  localStorage.setItem("sp_prayer_step", state.prayerStep);
  localStorage.setItem("sp_wudu_step", state.wuduStep);
}
function asset(name, ext="svg") { return `/public/assets/${name}.${ext}`; }
function img(name, cls="") { return `<img class="${cls}" src="${asset(name)}" onerror="this.style.visibility='hidden'" alt="">`; }

function setScreen(screen) {
  state.screen = screen;
  save();
  const url = new URL(location.href);
  url.searchParams.set("screen", screen);
  history.replaceState({}, "", url);
  render();
}
window.setScreen = setScreen;

function header(title) {
  const phase = state.screen === "home" ? "maghrib" : "discover";
  return `<div class="navbar">
    <div class="brand-state">${img("feature_"+phase)}<span>${state.screen === "home" ? t("Tagesphase","Gün durumu") : "SalahPath"}</span></div>
    <strong>${title}</strong>
  </div>`;
}

function tile(icon, title, sub, screen) {
  return `<button class="tile" onclick="${screen ? `setScreen('${screen}')` : ""}">
    ${img("feature_"+icon)}<b>${title}</b><span>${sub}</span>
  </button>`;
}

function row(icon, title, sub, screen) {
  return `<button class="row" onclick="${screen ? `setScreen('${screen}')` : ""}">
    ${img("feature_"+icon)}<div class="grow"><b>${title}</b><span>${sub}</span></div><b>›</b>
  </button>`;
}

function home() {
  return `${header(t("Start","Ana Sayfa"))}<div class="content">
    <div class="hero"><span class="badge">${t("Freitag · Mönchengladbach","Cuma · Mönchengladbach")}</span>
      <h3>${t("Assalamu alaikum","Esselamu aleyküm")}</h3>
      <p>${t("Nächstes Gebet: Maghrib","Sonraki namaz: Akşam")}</p>
      <div class="prayer-strip">
        <div class="prayer-card">${img("feature_fajr")}<b>Fajr</b><span>05:31</span></div>
        <div class="prayer-card">${img("feature_dhuhr")}<b>Dhuhr</b><span>13:24</span></div>
        <div class="prayer-card">${img("feature_maghrib")}<b>Maghrib</b><span>19:29</span></div>
      </div>
    </div>
    <div class="section-title">${t("Schnellzugriff","Hızlı erişim")}</div>
    <div class="grid">
      ${tile("quran",t("Koran","Kur'an"),t("Lesen & hören","Oku ve dinle"),"quran")}
      ${tile("prayer",t("Gebet lernen","Namaz öğren"),t("Schritt für Schritt","Adım adım"),"prayer")}
      ${tile("wudu",t("Abdest","Abdest"),t("13 Schritte","13 adım"),"wudu")}
      ${tile("qibla",t("Qibla","Kıble"),t("Richtung zur Kaaba","Kâbe yönü"),"qibla")}
      ${tile("checkmark",t("Gebetstracker","Namaz takip"),t("Heute erfassen","Bugünü kaydet"),"tracker")}
      ${tile("discover",t("Entdecken","Keşfet"),t("Mehr Inhalte","Daha fazla"),"more")}
    </div>
  </div>`;
}

function quran() {
  return `${header(t("Koran","Kur'an"))}<div class="content">
    <div class="hero"><h3>${t("Koran","Kur'an-ı Kerim")}</h3><p>${t("Offline-Inhalt · Reader-Vorschau","Çevrimdışı içerik · Okuyucu önizleme")}</p></div>
    <div class="section-title">${t("Suren","Sureler")}</div>
    <div class="list">
      ${row("quran","1 · Al-Fātiḥa","7 Ayat","reader")}
      ${row("quran","2 · Al-Baqara","286 Ayat","reader")}
      ${row("bookmarks",t("Favoriten","Favoriler"),t("Gespeicherte Stellen","Kaydedilen ayetler"))}
      ${row("list","Juz","1–30")}
    </div>
  </div>`;
}

function reader() {
  return `${header("Al-Fātiḥa")}<div class="content">
    <div class="quran-page">
      <span class="badge">${t("Seite 1","Sayfa 1")}</span>
      <div class="arabic">بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ<br>الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ<br>الرَّحْمَٰنِ الرَّحِيمِ<br>مَالِكِ يَوْمِ الدِّينِ<br>إِيَّاكَ نَعْبُدُ وَإِيَّاكَ نَسْتَعِينُ<br>اهْدِنَا الصِّرَاطَ الْمُسْتَقِيمَ</div>
      <div class="note">${t("Browser-Vorschau: Seiten 1 / 302 / 604 werden in der nativen QA zusätzlich geprüft.","Tarayıcı önizlemesi: 1 / 302 / 604. sayfalar native QA'da ayrıca kontrol edilir.")}</div>
    </div>
  </div>`;
}

function prayer() {
  const [pose,label] = prayerSteps[state.prayerStep];
  const name = `${state.audience}_${pose}`;
  return `${header(t("Gebet lernen","Namaz Öğren"))}<div class="content">
    <div class="hero"><span class="badge">${state.audience === "male" ? t("Mann","Erkek") : t("Frau","Kadın")}</span><h3>${label}</h3><p>${t("Scroll-/Sequenz-Vorschau","Akış / sıra önizlemesi")}</p></div>
    <div class="steps">${prayerSteps.map((s,i)=>`<button class="step ${i===state.prayerStep?"active":""}" data-prayer="${i}">${i+1}. ${s[1]}</button>`).join("")}</div>
    <div class="person-stage">${img(name)}</div>
    <div class="note"><span class="ok">✓</span> ${t("2. Rakʿah vollständig · Salam rechts → links","2. rekât tam · Selam sağ → sol")}</div>
  </div>`;
}

function wudu() {
  const [pose,label] = wuduSteps[state.wuduStep];
  return `${header(t("Abdest","Abdest"))}<div class="content">
    <div class="hero"><span class="badge">${state.wuduStep+1} / 13</span><h3>${label}</h3><p>${t("Rechts/links aus Sicht der betenden Person","Sağ/sol kişinin kendi açısından")}</p></div>
    <div class="steps">${wuduSteps.map((s,i)=>`<button class="step ${i===state.wuduStep?"active":""}" data-wudu="${i}">${i+1}. ${s[1]}</button>`).join("")}</div>
    <div class="person-stage">${img("wudu_"+pose)}</div>
    <div class="note"><span class="ok">✓</span> ${t("Rechter Arm vor linkem Arm · rechter Fuß vor linkem Fuß","Sağ kol soldan önce · sağ ayak soldan önce")}</div>
  </div>`;
}

function qibla() {
  return `${header(t("Qibla","Kıble"))}<div class="content">
    <div class="hero"><h3>${t("Qibla-Richtung","Kıble Yönü")}</h3><p>Mönchengladbach · QA</p></div>
    <div class="compass"><div class="north">N</div><div class="arrow" style="transform:translate(-50%,-100%) rotate(${state.heading}deg)"></div><div class="kaaba"></div></div>
    <div class="control"><label>${t("Simulierter Geräte-Heading","Simüle cihaz yönü")}: ${state.heading}°</label><input id="heading" type="range" min="-180" max="180" value="${state.heading}"></div>
    <div class="note">${t("Pfeilspitze und Kaaba müssen dieselbe physische Zielrichtung zeigen. Echter Magnetometer-Test erst am Ende auf dem iPhone.","Ok ucu ve Kâbe aynı fiziksel hedef yönünü göstermeli. Gerçek pusula testi en sonda iPhone'da.")}</div>
  </div>`;
}

function tracker() {
  return `${header(t("Gebetstracker","Namaz Takibi"))}<div class="content">
    <div class="hero"><h3>${t("Heute","Bugün")}</h3><p>${t("Fünf Pflichtgebete","Beş farz namaz")}</p></div>
    <div class="list">${["Fajr","Dhuhr","Asr","Maghrib","Isha"].map((p,i)=>`<label class="row"><input type="checkbox" ${i<2?"checked":""}><div class="grow"><b>${p}</b><span>${i<2?t("Erledigt","Tamamlandı"):t("Offen","Açık")}</span></div></label>`).join("")}</div>
  </div>`;
}

function more() {
  return `${header(t("Entdecken","Keşfet"))}<div class="content">
    <div class="hero"><h3>${t("Entdecken","Keşfet")}</h3><p>${t("Inhalte im einheitlichen SalahPath-Stil","Birleşik SalahPath tasarımı")}</p></div>
    <div class="list" style="margin-top:12px">
      ${row("dhikr",t("Dhikr & Duas","Zikir & Dualar"),t("Morgen, Abend, Alltag","Sabah, akşam, günlük"))}
      ${row("calendar",t("Islamischer Kalender","Hicri Takvim"),t("Termine und Tage","Tarihler ve günler"))}
      ${row("community",t("Gemeinschaft","Topluluk"),t("Lokale Inhalte","Yerel içerikler"))}
      ${row("info",t("Islam lernen","İslam öğren"),t("Grundlagen","Temel bilgiler"))}
    </div>
  </div>`;
}

function settings() {
  return `${header(t("Profil & Einstellungen","Profil & Ayarlar"))}<div class="content">
    <div class="list">
      ${row("profile",t("Profil","Profil"),state.audience === "male" ? t("Mann","Erkek") : t("Frau","Kadın"))}
      ${row("location",t("Standort","Konum"),"Mönchengladbach")}
      ${row("notifications",t("Gebetsbenachrichtigungen","Namaz bildirimleri"),t("Adhan & Erinnerungen","Ezan & hatırlatıcılar"))}
      ${row("language",t("Sprache","Dil"),state.language === "de" ? "Deutsch" : "Türkçe")}
      ${row("settings",t("Darstellung","Görünüm"),t("System","Sistem"))}
    </div>
  </div>`;
}

function screen() {
  switch(state.screen) {
    case "quran": return quran();
    case "reader": return reader();
    case "prayer": return prayer();
    case "wudu": return wudu();
    case "qibla": return qibla();
    case "tracker": return tracker();
    case "more": return more();
    case "settings": return settings();
    default: return home();
  }
}

function tabs() {
  const items = [
    ["home",t("Start","Ana Sayfa")],
    ["quran",t("Koran","Kur'an")],
    ["prayer",t("Gebet","Namaz")],
    ["more",t("Entdecken","Keşfet")],
    ["settings",t("Profil","Profil")]
  ];
  return `<nav class="tabs">${items.map(([key,label])=>`<button class="tab ${state.screen===key?"active":""}" data-screen="${key}">${img("feature_"+(key==="settings"?"profile":key))}<span>${label}</span></button>`).join("")}</nav>`;
}

function render() {
  const app = document.querySelector("#app");
  app.innerHTML = `<div class="workspace">
    <aside class="panel">
      <h1>SalahPath Browser Preview</h1>
      <p>Lokale UI-Vorschau für schnelle Iteration. Änderungen hier ersetzen nicht den finalen SwiftUI/iPhone-Test.</p>
      <div class="control"><label>Screen</label><select id="screenSelect">
        ${[["home","Start"],["quran","Koran"],["reader","Koran Reader"],["prayer","Gebet"],["wudu","Abdest"],["qibla","Qibla"],["tracker","Tracker"],["more","Entdecken"],["settings","Profil / Settings"]].map(([v,l])=>`<option value="${v}" ${state.screen===v?"selected":""}>${l}</option>`).join("")}
      </select></div>
      <div class="control"><label>Sprache</label><select id="language"><option value="de" ${state.language==="de"?"selected":""}>Deutsch</option><option value="tr" ${state.language==="tr"?"selected":""}>Türkçe</option></select></div>
      <div class="control"><label>Gebetsdarstellung</label><select id="audience"><option value="male" ${state.audience==="male"?"selected":""}>Mann</option><option value="female" ${state.audience==="female"?"selected":""}>Frau</option></select></div>
      <div class="control"><button id="reset">Vorschau zurücksetzen</button></div>
      <p class="small"><b>Browser-first:</b> Oberfläche hier prüfen. Native Funktionen wie Magnetometer, Background Audio und Notifications werden später im iOS-Simulator bzw. final auf dem iPhone geprüft.</p>
    </aside>
    <section class="phone"><div class="status"><span>9:41</span><span>●●● Wi-Fi 100%</span></div><div class="app-shell"><div class="screen">${screen()}</div>${tabs()}</div></section>
    <aside class="panel">
      <h2>Aktuelle Abnahme</h2>
      <p><span class="ok">✓</span> Standalone Feature Icons</p>
      <p><span class="ok">✓</span> Gebet Mann/Frau separat</p>
      <p><span class="ok">✓</span> 2. Rakʿah sichtbar</p>
      <p><span class="ok">✓</span> Salam rechts → links</p>
      <p><span class="ok">✓</span> Abdest 13 Schritte</p>
      <p><span class="ok">✓</span> Rechts/links Reihenfolge sichtbar</p>
      <p>Quran Audio, echtes Qibla Heading und Background Verhalten bleiben native QA.</p>
    </aside>
  </div>`;

  document.querySelectorAll("[data-screen]").forEach(el=>el.addEventListener("click",()=>setScreen(el.dataset.screen)));
  document.querySelector("#screenSelect").addEventListener("change",e=>setScreen(e.target.value));
  document.querySelector("#language").addEventListener("change",e=>{state.language=e.target.value;save();render();});
  document.querySelector("#audience").addEventListener("change",e=>{state.audience=e.target.value;save();render();});
  document.querySelector("#reset").addEventListener("click",()=>{localStorage.clear();location.href="/";});
  document.querySelectorAll("[data-prayer]").forEach(el=>el.addEventListener("click",()=>{state.prayerStep=Number(el.dataset.prayer);save();render();}));
  document.querySelectorAll("[data-wudu]").forEach(el=>el.addEventListener("click",()=>{state.wuduStep=Number(el.dataset.wudu);save();render();}));
  const heading = document.querySelector("#heading");
  if (heading) heading.addEventListener("input",e=>{state.heading=Number(e.target.value);render();});
}

render();
