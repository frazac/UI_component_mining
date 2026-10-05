#!/usr/bin/env python3
"""
Genera le pagine dalle schede (dati/componenti/*.md), solo libreria standard:
  dati/componenti.json   tutti i dati, per chi li vuole riusare
  index.html             la grande tabella (ricerca, filtri, 4 lingue)
  slide.html             le slide (una per componente, 4 lingue; ?lingua=xx per il PDF)
Uso: python3 strumenti/costruisci.py
"""
import html
import json
import re
from datetime import date
from pathlib import Path

import schede

R = schede.RADICE
LINGUE = schede.LINGUE
CAT = schede.categorie()

VERSIONE = (R / 'VERSION').read_text().strip() if (R / 'VERSION').exists() else '0'

T = {  # testi fissi dell'interfaccia
    'titolo': {'it': 'UI Design: i componenti', 'en': 'UI Design: Components', 'fr': 'UI Design : les composants', 'zh': 'UI 设计：界面组件'},
    'sottotitolo': {'it': 'Una carrellata ragionata dei componenti di interfaccia, dai fondamentali a quelli avanzati.',
                    'en': 'A reasoned overview of interface components, from the fundamental to the advanced.',
                    'fr': 'Un panorama raisonné des composants d\'interface, des fondamentaux aux plus avancés.',
                    'zh': '界面组件的系统梳理：从基础组件到进阶组件。'},
    'intro': {'it': 'Nata come «mining» in aula con gli studenti del corso di UI Design (NABA, Milano) e cresciuta in un catalogo. '
                    'Ogni componente ha la sua fonte; gli esempi sono ricostruiti in HTML, CSS e JavaScript.',
              'en': 'Born as classroom "mining" with the students of the UI Design course (NABA, Milan) and grown into a catalogue. '
                    'Every component has its source; the examples are rebuilt in HTML, CSS and JavaScript.',
              'fr': 'Né d\'un « mining » en classe avec les étudiants du cours d\'UI Design (NABA, Milan), devenu un catalogue. '
                    'Chaque composant a sa source ; les exemples sont reconstruits en HTML, CSS et JavaScript.',
              'zh': '源自 NABA（米兰）UI 设计课程中与学生一起进行的课堂“挖掘”，逐渐发展为一份目录。每个组件都注明出处；示例均以 HTML、CSS 和 JavaScript 重新制作。'},
    'cerca': {'it': 'Cerca un componente…', 'en': 'Search a component…', 'fr': 'Chercher un composant…', 'zh': '搜索组件…'},
    'tutte': {'it': 'Tutte le categorie', 'en': 'All categories', 'fr': 'Toutes les catégories', 'zh': '全部类别'},
    'tutti': {'it': 'Tutti', 'en': 'All', 'fr': 'Tous', 'zh': '全部'},
    'nome': {'it': 'Nome', 'en': 'Name', 'fr': 'Nom', 'zh': '名称'},
    'note': {'it': 'Note', 'en': 'Notes', 'fr': 'Notes', 'zh': '说明'},
    'categoria': {'it': 'Categoria', 'en': 'Category', 'fr': 'Catégorie', 'zh': '类别'},
    'livello': {'it': 'Livello', 'en': 'Level', 'fr': 'Niveau', 'zh': '层级'},
    'anno': {'it': 'Anno', 'en': 'Year', 'fr': 'Année', 'zh': '年份'},
    'fonti': {'it': 'Fonti', 'en': 'Sources', 'fr': 'Sources', 'zh': '来源'},
    'letture': {'it': 'Approfondimenti', 'en': 'Further reading', 'fr': 'Pour aller plus loin', 'zh': '延伸阅读'},
    'vedi': {'it': 'Vedi anche', 'en': 'See also', 'fr': 'Voir aussi', 'zh': '另见'},
    'esempio': {'it': 'Esempio', 'en': 'Example', 'fr': 'Exemple', 'zh': '示例'},
    'componenti': {'it': 'componenti', 'en': 'components', 'fr': 'composants', 'zh': '个组件'},
    'nessuno': {'it': 'Nessun componente corrisponde alla ricerca.', 'en': 'No component matches your search.',
                'fr': 'Aucun composant ne correspond à la recherche.', 'zh': '没有符合搜索条件的组件。'},
    'slide': {'it': 'Le slide', 'en': 'Slides', 'fr': 'Les diapositives', 'zh': '幻灯片'},
    'tabella': {'it': 'La tabella', 'en': 'Table', 'fr': 'Le tableau', 'zh': '表格'},
    'claude': {'it': 'Testo di Claude, da rivedere', 'en': 'Text by Claude, to be reviewed', 'fr': 'Texte de Claude, à relire', 'zh': '由 Claude 撰写，待审阅'},
    'da-ricostruire': {'it': 'Esempio da ricostruire', 'en': 'Example to be rebuilt', 'fr': 'Exemple à reconstruire', 'zh': '示例待重建'},
    'licenza': {'it': 'Testi, tabella e slide: CC BY-NC-SA 4.0. Codice degli esempi: MIT.',
                'en': 'Texts, table and slides: CC BY-NC-SA 4.0. Example code: MIT.',
                'fr': 'Textes, tableau et diapositives : CC BY-NC-SA 4.0. Code des exemples : MIT.',
                'zh': '文字、表格与幻灯片：CC BY-NC-SA 4.0。示例代码：MIT。'},
    'gradiente': {'it': 'Gradiente IA, livello 4 (Regia): l\'autore dirige, l\'IA produce bozze, traduzioni e codice; tutto è rivisto da persone.',
                  'en': 'Gradient AI, level 4 (Directing): the author directs, AI drafts texts, translations and code; everything is reviewed by people.',
                  'fr': 'Gradient IA, niveau 4 (Régie) : l\'auteur dirige, l\'IA rédige brouillons, traductions et code ; tout est relu par des personnes.',
                  'zh': 'Gradient AI 第 4 级（导演）：作者主导，AI 起草文字、翻译和代码；所有内容均由人工审阅。'},
    'versione': {'it': 'Versione', 'en': 'Version', 'fr': 'Version', 'zh': '版本'},
}
T['cookie'] = {'it': 'Solo cookie tecnici, per statistiche anonime e aggregate con matomo.masterismi.com.',
               'en': 'Technical cookies only, for anonymous, aggregated analytics via matomo.masterismi.com.',
               'fr': 'Cookies techniques uniquement, pour des statistiques anonymes et agrégées via matomo.masterismi.com.',
               'zh': '仅使用技术性 Cookie，通过 matomo.masterismi.com 进行匿名汇总统计。'}
