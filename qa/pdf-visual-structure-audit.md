# SalahPath PDF visual / structural audit

Source: `pdf24_umgewandelt.pdf`  
Pages visually inspected: **1–139 / 139**  
Reference date visible in the captured legacy app: 22 September 2026  
Current SalahPath comparison baseline: `main@db415c0552109bb182bad1d715f8c9fa2df29e5d`

## Purpose

This is the canonical handoff for the user's PDF reference. The PDF is a container for many screenshots so the screenshots do not need to be sent individually.

The audit is intentionally stricter than the earlier feature-only audit:

- every PDF page was rendered and visually inspected;
- visible controls, navigation paths, subpages and repeated scroll states were considered;
- the PDF is used to discover useful features and interaction patterns, not to clone its old visual shell;
- ads, obsolete navigation chrome and third-party media are not requirements;
- religious text must not be bulk-transcribed from screenshots. New religious content needs a verified structured source.

## Status legend

| Status | Meaning |
| --- | --- |
| COMPLETE | Current SalahPath has a reachable native equivalent that covers the useful requirement. |
| PARTIAL | The concept exists, but one or more visible PDF subfeatures or navigation paths are not yet represented. |
| MISSING | No equivalent was found in the current native source. |
| SOURCE-GATED | Useful feature, but full implementation requires verified religious/source data or media rights. |
| EXCLUDED | Deliberately not part of SalahPath's product scope. |

## Full page coverage

