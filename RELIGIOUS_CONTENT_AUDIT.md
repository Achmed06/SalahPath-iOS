# SalahPath religious-content audit

Audit date: 5 October 2026  
Target build: SalahPath 3.62 (78)

This audit is intended to reduce inaccurate or misleading religious quotations and to make school-specific guidance explicit. It is not a claim that every juristic opinion is universal.

## Sources checked

Primary factual checks were made against official Diyanet Din İşleri Yüksek Kurulu guidance for Hanafi/Turkish practice and against the referenced hadith/Quran texts where the app displays a quotation or formula.

Diyanet references checked:

- Wudu: https://kurul.diyanet.gov.tr/tr/fetva/abdest-nedir-ve-nasil-alinir/0193c42d-4493-7cd5-0d48-874d6be1a7d3
- Wudu obligatory-vs-Sunnah repetition: https://kuran.diyanet.gov.tr/mushaf/tefsir-2/maide-suresi-5/ayet-3/diyanet-vakfi-meali-4
- Neck wiping classification (Hanafi adab): https://islamansiklopedisi.org.tr/mesh--abdest
- Mest / qualifying socks: https://kurul.diyanet.gov.tr/tr/fetva/mest-uzerine-mesh-nasil-yapilir-ve-bunun-sartlari-nelerdir/0193c42d-4872-7a2c-ca0b-e6a5a832dc93
- Water barriers / nail polish: https://kurul.diyanet.gov.tr/Cevap-Ara/43/boya-oje-ruj-ve-jole-gibi-maddeler-abdest-ve-gusle-engel-olur-mu
- Bandages / wounds: https://kurul.diyanet.gov.tr/tr/fetva/bedeninde-veya-bir-uzvunda-sargi-alci-ya-da-yara-bulunan-kimse-nasil-abdest-alir/0193c42d-492b-764e-c148-284760fd9c5c
- Diyanet prayer learning texts (Tashahhud / Salli-Bārik / Rabbana): https://dijital.diyanet.gov.tr/File/Download?id=4218&path=4218_1.pdf
- Diyanet Namaz İlmihali Qunūt reading: https://namaz.diyanet.gov.tr/namaz/html/kutuphane/HTML/NamazIlmihali/assets/common/downloads/publication.pdf
- Quran 14:41: https://kuran.diyanet.gov.tr/mushaf/kuran-tefsir-1/ibrahim-suresi-14/ayet-41/diyanet-isleri-baskanligi-meali-1
- Ghusl: https://kurul.diyanet.gov.tr/tr/fetva/gusul-boy-abdesti-ne-zaman-gereklidir-ve-sunnete-uygun/0193c42d-4959-7fa3-b0b7-5a3001c5f706
- Tayammum: https://kurul.diyanet.gov.tr/tr/fetva/teyemmum-nedir-nasil-yapilir-teyemmumu-bozan-seyler-nelerdir/0193c42d-4a83-7216-84a3-951c2fa115aa
- Menstruation/postpartum worship rules: https://kurul.diyanet.gov.tr/tr/fetva/kadinlarin-adet-veya-lohusalik-hallerinde-yapamayacaklari/0193c42d-4b21-7774-1a09-738831304296
- Fatiha behind an imam: https://kurul.diyanet.gov.tr/tr/fetva/imama-uyan-bir-kimse-fatiha-okuyabilir-mi/0193c42d-58f7-7851-de88-9e1eaf349583
- Four-rak'ah non-muakkadah sitting details: https://kurul.diyanet.gov.tr/tr/fetva/ikindi-namazinin-sunneti-ile-yatsi-namazinin-ilk-sunnetinin/0193c42d-547b-7b06-0e8e-33a7ee736367
- Wudu invalidators: https://kurul.diyanet.gov.tr/tr/fetva/abdesti-bozan-seyler-nelerdir
- Ruku rising dhikr roles: https://kurul.diyanet.gov.tr/tr/fetva/namazda-rukudan-kalkarken-semi-allahu-limen-hamideh-ve-rabbena-lekel-hamd-sozlerini-kimler-soyler
- Sehiv sajdah: https://kurul.diyanet.gov.tr/tr/fetva/hangi-sebeplerle-sehiv-secdesi-yapmak-gerekir-sehiv-secdesi-nasil-yapilir/0193c42d-5eb1-7caa-b1ce-6346f72b89fb
- Tilawah sajdah: https://kuran.diyanet.gov.tr/kuran-sozlugu/detay/55-tilavet-secdesi
- Tilawah sajdah procedure: https://kurul.diyanet.gov.tr/tr/fetva/namazin-disinda-veya-namazda-tilavet-secdesi-nasil-yapilir/0193c42d-5f85-7ec7-03cc-bb01f1c46aca
- Traveller prayer: https://kurul.diyanet.gov.tr/tr/fetva/umreye-gidenler-seferilik-hukumleri-acisindan-mekke-ve/009d3a5e-4dc0-4a27-090b-08dd1c135351
- Prayer with illness / ima: https://kurul.diyanet.gov.tr/tr/fetva/ima-ile-namaz-nasil-kilinir-gozle-ima-ederek-namaz/0193c42d-5e9a-735a-7cab-30fe0c77cf53
- Eid obligation for women: https://kurul.diyanet.gov.tr/tr/fetva/kadinlar-bayram-namazi-ile-sorumlu-mudur/0193c42d-5bff-71a3-b84e-f05e51454b22
- Asr-i awwal / Asr-i thani: https://kurul.diyanet.gov.tr/tr/fetva/asr-i-evvel-ve-asr-i-sani-ne-demektir/0193c42d-4d64-7acf-2961-12b0db4e1723

