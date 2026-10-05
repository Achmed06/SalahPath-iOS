# SalahPath religious-content audit

Audit date: 5 October 2026  
Target build: SalahPath 3.62 (78)

This audit is intended to reduce inaccurate or misleading religious quotations, overly broad fiqh claims, and school-specific guidance presented as universal. It is not a claim that every juristic opinion is universal.

## Method

Primary factual checks use official Diyanet Din İşleri Yüksek Kurulu guidance for the Hanafi/Turkish presentation used by SalahPath. Quran/hadith wording and fixed-count adhkar are checked against the displayed reference where practical. Where schools materially differ, the app should say so instead of presenting a Hanafi rule as an unqualified Islamic universal.

## Sources checked

Diyanet references checked include:

- Wudu: https://kurul.diyanet.gov.tr/tr/fetva/abdest-nedir-ve-nasil-alinir/0193c42d-4493-7cd5-0d48-874d6be1a7d3
- Ghusl basics: https://kurul.diyanet.gov.tr/tr/fetva/gusul-boy-abdesti-ne-zaman-gereklidir-ve-sunnete-uygun/0193c42d-4959-7fa3-b0b7-5a3001c5f706
- Ghusl triggers / sexual discharge wording: https://kurul.diyanet.gov.tr/tr/fetva/bir-kadinin-jinekolojik-muayene-olmasi-ya-da-rahim/0195dc3a-5579-76ec-b042-4c180f3f4e4a
- Tayammum: https://kurul.diyanet.gov.tr/tr/fetva/teyemmum-nedir-nasil-yapilir-teyemmumu-bozan-seyler-nelerdir/0193c42d-4a83-7216-84a3-951c2fa115aa
- Witr: https://kurul.diyanet.gov.tr/tr/fetva/vitir-namazi-nedir-nasil-kilinir/0193c42d-5d22-7a98-69e2-22aa16cc28f1
- Qunut when not memorized: https://kurul.diyanet.gov.tr/tr/fetva/kunut-duasini-bilmeyen-bir-kimse-ne-yapar/0193c42d-5d9a-7c56-51a8-e76a981e98a9
- Eid prayer scope and procedure: https://igdir.diyanet.gov.tr/sayfalar/contentdetail.aspx?ContentId=1850&MenuCategory=Kurumsal
- Jumuʿah obligation / validity: https://kurul.diyanet.gov.tr/tr/fetva/cuma-namazi-ve-zuhr-i-ahir-namazinin-hukmu/f0ecca63-4fac-4234-b733-08dd1c135350
- Jumuʿah after the khutbah has begun: https://kurul.diyanet.gov.tr/tr/fetva/mekke-ve-medinede-cuma-namazi-vaktinde-ezanin-hemen/0193f3cd-bcef-7474-9985-d1ca582d1acd
- Janazah procedure: https://kurul.diyanet.gov.tr/tr/fetva/cenaze-namazi-nasil-kilinir/0193c42d-5ff0-7a8b-b744-96f510e9362a
- Fasting intention deadline: https://kurul.diyanet.gov.tr/tr/fetva/oruca-ne-zaman-ve-nasil-niyet-edilir/0193c42d-6bc5-745a-7532-60288956700e
- Fatiha behind an imam: https://kurul.diyanet.gov.tr/tr/fetva/imama-uyan-bir-kimse-fatiha-okuyabilir-mi/0193c42d-58f7-7851-de88-9e1eaf349583
- Four-rakʿah non-muʾakkadah sitting details: https://kurul.diyanet.gov.tr/tr/fetva/ikindi-namazinin-sunneti-ile-yatsi-namazinin-ilk-sunnetinin/0193c42d-547b-7b06-0e8e-33a7ee736367

Hadith/adhkar reference checked:

- Hisn al-Muslim 78: https://sunnah.com/hisn/79

## Findings and corrections present in the current audit branch

- Prayer learning no longer says “Fatiha in every rakʿah” as a universal rule for a Hanafi follower behind an imam.
- Quran 3:8 is complete; Quran 25:74 transliteration is complete; short Quran extracts are labelled as extracts.
- Sayyid al-Istighfar is not presented as a truncated complete formula.
- The morning/evening “Allahumma bika asbahna / amsayna” card now uses the Hisn al-Muslim 78 morning/evening wording and labels the source as a wording variant rather than implying all cited narrations are text-identical.
- The Three Quls card states that only opening lines are shown while the complete surahs are to be recited.
- Astaghfirullah is not assigned an unsupported fixed count in the morning/evening screen.
- Witr is explicitly identified as Hanafi Wajib; the app now also states that other Sunni schools classify Witr differently and may differ on rakʿah count and qunut.
- Eid is no longer phrased as an unqualified Hanafi Wajib for everyone: the text ties the Hanafi obligation to those meeting the Jumuʿah-obligation conditions. The Eid khutbah is identified as Sunnah after the prayer, and the absence of adhan/iqamah remains explicit.
- Jumuʿah now distinguishes the obligation group and exemptions, states that the khutbah before the prayer is a validity condition, and warns not to begin Sunnah/Nafila once the khutbah has begun.
- Janazah now explicitly says the third takbir is also taken without raising the hands in the audited Hanafi/Diyanet presentation.
- Ghusl no longer uses the overbroad German phrase “after ejaculation” without qualification; it specifies semen discharge with sexual arousal / orgasm, while intercourse remains independently listed as a trigger.
- Tayammum wording was narrowed from generic “earthy/mineral” material to clean earth or material counted as earth substance, matching the Diyanet formulation more closely.
- Ramadan niyyah no longer says only “before the Islamic midday boundary.” It states Diyanet’s explicit deadline of 10 minutes before solar zenith under the applicable conditions and separately states that Qada, Kaffarah, and non-time-fixed vow fasts require intention by Imsak.

## Areas checked without a required correction in this pass

- The Hanafi/Diyanet three obligatory components of ghusl (mouth, nose, entire body).
- The two-contact tayammum sequence: face once, then both arms including elbows.
- The core Hanafi Witr sequence: three rakʿat, only Tahiyyat after rakʿah two, qunut takbir and qunut in rakʿah three.
- The six additional Eid takbirs in the displayed Hanafi sequence.
- The four-takbir Janazah structure without rukuʿ or sujud.
- Basic fasting start/end wording: true Fajr/Imsak to sunset.
- Quranic dua entries reviewed in the earlier pass.
- Fixed counts on the reviewed morning/evening adhkar entries that are tied to identifiable Hisn al-Muslim references.

Hijri-calendar screens already state that the app uses a calculated calendar and that regional moon sighting may shift an actual lunar-month start. This distinction should remain.

## Release rule

Future additions that quote Quran or hadith text, prescribe a fixed count, or present a school-specific fiqh practice must include an identifiable source or be clearly labelled as app convenience rather than religious prescription. School differences should be stated where they materially change what the user is told to do. A phrase that merely “sounds Islamic” is not sufficient evidence.
