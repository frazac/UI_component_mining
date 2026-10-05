#!/usr/bin/env python3
"""
Importazione una tantum (2026-10-05): slide «UI Design: Fundamental Components» (2026, IT/EN)
+ tabella del mining (index.html, 86 righe) → dati/componenti/<id>.md.
Testi in inglese come nelle fonti; nomi italiani dalle slide. FR, ZH (e IT delle note) si aggiungono dopo.
Uso: python3 strumenti/importa_2026.py righe.json   (righe.json = estrazione della tabella del mining)
"""
import json
import re
import sys

import schede

L = lambda url, titolo='': {'url': url, 'titolo': titolo}


def scheda(id, livello, categoria, ordine, en, it='', note='', anno=2024, parole='', esempio='', vedi='',
           origine='', fonti=(), letture=(), scritto=''):
    return {'id': id, 'livello': livello, 'categoria': categoria, 'anno': anno, 'ordine': ordine,
            'parole': [p.strip() for p in parole.split(',') if p.strip()], 'esempio': esempio,
            'vedi': [v.strip() for v in vedi.split(',') if v.strip()], 'origine': origine, 'scritto': scritto,
            'fonti': list(fonti), 'letture': list(letture),
            'testi': {'it': {'nome': it, 'note': ''}, 'en': {'nome': en, 'note': note.strip()},
                      'fr': {'nome': '', 'note': ''}, 'zh': {'nome': '', 'note': ''}}}


