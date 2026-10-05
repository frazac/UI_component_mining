/*
 * Tabella dei componenti: ricerca per parole (nella lingua scelta), filtro per livello e categoria.
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

  function normalizza(s) { return s.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, ''); }

  function filtra() {
    var lingua = window.Lingua ? window.Lingua.get() : 'en';
    var parole = normalizza(cerca.value.trim()).split(/\s+/).filter(Boolean);
    var cat = categoria.value;
    var n = 0;
    righe.forEach(function (tr) {
      var testo = normalizza(tr.getAttribute('data-cerca-' + lingua) + ' ' + tr.getAttribute('data-cerca-en'));
      var ok = (!livello || tr.dataset.livello === livello) &&
               (!cat || tr.dataset.categoria === cat) &&
               parole.every(function (p) { return testo.indexOf(p) !== -1; });
      tr.hidden = !ok;
      if (ok) n++;
    });
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
  document.addEventListener('lingua', filtra);

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