| PDF pages | Visible screen / interaction | Current SalahPath mapping | Status / action |
| --- | --- | --- | --- |
| 1 | Prayer dashboard: Gregorian and Hijri date, city, six displayed prayer/sun times, countdown, weather strip, quick-action icons, audio/menu controls. | `HomeView`, `PrayerEngine`, quick actions and next-prayer hero cover the core prayer dashboard. | **PARTIAL**: weather strip is not a current requirement/equivalent. Do not clone the crowded legacy icon row. |
| 2–4 | “Takvim Arkası”: one long daily scroll containing ayah, dua, hadith, knowledge entry, religious term and quote; A+/A− text controls. | Home has rotating `DailyDuaDetailView` and reference/quote content. | **PARTIAL**: no single daily digest exposing all six legacy content categories together. High-value future complement if backed by verified sources. |
| 5–9 | Full legacy side-menu inventory. It exposes many deeper areas that were hidden by the earlier coarse audit. | SalahPath uses native tabs + `MoreView`/Discover instead of a side drawer. | **PARTIAL inventory**, not a request to copy the drawer. Detailed menu crosswalk is below. |
| 10 | Multi-day İmsakiye prayer timetable. | Existing prayer calculation and prayer-time overview. | **COMPLETE conceptually**. Keep native presentation. |
| 11 | “Özel Günler”: Islamic special-day list for the year. | `HijriCalendarView` plus calendar-export work. | **COMPLETE**. |
| 12–13 | Settings: city; Alarm1/Alarm2 per prayer; per-prayer minute adjustments; save/basic/advanced; Friday sela offset; single/bulk time adjustment; manual DST; theme; kerahat warning; content toggles; iftar counter; read remaining time; step counter; special-day badge; weather; home clock; background. | `SettingsView` + `AppSettings` provide calculation method, Asr rule, per-prayer offsets, notification enable/at-time/lead, prayer selection, language, audience, appearance and Quran settings. | **PARTIAL**. Useful missing candidates: separate Friday-sela handling and optional prayer-specific notification profiles. Manual DST/weather/step counter/background color are not automatic requirements. |
| 14 | Qibla compass with Kaaba direction and distance. | `QiblaView`. | **COMPLETE**, with newer true-north/location hardening. |
| 15 | Zikirmatik: category selector, large counter, elapsed timer, increment, reset and sound. | `DhikrView` / `TasbihCounterView`. | **COMPLETE core use case**. |
| 16 | İlahi audio player with song list and transport controls. | No general ilahi catalogue. | **EXCLUDED / SOURCE-GATED** because media rights and catalogue provenance are required. |
| 17 | Community board with Dua / Other / Popular tabs and user posts. | No accounts/community posting system. | **EXCLUDED** for current scope because it creates moderation, account, abuse and backend requirements. |
| 18 | Wudu step index. | `WuduGuideView`. | **COMPLETE**. |
| 19 | Wudu intro / niyyah / basmala visual. | Detailed native Wudu flow and dedicated basmala artwork. | **COMPLETE**. |
| 20 | Hands washing. | Wudu flow. | **COMPLETE**. |
| 21 | Mouth with right hand. | Wudu flow. | **COMPLETE**. |
| 22 | Water into nose with right hand. | Wudu flow explicitly states right-hand water use. | **COMPLETE**. |
| 23 | Nose cleaning/blowing with left hand. | Wudu flow explicitly states left-hand cleaning. | **COMPLETE**. |
| 24 | Face washing. | Wudu flow. | **COMPLETE**. |
| 25 | Right arm to elbows. | Wudu rendered asset mapping verified anatomically. | **COMPLETE**. |
| 26 | Left arm to elbows. | Wudu rendered asset mapping verified anatomically. | **COMPLETE**. |
| 27 | Masah of head. | Wudu flow. | **COMPLETE**. |
| 28 | Ear cleaning. | Wudu flow. | **COMPLETE**. |
| 29 | Neck masah shown in legacy app. | SalahPath's authoritative Wudu lesson takes precedence over copying every legacy pose. | **DO NOT COPY BLINDLY**; retain verified Hanafi guidance. |
| 30 | Right foot. | Wudu rendered asset mapping verified anatomically. | **COMPLETE**. |
| 31 | Left foot. | Wudu rendered asset mapping verified anatomically. | **COMPLETE**. |
| 32 | Post-Wudu shahada. | Wudu lesson completion. | **COMPLETE conceptually**. |
| 33–35 | Ghusl: reasons, restrictions, fard acts and method, long scroll. | `GhuslGuideView`. | **COMPLETE native guide**. |
| 36–37 | Prayer catalogue: daily sunnah/fard units plus Witr, Eid, Tarawih, Tasbih, Friday and tesbihat. | `PrayerCatalogView` contains individual prayer entries, rulings, rakah counts, steps, notes and sources. | **COMPLETE / stronger native equivalent**. |
| 38 | Prayer walkthrough shell: Bay/Bayan segmented audience control, close, QR-style control, image, left/right navigation, independent explanation area. | `PrayerHowToView` with male/female audience and step navigation. | **COMPLETE core structure**. |
| 39–43 | Fajr-sunnah start: niyyah, opening takbir, hand placement and text scroll continuation. | Prayer tutorial + recitation references. | **COMPLETE**. |
| 44–45 | Ruku pose and continued male/female detail. | Prayer tutorial. | **COMPLETE**. |
| 46 | Standing after ruku. | Prayer tutorial. | **COMPLETE**. |
| 47–49 | First sujud and male/female placement details. | Prayer tutorial. | **COMPLETE**. |
| 50 | Sitting between sujud. | Prayer tutorial. | **COMPLETE**. |
| 51–53 | Second sujud and transition to next rakah. | Dedicated second-sujud assets now used. | **COMPLETE**. |
| 54–66 | Second rakah flow through final sitting and recitations; multiple text-scroll states. | Prayer tutorial, prayer recitation views and tashahhud detail. | **COMPLETE**, including existing finger visual. |
| 67 | Salam to worshipper's own RIGHT first. | Verified against rendered assets: own right first. | **COMPLETE / correctness gate**. |
| 68 | Salam to worshipper's own LEFT second. | Verified against rendered assets: own left second. | **COMPLETE / correctness gate**. |
| 69–72 | Long post-prayer tesbihat / Ayat al-Kursi / dhikr text. | Prayer text hub, dua/dhikr views. | **COMPLETE conceptually**, do not copy legacy text verbatim. |
| 73–76 | Fajr fard begins in same tutorial shell; speaker/audio control visible. | Prayer catalogue + tutorial + supported audio. | **COMPLETE core flow**. |
| 77 | “Namaz Sureleri”: Fatiha and short surahs list. | `PrayerTextsHubView`, `ShortSurahLearningView`. | **COMPLETE**. |
| 78–79 | Prayer duas and selected ayat: Subhaneke, Ettehiyyatu, Salli, Barik, Rabbana, Qunut; Ayat al-Kursi, Hashr 22–24, Baqara 285–286. | `PrayerDuaAudioView`, `QunutDuaView`, Quran reference links. | **COMPLETE core set**. |
| 80 | Yasin: Arabic text, Turkish reading, Turkish meaning, tafsir. | Full Quran reader plus Yasin/reference entry. | **PARTIAL** only if a dedicated tafsir mode is expected; Quran reading itself is complete. |
| 81 | Tesbih counter with bead visual, count, audio/reset/settings. | `DhikrView` / `TasbihCounterView`. | **COMPLETE core use case**. |
| 82 | Qada counters for Fajr, Dhuhr, Asr, Maghrib, Isha, Witr and fasting with +/−. | `PrayerDebtTrackerView`, persistent counters. | **COMPLETE**. |
| 83–84 | “Ezan / Dua Dinle”: multiple adhans by prayer/makam, Mecca adhan, extra adhans, Sela, adhan dua, Lebbeyk, iftar dua. | Build 77 now has separate optional 28-second Fajr and standard Doha Adhan notification sounds at exact prayer time plus Settings test actions. `PrayerDuaAudioView` remains separate prayer-recitation content. | **PARTIAL / SOURCE-GATED**. The core prayer-time Adhan is implemented; the broader Sela/makam/dua catalogue still requires separately verified audio rights. |
| 85 | Nearby mosques using map/location. | `NearbyMosquesView` backed by Apple MapKit local search. | **COMPLETE / stronger native equivalent**. |
| 86–98 | “40 Hadis”: long vertically scrolling set of 40 hadith cards with citations. | No dedicated Forty Hadith view found. | **MISSING / SOURCE-GATED**. Valuable addition only from verified hadith dataset; do not transcribe screenshots. |
| 99–103 | Veda Hutbesi long text with A+/A−. | `FarewellSermonView` now exists and intentionally presents sourced core messages while explaining that the commonly circulated sermon is compiled from multiple reports. | **COMPLETE as a safer native learning view**, not a screenshot transcript. |
| 104–105 | 32 Farz compact list. | `ThirtyTwoFardView`. | **COMPLETE**. |
| 106 | “Dini Yayın” media player. | No general broadcast player. | **EXCLUDED / SOURCE-GATED** unless a trusted, licensed source is selected later. |
| 107–115 | Esmaül Hüsna search and full 1–99 list with Arabic forms and names. | `EsmaulHusnaView` has searchable 99-name data with Arabic and German/Turkish meanings. | **COMPLETE / stronger native equivalent**. |
| 116–124 | Searchable, very large İslam İlmihali hierarchy covering creed, fiqh, purity, prayer, fasting, zakat, Hajj, family, commerce, social life, ethics and more. | `IlmihalDirectoryView` + `IslamLearningHubView` cover major areas as concise sourced learning topics. | **PARTIAL**: native content is real and useful, but not yet as hierarchically comprehensive as the PDF's large table of contents. |
| 125 | Quran directory “Sayfa”: page navigation. | `QuranDirectoryView` pages 1–604 with direct page reader. | **COMPLETE**. |
| 126 | Quran directory “Cüz”: Juz navigation. | `QuranDirectoryView` 30 Juz. | **COMPLETE**. |
| 127 | Quran directory “İniş Sırası”: revelation-order list. | `QuranDirectoryView` has revelation-order tab and Diyanet order mapping. | **COMPLETE**. |
| 128–129 | Quran directory “Sureler”: canonical surah list. | `QuranDirectoryView` 114 surahs with search. | **COMPLETE**. |
| 130 | “Sesli Kur'an”: Turkish meaning / Arabic Quran audio modes by Juz. | Current Quran reader has reciter/audio infrastructure, caching and playback. | **COMPLETE core audio-Quran requirement**, UI need not mirror Juz-only legacy player. |
| 131 | “Kur'an Fihristi”: searchable alphabetical topical Quran index with A–Z side index. | No dedicated topical Quran index found. | **MISSING**. High-value structural feature, but topic→ayah mappings need a verified dataset. |
| 132 | Yasin entry repeated. | Quran reader/reference entry. | **COMPLETE core reading requirement**. |
| 133 | Hac Umre Rehberi: Hajj info, Umrah info, Makkah places, Medina places, Tawaf duas, Sa'y duas, glossary, video, ayat, hadith, sermons and articles. | `HajjUmrahGuideView` has native Umrah/Hajj/Places/Duas segments and verified instructional summaries. | **PARTIAL**: explicit glossary, dedicated ayat/hadith collections, sermons/articles and video are not represented as separate sections. Do not add media/content without sources. |
| 134 | Islamic quiz entry; partially visible category cards behind menu. | No quiz view found. | **MISSING**. Could be added later using verified in-app learning content rather than copied questions. |
| 135 | Searchable Friday-sermon list. | No dedicated Friday-sermon directory found. | **MISSING / SOURCE-GATED**. Requires an authoritative maintained source. |
| 136 | Cevşen index: “Cevşen Nedir?” plus numbered pages. | No dedicated Cevşen area found. | **MISSING / SOURCE-GATED**. Do not transcribe raster pages; verify text, edition and rights first. |
| 137 | Ramadan & fasting menu: Tarawih, Tasbih prayer, Eid prayer and how-to, fasting wisdom, verses, hadiths, stories, Ramadan sermons, duas, Q&A, Laylat al-Qadr. | `RamadanGuideIndexView` links fasting basics/rules/exceptions/tracker, prayer catalogue, Quran ayat and duas. | **PARTIAL**: dedicated fasting stories, Ramadan sermons and Q&A are not separate current modules. |
| 138 | Four Caliphs list. | `FourCaliphsView`. | **COMPLETE / stronger native equivalent** with sourced individual lessons. |
| 139 | Four Caliphs open while legacy menu is visible. | `FourCaliphsView` reachable from Discover; legacy drawer intentionally not copied. | **COMPLETE content / EXCLUDED drawer**. |