TAMS = 'https://uxdesign.cc/button-design-user-interface-components-series-85243b6736c7'
FONDAMENTALI = [
    scheda('atomic-design', 'introduzione', 'introduzione', 10, 'Atomic design', 'Atomic design', origine='slide 3-5',
           parole='atoms, molecules, organisms, design system, Brad Frost',
           note='In the metaphor of "atomic design", atoms and molecules correspond to single or grouped components: '
                'atoms are the smallest building blocks (a label, an input, a button), molecules are simple groups of '
                'atoms working together (a search form).',
           fonti=[L('https://atomicdesign.bradfrost.com/chapter-2/', 'Atomic Design Methodology | Atomic Design by Brad Frost')]),
    scheda('design-systems', 'introduzione', 'introduzione', 20, 'Main sources: design systems', 'Fonti principali: i design system',
           origine='slide 41', parole='design system, Carbon, Atlassian, Material',
           note='The reasoned list is built on three reference design systems: IBM Carbon, Atlassian Design System and '
                'Google Material Design.',
           fonti=[L('https://carbondesignsystem.com/migrating/guide/overview/', 'Guide – Carbon Design System'),
                  L('https://atlassian.design/', 'Atlassian Design'),
                  L('https://m3.material.io/', "Material Design 3 - Google's latest open source design system")]),
    scheda('hyperlink', 'fondamentale', 'navigazione', 10, 'Hyperlink', 'Collegamento ipertestuale', origine='slide 6',
           parole='link, anchor, href, visited', vedi='interaction-states, button', esempio='resources/component-handout-states1.html',
           note='Links are the fundamental element that allows hypertexts to be linked together.\n\n'
                'Links have different interaction states: here are the standard HTML states.'),
    scheda('interaction-states', 'fondamentale', 'feedback', 20, 'Interaction states', 'Stati interattivi', origine='slide 7-9, mining 8',
           parole='hover, focus, active, visited, disabled, pressed, tab key', vedi='hyperlink, button, feedback',
           esempio='resources/component-handout-states2.html', anno=2024,
           note='Interaction states extend to all interactive components: links, buttons, draggable elements, forms, etc.\n\n'
                'The focus state can be operated from the keyboard and applies to only one component at a time: in web '
                'browsers it is managed with the tab key.\n\n'
                'In the example, a transparency scale is studied to make the components interoperable on different '
                'colour backgrounds: changing the background, the interaction states keep the same structure and are '
                'just calibrated depending on the contrast.',
           fonti=[L('https://uxdesign.cc/an-interaction-state-of-mind-705572b3ad51', 'An interaction state of mind | UX Collective'),
                  L('https://m3.material.io/foundations/interaction-states', 'Interaction states – Material Design 3')],
           letture=[L('https://uxplanet.org/focusing-on-buttons-e31d575953bd', 'Focusing on Buttons | by Carlota Antón | UX Planet'),
                    L('https://www.w3schools.com/css/tryit.asp?filename=trycss_link', 'W3Schools Tryit Editor'),
                    L('https://m2.material.io/design/interaction/states.html#usage', 'States - Material Design')]),
    scheda('feedback', 'fondamentale', 'feedback', 30, 'Feedback', 'Retroazione', origine='slide 10-11',
           parole='haptics, vibration, throbber, confirmation, principle', vedi='interaction-states',
           esempio='resources/component-handout-feedback.html',
           note='Feedback conveys pieces of information to the user in an interaction context.\n\n'
                'It is not a specific component but the principle that determines the existence of the different '
                'interaction states. It should be one of the guiding principles of UX and UI design: in human-machine '
                'interaction, a feedback message must always be given to the user in the shortest reasonable time. '
                'The interaction states:\n\n'
                '- default\n- mouse over (hover)\n- a click: press and release (a pulse)\n'
                '- throbber for the loading status\n- confirmation\n\n'
                'Feedback is not only visual. The word "haptics" derives from the Greek for "I touch": haptic feedback '
                '(vibrations and waveform patterns) is given by a vibrating component or actuator such as a resonant '
                'motor. The Motorola StarTAC was the first phone with vibration (1993); the first PlayStation haptic '
                'controller was released in North America in 1997.'),
    scheda('pointer', 'fondamentale', 'navigazione', 40, 'Pointer', 'Puntatore', origine='slide 12',
           parole='cursor, mouse, throbber, hourglass, wait cursor', vedi='text-caret',
           note='The cursor or pointer is a graphical element that mirrors the position and movement of a pointing '
                'device. The cursor can change appearance or interaction state depending on context and position. '
                'The most remarkable is the wait cursor ([throbber](https://en.wikipedia.org/wiki/Throbber)), depicted '
                'as an arrow in Apple macOS and as an hourglass in Microsoft Windows.',
           fonti=[L('https://developer.apple.com/design/human-interface-guidelines/pointing-devices', 'Apple Human Interface Guidelines (HIG)')],
           letture=[L('https://www.youtube.com/watch?v=B6rKUf9DWRI', '1968 "Mother of All Demos" by SRI\'s Doug Engelbart and Team - YouTube'),
                    L('https://ux.stackexchange.com/questions/52336/why-is-the-mouse-cursor-slightly-tilted-and-not-straight',
                      'Why is the mouse cursor slightly tilted and not straight? - User Experience Stack Exchange')]),
    scheda('breadcrumb', 'fondamentale', 'navigazione', 50, 'Breadcrumb', 'Briciole di pane', origine='slide 13',
           parole='hierarchy, path, location',
           note='Breadcrumbs represent the content structure by nesting and hierarchy; they do not represent the '
                'chronological navigation order. They are essential to give users a sense of their current location '
                'within the hierarchy.'),
    scheda('context-menu', 'fondamentale', 'azioni', 60, 'Contextual menu', 'Menu contestuale', origine='slide 14',
           parole='right-click, long press, copy, paste', vedi='kebab-menu',
           note='A contextual menu appears upon a user interaction, typically a right-click or a long press, offering a '
                'list of actions relevant to the selected item or area. Context menus give quick access to functions '
                'like copy, paste, delete, or features tailored to the context, enhancing usability by minimising '
                'navigation.'),
    scheda('selectors', 'fondamentale', 'input', 70, 'Selectors', 'Selettori', origine='slide 19',
           parole='radio, checkbox, switch, toggle', vedi='radio-button, checkbox, switch, dropdown-filter',
           note='Selectors such as radio buttons, checkboxes and switches are essential tools to let users interact '
                'with interfaces clearly and efficiently. The choice depends on the number of options and on the '
                'selection context:\n\n'
                '- radio buttons: one choice among a few options;\n'
                '- checkboxes: multiple selections on few or more options;\n'
                '- switches: an on/off decision for just one option.\n\n'
                'Effective design considers not only aesthetics and accessibility but also the number of options, to '
                'ensure a smooth and intuitive experience.',
           letture=[L('https://uxdesign.cc/ui-cheat-sheet-radio-buttons-checkboxes-and-other-selectors-bf56777ad59e',
                      'UI cheat sheet: radio buttons, checkboxes, and other selectors | Tess Gadd')]),
    scheda('dropdown-filter', 'fondamentale', 'input', 71, 'Dropdown selector with filtering', 'Selettore a tendina con filtro',
           origine='slide 15', parole='dropdown, combobox, select, autocomplete, filter', vedi='selectors, predictive-input',
           note='Several components combined: text filter, button and drop-down list. The dropdown lets users select '
                'options from a menu; the filter lets them quickly narrow down the options by typing keywords, which '
                'is particularly useful with long lists. It reduces cognitive load and improves selection efficiency.'),
    scheda('radio-button', 'fondamentale', 'input', 72, 'Radio button', 'Pulsante di opzione («radio»)', origine='slide 16',
           parole='option, single choice', vedi='selectors',
           note='One choice among a few mutually exclusive options.',
           fonti=[L('https://m3.material.io/components/radio-button/overview', 'Radio button – Material Design 3')]),
    scheda('checkbox', 'fondamentale', 'input', 73, 'Checkbox', 'Casella di spunta (checkbox)', origine='slide 17',
           parole='tick, multiple choice, indeterminate', vedi='selectors',
           note='Multiple selections among few or more options.',
           fonti=[L('https://m3.material.io/components/checkbox/overview', 'Checkbox – Material Design 3')]),
    scheda('switch', 'fondamentale', 'input', 74, 'Switch', 'Interruttore (commutatore)', origine='slide 18',
           parole='toggle, on/off', vedi='selectors, dark-mode-switch',
           note='An on/off decision for just one option, applied immediately.',
           fonti=[L('https://m3.material.io/components/switch/overview', 'Switch – Material Design 3')]),
    scheda('button', 'fondamentale', 'azioni', 80, 'Button', 'Pulsante', origine='slide 20, 22, 24',
           parole='CTA, call to action, affordance, primary, secondary', vedi='hyperlink, ghost-button, badge, floating-action-button, tooltip',
           note='A button is a fundamental component designed to trigger an action, such as submitting a form or '
                'navigating to another page. It must be easily recognisable as a button, through visual cues '
                '(affordances) like distinct shapes, borders, colours, shadows. Appearance and positioning affect the '
                'recognition of a button.\n\n'
                'While similar to hyperlinks in enabling navigation, buttons are typically used for tasks, actions or '
                'commands within an application, whereas hyperlinks are primarily meant to navigate to other pages or '
                'resources. Keeping this distinction maintains clarity and usability.',
           fonti=[L(TAMS, 'Button design — UI components series | Taras Bakusevych | UX Collective')],
           letture=[L('https://uxdesign.cc/ui-cheat-sheets-buttons-7329ed9d6112', 'UI cheat sheet: buttons | UX Collective')]),
    scheda('ghost-button', 'fondamentale', 'azioni', 81, 'Ghost button', 'Pulsante fantasma (ghost button)', origine='slide 21',
           parole='outline, secondary action, transparent', vedi='button', esempio='resources/component-ghost-button.html',
           note='A minimalist button with a transparent or semi-transparent background and a simple border. The subtle '
                'styling makes it less prominent: it is often used for secondary or tertiary actions, so as not to '
                'distract from primary buttons.\n\n'
                'Like all buttons, it must remain recognisable as interactive, through clear outlines, hover effects or '
                'text cues. Ghost buttons may resemble hyperlinks, but they are reserved for actions within an '
                'application.'),
    scheda('badge', 'fondamentale', 'feedback', 82, 'Badge', 'Badge', origine='slide 23', parole='count, status, dot, notification',
           vedi='button, notification-system',
           note='An extension of a button or icon that provides additional information like counts or statuses.'),
    scheda('floating-action-button', 'fondamentale', 'azioni', 83, 'Floating Action Button (FAB)', 'Pulsante d\'azione fluttuante (FAB)',
           origine='slide 23', parole='FAB, primary action, mobile', vedi='button',
           note='A circular button, often used to represent the primary action in mobile and web interfaces.',
           fonti=[L('https://m3.material.io/components/floating-action-button/overview', 'FAB – Material Design 3')]),
    scheda('tooltip', 'fondamentale', 'feedback', 84, 'Tooltip', 'Tooltip (suggerimento)', origine='slide 23',
           parole='hint, hover, help', vedi='button',
           note='A small label that offers contextual guidance about an element, usually shown on hover or focus.',
           letture=[L('https://www.thedesignerstoolbox.com/design-system/when-to-use-tooltips/', "When to use tooltips in UX design - The Designer's Toolbox")]),
    scheda('tag-chip', 'fondamentale', 'contenuti', 90, 'Tag and chip', 'Tag e chip', origine='slide 25',
           parole='label, category, filter, metadata', vedi='label, image-tags', esempio='resources/component-tag.html',
           note='A tag is used to categorise, label or highlight content, often providing quick context or metadata '
                'about the associated item. Tags are typically small, stylised text elements, sometimes with icons, '
                'and may be interactive (clickable to filter or manage content). When they include icons or other '
                'elements they are often called "chips", after the name given by Google\'s Material Design library.',
           letture=[L('https://m3.material.io/components/chips/specs', 'Chips – Material Design 3')]),
    scheda('modal', 'fondamentale', 'contenitori', 100, 'Modal, overlay and dialog box', 'Modale, overlay e finestra di dialogo',
           origine='slide 26, 37', parole='dialog, lightbox, backdrop, popup', vedi='irreversible-action-warning, sheet',
           note='Modals let users act on-page without leaving the current page, staying in context. They are often used '
                'for dialog boxes (the software has to ask something to go on) or to show bigger images.',
           fonti=[L('https://itnext.io/managing-modals-with-react-hooks-c9c55c458368', 'Evan Burbidge | itnext.io')],
           letture=[L('https://getbootstrap.com/docs/5.3/components/modal/', 'Modal · Bootstrap'),
                    L('https://www.w3schools.com/cssref/css3_pr_backdrop-filter.php', 'CSS backdrop-filter')]),
    scheda('input-form', 'fondamentale', 'input', 110, 'Input form', 'Form (modulo di inserimento dati)', origine='slide 27-29',
           parole='field, text box, registration, login, submit', vedi='live-validation, selectors',
           note='An input form lets users enter and submit data to a system. It consists of fields such as text boxes, '
                'checkboxes, radio buttons, drop-down menus and buttons, where users input names, email addresses, '
                'passwords or other data. The form captures the input and sends it to a server or database, as in '
                'registration, login or data submission.',
           fonti=[L('https://uxdesign.cc/text-fields-forms-design-ui-components-series-2b32b2beebd0',
                    'Text fields & Forms design — UI components series | Taras Bakusevych | UX Collective'),
                  L('https://makeitclear.com/ux-ui-tips-a-guide-to-creating-world-class-forms/', 'UX/UI tips: A guide to creating world class forms | makeitclear.com')]),
    scheda('pagination', 'fondamentale', 'navigazione', 120, 'Pagination system', 'Sistema di paginazione', origine='slide 30',
           parole='next, previous, page numbers, infinite scroll', vedi='page-dots',
           note='Pagination divides content into discrete pages, so that users can navigate large datasets or long '
                'content efficiently, with controls such as "Next", "Previous" and page numbers.\n\n'
                'It can be combined with infinite scrolling: the first pages load in sequence, then more content loads '
                'as the user scrolls, balancing usability and performance.',
           letture=[L('https://stevesohcot.medium.com/whats-the-ideal-pagination-from-a-ui-ux-perspective-d2d954a8126',
                      "What's The Ideal Pagination From A UI/UX Perspective? | Medium")]),
    scheda('bar-header', 'fondamentale', 'navigazione', 130, 'Bar (and header)', 'Barra (e intestazione)', origine='slide 31-32',
           parole='navbar, header, tabs, pills, menu', vedi='tab-audio-indicator, sticky',
           note='The navigation bar evolves over time (see Facebook 2010, 2019, 2022, 2025) and can be designed like '
                '"tabs" or "pills".',
           letture=[L('https://www.versionmuseum.com/history-of/facebook-website', '20 Years of Facebook Website Design History - Version Museum'),
                    L('https://www.w3schools.com/bootstrap/bootstrap_tabs_pills.asp', 'Bootstrap Tabs and Pills (W3Schools)')]),
    scheda('search-field', 'fondamentale', 'input', 140, 'Search field', 'Campo di ricerca', origine='slide 33',
           parole='search, query, results', vedi='predictive-input, prompt-suggestions',
           note='A combined component, always determined by the operation of the back end: the search is a request '
                '(query) to the database and produces a "view" of results.',
           fonti=[L('https://www.behance.net/gallery/28198219/CSS3-JQUERY-Search-Animation', 'Antonio Di Nardo | CSS3 + JQUERY - Search Animation | Behance')]),
    scheda('picker', 'fondamentale', 'input', 150, 'Picker', 'Selettore (picker)', origine='slide 34',
           parole='date, time, colour, wheel', vedi='calendar-picker, color-picker',
           note='There are various types of pickers: colour, time, date, etc.'),
    scheda('splash-page', 'fondamentale', 'feedback', 160, 'Splash page', 'Splash (schermata d\'avvio)', origine='slide 35',
           parole='launch screen, boot, branding', vedi='loading-screen', esempio='resources/splash-screen-exergo.jpg',
           note='A visually prominent introductory screen shown during a platform\'s initial boot or data loading. It is '
                'a branding touchpoint and gives immediate visual feedback. Two different best practices:\n\n'
                '- native apps: recommended. Splash screens mask technical latency and initialisation, reinforcing '
                'brand identity;\n'
                '- web: discouraged. Web users expect instant access; artificial delays increase bounce rates and '
                'hurt SEO and "Time to Interactive".',
           letture=[L('https://www.youtube.com/watch?v=PV9ThwQegks', "Web Apps vs. PWA vs. Hybrid vs. Native: What's the Difference? - YouTube")]),
    scheda('slider', 'fondamentale', 'input', 170, 'Slider', 'Cursore (slider)', origine='slide 36', parole='range, volume',
           note='Selects a value within a range by dragging a handle along a track.'),
    scheda('stepper', 'fondamentale', 'input', 171, 'Stepper', 'Stepper (incrementatore)', origine='slide 36',
           parole='spinner, number input, plus minus', note='Increases or decreases a numeric value step by step (called "spinner" in jQuery).'),
    scheda('toast', 'fondamentale', 'feedback', 180, 'Notification or "toast"', 'Notifica o «toast»', origine='slide 37',
           parole='snackbar, notification, message', vedi='notification-system',
           note='A brief, non-blocking message that appears and disappears on its own.'),
    scheda('progress-bar', 'fondamentale', 'feedback', 190, 'Progress bar', 'Barra di avanzamento', origine='slide 38',
           parole='loading, steps, stepper', vedi='loading-screen, skeleton-screen',
           note='Shows the progress of a process or of the steps of a procedure (sometimes called "stepper").'),
    scheda('data-table', 'fondamentale', 'contenitori', 200, 'Data table with filtering', 'Tabella di dati con filtri', origine='slide 38',
           parole='table, grid, filter, sort', vedi='sort-options', note='A table of data that users can filter (and often sort).'),
    scheda('carousel', 'fondamentale', 'contenitori', 210, 'Carousel', 'Carosello (slideshow)', origine='slide 39',
           parole='slideshow, slider, gallery', vedi='page-dots', note='Shows a series of items one at a time, in rotation.'),
    scheda('accordion', 'fondamentale', 'contenitori', 220, 'Accordion', 'Accordion («fisarmonica»)', origine='slide 39',
           parole='collapse, expand, disclosure', vedi='expand-collapse, faq',
           note='Stacked sections that expand and collapse to show or hide their content.'),
    scheda('pictograms', 'fondamentale', 'contenuti', 230, 'Pictograms and icons', 'Pittogrammi e icone', origine='slide 40',
           parole='icon, symbol, Otl Aicher, Lance Wyman, Fluent', vedi='emoji',
           note='From the pictograms of the 1968 Mexico City Olympic Games to the icons of Microsoft Fluent UI.'),
]

