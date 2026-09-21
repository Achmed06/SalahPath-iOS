from pathlib import Path

guide = Path("SalahZeit/Views/GuideView.swift")
text = guide.read_text(encoding="utf-8")

marker = "@MainActor\nfinal class RemoteAudioPlayer: ObservableObject {"
if marker not in text:
    raise SystemExit("v428: RemoteAudioPlayer marker missing")

cache = r'''actor QuranAudioCache {
    static let shared = QuranAudioCache()

    private let fileManager = FileManager.default
    private let maxBytes: Int64 = 300 * 1024 * 1024

    private var directoryURL: URL {
        let base = fileManager.urls(for: .applicationSupportDirectory, in: .userDomainMask).first!
        return base.appendingPathComponent("SalahPathAudioCache", isDirectory: true)
    }

    func playbackURL(for remoteURL: URL) async -> URL {
        guard remoteURL.scheme?.lowercased() == "https" else { return remoteURL }

        do {
            try ensureDirectory()
            let localURL = destinationURL(for: remoteURL)

            if isValidFile(localURL) {
                touch(localURL)
                return localURL
            }

            var request = URLRequest(url: remoteURL)
            request.timeoutInterval = 30

            let (temporaryURL, response) = try await URLSession.shared.download(for: request)
            guard let http = response as? HTTPURLResponse,
                  (200...299).contains(http.statusCode) else {
                throw URLError(.badServerResponse)
            }

            let attributes = try fileManager.attributesOfItem(atPath: temporaryURL.path)
            let size = (attributes[.size] as? NSNumber)?.int64Value ?? 0
            guard size > 0 else { throw URLError(.zeroByteResource) }

            if fileManager.fileExists(atPath: localURL.path) {
                try fileManager.removeItem(at: localURL)
            }

            try fileManager.moveItem(at: temporaryURL, to: localURL)
            touch(localURL)
            trimIfNeeded()
            return localURL
        } catch {
            // If caching fails, streaming must still work.
            return remoteURL
        }
    }

    func stats() -> (count: Int, bytes: Int64) {
        guard let files = try? fileManager.contentsOfDirectory(
            at: directoryURL,
            includingPropertiesForKeys: [.fileSizeKey],
            options: [.skipsHiddenFiles]
        ) else {
            return (0, 0)
        }

        var count = 0
        var total: Int64 = 0
        for url in files {
            guard let values = try? url.resourceValues(forKeys: [.isRegularFileKey, .fileSizeKey]),
                  values.isRegularFile == true else { continue }
            count += 1
            total += Int64(values.fileSize ?? 0)
        }
        return (count, total)
    }

    func clear() {
        guard fileManager.fileExists(atPath: directoryURL.path) else { return }
        try? fileManager.removeItem(at: directoryURL)
    }

    private func ensureDirectory() throws {
        if !fileManager.fileExists(atPath: directoryURL.path) {
            try fileManager.createDirectory(at: directoryURL, withIntermediateDirectories: true)
        }

        var values = URLResourceValues()
        values.isExcludedFromBackup = true
        var url = directoryURL
        try? url.setResourceValues(values)
    }

    private func destinationURL(for remoteURL: URL) -> URL {
        let rawExtension = remoteURL.pathExtension.lowercased()
        let ext = ["mp3", "m4a", "aac"].contains(rawExtension) ? rawExtension : "mp3"
        return directoryURL.appendingPathComponent("\(String(fnv1a(remoteURL.absoluteString), radix: 16)).\(ext)")
    }

    private func fnv1a(_ value: String) -> UInt64 {
        var hash: UInt64 = 14695981039346656037
        for byte in value.utf8 {
            hash ^= UInt64(byte)
            hash &*= 1099511628211
        }
        return hash
    }

    private func isValidFile(_ url: URL) -> Bool {
        guard fileManager.fileExists(atPath: url.path),
              let attributes = try? fileManager.attributesOfItem(atPath: url.path),
              let size = (attributes[.size] as? NSNumber)?.int64Value else {
            return false
        }
        return size > 0
    }

    private func touch(_ url: URL) {
        try? fileManager.setAttributes([.modificationDate: Date()], ofItemAtPath: url.path)
    }

    private func trimIfNeeded() {
        guard let files = try? fileManager.contentsOfDirectory(
            at: directoryURL,
            includingPropertiesForKeys: [.fileSizeKey, .contentModificationDateKey],
            options: [.skipsHiddenFiles]
        ) else { return }

        var entries: [(URL, Int64, Date)] = []
        var total: Int64 = 0

        for url in files {
            guard let values = try? url.resourceValues(
                forKeys: [.isRegularFileKey, .fileSizeKey, .contentModificationDateKey]
            ),
            values.isRegularFile == true else { continue }

            let size = Int64(values.fileSize ?? 0)
            total += size
            entries.append((url, size, values.contentModificationDate ?? .distantPast))
        }

        guard total > maxBytes else { return }

        for entry in entries.sorted(by: { $0.2 < $1.2 }) {
            try? fileManager.removeItem(at: entry.0)
            total -= entry.1
            if total <= maxBytes { break }
        }
    }
}

'''
text = text.replace(marker, cache + marker, 1)