## Full legacy-menu crosswalk from pages 5–9

The menu itself is not a UI requirement. Its entries are a discovery inventory.

| Legacy menu entry | SalahPath status |
| --- | --- |
| Namaz Vakitleri | COMPLETE: Home / prayer engine |
| İmsakiye | COMPLETE conceptually: prayer-time overview |
| Özel Günler | COMPLETE: Hijri calendar |
| Ayarlar | COMPLETE core settings; some legacy-specific toggles intentionally absent |
| Takvim Arkası | PARTIAL: daily dua/reference content exists, not the full six-category daily digest |
| Kıble Pusulası | COMPLETE |
| Zikirmatik | COMPLETE |
| İlahiler | EXCLUDED / SOURCE-GATED |
| Paylaşım Panosu | EXCLUDED |
| Abdest | COMPLETE |
| Namaz | COMPLETE |
| Namaz Sureleri | COMPLETE |
| Yasin Suresi | COMPLETE core reading/reference |
| Tesbih | COMPLETE |
| Kaza Takip | COMPLETE |
| Ezan / Dua Dinle | MISSING / SOURCE-GATED as a dedicated adhan/sela audio catalogue |
| Yakın Camiler | COMPLETE |
| 40 Hadis | MISSING / SOURCE-GATED |
| Veda Hutbesi | COMPLETE |
| 32 Farz | COMPLETE |
| Dini Yayın | EXCLUDED / SOURCE-GATED |
| Esma'ül Hüsna | COMPLETE |
| İslam İlmihali | PARTIAL: substantial native directory exists, but is less encyclopedic than legacy TOC |
| Kur'an-ı Kerim | COMPLETE |
| Sesli Kur'an Online | COMPLETE core Quran audio |
| Kur'an Fihristi | MISSING topical index |
| Hadis Fihristi | MISSING / SOURCE-GATED |
| 7300 Hadis | MISSING / SOURCE-GATED; do not chase quantity over source quality |
| Seçme Ayetler | PARTIAL: Quran reference links exist; no dedicated curated “selected verses” module |
| Güzel Dualar | COMPLETE/PARTIAL: Quranic dua library + morning/evening adhkar cover the core need |
| Güzel Sözler | MISSING as a standalone quote library; low priority |
| Salavatlar | PARTIAL: salawat appears in prayer text content, no standalone collection |
| Peygamberler Tarihi | PARTIAL: Prophet learning content exists, no full prophets-history directory |
| Efendimizin Hayatı | PARTIAL: learning content exists, no full Sira curriculum |
| 4 Halife | COMPLETE |
| Sahabelerimizin Hayatı | MISSING as a dedicated companion-biography library |
| Hz. Mevlana | MISSING / SOURCE-GATED |
| Mesnevi (6 Cilt) | MISSING / SOURCE-GATED and rights-sensitive |
| Ramazan ve Oruç | PARTIAL, substantial native hub exists |
| Dini Sözlük | PARTIAL: `PrayerTermsView` covers prayer terms, not a general religious dictionary |
| İsimler Sözlüğü | MISSING; low priority unless product scope explicitly needs it |
| Cevşen | MISSING / SOURCE-GATED |
| İslami Soru / Cevap | MISSING; any future version needs carefully sourced, non-fatwa framing |
| Cuma Hutbeleri | MISSING / SOURCE-GATED |
| Namazın Türkçesi | COMPLETE conceptually: prayer recitations expose meaning in current language |
| İslami Yarışma | MISSING |
| Hac Umre Rehberi | PARTIAL, substantial native guide exists |
| iOS Uygulamalarımız | EXCLUDED legacy self-promotion |
| Yardım | COMPLETE conceptually through current settings/support paths |

