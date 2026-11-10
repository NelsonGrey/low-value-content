// Highlights the next royal observance. External file so the dev/staging CSP allows it.
(function () {
  var items = Array.prototype.slice.call(document.querySelectorAll('[data-obs]'));
  var now = new Date(), today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
  var best = null, bestDays = Infinity;
  items.forEach(function (el) {
    var p = el.dataset.obs.split('-'), t = new Date(today.getFullYear(), +p[0] - 1, +p[1]);
    if (t < today) t = new Date(today.getFullYear() + 1, +p[0] - 1, +p[1]);
    var days = Math.round((t - today) / 864e5);
    if (days < bestDays) { bestDays = days; best = { el: el, t: t }; }
  });
  if (!best) return;
  var label = bestDays === 0 ? 'Today' : bestDays === 1 ? 'Tomorrow' : 'In ' + bestDays + ' days';
  var month = best.t.toLocaleString('en-US', { month: 'long' });
  document.getElementById('next-day').textContent = String(best.t.getDate()).padStart(2, '0');
  document.getElementById('next-month').textContent = month;
  document.getElementById('next-name').textContent = best.el.dataset.name;
  document.getElementById('next-countdown').textContent = label;
  document.getElementById('next-link').setAttribute('href', '#' + best.el.id);
  document.getElementById('next-up').hidden = false;
  best.el.classList.add('is-next');
  var tag = best.el.querySelector('.next-tag'); tag.textContent = 'Next · ' + label.toLowerCase(); tag.hidden = false;
})();
