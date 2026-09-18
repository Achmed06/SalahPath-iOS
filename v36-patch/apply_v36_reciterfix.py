from pathlib import Path

p = Path('SalahZeit/Models/AppSettings.swift')
s = p.read_text(encoding='utf-8')
s = s.replace('''enum QuranReciter: String, CaseIterable, Identifiable {
    case alafasy
    case husary
    case minshawi
    case sudais

    var id: String { rawValue }

    var edition: String {
        switch self {
        case .alafasy: return "ar.alafasy"
        case .husary: return "ar.husary"
        case .minshawi: return "ar.minshawi"
        case .sudais: return "ar.sudais"
        }
    }

    var bitrate: Int { self == .sudais ? 192 : 128 }

    var title: String {
        switch self {
        case .alafasy: return "Mishary Rashid Alafasy"
        case .husary: return "Mahmoud Khalil Al-Husary"
        case .minshawi: return "Mohamed Siddiq al-Minshawi"
        case .sudais: return "Abdul Rahman Al-Sudais"
        }
    }
}''','''enum QuranReciter: String, CaseIterable, Identifiable {
    case alafasy
    case husary
    case minshawi

    var id: String { rawValue }

    var edition: String {
        switch self {
        case .alafasy: return "ar.alafasy"
        case .husary: return "ar.husary"
        case .minshawi: return "ar.minshawi"
        }
    }

    var bitrate: Int { 128 }

    var title: String {
        switch self {
        case .alafasy: return "Mishary Rashid Alafasy"
        case .husary: return "Mahmoud Khalil Al-Husary"
        case .minshawi: return "Mohamed Siddiq al-Minshawi"
        }
    }
}''')
p.write_text(s, encoding='utf-8')

p = Path('scripts/build_unsigned_ipa.sh')
s = p.read_text(encoding='utf-8')
s = s.replace('CURRENT_PROJECT_VERSION="11"', 'CURRENT_PROJECT_VERSION="12"')
p.write_text(s, encoding='utf-8')
print('v3.6 reciter reliability fix applied')
