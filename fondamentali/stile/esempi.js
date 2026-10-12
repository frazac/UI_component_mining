/*
 * Esempi dei componenti nelle slide (.s-componente figure.esempio[data-esempio]): a schermo l'esempio è già
 * interattivo, senza clic (FZ, 2026-10-12). L'iframe carica la copia pulita in assets/componenti-esempi/ nella
 * lingua della pagina, alla stessa misura delle schermate (750 × 684) ridotta al riquadro: si vede come la
 * schermata. Nella stampa e nei PDF resta la schermata (img).
 */
(function () {
  'use strict';

  var W = 750, H = 684;   // come strumenti/schermate.py

  function lingua() { return document.documentElement.getAttribute('data-lingua') || 'en'; }
  function indirizzo(fig) {
    var l = lingua();
    return fig.getAttribute('data-esempio') + '?lingua=' + (l === 'zh' || l === 'it' || l === 'fr' ? l : 'en');
  }

  function scala(fig) {
    var f = fig.querySelector('iframe');
    if (!f) return;
    var r = fig.getBoundingClientRect();
    var s = Math.min(r.width / W, r.height / H);
    f.style.transform = 'translate(' + (r.width - W * s) / 2 + 'px,' + (r.height - H * s) / 2 + 'px) scale(' + s + ')';
  }

  function prepara(fig) {
    var f = document.createElement('iframe');
    f.src = indirizzo(fig);
    f.title = fig.getAttribute('data-titolo') || '';
    f.setAttribute('loading', 'lazy');
    f.style.width = W + 'px';
    f.style.height = H + 'px';
    f.style.transformOrigin = '0 0';
    fig.appendChild(f);
    fig.classList.add('interattivo');
    scala(fig);
  }

  function avvia() {
    var figure = document.querySelectorAll('.s-componente figure.esempio[data-esempio]');
    Array.prototype.forEach.call(figure, prepara);
    if (window.ResizeObserver) {
      var ro = new ResizeObserver(function (voci) { voci.forEach(function (v) { scala(v.target); }); });
      Array.prototype.forEach.call(figure, function (fig) { ro.observe(fig); });
    }
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', avvia);
  else avvia();

  document.addEventListener('lingua', function () {
    Array.prototype.forEach.call(document.querySelectorAll('figure.esempio.interattivo iframe'), function (f) {
      f.src = indirizzo(f.parentNode);
    });
  });
})();