# mining: riga (1-86) → id, categoria, nome inglese ripulito, note (None = quelle originali), unione con altre righe
M = {
    1: ('page-404', 'errori', '404 page'),
    2: ('activity-rings', 'feedback', 'Apple Fitness rings'),
    3: ('archiving-systems', 'sistema', 'Archiving systems'),
    4: ('ar-video-filters', 'contenuti', 'Augmented reality video filters'),
    5: ('battery-indicator', 'sistema', 'Battery indicator'),
    6: ('read-receipts', 'conversazione', 'Read receipts (blue double tick)',
        "Visual feedback for the read status of a message, like WhatsApp's blue double tick.", [75]),
    7: ('chat-bubble', 'conversazione', 'Bubble (not just in the AI context)'),
    9: ('play-pause-button', 'azioni', 'Play/pause button'),
    10: ('share-button', 'azioni', 'Share button or box'),
    11: ('shuffle-button', 'azioni', 'Shuffle button (and smart shuffle)', 'Includes smart shuffle (e.g., Spotify).'),
    12: ('window-close-button', 'azioni', 'macOS close button (the dot in the red button)',
         'The dot inside the red close button signals unsaved changes.'),
    13: ('current-location-button', 'azioni', 'Current location button', ''),
    14: ('calendar-picker', 'input', 'Calendar and date picker'),
    15: ('flip-card', 'contenitori', 'Flipping cards'),
    16: ('cart', 'social', 'Cart'),
    17: ('color-picker', 'input', 'Colour picker', 'Like the ones in the graphic suites (e.g., Adobe Photoshop).'),
    18: ('command-palette', 'navigazione', 'Command palette'),
    19: ('cookie-banner', 'sistema', 'Cookie consent banner'),
    20: ('dark-mode-switch', 'input', 'Dark and light mode switch'),
    21: ('distraction-free-mode', 'sistema', 'Distraction-free modes'),
    22: ('drag-drop-uploader', 'input', 'Drag and drop uploader', 'Includes sub-components such as the dashed target area.'),
    23: ('emoji', 'contenuti', 'Emoticons and emoji'),
    24: ('empty-state', 'errori', 'Empty state', 'A fallback solution for no contents.'),
    25: ('expand-collapse', 'contenitori', 'Expanded/collapsed display mode', 'Declined in macOS with the minimiser feature.'),
    26: ('faq', 'contenuti', 'FAQ'),
    27: ('favicon', 'sistema', 'Favicon (favourite icon)', 'Short for "favourite icon".'),
    28: ('favourites-wishlist', 'social', 'Favourites or wishlist', 'With many declinations: ❤️ ⭐️ 🏷️.'),
    29: ('floating-sticky-sidebar', 'navigazione', 'Floating sticky sidebar'),
    30: ('hero-unit', 'contenitori', 'Hero unit'),
    31: ('link-chain-icon', 'navigazione', 'Hyperlink chain icon'),
    32: ('label', 'contenuti', 'Label'),
    33: ('language-switch', 'navigazione', 'Language switch',
         'With a look at ISO [language](https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes) and '
         '[country](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2) codes, e.g. en-US and en-GB, '
         '[uk-UA](https://www.ukrainer.net/) and [ru-UA](https://www.ukrainer.net/ru/), '
         '[lld-IT](https://home.provinzia.bz.it/lld/home) and [it-IT](https://home.provincia.bz.it/it/home).'),
    34: ('loading-screen', 'feedback', 'Loading screen'),
    35: ('login', 'sistema', 'Login icon and process (and permission system)'),
    36: ('marquee', 'contenuti', 'Marquee (rolling stripe)'),
    37: ('mobile-display-parts', 'sistema', 'Mobile display parts: notch, Dynamic Island, detents'),
    38: ('notification-system', 'feedback', 'Notification system'),
    39: ('finder-views', 'contenitori', 'macOS Finder views (with preview)'),
    40: ('page-dots', 'navigazione', 'Page dot indicators', 'With or without animation.'),
    41: ('picture-in-picture', 'contenuti', 'Picture-in-Picture'),
    42: ('pin', 'azioni', 'Pin'),
    43: ('image-placeholder', 'contenuti', 'Placeholder for pictures'),
    44: ('rating', 'social', 'Rating system'),
    45: ('scrollbar', 'navigazione', 'Scrollbar', ''),
    46: ('seat-map', 'social', 'Seating map (seat selection at checkout)'),
    47: ('text-selection', 'testo', 'Text selection and highlighting'),
    48: ('skeleton-screen', 'feedback', 'Skeleton screen'),
    49: ('sort-options', 'input', 'Sort options in tables and views'),
    50: ('sticky', 'contenitori', 'Sticky box, bar or menu ("affix")'),
    51: ('stories', 'social', 'Stories', 'From Snapchat and Instagram, then everywhere.'),
    52: ('tab-audio-indicator', 'navigazione', 'Tabs with audio indicator', "An icon in the browser's tab list shows which tab is playing sound."),
    53: ('image-tags', 'social', 'Tags on pictures'),
    54: ('text-caret', 'testo', 'Text caret (input text cursor)',
         'The vertical bar, sometimes blinking, that represents the current writing point.', [86]),
    55: ('ocr-text-recognition', 'testo', 'Text recognition on pictures (OCR)'),
    56: ('ai-thinking-steps', 'conversazione', 'AI "thinking" and process-step feedback', 'Three dots, then the steps of the process.'),
    57: ('thumbnav', 'navigazione', 'Thumbnav'),
    58: ('timer-countdown', 'feedback', 'Timer, countdown, stopwatch'),
    59: ('trash', 'errori', 'Trash, bin'),
    60: ('kebab-menu', 'azioni', 'Triple dot menu'),
    61: ('typing-indicator', 'conversazione', 'Typing indicator (dot-dot-dot)', 'In messaging apps and chatbots.'),
    62: ('card', 'contenitori', 'Card'),
    63: ('undo-history', 'errori', 'Undo and history'),
    64: ('undo-send', 'errori', 'Undo send (message buffer)', 'A usual feature of mailbox interfaces.'),
    65: ('versioning', 'sistema', 'Versioning system (e.g., Git)'),
    66: ('voice-ui', 'conversazione', 'Voice note and Voice User Interface (VUI) components'),
    67: ('irreversible-action-warning', 'errori', 'Warning before irreversible actions', None, [68]),
    69: ('paywall', 'social', 'Paywall / content locker'),
    70: ('pull-to-refresh', 'azioni', 'Pull-to-refresh', 'The update gesture, introduced by Loren Brichter in Tweetie (later Twitter).'),
    71: ('slash-command', 'conversazione', 'Slash command ( / ) or colon ( : )'),
    72: ('prompt-suggestions', 'conversazione', 'Sample queries and prompt suggestions'),
    73: ('tree-menu', 'navigazione', 'Tree menu / tree diagram'),
    74: ('sheet', 'contenitori', 'Sheet (bottom and top)', 'Contextual surfaces that slide in from the top or bottom edge of the screen.'),
    76: ('upgrade-button', 'social', 'Upgrade button'),
    77: ('add-to-collection-button', 'azioni', 'Add image button (plugin/extension)',
         'Triggers to add content to external tools (e.g., Cosmos or Pinterest).'),
    78: ('plugin-puzzle-button', 'azioni', 'Puzzle button', None),
    79: ('draggable-overflow-text', 'testo', 'Panning / draggable text',
         'The manual dragging of "overflowing" text that exceeds the visual space. See also the marquee.'),
    80: ('live-validation', 'errori', 'Real-time input validation', 'Auto-formatting and live validation feedback while typing.'),
    81: ('autocorrection', 'testo', 'Autocorrection and grammar checkers', 'Includes the visual feedback of the red (and other colours) underline.'),
    82: ('predictive-input', 'input', 'Predictive input (and predictive drop-down lists)'),
    83: ('skip-button', 'azioni', 'Skip button'),
    84: ('like-dislike', 'social', 'Like and dislike button'),
    85: ('onboarding', 'navigazione', 'Interface/product onboarding (walkthroughs and coach marks)'),
}
VEDI = {'marquee': 'draggable-overflow-text', 'loading-screen': 'skeleton-screen, splash-page, progress-bar',
        'text-caret': 'pointer, live-validation', 'calendar-picker': 'picker', 'color-picker': 'picker',
        'notification-system': 'toast, badge', 'kebab-menu': 'context-menu', 'label': 'tag-chip',
        'typing-indicator': 'ai-thinking-steps, chat-bubble', 'irreversible-action-warning': 'modal, undo-history',
        'empty-state': 'page-404', 'dark-mode-switch': 'switch', 'predictive-input': 'search-field, dropdown-filter'}


