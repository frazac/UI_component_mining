# UI Design: Components

A reasoned overview of user-interface components, from the fundamental ones (links, buttons, selectors,
forms…) to the advanced ones mined in class (command palette, skeleton screen, slash commands, read receipts…).
Two formats, four languages: **Italiano, English, Français, 中文**.

- **Table** — searchable, with filters by level and category: <https://frazac.github.io/UI_component_mining/>
- **Slides** — one slide per component: <https://frazac.github.io/UI_component_mining/slide.html>
  (PDFs are distributed to the students of the course)
- **Data** — every component as plain text in [`dati/componenti/`](dati/componenti/), all of them in
  [`dati/componenti.json`](dati/componenti.json)

Born as classroom "mining" with the students of the UI Design course by
[Francesco Zaccaria](https://linktr.ee/frazac) at NABA, Milan, and grown into a catalogue.
Every component has its source; the examples are **rebuilt from scratch** in HTML, CSS and JavaScript
([`esempi/`](esempi/)), so that no third-party screenshots or code are redistributed.

## How it works

One card per component, `dati/componenti/<id>.md`: a short header (level, category, keywords, sources,
further reading, example) and four sections, `## it`, `## en`, `## fr`, `## zh`, each with the name and the notes.
The format is described at the top of [`strumenti/schede.py`](strumenti/schede.py).

```bash
python3 strumenti/costruisci.py      # cards → index.html, slide.html, dati/componenti.json
python3 strumenti/pdf.py             # slides → one PDF per language (needs Google Chrome)
```

Only the Python standard library is needed. The same cards are used, through `git subtree`, in the
course's slides, and can be edited from either side.

## Languages and proofreading

Italian and English come from the author. French and Chinese translations, and the descriptions of the
components that only had a name, were drafted with AI and are marked as *to be reviewed* until a human
proofreader checks them sentence by sentence. Machine translation is not enough: every language has a
proofreader with a name, credited below.

<!-- revisori -->
### Proofreaders

None yet. Would you like to proofread French or Chinese? Get in touch via [Linktree](https://linktr.ee/frazac).
<!-- /revisori -->

## AI

This project is at level 4 (*Directing*) of the [Gradient AI](https://frazac.github.io/gradient-ai/):
the author directs; AI drafts texts, translations and code; everything is reviewed by people.

## License

- Texts, table, slides and images: [CC BY-NC-SA 4.0](LICENSE) — attribution, non-commercial, share alike.
- Source code (examples in `esempi/` and `resources/`, scripts in `strumenti/`, files in `assets/`): [MIT](LICENSE-CODE).

Until October 2026 the repository was released under GPL-3.0; copies obtained under that license keep it.
Component names, products and brands mentioned belong to their owners and are cited for educational analysis.
If something is attributed incorrectly, please write via [Linktree](https://linktr.ee/frazac).

© 2024–2026 Francesco Zaccaria
