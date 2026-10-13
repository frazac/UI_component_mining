---
id: seek-buttons
livello: avanzato
categoria: azioni
anno: 2026
ordine: 880
parole: seek, seek forward, seek backward, forward and rewind few seconds, skip few seconds, skip forward, skip back, rewind, replay 10, forward 10, double tap, hotkeys, J L keys
esempio: esempi/seek-buttons/
vedi: play-pause-button, skip-button, slider, picture-in-picture
origine: FZ, 2026-10-12
fonti:
  - https://developer.mozilla.org/en-US/docs/Web/API/MediaSession/setActionHandler | MediaSession: setActionHandler() method - MDN
  - https://foliovision.com/player/demos/rewind-button | Rewind and Forward Buttons - Foliovision
  - https://github.com/dayanch96/YTLite/issues/634 | Skip-forward / back buttons in iOS Media Controls - GitHub
  - https://www.youtube.com/watch?v=EZA-TnVAyDo | Global Speed: Seek, pause, adjust volume for PiP videos using hotkeys! - YouTube
---

## it
# Avanti e indietro di qualche secondo (seek)
Due pulsanti accanto al play che spostano la riproduzione di un intervallo fisso, di solito 10 secondi (a volte 5, 15 o 30 nei podcast): l’icona è una freccia circolare con il numero dei secondi dentro. In inglese si chiama seek (seek forward, seek backward), ma anche skip forward / skip back o forward and rewind few seconds: è il nome che usano anche le API dei browser (Media Session, azioni seekforward e seekbackward).

Ha quasi sempre una scorciatoia: su YouTube il doppio tocco ai lati del video, i tasti J e L (10 secondi) e le frecce (5 secondi). Diverso dal pulsante «Salta», che salta un intero blocco (l’intro, la pubblicità). Anche i comandi di sistema (schermata di blocco, Centro di Controllo di iOS) mostrano questi pulsanti «a tempo» per i media lunghi, al posto di brano o capitolo precedente e successivo: ogni app sceglie quali chiedere.

## en
# Forward and rewind few seconds (seek)
Two buttons next to play that move playback by a fixed interval, usually 10 seconds (sometimes 5, 15 or 30 in podcasts): the icon is a circular arrow with the number of seconds inside. It is called seek (seek forward, seek backward), but also skip forward / skip back, skip few seconds or forward and rewind few seconds; seek is also the name used by browser APIs (Media Session, actions seekforward and seekbackward).

It almost always has a shortcut: on YouTube, double-tapping the sides of the video, the J and L keys (10 seconds) and the arrow keys (5 seconds). Unlike the Skip button, which jumps over a whole block (the intro, an ad). System controls (Lock Screen, iOS Control Center) also show these time-based buttons for long-form media, instead of previous and next track or chapter: each app chooses which ones to request.

## fr
# Avancer et reculer de quelques secondes (seek)
Deux boutons à côté de la lecture qui déplacent la lecture d’un intervalle fixe, en général 10 secondes (parfois 5, 15 ou 30 dans les podcasts) : l’icône est une flèche circulaire avec le nombre de secondes à l’intérieur. En anglais on dit seek (seek forward, seek backward), mais aussi skip forward / skip back ou forward and rewind few seconds ; c’est aussi le nom utilisé par les API des navigateurs (Media Session, actions seekforward et seekbackward).

Il a presque toujours un raccourci : sur YouTube, le double toucher sur les côtés de la vidéo, les touches J et L (10 secondes) et les flèches (5 secondes). À ne pas confondre avec le bouton « Passer », qui saute tout un bloc (l’intro, la publicité). Les commandes du système (écran verrouillé, Centre de contrôle d’iOS) affichent aussi ces boutons « temporels » pour les médias longs, à la place de la piste ou du chapitre précédent et suivant : chaque application choisit lesquels demander.

## zh
# 快进与快退几秒（seek）
播放键旁边的两个按钮，把播放位置前后移动固定的时长，通常是 10 秒（播客中有时是 5、15 或 30 秒）：图标是一个环形箭头，中间写着秒数。英文叫 seek（seek forward、seek backward），也叫 skip forward / skip back、skip few seconds 或 forward and rewind few seconds；浏览器 API 也用这个名字（Media Session 的 seekforward 和 seekbackward 操作）。

它几乎总有快捷方式：在 YouTube 上，双击视频两侧、按 J 和 L 键（10 秒）或方向键（5 秒）。它不同于“跳过”按钮，后者跳过整段内容（片头、广告）。对于长时媒体，系统控件（锁屏、iOS 控制中心）也会显示这类按时间跳转的按钮，而不是上一曲/下一曲或上一章/下一章：由每个应用决定请求哪一种。