T['revisori'] = {'it': 'Revisione delle traduzioni', 'en': 'Translation proofreading', 'fr': 'Relecture des traductions', 'zh': '译文审校'}
# statistiche Matomo (come le pagine in resources/), solo sul sito pubblicato: niente in locale né nei PDF
MATOMO = '''<script>
  if (/github\\.io$/.test(location.hostname)) {
    var _paq = window._paq = window._paq || [];
    _paq.push(['trackPageView']); _paq.push(['enableLinkTracking']);
    (function () { var u = 'https://matomo.masterismi.com/'; _paq.push(['setTrackerUrl', u + 'matomo.php']); _paq.push(['setSiteId', '15']);
      var d = document, g = d.createElement('script'), s = d.getElementsByTagName('script')[0]; g.async = true; g.src = u + 'matomo.js'; s.parentNode.insertBefore(g, s); })();
  }
</script>'''
AUTORE = 'Francesco Zaccaria'
GRADIENTE = 'https://frazac.github.io/gradient-ai/'
LICENZA = 'https://creativecommons.org/licenses/by-nc-sa/4.0/'


def e(s):
    return html.escape(str(s), quote=True)


def inline(s):
    s = e(s)
    s = re.sub(r'\[([^\]]+)\]\((https?://[^)\s]+)\)', lambda m: f'<a href="{m.group(2)}" target="_blank" rel="noopener">{m.group(1)}</a>', s)
    return re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)


def md(testo):
    """Markdown minimo: paragrafi, elenchi «- », link, grassetto."""
    out = []
    for blocco in re.split(r'\n\s*\n', testo.strip()):
        righe = blocco.split('\n')
        if all(r.startswith('- ') for r in righe):
            out.append('<ul>' + ''.join(f'<li>{inline(r[2:])}</li>' for r in righe) + '</ul>')
        elif blocco.strip():
            out.append('<p>' + '<br>'.join(inline(r) for r in righe) + '</p>')
    return ''.join(out)


