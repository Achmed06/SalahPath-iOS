from pathlib import Path

p=Path('SalahZeit/Views/GuideView.swift')
s=p.read_text(encoding='utf-8')
s=s.replace('private struct AudioAyahData: Decodable { let audio: String? }','private struct AudioAyahData: Decodable { let number: Int; let audio: String? }')
old='''private enum QuranAudioResolver {
    static func urls(surah: Int, edition: String) async throws -> [URL] {
        let url = URL(string: "https://api.alquran.cloud/v1/surah/\\(surah)/\\(edition)")!
        var request = URLRequest(url: url)
        request.timeoutInterval = 20
        let (data, response) = try await URLSession.shared.data(for: request)
        guard let http = response as? HTTPURLResponse, (200...299).contains(http.statusCode) else { throw URLError(.badServerResponse) }
        let decoded = try JSONDecoder().decode(AudioEditionResponse.self, from: data)
        return decoded.data.ayahs.compactMap { item in
            guard let raw = item.audio else { return nil }
            return URL(string: raw.replacingOccurrences(of: "http://", with: "https://"))
        }
    }
}
'''
new='''private enum QuranAudioResolver {
    static func urls(surah: Int, reciter: QuranReciter) async throws -> [URL] {
        let url = URL(string: "https://api.alquran.cloud/v1/surah/\\(surah)/\\(reciter.edition)")!
        var request = URLRequest(url: url)
        request.timeoutInterval = 20
        let (data, response) = try await URLSession.shared.data(for: request)
        guard let http = response as? HTTPURLResponse, (200...299).contains(http.statusCode) else { throw URLError(.badServerResponse) }
        let decoded = try JSONDecoder().decode(AudioEditionResponse.self, from: data)
        return decoded.data.ayahs.compactMap { item in
            if let raw = item.audio, let url = URL(string: raw.replacingOccurrences(of: "http://", with: "https://")) { return url }
            return URL(string: "https://cdn.islamic.network/quran/audio/\\(reciter.bitrate)/\\(reciter.edition)/\\(item.number).mp3")
        }
    }
}
'''
if old not in s: raise SystemExit('resolver block not found')
s=s.replace(old,new)
s=s.replace('QuranAudioResolver.urls(surah: item.surahNumber, edition: settings.quranReciter.edition)','QuranAudioResolver.urls(surah: item.surahNumber, reciter: settings.quranReciter)')
old='''    private func playAyah(at index: Int) {
        guard let raw = audioSurah?.ayahs[safe: index]?.audio,
              let url = secureURL(raw) else {
            audio.lastError = settings.t("Audio für diese Ayah nicht verfügbar.", "Bu ayet için ses mevcut değil.")
            return
        }
        audio.toggle(url)
    }

    private var audioURLs: [URL] {
        (audioSurah?.ayahs ?? []).compactMap { ayah in
            guard let raw = ayah.audio else { return nil }
            return secureURL(raw)
        }
    }
'''
new='''    private func playAyah(at index: Int) {
        guard let ayah = audioSurah?.ayahs[safe: index],
              let url = audioURL(for: ayah) else {
            audio.lastError = settings.t("Audio für diese Ayah nicht verfügbar.", "Bu ayet için ses mevcut değil.")
            return
        }
        audio.toggle(url)
    }

    private var audioURLs: [URL] {
        (audioSurah?.ayahs ?? []).compactMap(audioURL)
    }

    private func audioURL(for ayah: AyahData) -> URL? {
        if let raw = ayah.audio, let resolved = secureURL(raw) { return resolved }
        return URL(string: "https://cdn.islamic.network/quran/audio/\\(settings.quranReciter.bitrate)/\\(settings.quranReciter.edition)/\\(ayah.number).mp3")
    }
'''
if old not in s: raise SystemExit('ayah audio block not found')
s=s.replace(old,new)
p.write_text(s,encoding='utf-8')

p=Path('scripts/build_unsigned_ipa.sh')
s=p.read_text(encoding='utf-8').replace('CURRENT_PROJECT_VERSION="10"','CURRENT_PROJECT_VERSION="11"')
p.write_text(s,encoding='utf-8')
print('v3.6 audio fallback applied')