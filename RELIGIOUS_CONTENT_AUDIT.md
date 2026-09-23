# SalahPath religious-content audit

Audit date: 23 September 2026  
Target build: SalahPath 3.62 (76)

This audit is intended to reduce inaccurate or misleading religious quotations and to make school-specific guidance explicit. It is not a claim that every juristic opinion is universal.

## Sources checked

Primary factual checks were made against official Diyanet Din İşleri Yüksek Kurulu guidance for Hanafi/Turkish practice and against the referenced hadith/Quran texts where the app displays a quotation or formula.

Diyanet references checked:

- Wudu: https://kurul.diyanet.gov.tr/tr/fetva/abdest-nedir-ve-nasil-alinir/0193c42d-4493-7cd5-0d48-874d6be1a7d3
- Ghusl: https://kurul.diyanet.gov.tr/tr/fetva/gusul-boy-abdesti-ne-zaman-gereklidir-ve-sunnete-uygun/0193c42d-4959-7fa3-b0b7-5a3001c5f706
- Tayammum: https://kurul.diyanet.gov.tr/tr/fetva/teyemmum-nedir-nasil-yapilir-teyemmumu-bozan-seyler-nelerdir/0193c42d-4a83-7216-84a3-951c2fa115aa
- Menstruation/postpartum worship rules: https://kurul.diyanet.gov.tr/tr/fetva/kadinlarin-adet-veya-lohusalik-hallerinde-yapamayacaklari/0193c42d-4b21-7774-1a09-738831304296
- Fatiha behind an imam: https://kurul.diyanet.gov.tr/tr/fetva/imama-uyan-bir-kimse-fatiha-okuyabilir-mi/0193c42d-58f7-7851-de88-9e1eaf349583
- Four-rak'ah non-muakkadah sitting details: https://kurul.diyanet.gov.tr/tr/fetva/ikindi-namazinin-sunneti-ile-yatsi-namazinin-ilk-sunnetinin/0193c42d-547b-7b06-0e8e-33a7ee736367

Hadith reference checked for the morning/evening formula used by SalahPath:

- Hisn al-Muslim 78: https://sunnah.com/hisn/79

## Findings and corrections present in the current native source

- Corrected the prayer-learning wording so the statement “Fatiha in every rak'ah” is not presented as universal for a Hanafi follower in congregational prayer. The guide now distinguishes praying alone / as imam from following an imam.
- Completed Quran 3:8 in the dua library; the prior text omitted the final phrase.
- Completed the transliteration of Quran 25:74.
- Marked short Quran extracts (20:114 and 3:173) as excerpts instead of implying that the displayed words are the complete verse.
- The Home-card Sayyid al-Istighfar entry now contains the full displayed formula; it is no longer a truncated quotation presented as complete.
- Corrected the morning/evening “Allahumma bika asbahna / amsayna” display so the evening tab shows the evening wording and the morning wording includes its closing phrase.
- Clarified that the Three Quls card displays only the opening lines while the practice refers to the complete surahs.
- Removed the unsupported implication that `Astaghfirullah` has a fixed count of 33 in this morning/evening screen. The counter is no longer presented as a transmitted prescribed number.
- Reworded broad claims of “authentic hadiths” to “hadith sources” and explicitly notes that grading can differ.

## Areas checked without a required code correction

The current Hanafi/Diyanet descriptions of the four obligatory elements of wudu, the three Hanafi obligatory components of ghusl, basic tayammum procedure, menstruation/postpartum prayer and fasting rules, and the special first-sitting rule for the four-rak'ah non-muakkadah sunnah before Asr/Isha are consistent with the cited Diyanet guidance reviewed for this audit.

Hijri-calendar screens already state that the app uses the Umm al-Qura calculation and that regional moon sighting may shift the actual beginning of a lunar month. This distinction should remain.

## Release rule

Future additions that quote Quran or hadith text, prescribe a fixed number, or present a school-specific fiqh practice must include an identifiable source or be clearly labelled as an app convenience rather than a religious prescription. School differences should be stated where they materially change what the user is told to do.
