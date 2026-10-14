---
id: alert
livello: avanzato
categoria: feedback
anno: 2026
ordine: 970
parole: alert, inline alert, banner, notification banner, callout, inline notification, section message, message box, avviso, messaggio
esempio: esempi/alert/
vedi: toast, modal, live-validation, irreversible-action-warning, notification-system, empty-state
origine: FZ, 2026-10-15
fonti:
  - https://design-system.service.gov.uk/components/notification-banner/ | Notification banner - GOV.UK Design System
  - https://carbondesignsystem.com/components/notification/usage/ | Notification - Carbon Design System
  - https://www.w3.org/WAI/ARIA/apg/patterns/alert/ | Alert pattern - WAI-ARIA Authoring Practices Guide
---

## it
# Avviso (alert)
Un riquadro nella pagina che comunica qualcosa di importante sullo stato del sistema o dell'azione appena fatta: un'informazione, un successo, un'attenzione, un errore. Ha un colore, un'icona e un titolo che dicono subito di che tipo è, poi un testo breve e, se serve, un'azione («Riprova», «Vedi i dettagli») o una × per chiuderlo. Resta finché il problema c'è o finché l'utente non lo chiude.

È diverso dal toast, che compare in sovrimpressione e sparisce da solo, e dalla finestra di dialogo d'allarme, che blocca tutto e chiede una risposta. Il colore non basta, per chi non distingue i colori: servono anche icona e parole. Se compare dopo il caricamento della pagina va annunciato agli screen reader (role="alert" per gli errori urgenti, role="status" per il resto). Gli errori di un form vanno vicino al campo, con un riepilogo in alto.

## en
# Alert
A box in the page that communicates something important about the state of the system or of the action just taken: information, success, a warning, an error. It has a colour, an icon and a title that immediately say what kind it is, then a short text and, if needed, an action (“Try again”, “See details”) or a × to dismiss it. It stays as long as the problem exists or until the user dismisses it.

It differs from the toast, which appears as an overlay and disappears by itself, and from the alert dialog, which blocks everything and asks for an answer. Colour is not enough, for people who cannot tell colours apart: an icon and words are needed too. If it appears after the page has loaded it must be announced to screen readers (role="alert" for urgent errors, role="status" for the rest). Form errors go next to the field, with a summary at the top.

## fr
# Alerte (alert)
Un encadré dans la page qui communique quelque chose d’important sur l’état du système ou de l’action qu’on vient de faire : une information, un succès, un avertissement, une erreur. Il a une couleur, une icône et un titre qui disent tout de suite de quel type il s’agit, puis un texte court et, si besoin, une action (« Réessayer », « Voir les détails ») ou un × pour le fermer. Il reste tant que le problème existe ou jusqu’à ce que l’utilisateur le ferme.

Il se distingue du toast, qui apparaît en surimpression et disparaît tout seul, et de la boîte de dialogue d’alerte, qui bloque tout et demande une réponse. La couleur ne suffit pas, pour qui ne distingue pas les couleurs : il faut aussi une icône et des mots. S’il apparaît après le chargement de la page, il doit être annoncé aux lecteurs d’écran (role="alert" pour les erreurs urgentes, role="status" pour le reste). Les erreurs d’un formulaire se placent près du champ, avec un récapitulatif en haut.

## zh
# 提示框（alert）
页面中的一个区块，用来传达有关系统状态或刚完成操作的重要信息：普通信息、成功、警告或错误。它用颜色、图标和标题立即表明类型，然后是一段简短文字，必要时附带一个操作（“重试”“查看详情”）或用于关闭的 ×。只要问题仍然存在，或直到用户将其关闭，它就一直保留。

它不同于以浮层出现并自动消失的 toast，也不同于阻断一切、要求用户回应的警告对话框。仅靠颜色是不够的，因为有人无法区分颜色：还需要图标和文字。如果它在页面加载后才出现，必须让读屏软件播报（紧急错误用 role="alert"，其他情况用 role="status"）。表单错误应放在对应字段旁边，并在顶部给出汇总。
