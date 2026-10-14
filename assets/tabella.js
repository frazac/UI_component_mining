/*
 * Tabella dei componenti: ricerca per parole (in tutte le lingue, risultati ordinati per pertinenza),
 * filtro per livello e categoria.
 * Lo stato dei filtri sta nell'indirizzo (#q=…&livello=…&categoria=…) per poterlo condividere. Licenza MIT.
 */
(function () {
  'use strict';

  var righe = Array.prototype.slice.call(document.querySelectorAll('table.componenti tbody tr'));
  var cerca = document.getElementById('cerca');
  var categoria = document.getElementById('categoria');
  var chips = Array.prototype.slice.call(document.querySelectorAll('.chip[data-livello]'));
  var conteggio = document.getElementById('conteggio');
  var vuoto = document.querySelector('.vuoto');
  var livello = '';

  function normalizza(s) { return s.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, ''); }
  function parole(s) { return normalizza(s).split(/[^\p{L}\p{N}]+/u).filter(Boolean); }
  var HAN = /\p{Script=Han}/u;

  // per ogni riga: le parole dei tre campi, dal più pesante (nomi) al più leggero (note e categoria)
  var CAMPI = [['nomi', 3], ['parole', 2], ['testo', 1]];
  righe.forEach(function (tr, i) {
    tr._ordine = i;
    tr._campi = CAMPI.map(function (c) {
      var t = tr.getAttribute('data-cerca-' + c[0]) || '';
      return { peso: c[1], testo: normalizza(t), parole: parole(t) };
    });
  });

  // pertinenza di un termine: inizio di parola (non sottostringa: «spinner» non trova «stepper»),
  // parola intera vale di più; in cinese, dove non ci sono spazi, basta la sottostringa
  function punti(tr, termine) {
    var meglio = 0;
    tr._campi.forEach(function (c) {
      var p = 0;
      if (HAN.test(termine)) p = c.testo.indexOf(termine) !== -1 ? c.peso * 2 : 0;
      else c.parole.forEach(function (w) {
        if (w === termine) p = Math.max(p, c.peso * 2 + 1);
        else if (w.indexOf(termine) === 0) p = Math.max(p, c.peso * 2);
      });
      meglio = Math.max(meglio, p);
    });
    return meglio;
  }

  function filtra() {
    var termini = parole(cerca.value);
    var cat = categoria.value;
    var n = 0;
    righe.forEach(function (tr) {
      var tot = 0;
      var ok = (!livello || tr.dataset.livello === livello) && (!cat || tr.dataset.categoria === cat) &&
               termini.every(function (t) { var p = punti(tr, t); tot += p; return p > 0; });
      tr._punti = tot;
      tr.hidden = !ok;
      if (ok) n++;
    });
    var corpo = righe[0].parentNode;
    righe.slice().sort(function (a, b) { return (b._punti - a._punti) || (a._ordine - b._ordine); })
      .forEach(function (tr) { corpo.appendChild(tr); });
    conteggio.value = n;
    vuoto.hidden = n > 0;
    var stato = new URLSearchParams();
    if (cerca.value.trim()) stato.set('q', cerca.value.trim());
    if (livello) stato.set('livello', livello);
    if (cat) stato.set('categoria', cat);
    var h = stato.toString();
    if (h || /[=]/.test(location.hash)) history.replaceState(null, '', h ? '#' + h : location.pathname + location.search);
  }

  chips.forEach(function (b) {
    b.addEventListener('click', function () {
      livello = b.dataset.livello;
      chips.forEach(function (c) { c.setAttribute('aria-pressed', String(c === b)); });
      filtra();
    });
  });
  cerca.addEventListener('input', filtra);
  categoria.addEventListener('change', filtra);

  // stato iniziale dall'indirizzo (solo se è uno stato di filtri, non un'ancora a un componente)
  if (/=/.test(location.hash)) {
    var p = new URLSearchParams(location.hash.slice(1));
    cerca.value = p.get('q') || '';
    categoria.value = p.get('categoria') || '';
    livello = p.get('livello') || '';
    chips.forEach(function (c) { c.setAttribute('aria-pressed', String(c.dataset.livello === livello)); });
    filtra();
  }
  // «/» porta alla ricerca
  document.addEventListener('keydown', function (ev) {
    if (ev.key === '/' && document.activeElement !== cerca) { ev.preventDefault(); cerca.focus(); }
  });
})();
