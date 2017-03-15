import math
import random
import re


def choose(items, exponent=1):
    return items[math.floor(pow(random.random(), exponent) * len(items))]


def spell(lang, syll):
    if lang['noortho']:
        return syll

    s = ''
    for c in syll:
        s += lang['cortho'].get(c, lang['vortho'].get(c, defaultOrtho.get(c, c)))

    return s


def makeSyllable(lang):
    while True:
        syll = ""
        i = 0
        while i < len(lang['structure']):
            ptype = lang['structure'][i]
            if i + 1 < len(lang['structure']) and lang['structure'][i + 1] == '?':
                i += 1
                if random.random() < 0.5:
                    i += 1
                    continue

            syll += choose(lang['phonemes'][ptype], lang['exponent'])
            i += 1

        bad = False
        for i in range(len(lang['restricts'])):
            if re.match(syll, lang['restricts'][i]):
                bad = True
            break

        if bad:
            continue

        return spell(lang, syll)


def getMorpheme(lang, key=None):
    if key is None:
        key = ''

    if lang['nomorph']:
        return makeSyllable(lang)

    items = lang['morphemes'].get(key, [])
    extras = 10
    if key:
        extras = 1

    while True:
        n = random.randrange(len(items) + extras)

        if n in items:
            return items[n]

        morph = makeSyllable(lang)
        bad = False

        for k in lang['morphemes']:
            if morph in lang['morphemes'][k]:
                bad = True
                break

        if bad:
            continue

        items.append(morph)
        lang['morphemes'][key] = items
        return morph


def makeWord(lang, key):
    nsylls = random.randrange(lang['minsyll'], lang['maxsyll'] + 1)
    w = ''
    keys = {random.randrange(nsylls): key}

    for i in range(nsylls):
        w += getMorpheme(lang, keys.get(i, None))

    return w


def getWord(lang, key=''):
    ws = lang['words'].get(key, [])
    extras = 3
    if key:
        extras = 2

    while True:
        n = random.randrange(len(ws) + extras)

        if n in ws:
            return ws[n]

        w = makeWord(lang, key)
        bad = False
        for k in lang['words']:
            if w in lang['words'][k]:
                bad = True
                break

        if bad:
            continue

        ws.append(w)
        lang['words'][key] = ws
        return w


def makeName(lang, key=''):
    lang['genitive'] = lang.get('genitive', getMorpheme(lang, 'of'))
    lang['definite'] = lang.get('definite', getMorpheme(lang, 'the'))

    while True:
        name = None

        if random.random() < 0.5:
            name = getWord(lang, key).title()

        else:
            w1 = getWord(lang, key if random.random() < 0.6 else '').title()
            w2 = getWord(lang, key if random.random() < 0.6 else '').title()

            if w1 == w2:
                continue

            if random.random() > 0.5:
                name = lang['joiner'].join([w1, w2])

            else:
                name = lang['joiner'].join([w1, lang['genitive'], w2])

        if random.random() < 0.1:
            name = lang['joiner'].join([lang['definite'], name])

        if len(name) < lang['minchar'] or len(name) > lang['maxchar']:
            continue

        used = False

        for name2 in lang['names']:
            if name2 in name or name in name2:
                used = True
                break

        if used:
            continue

        lang['names'].append(name)
        return name


def makeBasicLanguage():
    return {
        'phonemes': {
            'C': "ptkmnls",
            'V': "aeiou",
            'S': "s",
            'F': "mn",
            'L': "rl"
        },
        'structure': "CVC",
        'exponent': 2,
        'restricts': [],
        'cortho': {},
        'vortho': {},
        'noortho': True,
        'nomorph': True,
        'nowordpool': True,
        'minsyll': 1,
        'maxsyll': 1,
        'morphemes': {},
        'words': {},
        'names': [],
        'joiner': ' ',
        'maxchar': 12,
        'minchar': 5
    }


def makeOrthoLanguage():
    lang = makeBasicLanguage()
    lang.noortho = False
    return lang


def makeRandomLanguage():
    lang = makeBasicLanguage()
    lang['noortho'] = False
    lang['nomorph'] = False
    lang['nowordpool'] = False
    lang['phonemes']['C'] = list(choose(consets, 2)['C'])
    lang['phonemes']['V'] = list(choose(vowsets, 2)['V'])
    lang['phonemes']['L'] = list(choose(lsets, 2)['L'])
    lang['phonemes']['S'] = list(choose(ssets, 2)['S'])
    lang['phonemes']['F'] = list(choose(fsets, 2)['F'])

    random.shuffle(lang['phonemes']['C'])
    random.shuffle(lang['phonemes']['V'])
    random.shuffle(lang['phonemes']['L'])
    random.shuffle(lang['phonemes']['S'])
    random.shuffle(lang['phonemes']['F'])

    lang['structure'] = choose(syllstructs)
    lang['restricts'] = ressets[2]['res']
    lang['cortho'] = choose(corthsets, 2)['orth']
    lang['vortho'] = choose(vorthsets, 2)['orth']
    lang['minsyll'] = random.randrange(1, 3)

    if len(lang['structure']) < 3:
        lang['minsyll'] += 1

    lang['maxsyll'] = random.randrange(lang['minsyll'] + 1, 7)
    lang['joiner'] = choose('   -')
    return lang


