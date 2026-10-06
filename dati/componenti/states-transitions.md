---
id: states-transitions
livello: introduzione
categoria: introduzione
anno: 2026
ordine: 45
parole: states, transitions, motion, duration, easing, reduced motion, accessibility, animation
esempio: esempi/states-transitions/
vedi: interaction-states, feedback, microinteractions, skeleton-screen, loading-screen, live-validation
origine: nuova 2026
scritto: claude
fonti:
  - https://www.nngroup.com/articles/animation-duration/ | Executing UX Animations: Duration and Motion Characteristics – Nielsen Norman Group
  - https://m3.material.io/styles/motion/overview | Motion – Material Design 3
  - https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion | prefers-reduced-motion – MDN
---

## it
# Stati e transizioni
Ogni componente vive in più stati: normale, hover, focus, premuto, disabilitato, caricamento, errore, successo. Progettarlo vuol dire disegnarli tutti, non solo quello «bello».

La transizione è il passaggio da uno stato all'altro, e ha tre decisioni:

- **durata**: di solito tra 100 e 300 millisecondi; sotto i 100 non si percepisce, sopra i 500 sembra lenta;
- **curva di accelerazione** (*easing*): un oggetto reale non parte e non si ferma di colpo; *ease-out* per ciò che entra, *ease-in* per ciò che esce;
- **che cosa si muove**: solo ciò che aiuta a capire il cambiamento.

Accessibilità: chi soffre di disturbi vestibolari può chiedere al sistema di ridurre il movimento (`prefers-reduced-motion`). Il design deve rispettarlo: meno movimento, stesso significato.

## en
# States and transitions
Every component lives in several states: default, hover, focus, pressed, disabled, loading, error, success. Designing it means drawing all of them, not only the "nice" one.

A transition is the passage from one state to another, and it involves three decisions:

- **duration**: usually between 100 and 300 milliseconds; under 100 it is not perceived, over 500 it feels slow;
- **easing curve**: a real object does not start or stop abruptly; *ease-out* for what enters, *ease-in* for what leaves;
- **what moves**: only what helps to understand the change.

Accessibility: people with vestibular disorders can ask the system to reduce motion (`prefers-reduced-motion`). Design must respect it: less motion, same meaning.

## fr
# États et transitions
Chaque composant vit dans plusieurs états : normal, survol, focus, appuyé, désactivé, chargement, erreur, succès. Le concevoir, c’est les dessiner tous, pas seulement le « beau ».

La transition est le passage d’un état à l’autre, et elle demande trois décisions :

- **durée** : en général entre 100 et 300 millisecondes ; sous 100 on ne la perçoit pas, au-delà de 500 elle paraît lente ;
- **courbe d’accélération** (*easing*) : un objet réel ne démarre ni ne s’arrête d’un coup ; *ease-out* pour ce qui entre, *ease-in* pour ce qui sort ;
- **ce qui bouge** : seulement ce qui aide à comprendre le changement.

Accessibilité : les personnes souffrant de troubles vestibulaires peuvent demander au système de réduire les animations (`prefers-reduced-motion`). Le design doit le respecter : moins de mouvement, même sens.

## zh
# 状态与过渡
每个组件都有多种状态：默认、悬停、焦点、按下、禁用、加载、错误、成功。设计一个组件，就要把所有状态都画出来，而不只是“好看”的那一个。

过渡是从一个状态到另一个状态的变化，需要做三个决定：

- **时长**：通常在 100 到 300 毫秒之间；低于 100 毫秒几乎察觉不到，超过 500 毫秒会显得迟缓；
- **缓动曲线（easing）**：真实物体不会突然启动或停止；进入用 *ease-out*，离开用 *ease-in*；
- **什么在动**：只让有助于理解变化的部分动起来。

无障碍：患有前庭功能障碍的人可以让系统减少动效（`prefers-reduced-motion`）。设计必须尊重这一设置：动效更少，含义不变。
