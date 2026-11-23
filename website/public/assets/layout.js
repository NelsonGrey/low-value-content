/* Page shell helper. On wide screens the header is pinned and only #page-scroll scrolls (see BaseLayout.astro).
   Kept as an external, synchronous script in <head> so the dev and staging Content-Security-Policy
   (script-src 'self') allows it and the scrollbar width is known before the first paint. */
(function () {
  var root = document.documentElement;

  /* 1. Width of a classic scrollbar (0 for overlay scrollbars). The header uses it to line its content up
        with the scrolling body, whose content box is that much narrower. */
  try {
    var probe = document.createElement('div');
    probe.style.cssText = 'position:absolute;top:-9999px;width:100px;height:100px;overflow:scroll';
    root.appendChild(probe);
    var width = probe.offsetWidth - probe.clientWidth;
    root.removeChild(probe);
    root.style.setProperty('--sbw', Math.max(0, width) + 'px');
  } catch (e) { /* the CSS default of 0px applies */ }

  /* 2. Keyboard scrolling and scroll restoration for the inner scroller. */
  document.addEventListener('DOMContentLoaded', function () {
    var scroller = document.getElementById('page-scroll');
    if (!scroller) return;
    var key = 'lvc-scroll:' + location.pathname;

    scroller.setAttribute('tabindex', '-1');
    scroller.focus({ preventScroll: true });

    /* Browsers restore the window's scroll position on Back, not an inner scroller's. */
    try {
      var nav = performance.getEntriesByType('navigation')[0];
      var saved = Number(sessionStorage.getItem(key));
      if (nav && nav.type === 'back_forward' && saved > 0) {
        var restore = function () { scroller.scrollTop = saved; };
        restore();
        window.addEventListener('load', restore);
      }
      window.addEventListener('pagehide', function () {
        try { sessionStorage.setItem(key, String(scroller.scrollTop)); } catch (e) { /* storage unavailable */ }
      });
    } catch (e) { /* scroll restoration is a nicety */ }
  });
})();
