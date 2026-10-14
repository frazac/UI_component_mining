---
id: spinner
livello: avanzato
categoria: feedback
anno: 2026
ordine: 960
parole: spinner, throbber, loader, loading spinner, activity indicator, progress circle, indeterminate, rotella, caricamento
esempio: esempi/spinner/
vedi: loading-screen, progress-bar, skeleton-screen, pointer, feedback
origine: FZ, 2026-10-15
fonti:
  - https://developer.apple.com/design/human-interface-guidelines/progress-indicators | Progress indicators - Apple Human Interface Guidelines
  - https://m3.material.io/components/progress-indicators/overview | Progress indicators - Material Design 3
  - https://www.nngroup.com/articles/progress-indicators/ | Progress Indicators Make a Slow System Less Insufferable - Nielsen Norman Group
---

## it
# Spinner (indicatore di attività)
Una piccola figura che gira (un cerchio aperto, una corona di trattini, dei punti) per dire che il sistema sta lavorando e non si è bloccato. È un indicatore indeterminato: mostra che qualcosa succede, non quanto manca. Per attese brevi, da uno a pochi secondi, basta; oltre i dieci secondi serve una barra di avanzamento con la percentuale o il tempo stimato.

Va messo dove arriverà il risultato: dentro il pulsante appena premuto, al posto dell'elenco che si sta caricando, non in un angolo lontano. Se l'attesa è quasi sempre brevissima conviene mostrarlo con un piccolo ritardo, per evitare un lampo inutile. Per chi usa lo screen reader va annunciato lo stato («caricamento in corso»), e con prefers-reduced-motion la rotazione va rallentata o sostituita. Lo skeleton screen è l'alternativa che anticipa anche la forma del contenuto.

## en
# Spinner (activity indicator)
A small rotating figure (an open circle, a ring of dashes, dots) that says the system is working and has not frozen. It is an indeterminate indicator: it shows that something is happening, not how much is left. For short waits, from one to a few seconds, it is enough; beyond ten seconds a progress bar with a percentage or an estimated time is needed.

It belongs where the result will appear: inside the button just pressed, in place of the list being loaded, not in a distant corner. If the wait is almost always very short, it is better to show it after a small delay, to avoid a pointless flash. Screen reader users need the status announced (“loading”), and with prefers-reduced-motion the rotation should be slowed down or replaced. The skeleton screen is the alternative that also anticipates the shape of the content.

## fr
# Spinner (indicateur d’activité)
Une petite figure qui tourne (un cercle ouvert, une couronne de tirets, des points) pour dire que le système travaille et ne s’est pas bloqué. C’est un indicateur indéterminé : il montre qu’il se passe quelque chose, pas combien il reste. Pour des attentes courtes, d’une à quelques secondes, il suffit ; au-delà de dix secondes, il faut une barre de progression avec le pourcentage ou le temps estimé.

Il se place là où le résultat arrivera : dans le bouton qu’on vient d’appuyer, à la place de la liste en cours de chargement, pas dans un coin éloigné. Si l’attente est presque toujours très brève, mieux vaut l’afficher avec un léger délai, pour éviter un clignotement inutile. Pour les utilisateurs de lecteur d’écran, l’état doit être annoncé (« chargement en cours ») et, avec prefers-reduced-motion, la rotation doit être ralentie ou remplacée. Le skeleton screen est l’alternative qui anticipe aussi la forme du contenu.

## zh
# 加载指示器（spinner）
一个旋转的小图形（开口的圆环、一圈短线或几个圆点），表示系统正在工作、没有卡住。它是不确定型指示器：只表明正在进行，不表明还剩多少。等待时间较短（一到几秒）时用它就够了；超过十秒则需要显示百分比或预计时间的进度条。

它应放在结果将要出现的位置：刚按下的按钮里、正在加载的列表处，而不是远处的角落。如果等待几乎总是很短，最好稍作延迟再显示，避免一闪而过。对于使用读屏软件的用户，需要播报状态（“正在加载”）；开启 prefers-reduced-motion 时，应放慢或替换旋转动画。骨架屏（skeleton screen）是另一种选择，还能预先呈现内容的形状。
