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
Lo stato redazionale non va nelle schede (sono pubbliche): sta in riservato/stato.json, fuori da git.
Un vecchio campo «scritto: …» in una scheda viene spostato lì da sposta_riservati() (lo chiama costruisci.py).
"""
import json
import re
from pathlib import Path

RADICE = Path(__file__).resolve().parent.parent
CARTELLA = RADICE / 'dati' / 'componenti'
LINGUE = ('it', 'en', 'fr', 'zh')
LIVELLI = ('introduzione', 'fondamentale', 'avanzato')
CAMPI = ('id', 'livello', 'categoria', 'anno', 'ordine', 'parole', 'esempio', 'vedi', 'origine')
ELENCHI = ('fonti', 'letture')
VIRGOLE = ('parole', 'vedi')


RISERVATO = RADICE / 'riservato' / 'stato.json'   # fuori da git (.gitignore a elenco di permessi)


def sposta_riservati():
    """toglie dalle schede il campo «scritto:» (chi ha scritto il testo) e lo annota in RISERVATO"""
    dati = json.loads(RISERVATO.read_text()) if RISERVATO.exists() else {}
    scritti = dati.setdefault('scritto', {})
    spostati = 0
    for f in sorted(CARTELLA.glob('*.md')):
        testo = f.read_text()
        m = re.search(r'^scritto:[ \t]*(.*)\n', testo.split('\n---\n', 1)[0] + '\n', re.M)
        if not m:
            continue
        scritti[f.stem] = m.group(1).strip()
        f.write_text(testo.replace(m.group(0), '', 1))
        spostati += 1
    if spostati:
        dati['nota'] = 'Chi ha scritto il testo delle schede. Riservato: non va nel repo pubblico.'
        RISERVATO.parent.mkdir(exist_ok=True)
        RISERVATO.write_text(json.dumps(dati, ensure_ascii=False, indent=1) + '\n')
    return spostati


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