def piatto(testo):
    return re.sub(r'\s+', ' ', re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', testo.replace('**', ''))).strip()


def varianti(valori, tag='span', blocco=False, attr=''):
    """Un <tag data-l="xx"> per lingua. valori: dict lingua → html già pronto."""
    return ''.join(f'<{tag} data-l="{l}"{attr}>{valori.get(l, "")}</{tag}>' for l in LINGUE)


def tt(chiave):
    return varianti({l: e(T[chiave][l]) for l in LINGUE})


def nomi(s):
    return varianti({l: e(s['testi'][l]['nome']) for l in LINGUE})


def note(s):
    return varianti({l: md(s['testi'][l]['note']) for l in LINGUE}, tag='div')


def cat(s):
    return varianti({l: e(CAT['categorie'][s['categoria']][l]) for l in LINGUE})


def liv(s):
    return varianti({l: e(CAT['livelli'][s['livello']][l]) for l in LINGUE})


def dominio(u):
    return re.sub(r'^https?://(www\.)?([^/]+).*', r'\2', u)


def link_md(x):
    titolo = x['titolo'] or dominio(x['url'])
    return (f'<a class="link-md" href="{e(x["url"])}" target="_blank" rel="noopener">{e(titolo)}'
            f'<span class="u">{e(dominio(x["url"]))}</span></a>')


def testa(titolo, css_extra=''):
    return f'''<!doctype html>
<html lang="en" data-lingua="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{e(titolo)}</title>
  <meta name="description" content="{e(T['sottotitolo']['en'])}">
  <meta name="author" content="{AUTORE}">
  <link rel="icon" type="image/svg+xml" href="favicon.svg">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;700&family=Noto+Sans+SC:wght@400;500;700&display=swap">
  <link rel="stylesheet" href="assets/componenti.css?v={VERSIONE}">{css_extra}
  <script src="assets/lingua.js?v={VERSIONE}"></script>
</head>
'''


def colophon():
    return f'''<footer class="colophon">
  <p>© 2024–{date.today().year} {AUTORE} · <a href="{LICENZA}" target="_blank" rel="noopener">CC BY-NC-SA 4.0</a> · {tt('licenza')}</p>
  <p><a href="{GRADIENTE}" target="_blank" rel="noopener">{tt('gradiente')}</a></p>
  <p>{revisori()}</p>
  <p>{tt('versione')} {e(VERSIONE)} · <a href="https://github.com/frazac/UI_component_mining" target="_blank" rel="noopener">GitHub</a> · <a href="https://linktr.ee/frazac" target="_blank" rel="noopener">Linktree</a></p>
  <p>{tt('cookie')}</p>
</footer>'''


def revisori():
    """Colophon dei proof reader da dati/revisori.json: [{"nome", "lingue": ["en"], "instagram", "github"}]."""
    f = R / 'dati' / 'revisori.json'
    persone = json.loads(f.read_text()) if f.exists() else []
    if not persone:
        return ''
    voci = []
    for p in persone:
        link = ' '.join(f'<a href="{e(u)}" target="_blank" rel="noopener">{k}</a>' for k, u in
                        (('Instagram', p.get('instagram')), ('GitHub', p.get('github'))) if u)
        voci.append(f'{e(p["nome"])} ({", ".join(l.upper() for l in p["lingue"])}) {link}'.strip())
    return f'{tt("revisori")}: ' + ' · '.join(voci)


# --- tabella ---------------------------------------------------------------

def riga(s, per_id):
    cerca = {l: piatto(' '.join([s['testi'][l]['nome'], s['testi'][l]['note'], s['testi']['en']['nome'],
                                 CAT['categorie'][s['categoria']][l], ' '.join(s['parole'])])).lower() for l in LINGUE}
    attr = ' '.join(f'data-cerca-{l}="{e(cerca[l])}"' for l in LINGUE)
    collegamenti = ''
    for chiave in ('fonti', 'letture'):
        if s[chiave]:
            collegamenti += f'<p class="piccolo"><b>{tt(chiave)}</b> ' + ' '.join(link_md(x) for x in s[chiave]) + '</p>'
    if s['vedi']:
        collegamenti += f'<p class="piccolo"><b>{tt("vedi")}</b> ' + ', '.join(
            f'<a href="#{v}">{nomi(per_id[v])}</a>' for v in s['vedi'] if v in per_id) + '</p>'
    if s['esempio']:
        nome_es = s['esempio'].rstrip('/').split('/')[-1]
        collegamenti += f'<p class="piccolo"><b>{tt("esempio")}</b> <a href="{e(s["esempio"])}" target="_blank">{e(nome_es)}</a></p>'
    claude = f'<span class="claude" title="{e(T["claude"]["en"])}">{tt("claude")}</span>' if s['scritto'] == 'claude' else ''
    return (f'<tr id="{e(s["id"])}" data-livello="{s["livello"]}" data-categoria="{s["categoria"]}" data-anno="{s["anno"]}" {attr}>'
            f'<th scope="row"><a class="ancora" href="#{e(s["id"])}">{nomi(s)}</a></th>'
            f'<td class="note">{note(s)}{claude}{collegamenti}</td>'
            f'<td>{cat(s)}</td><td>{liv(s)}</td><td>{s["anno"] or ""}</td></tr>')


def tabella(tutte):
    per_id = {s['id']: s for s in tutte}
    opzioni = ''.join(f'<option value="{k}" data-it="{e(v["it"])}" data-en="{e(v["en"])}" data-fr="{e(v["fr"])}" data-zh="{e(v["zh"])}">{e(v["en"])}</option>'
                      for k, v in CAT['categorie'].items())
    livelli = ''.join(f'<button type="button" class="chip" data-livello="{k}" aria-pressed="false">{varianti({l: e(v[l]) for l in LINGUE})}</button>'
                      for k, v in CAT['livelli'].items())
    righe = '\n'.join(riga(s, per_id) for s in tutte)
    return testa('UI Design: Components — table · Francesco Zaccaria') + f'''<body class="pagina-tabella">
<header class="testata">
  <nav class="viste"><a aria-current="page" href="index.html">{tt('tabella')}</a> <a href="slide.html">{tt('slide')}</a></nav>
  <h1>{tt('titolo')}</h1>
  <p class="sottotitolo">{tt('sottotitolo')}</p>
  <p class="intro">{tt('intro')}</p>
</header>
<form class="filtri" role="search" onsubmit="return false">
  <input type="search" id="cerca" autocomplete="off" data-it="{e(T['cerca']['it'])}" data-en="{e(T['cerca']['en'])}" data-fr="{e(T['cerca']['fr'])}" data-zh="{e(T['cerca']['zh'])}" placeholder="{e(T['cerca']['en'])}">
  <div class="chips"><button type="button" class="chip" data-livello="" aria-pressed="true">{tt('tutti')}</button>{livelli}</div>
  <select id="categoria"><option value="" data-it="{e(T['tutte']['it'])}" data-en="{e(T['tutte']['en'])}" data-fr="{e(T['tutte']['fr'])}" data-zh="{e(T['tutte']['zh'])}">{e(T['tutte']['en'])}</option>{opzioni}</select>
  <p class="conteggio"><output id="conteggio">{len(tutte)}</output> {tt('componenti')}</p>
</form>
<main>
<table class="componenti">
<thead><tr><th scope="col">{tt('nome')}</th><th scope="col">{tt('note')}</th><th scope="col">{tt('categoria')}</th><th scope="col">{tt('livello')}</th><th scope="col">{tt('anno')}</th></tr></thead>
<tbody>
{righe}
</tbody>
</table>
<p class="vuoto" hidden>{tt('nessuno')}</p>
</main>
{colophon()}
<script src="assets/tabella.js?v={VERSIONE}"></script>
{MATOMO}
</body>
</html>
'''


# --- slide -----------------------------------------------------------------

def slide_componente(s, n):
    lunghezza = max(len(s['testi'][l]['note']) for l in LINGUE)
    classe = 'lungo' if lunghezza > 700 else 'medio' if lunghezza > 350 else ''
    es = s['esempio'] + ('index.html' if s['esempio'].endswith('/') else '')
    if es.endswith('.html'):
        figura = f'<figure class="esempio"><iframe src="{e(es)}" loading="lazy" title="{e(s["testi"]["en"]["nome"])}"></iframe></figure>'
    elif re.search(r'\.(jpe?g|png|gif|svg|webp)$', es):
        figura = f'<figure class="esempio"><img src="{e(es)}" alt="" loading="lazy"></figure>'
    else:
        figura = f'<figure class="esempio da-ricostruire"><p>{tt("da-ricostruire")}</p></figure>'
    fonti = s['fonti'] + s['letture']
    piede = '<p class="fonte-breve">' + '<br>'.join(link_md(x) for x in fonti[:4]) + '</p>' if fonti else ''
    nome_en = f'<p class="nome-en">{e(s["testi"]["en"]["nome"])}</p>'
    return f'''<section class="slide s-componente {classe}" id="{e(s['id'])}" data-cap-it="{e(CAT['categorie'][s['categoria']]['it'])}" data-cap-en="{e(CAT['categorie'][s['categoria']]['en'])}" data-cap-fr="{e(CAT['categorie'][s['categoria']]['fr'])}" data-cap-zh="{e(CAT['categorie'][s['categoria']]['zh'])}">
  <div class="colonna">
    <p class="etichetta">{liv(s)} · {cat(s)}</p>
    <h2>{nomi(s)}</h2>
    {nome_en}
    <div class="testo">{note(s)}</div>
  </div>
  {figura}
  {piede}
</section>'''


def slide(tutte):
    parti = [f'''<section class="slide s-copertina senza-pie">
  <p class="etichetta">NABA — Interface Design · UI_component_mining</p>
  <h1 class="strillo">{tt('titolo')}</h1>
  <div><p class="meta">{AUTORE}<br>{tt('sottotitolo')}</p></div>
</section>''']
    livello = None
    n = 1
    for s in tutte:
        if s['livello'] != livello:
            livello = s['livello']
            quanti = sum(1 for x in tutte if x['livello'] == livello)
            parti.append(f'''<section class="slide s-sezione senza-pie">
  <p class="etichetta">{quanti} {tt('componenti')}</p>
  <h2 class="strillo">{varianti({l: e(CAT['livelli'][livello][l]) for l in LINGUE})}</h2>
</section>''')
        n += 1
        parti.append(slide_componente(s, n))
    parti.append(f'''<section class="slide s-crediti senza-pie">
  <h2>{AUTORE}</h2>
  <p>{tt('intro')}</p>
  <p>© 2024–{date.today().year} {AUTORE} · <a href="{LICENZA}">CC BY-NC-SA 4.0</a> · {tt('licenza')}</p>
  <p>{tt('gradiente')}</p>
  <p>{tt('versione')} {e(VERSIONE)} · github.com/frazac/UI_component_mining</p>
</section>''')
    return testa('UI Design: Components — slides · Francesco Zaccaria',
                 f'\n  <link rel="stylesheet" href="assets/slide-print.css?v={VERSIONE}" media="print">') + \
        '<body class="pagina-slide">\n' + '\n\n'.join(parti) + f'\n{MATOMO}\n</body>\n</html>\n'


def readme_revisori():
    """Riscrive nel README il blocco <!-- revisori --> dal file dati/revisori.json (colophon dei proof reader)."""
    f, readme = R / 'dati' / 'revisori.json', R / 'README.md'
    persone = json.loads(f.read_text()) if f.exists() else []
    if not persone or not readme.exists():
        return
    righe = ['<!-- revisori -->', '### Proofreaders', '']
    for p in persone:
        link = ' · '.join(f'[{k}]({u})' for k, u in (('Instagram', p.get('instagram')), ('GitHub', p.get('github'))) if u)
        righe.append(f'- **{p["nome"]}** — {", ".join(l.upper() for l in p["lingue"])}' + (f' — {link}' if link else ''))
    righe.append('<!-- /revisori -->')
    testo = readme.read_text()
    nuovo = re.sub(r'<!-- revisori -->.*?<!-- /revisori -->', lambda m: '\n'.join(righe), testo, flags=re.S)
    if nuovo != testo:
        readme.write_text(nuovo)


def json_dati(tutte):
    return json.dumps({'versione': VERSIONE, 'categorie': CAT, 'componenti': tutte}, ensure_ascii=False, indent=1)


if __name__ == '__main__':
    tutte = schede.tutte()
    (R / 'dati' / 'componenti.json').write_text(json_dati(tutte))
    (R / 'index.html').write_text(tabella(tutte))
    (R / 'slide.html').write_text(slide(tutte))
    readme_revisori()
    mancano = [(s['id'], l) for s in tutte for l in LINGUE if not (s['testi'][l]['nome'] and (s['testi'][l]['note'] or not s['testi']['en']['note']))]
    print(f'{len(tutte)} componenti → index.html, slide.html, dati/componenti.json')
    if mancano:
        print(f'{len(mancano)} testi da tradurre (es. {mancano[:3]})')
