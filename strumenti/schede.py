#!/usr/bin/env python3
"""
Schede dei componenti: lettura e scrittura di dati/componenti/<id>.md (solo libreria standard).

Formato di una scheda:

    ---
    id: hyperlink
    livello: fondamentale            introduzione | fondamentale | avanzato
    categoria: navigazione           una delle chiavi di dati/categorie.json
    anno: 2024
    ordine: 100                      ordine nelle slide (dentro il livello)
    parole: link, anchor, href       parole chiave per la ricerca
    esempio: esempi/stati-link/      esempio ricostruito (html+css+js, MIT)
    vedi: interaction-states, button schede collegate
    origine: slide 6                 da dove viene (slide 2026, riga del mining…)
    scritto: claude                  testo scritto da Claude (Gradiente IA 4), da rivedere
    fonti:
      - https://… | Titolo           fonti e «courtesy»
    letture:
      - https://… | Titolo           approfondimenti
    ---

    ## it
    # Nome in italiano
    Note in Markdown (paragrafi, elenchi «- », [link](url), **grassetto**).

    ## en
    # Name in English
    …

    ## fr
    ## zh

Una sezione di lingua vuota vuol dire «da tradurre».
"""
import json
import re
from pathlib import Path

RADICE = Path(__file__).resolve().parent.parent
CARTELLA = RADICE / 'dati' / 'componenti'
LINGUE = ('it', 'en', 'fr', 'zh')
LIVELLI = ('introduzione', 'fondamentale', 'avanzato')
CAMPI = ('id', 'livello', 'categoria', 'anno', 'ordine', 'parole', 'esempio', 'vedi', 'origine', 'scritto')
ELENCHI = ('fonti', 'letture')
VIRGOLE = ('parole', 'vedi')


def categorie():
    return json.loads((RADICE / 'dati' / 'categorie.json').read_text())


def leggi(percorso):
    testo = Path(percorso).read_text()
    m = re.match(r'---\n(.*?)\n---\n(.*)', testo, re.S)
    if not m:
        raise ValueError(f'{percorso}: manca l\'intestazione ---')
    s = {k: '' for k in CAMPI}
    s.update({k: [] for k in ELENCHI})
    elenco = None
    for riga in m.group(1).split('\n'):
        if not riga.strip():
            continue
        if riga.startswith('  - ') and elenco:
            url, _, titolo = riga[4:].partition(' | ')
            s[elenco].append({'url': url.strip(), 'titolo': titolo.strip()})
            continue
        chiave, _, valore = riga.partition(':')
        chiave, valore = chiave.strip(), valore.strip()
        if chiave in ELENCHI:
            elenco = chiave
        elif chiave in CAMPI:
            elenco = None
            s[chiave] = valore
        else:
            raise ValueError(f'{percorso}: campo sconosciuto «{chiave}»')
    for k in VIRGOLE:
        s[k] = [v.strip() for v in s[k].split(',') if v.strip()] if s[k] else []
    for k in ('anno', 'ordine'):
        s[k] = int(s[k]) if str(s[k]).strip() else 0
    s['testi'] = {}
    parti = re.split(r'^## (\w+)\s*$', m.group(2), flags=re.M)
    for i in range(1, len(parti), 2):
        lingua, corpo = parti[i], parti[i + 1].strip('\n')
        nome, note = '', corpo
        t = re.match(r'# ([^\n]*)\n?(.*)', corpo, re.S)
        if t:
            nome, note = t.group(1).strip(), t.group(2).strip()
        s['testi'][lingua] = {'nome': nome, 'note': note.strip()}
    for l in LINGUE:
        s['testi'].setdefault(l, {'nome': '', 'note': ''})
    return s


def scrivi(s, percorso=None):
    righe = ['---']
    for k in CAMPI:
        v = s.get(k)
        if isinstance(v, list):
            v = ', '.join(v)
        if v not in (None, '', 0):
            righe.append(f'{k}: {v}')
    for k in ELENCHI:
        if s.get(k):
            righe.append(f'{k}:')
            righe += [f'  - {x["url"]} | {x["titolo"]}'.rstrip(' |') for x in s[k]]
    righe.append('---')
    for l in LINGUE:
        t = s['testi'].get(l, {})
        righe += ['', f'## {l}']
        if t.get('nome'):
            righe.append(f'# {t["nome"]}')
        if t.get('note'):
            righe.append(t['note'])
    testo = '\n'.join(righe) + '\n'
    percorso = Path(percorso or CARTELLA / f'{s["id"]}.md')
    percorso.parent.mkdir(parents=True, exist_ok=True)
    percorso.write_text(testo)
    return percorso


def tutte():
    return sorted((leggi(p) for p in CARTELLA.glob('*.md')),
                  key=lambda s: (LIVELLI.index(s['livello']) if s['livello'] in LIVELLI else 9, s['ordine'], s['id']))
