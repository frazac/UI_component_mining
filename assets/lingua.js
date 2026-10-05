/*
 * Lingua delle pagine: IT, EN, FR, 中文 (cinese semplificato). Licenza MIT.
 * Si carica nel <head> senza defer, così la pagina compare già nella lingua giusta.
 * Ordine di scelta: ?lingua=it|en|fr|zh nell'indirizzo (lo usa la generazione dei PDF),
 * poi l'ultima scelta fatta in questo browser, poi l'inglese.
 * Ogni testo ha una variante per lingua: <span data-l="it">…</span><span data-l="en">…</span>…
 * Se la variante della lingua scelta è vuota si mostra l'inglese (data-ripiego).
 * Segnaposto e opzioni: attributi data-it / data-en / data-fr / data-zh.
 * Evento «lingua» su document a ogni cambio.
 */
(function () {
  'use strict';

  var LINGUE = { it: 'IT', en: 'EN', fr: 'FR', zh: '中文' };
  var LANG = { it: 'it', en: 'en', fr: 'fr', zh: 'zh-Hans' };
  var CHIAVE = 'componenti-lingua';
  var html = document.documentElement;

  function leggi() { try { return localStorage.getItem(CHIAVE); } catch (e) { return null; } }
  function scrivi(v) { try { localStorage.setItem(CHIAVE, v); } catch (e) { /* niente */ } }

  // dentro un iframe (esempi nelle slide e nella tabella): la lingua è quella della pagina che lo contiene
  var incorniciato = window.parent !== window;
  function delGenitore() { try { return window.parent.document.documentElement.getAttribute('data-lingua'); } catch (e) { return null; } }
  var daUrl = new URLSearchParams(location.search).get('lingua');
  var lingua = LINGUE[daUrl] ? daUrl : LINGUE[incorniciato && delGenitore()] ? delGenitore() : (LINGUE[leggi()] ? leggi() : 'en');
  html.setAttribute('data-lingua', lingua);
  html.setAttribute('lang', LANG[lingua]);

  function piena(v) { return !!v && (v.textContent.trim() !== '' || !!v.querySelector('img, svg')); }

  function ripieghi() {
    document.querySelectorAll('[data-ripiego]').forEach(function (el) { el.removeAttribute('data-ripiego'); });
    var visti = new Set();
    document.querySelectorAll('[data-l]').forEach(function (el) {
      var padre = el.parentNode;
      if (visti.has(padre)) return;
      visti.add(padre);
      var varianti = {};
      Array.prototype.forEach.call(padre.children, function (c) { if (c.hasAttribute('data-l')) varianti[c.getAttribute('data-l')] = c; });
      if (piena(varianti[lingua])) return;
      var sost = [varianti.en, varianti.it].filter(piena)[0];
      if (sost) sost.setAttribute('data-ripiego', '');
    });
    document.querySelectorAll('[data-en]').forEach(function (el) {
      var t = el.getAttribute('data-' + lingua) || el.getAttribute('data-en');
      if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') el.placeholder = t; else el.textContent = t;
    });
  }

  function imposta(l, daFuori) {
    lingua = l;
    html.setAttribute('data-lingua', l);
    html.setAttribute('lang', LANG[l]);
    if (!daFuori) scrivi(l);
    ripieghi();
    aggiorna();
    document.dispatchEvent(new CustomEvent('lingua', { detail: l }));
  }
  window.Lingua = { get: function () { return lingua; }, set: function (l) { if (LINGUE[l]) imposta(l); } };

  var selettore = null;
  function aggiorna() {
    if (!selettore) return;
    selettore.querySelectorAll('button').forEach(function (b) { b.setAttribute('aria-pressed', String(b.value === lingua)); });
  }

  function avvia() {
    ripieghi();
    if (incorniciato) {  // niente selettore: segue la pagina che lo contiene
      try { window.parent.document.addEventListener('lingua', function (ev) { imposta(ev.detail, true); }); } catch (e) { /* altra origine */ }
      return;
    }
    selettore = document.createElement('div');
    selettore.className = 'lingua-selettore';
    selettore.setAttribute('role', 'group');
    selettore.setAttribute('aria-label', 'Lingua / Language / Langue / 语言');
    Object.keys(LINGUE).forEach(function (l) {
      var b = document.createElement('button');
      b.type = 'button';
      b.value = l;
      b.textContent = LINGUE[l];
      b.addEventListener('click', function () { imposta(l); b.blur(); });
      selettore.appendChild(b);
    });
    document.body.appendChild(selettore);
    aggiorna();
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', avvia);
  else avvia();
})();