## Confirmed current native implementations that the old audit understated

The current source contains and exposes these real views:

- `PrayerCatalogView` and `PrayerCatalogDetailView`
- `PrayerHowToView`, `PrayerRecitationView`, `PrayerTextsHubView`
- `WuduGuideView`, `GhuslGuideView`, `TayammumGuideView`
- `PrayerDebtTrackerView`, `ThirtyTwoFardView`
- `NearbyMosquesView`
- `QuranDirectoryView` with Surah / revelation order / page / Juz modes
- `QuranView`, page reader, Juz, favorites, audio and progress
- `EsmaulHusnaView`
- `FarewellSermonView`
- `FourCaliphsView` and detail pages
- `HajjUmrahGuideView`
- `RamadanGuideIndexView`
- `IlmihalDirectoryView` and `IslamLearningHubView`
- `QuranicDuaLibraryView`, `MorningEveningAdhkarView`
- `HijriCalendarView`, fasting learning/tracker views and dhikr/tasbih tools

## Action backlog generated from the strict pass

### Highest-value missing complements

1. **Quran topical index**
   - Recreate the useful interaction from PDF page 131: search + alphabetical topics + topic detail linking to Quran references.
   - Do not invent topic mappings. Use a verified structured index dataset before shipping.

2. **40 Hadith / hadith discovery**
   - Add a curated, source-verified collection rather than transcribing pages 86–98 or chasing the legacy “7300” count.
   - Each item should include source/reference metadata and search/filtering.