def pulisci_url(u):
    return u.rstrip(')')


def da_mining(righe):
    out = []
    for n, v in M.items():
        id, cat, nome = v[:3]
        note_nuove = v[3] if len(v) > 3 else None
        unite = v[4] if len(v) > 4 else []
        r = righe[n - 1]
        fonti, letture = [], []
        for t, u in r['link_nome']:
            fonti.append(L(pulisci_url(u), t))
        note = r['note']
        for t, u in r['link_note']:
            # i link dentro la nota: «Further reading» → letture, il resto → fonti
            (letture if re.search(r'further reading', note, re.I) else fonti).append(L(pulisci_url(u), t))
        if note_nuove is not None:
            note = note_nuove
        else:
            note = re.sub(r'(Ref:|Further reading:).*', '', note, flags=re.S | re.I).strip()
            note = re.sub(r'Look for other OsX components with the search field\.', '', note).strip()
        if n == 33:
            fonti = []
        anni = [int(r['anno'])] + [int(righe[k - 1]['anno']) for k in unite]
        for k in unite:
            for t, u in righe[k - 1]['link_note'] + righe[k - 1]['link_nome']:
                letture.append(L(pulisci_url(u), t))
        visti = set()
        fonti = [x for x in fonti if not (x['url'] in visti or visti.add(x['url']))]
        letture = [x for x in letture if not (x['url'] in visti or visti.add(x['url']))]
        for x in fonti + letture:  # titoli come «here», «ref»: si sostituiscono col dominio
            if re.fullmatch(r'(a )?refs?|here|example|this one|another example|with|w/o animation|@?\S+\.(com|org)|.*@.*', x['titolo'].strip(), re.I) \
                    or x['titolo'].startswith('http'):
                x['titolo'] = re.sub(r'^https?://(www\.)?([^/]+).*', r'\2', x['url'])
        origine = 'mining ' + ', '.join(str(k) for k in [n] + unite)
        out.append(scheda(id, 'avanzato', cat, n * 10, nome, note=note, anno=min(anni), vedi=VEDI.get(id, ''),
                          origine=origine, fonti=fonti, letture=letture))
    return out


if __name__ == '__main__':
    righe = json.load(open(sys.argv[1]))
    tutte = FONDAMENTALI + da_mining(righe)
    ids = [s['id'] for s in tutte]
    assert len(ids) == len(set(ids)), 'id doppi'
    for s in tutte:
        for v in s['vedi']:
            assert v in ids, f'{s["id"]}: vedi «{v}» inesistente'
        schede.scrivi(s)
    print(len(tutte), 'schede')