Hadith reference checked for the morning/evening formula used by SalahPath:

- Hisn al-Muslim 78: https://sunnah.com/hisn/79

## Findings and corrections present in the current native source

- Removed `Amin` from the displayed Fatiha transliteration and explicitly states that Amin is said after al-Fatiha and is not part of the surah or a Quran verse.
- Corrected the Hanafi tashahhud index-finger wording: the finger is raised at `la ilaha` and lowered at `illallah`.
- Clarified the Hanafi/Diyanet division of the ruku-rising formulas between imam, person praying alone, and follower.
- Added a sourced Hanafi/Diyanet Wudu-invalidators overview and explicitly warns that other schools differ in several points.
- Corrected the Wudu step classification model: Hanafi neck wiping is now shown as **adab/âdâb**, not automatically as Sunnah.
- Clarified the mixed obligation/repetition issue in Wudu: washing the obligatory limbs once fulfills the obligatory wash, while the threefold washing shown in the full procedure is Sunnah; the head step separately explains the Hanafi minimum of one quarter versus wiping the full head.
- Added practical Wudu special cases for water-blocking coatings (including nail polish), medically necessary dressings/treatments, and Hanafi mest/qualifying-sock wiping conditions and time limits.
- Renamed the learning entry from the overbroad “Alle Gebete einzeln” to “Gebetsarten & Anleitungen” because the catalog is not an exhaustive list of every prayer/fiqh case.
- Began the strict Arabic/transliteration pass: the core Arabic strings for Fātiha, Tashahhud, Salli/Bārik and both Hanafi Qunūt duas were checked against Diyanet learning material; no substantive Arabic-text mismatch was found in those strings.
- Standardized the Qunūt transliterations to Diyanet's published Turkish reading form so learners are not taught inconsistent terminal vowels/consonants.
- Restored the separate Quran 14:41 “Rabbenâğfirli” recitation to the prayer-dua lesson and kept it distinct from the shorter between-sujūd “Rabbighfir lī”.
- Replaced the Fātiha “meaning” field's catalog-style summary with an actual German/Turkish meaning so the UI no longer labels a description as the meaning of the surah.
- Verified all four Quran-referenced Daily Dua entries (2:201, 20:114 excerpt, 3:173 excerpt, 25:74) against the cited Quran locations; no reference mismatch was found.
- Verified the 14 Tilāwah-Sajdah verse references against Diyanet's own Tilâvet Secdesi list; the existing list matches, so no verse-number correction was made.
- Corrected the source attribution for the “Allāhumma bika aṣbaḥnā / amsaynā” morning/evening dhikr: SalahPath keeps the displayed transmitted variant, but no longer attributes that exact wording to a Diyanet/Riyâzü’s-Sâlihîn rendering that differs in its evening wording.
- Added a Sehiv-Secdesi / prayer-error module instead of implying that every prayer mistake has the same consequence.
- Corrected the Turkish sunrise label from `Sabah` to `Güneş` in the reference prayer-time naming.
- Clarified Diyanet's Asr-i awwal calculation versus Abu Hanifa's Asr-i thani view in settings.
- Reframed `32 Farz` as a traditional Hanafi/Diyanet teaching framework rather than an independent creed category.
- Added the exact Hanafi/Diyanet Tashriq-takbir period and the prohibited fasting days around both Eids.
- Removed unsupported fixed-count implications from the free dhikr counter; transmitted morning/evening counts remain in the sourced adhkar screen.
- Added Tilawah-Secdesi guidance, the official Diyanet list of 14 sajdah verses, and an in-reader marker for those ayahs.
- Added Hanafi/Diyanet traveller-prayer (qasr) and illness/ima guidance with explicit school-difference wording.
- Added a dedicated Kerahat-times module because the prior app only mentioned prohibited prayer times incidentally. It now distinguishes the three strict solar windows from additional times when specifically voluntary prayer is makruh, with a warning that minute estimates are region-dependent.
- Added a women-specific purity overview for hayd, nifas and istihada. It states the prayer/fasting qada distinction, ghusl after the end of hayd/nifas, classical Hanafi duration rules, the 2026 Diyanet medical-pattern caveat, and explicitly refuses to auto-classify an individual's bleeding.
- Added a dedicated Hanafi/Diyanet qada-prayer guide. It distinguishes the five daily fard prayers and Hanafi witr from sunnah prayers, records the same-day Fajr-sunnah exception, preserves the travel-state rak'ah count, separates strict kerahat windows from the imsak-to-sunrise nafl restriction, and notes that Hanafi worshippers with qada debt may still pray rawatib and other nafl prayers.
- Expanded Zakat from a generic topic card into a sourced practical guide: Diyanet's 80.18 g 24-karat-gold nisab basis, the common 2.5% rule for money/gold/trade goods, lunar-year and debt handling, Hanafi jewelry treatment, recipient classes and close-relative exclusions. No changing currency price is hard-coded.
- Corrected the Iqamah/Kamet glossary: it is the call immediately before a fard prayer and is not definitionally restricted to congregational prayer. The qada guide now also records the Hanafi/Diyanet adhan/iqamah practice for missed prayers.
- Added a Fitre/Fıtır Sadakası guide distinguishing its nisab conditions from Zakat, its Hanafi Eid-dawn obligation point, early Ramadan payment, recipient restrictions and the deliberate omission of a permanently hard-coded annual cash amount.
- Added a Kurban/Udhiyah guide covering the Hanafi/Diyanet obligation criteria, sacrifice window, species/age rules, large-animal shares, proxy ownership, meat-distribution status and several common misconceptions. School-specific timing differences are explicitly marked.
- Corrected the Turkish Ilmihal navigation label from the unlocalized German/transliteration form `Tayammum` to `Teyemmüm`.
- Clarified that women are not obligated to attend Eid prayer and that women/travellers may attend Jumuah without being among those for whom it is obligatory.
- Clarified the prayer precondition as ritual purity: Wudu and, where required, Ghusl.
- Corrected the prayer-learning wording so the statement “Fatiha in every rak'ah” is not presented as universal for a Hanafi follower in congregational prayer. The guide now distinguishes praying alone / as imam from following an imam.
- Completed Quran 3:8 in the dua library; the prior text omitted the final phrase.
- Completed the transliteration of Quran 25:74.
- Marked short Quran extracts (20:114 and 3:173) as excerpts instead of implying that the displayed words are the complete verse.
- The Home-card Sayyid al-Istighfar entry now contains the full displayed formula; it is no longer a truncated quotation presented as complete.
- Corrected the morning/evening “Allahumma bika asbahna / amsayna” display so the evening tab shows the evening wording and the morning wording includes its closing phrase.
- Replaced the vague Ramadan daytime-intention cutoff with Diyanet's precise Hanafi rule: for Ramadan, specified vows and voluntary fasts the intention may be made until about 10 minutes before solar noon if nothing invalidating occurred after imsak; qada, kaffarah and unscheduled vow fasts must be intended by imsak.
- Added the consensus menstruation/postpartum qada distinction to the Qada tracker: prayers missed during hayd/nifas are not made up, while missed Ramadan fasts are made up after purification.
- Clarified that the Three Quls card displays only the opening lines while the practice refers to the complete surahs.
- Removed the unsupported implication that `Astaghfirullah` has a fixed count of 33 in this morning/evening screen. The counter is no longer presented as a transmitted prescribed number.
- Reworded broad claims of “authentic hadiths” to “hadith sources” and explicitly notes that grading can differ.