defaultOrtho = {
    'ʃ': 'sh',
    'ʒ': 'zh',
    'ʧ': 'ch',
    'ʤ': 'j',
    'ŋ': 'ng',
    'j': 'y',
    'x': 'kh',
    'ɣ': 'gh',
    'ʔ': '‘',
    'A': "á",
    'E': "é",
    'I': "í",
    'O': "ó",
    'U': "ú"
}

corthsets = [
    {
        'name': "Default",
        'orth': {}
    },
    {
        'name': "Slavic",
        'orth': {
            'ʃ': 'š',
            'ʒ': 'ž',
            'ʧ': 'č',
            'ʤ': 'ǧ',
            'j': 'j'
        }
    },
    {
        'name': "German",
        'orth': {
            'ʃ': 'sch',
            'ʒ': 'zh',
            'ʧ': 'tsch',
            'ʤ': 'dz',
            'j': 'j',
            'x': 'ch'
        }
    },
    {
        'name': "French",
        'orth': {
            'ʃ': 'ch',
            'ʒ': 'j',
            'ʧ': 'tch',
            'ʤ': 'dj',
            'x': 'kh'
        }
    },
    {
        'name': "Chinese (pinyin)",
        'orth': {
            'ʃ': 'x',
            'ʧ': 'q',
            'ʤ': 'j',
        }
    }
]

vorthsets = [
    {
        'name': "Ácutes",
        'orth': {}
    },
    {
        'name': "Ümlauts",
        'orth': {
            'A': "ä",
            'E': "ë",
            'I': "ï",
            'O': "ö",
            'U': "ü"
        }
    },
    {
        'name': "Welsh",
        'orth': {
            'A': "â",
            'E': "ê",
            'I': "y",
            'O': "ô",
            'U': "w"
        }
    },
    {
        'name': "Diphthongs",
        'orth': {
            'A': "au",
            'E': "ei",
            'I': "ie",
            'O': "ou",
            'U': "oo"
        }
    },
    {
        'name': "Doubles",
        'orth': {
            'A': "aa",
            'E': "ee",
            'I': "ii",
            'O': "oo",
            'U': "uu"
        }
    }
]

consets = [
    {
        'name': "Minimal",
        'C': "ptkmnls"
    },
    {
        'name': "English-ish",
        'C': "ptkbdgmnlrsʃzʒʧ"
    },
    {
        'name': "Pirahã (very simple)",
        'C': "ptkmnh"
    },
    {
        'name': "Hawaiian-ish",
        'C': "hklmnpwʔ"
    },
    {
        'name': "Greenlandic-ish",
        'C': "ptkqvsgrmnŋlj"
    },
    {
        'name': "Arabic-ish",
        'C': "tksʃdbqɣxmnlrwj"
    },
    {
        'name': "Arabic-lite",
        'C': "tkdgmnsʃ"
    },
    {
        'name': "English-lite",
        'C': "ptkbdgmnszʒʧhjw"
    }
]

ssets = [
    {
        'name': "Just s",
        'S': "s"
    },
    {
        'name': "s ʃ",
        'S': "sʃ"
    },
    {
        'name': "s ʃ f",
        'S': "sʃf"
    }
]

lsets = [
    {
        'name': "r l",
        'L': "rl"
    },
    {
        'name': "Just r",
        'L': "r"
    },
    {
        'name': "Just l",
        'L': "l"
    },
    {
        'name': "w j",
        'L': "wj"
    },
    {
        'name': "r l w j",
        'L': "rlwj"
    }
]

fsets = [
    {
        'name': "m n",
        'F': "mn"
    },
    {
        'name': "s k",
        'F': "sk"
    },
    {
        'name': "m n ŋ",
        'F': "mnŋ"
    },
    {
        'name': "s ʃ z ʒ",
        'F': "sʃzʒ"
    }
]

vowsets = [
    {
        'name': "Standard 5-vowel",
        'V': "aeiou"
    },
    {
        'name': "3-vowel a i u",
        'V': "aiu"
    },
    {
        'name': "Extra A E I",
        'V': "aeiouAEI"
    },
    {
        'name': "Extra U",
        'V': "aeiouU"
    },
    {
        'name': "5-vowel a i u A I",
        'V': "aiuAI"
    },
    {
        'name': "3-vowel e o u",
        'V': "eou"
    },
    {
        'name': "Extra A O U",
        'V': "aeiouAOU"
    }
]

syllstructs = [
    "CVC",
    "CVV?C",
    "CVVC?", "CVC?", "CV", "VC", "CVF", "C?VC", "CVF?",
    "CL?VC", "CL?VF", "S?CVC", "S?CVF", "S?CVC?",
    "C?VF", "C?VC?", "C?VF?", "C?L?VC", "VC",
    "CVL?C?", "C?VL?C", "C?VLC?"]

ressets = [
    {
        'name': "None",
        'res': []
    },
    {
        'name': "Double sounds",
        'res': [r'(.)\1']
    },
    {
        'name': "Doubles and hard clusters",
        'res': [r'[sʃf][sʃ]', r'(.)\1', r'[rl][rl]']
    }
]

if __name__ == '__main__':
    lang = makeRandomLanguage()
    for i in range(10):
        print(getWord(lang))

    print()
    for i in range(10):
        print(makeName(lang))