3. **Adhan / Sela audio hub**
   - Core notification Adhan is now implemented with pinned Fajr and standard derivatives from the Internet Archive Doha collection marked Public Domain Mark 1.0.
   - Keep it separate from prayer-dua recitations.
   - Any additional Sela, makam variant or catalogue recording must have clear rights/provenance before shipping.

4. **İlmihal expansion**
   - Keep the native SalahPath presentation but extend the current condensed directory toward the useful hierarchy visible on pages 116–124.
   - Prefer verified structured Diyanet/TDV material; avoid screenshot transcription.

5. **Hajj/Umrah completeness**
   - Existing guide is good.
   - Candidate complements: glossary, Quran references, verified hadith references and Sa'y/Tawaf dua discovery.
   - Video/sermon/article feeds remain source-dependent.

6. **Ramadan completeness**
   - Existing hub is good.
   - Candidate complements: dedicated fasting Q&A, Ramadan sermon/reference area and verified stories/learning modules.

7. **Daily knowledge digest**
   - Expand current daily dua/reference strip into an optional daily learning page containing verified ayah, dua, hadith, term and short lesson.
   - This captures the useful idea of pages 2–4 without cloning the legacy screen.

8. **Learning quiz**
   - Build questions from SalahPath's own verified learning modules so the quiz stays consistent with shipped content.

### Lower priority / only if explicitly desired

- broader Prophet/Sira curriculum;
- companion biographies;
- general religious dictionary;
- selected-verses library;
- standalone salawat collection;
- Islamic names dictionary.

### Keep excluded unless product scope changes

- community board;
- general ilahi/music catalogue without rights;
- generic religious broadcast player;
- legacy ads and self-promotional screens;
- copying the legacy side drawer or visual shell;
- bulk screenshot transcription of Cevşen, Mesnevi, sermons, hadith books or other long-form religious works.

## Regression requirements carried forward

- Prayer salam remains worshipper's own **RIGHT first, LEFT second**.
- Wudu right/left arm and foot mappings remain anatomical, even where front-facing artwork appears mirrored to the viewer.
- Wudu nose step remains explicit: right hand for water, left hand for cleaning/blowing.
- Second-sujud and tashahhud-finger visuals remain reachable.
- New PDF-inspired features must not weaken release privacy, strict-concurrency, crash-hardening or App Store gates.
- The PDF is a visual/product reference, not an authoritative religious source.