old = '        let cleaned = urls.filter { $0.scheme?.lowercased() == "https" }'
new = '        let cleaned = urls.filter { $0.isFileURL || $0.scheme?.lowercased() == "https" }'
if old not in text:
    raise SystemExit("v428: playQueue URL filter anchor missing")
text = text.replace(old, new, 1)

start = text.index("    private func loadCurrentAndPlay() {")
end = text.index("    private func removeObservers() {", start)

replacement = r'''    private func loadCurrentAndPlay() {
        guard queueURLs.indices.contains(queueIndex) else { return }
        removeObservers()

        do {
            try AVAudioSession.sharedInstance().setCategory(.playback, mode: .default)
            try AVAudioSession.sharedInstance().setActive(true, options: [])
        } catch {
            lastError = "Audio konnte nicht gestartet werden. Erneut versuchen. / Ses başlatılamadı. Tekrar dene."
            isLoading = false
            isPlaying = false
            return
        }

        lastError = nil
        isLoading = true
        isPlaying = false
        currentTime = 0
        duration = 0

        let sourceURL = queueURLs[queueIndex]
        let expectedIndex = queueIndex
        activeURL = sourceURL

        Task { [weak self] in
            let playbackURL = await QuranAudioCache.shared.playbackURL(for: sourceURL)
            guard let self,
                  self.queueIndex == expectedIndex,
                  self.activeURL == sourceURL else { return }
            self.startPlayback(playbackURL)
        }
    }

    private func startPlayback(_ url: URL) {
        let item = AVPlayerItem(url: url)
        let newPlayer = AVPlayer(playerItem: item)
        newPlayer.defaultRate = playbackRate
        player = newPlayer

        periodicTimeObserver = newPlayer.addPeriodicTimeObserver(
            forInterval: CMTime(seconds: 0.25, preferredTimescale: 600),
            queue: .main
        ) { [weak self, weak newPlayer] time in
            Task { @MainActor in
                guard let self else { return }
                let seconds = time.seconds
                self.currentTime = seconds.isFinite && seconds >= 0 ? seconds : 0
                if let itemDuration = newPlayer?.currentItem?.duration.seconds,
                   itemDuration.isFinite,
                   itemDuration > 0 {
                    self.duration = itemDuration
                }
            }
        }

        statusObservation = item.observe(\.status, options: [.initial, .new]) { [weak self] item, _ in
            Task { @MainActor in
                guard let self else { return }
                switch item.status {
                case .readyToPlay:
                    self.isLoading = false
                    self.lastError = nil
                case .failed:
                    self.isLoading = false
                    self.isPlaying = false
                    self.lastError = item.error?.localizedDescription ?? "Audio konnte nicht geladen werden / Ses yüklenemedi."
                default:
                    self.isLoading = true
                }
            }
        }

        timeControlObservation = newPlayer.observe(\.timeControlStatus, options: [.initial, .new]) { [weak self] player, _ in
            Task { @MainActor in
                guard let self else { return }
                self.isPlaying = player.timeControlStatus == .playing
                if player.timeControlStatus == .waitingToPlayAtSpecifiedRate {
                    self.isLoading = true
                }
                if player.timeControlStatus == .playing {
                    self.isLoading = false
                }
            }
        }

        endObserver = NotificationCenter.default.addObserver(
            forName: .AVPlayerItemDidPlayToEndTime,
            object: item,
            queue: .main
        ) { [weak self] _ in
            Task { @MainActor in
                guard let self else { return }
                if self.hasNext {
                    self.next()
                } else {
                    self.isPlaying = false
                    self.isLoading = false
                }
            }
        }

        failedObserver = NotificationCenter.default.addObserver(
            forName: .AVPlayerItemFailedToPlayToEndTime,
            object: item,
            queue: .main
        ) { [weak self] note in
            Task { @MainActor in
                guard let self else { return }
                self.isLoading = false
                self.isPlaying = false
                let error = note.userInfo?[AVPlayerItemFailedToPlayToEndTimeErrorKey] as? Error
                self.lastError = error?.localizedDescription ?? "Audio-Wiedergabe fehlgeschlagen / Ses oynatılamadı."
            }
        }

        newPlayer.playImmediately(atRate: playbackRate)
    }

'''

text = text[:start] + replacement + text[end:]
guide.write_text(text, encoding="utf-8")
print("v428 applied: persistent Quran audio cache with offline playback fallback")