## Areas checked without a required code correction

The current Hanafi/Diyanet descriptions of the four obligatory elements of wudu, the three Hanafi obligatory components of ghusl, basic tayammum procedure, menstruation/postpartum prayer and fasting rules, and the special first-sitting rule for the four-rak'ah non-muakkadah sunnah before Asr/Isha are consistent with the cited Diyanet guidance reviewed for this audit.

Hijri-calendar screens already state that the app uses the Umm al-Qura calculation and that regional moon sighting may shift the actual beginning of a lunar month. This distinction should remain.

## Open follow-up items

- Individual hayd/nifas/istihada classification is intentionally not automated. The new overview is educational only; irregular bleeding patterns, medication/IUD effects, pregnancy-related bleeding and miscarriage cases still require case-specific evaluation.
- Prayer artwork still needs a visual fiqh pass independent of the text audit. In particular, the male ruku artwork does not demonstrate a clearly straight back as well as the written Hanafi/Diyanet instruction does, and the male sujud/foot-position details deserve a clearer instructional redraw.
- The app's default Asr choice is a product setting, not a universal fiqh truth. The UI now names the Diyanet/asr-i awwal and Abu Hanifa/asr-i thani options explicitly; future product changes must not relabel one as the only Hanafi-valid view.

## Release rule

Future additions that quote Quran or hadith text, prescribe a fixed number, or present a school-specific fiqh practice must include an identifiable source or be clearly labelled as an app convenience rather than a religious prescription. School differences should be stated where they materially change what the user is told to do.
