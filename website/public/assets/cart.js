/* Cart and checkout client. Holds only {productId, variantId, quantity} in localStorage.
   The server prices every line from its own catalog, so nothing here is trusted for money. */
(function () {
  var KEY = 'lvc-cart-v1';
  var MAX_QTY = 5;
  var MAX_LINES = 6;

  function read() {
    try {
      var raw = JSON.parse(localStorage.getItem(KEY) || '[]');
      if (!Array.isArray(raw)) return [];
      return raw.filter(function (l) {
        return l && typeof l.p === 'string' && typeof l.v === 'string' && Number.isInteger(l.q) && l.q >= 1 && l.q <= MAX_QTY;
      }).slice(0, MAX_LINES);
    } catch (e) { return []; }
  }
  function write(lines) {
    try { localStorage.setItem(KEY, JSON.stringify(lines)); } catch (e) { /* private mode: cart lasts this page only */ }
    badge(lines);
  }
  function count(lines) { return lines.reduce(function (n, l) { return n + l.q; }, 0); }
  function badge(lines) {
    var n = count(lines || read());
    document.querySelectorAll('[data-cart-count]').forEach(function (el) {
      el.textContent = n ? String(n) : '';
      el.hidden = !n;
    });
  }

  /** Returns 'ok', 'full' (too many different items) or 'limit' (quantity cap reached). */
  function add(p, v, q) {
    var lines = read();
    var hit = lines.filter(function (l) { return l.p === p && l.v === v; })[0];
    if (hit) {
      if (hit.q + q > MAX_QTY) return 'limit';
      hit.q += q;
    } else {
      if (lines.length >= MAX_LINES) return 'full';
      lines.push({ p: p, v: v, q: q });
    }
    write(lines);
    return 'ok';
  }
  function setQty(p, v, q) {
    var lines = read().map(function (l) { return l.p === p && l.v === v ? { p: p, v: v, q: q } : l; })
      .filter(function (l) { return l.q >= 1; });
    write(lines);
  }
  function clear() { write([]); }

  function checkout(lines) {
    return fetch('/api/checkout-session', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ items: lines.map(function (l) { return { productId: l.p, variantId: l.v, quantity: l.q }; }) })
    }).then(function (res) {
      return res.json().then(function (data) { return { ok: res.ok, data: data }; });
    }).then(function (r) {
      if (!r.ok || !r.data.url) throw new Error(r.data.error || 'failed');
      window.location.assign(r.data.url);
    });
  }

  window.LVCCart = { read: read, add: add, setQty: setQty, clear: clear, checkout: checkout };

  /* Returning from Stripe with a paid-order token: the cart has done its job. */
  if (location.pathname.replace(/\.html$/, '') === '/order' && /[?&]token=/.test(location.search)) clear();

  /* Product page form */
  function productForm(form) {
    var variants = JSON.parse(form.dataset.variants || '[]');
    var product = form.dataset.product;
    var colorSel = form.elements.color;
    var sizeSel = form.elements.size;
    var note = form.querySelector('.buy-note');
    var idle = note.textContent;

    function fillSizes() {
      var color = colorSel.value;
      var keep = sizeSel.value;
      sizeSel.textContent = '';
      variants.filter(function (v) { return v.color === color; }).forEach(function (v) {
        var o = document.createElement('option');
        o.value = v.size; o.textContent = v.size.toUpperCase();
        if (v.size === keep) o.selected = true;
        sizeSel.appendChild(o);
      });
    }
    function say(msg, bad) { note.textContent = msg; note.classList.toggle('error', !!bad); }
    function line() {
      return { p: product, v: colorSel.value + '-' + sizeSel.value, q: Number(form.elements.quantity.value) };
    }

    if (colorSel.tagName === 'SELECT') colorSel.addEventListener('change', fillSizes);
    fillSizes();

    form.addEventListener('submit', function (event) {
      event.preventDefault();
      var l = line();
      var result = add(l.p, l.v, l.q);
      if (result === 'ok') {
        say('Added to your cart.');
        var link = document.createElement('a');
        link.href = '/cart.html'; link.textContent = ' View cart';
        note.appendChild(link);
      } else if (result === 'limit') {
        say('You can order at most ' + MAX_QTY + ' of one item.', true);
      } else {
        say('Your cart is full. Check out first, then start another.', true);
      }
    });

    var buy = form.querySelector('[data-action="buy"]');
    buy.addEventListener('click', function () {
      buy.disabled = true;
      say('Opening secure checkout…');
      checkout([line()]).catch(function () {
        buy.disabled = false;
        say('Checkout is unavailable right now. Please try again shortly.', true);
      });
    });

    window.addEventListener('pageshow', function (e) {
      if (e.persisted) { buy.disabled = false; say(idle); }
    });
  }

  /* Cart page */
  function cartPage(root) {
    var data = JSON.parse(document.getElementById('cart-catalog').textContent);
    var list = root.querySelector('[data-cart-lines]');
    var empty = root.querySelector('[data-cart-empty]');
    var summary = root.querySelector('[data-cart-summary]');
    var total = root.querySelector('[data-cart-subtotal]');
    var button = root.querySelector('[data-cart-checkout]');
    var note = root.querySelector('.buy-note');
    var money = function (cents) { return '$' + (cents / 100).toFixed(2); };

    function render() {
      /* Drop anything the catalog no longer sells, so a stale cart can never block checkout. */
      var lines = read().filter(function (l) { return data[l.p] && data[l.p].variants[l.v]; });
      if (lines.length !== read().length) write(lines);
      list.textContent = '';
      var subtotal = 0;
      lines.forEach(function (l) {
        var product = data[l.p];
        subtotal += product.price * l.q;
        var li = document.createElement('li');
        li.className = 'cart-line';
        if (product.image) {
          var img = document.createElement('img');
          img.src = product.image; img.alt = ''; img.width = 72; img.height = 90;
          li.appendChild(img);
        }
        var info = document.createElement('div');
        var name = document.createElement('a');
        name.href = product.href; name.textContent = product.name;
        var meta = document.createElement('p');
        meta.textContent = product.variants[l.v] + ' · ' + money(product.price);
        info.appendChild(name); info.appendChild(meta);
        li.appendChild(info);

        var qty = document.createElement('select');
        qty.setAttribute('aria-label', 'Quantity for ' + product.name + ', ' + product.variants[l.v]);
        for (var q = 1; q <= MAX_QTY; q++) {
          var o = document.createElement('option');
          o.value = String(q); o.textContent = String(q);
          if (q === l.q) o.selected = true;
          qty.appendChild(o);
        }
        qty.addEventListener('change', function () { setQty(l.p, l.v, Number(qty.value)); render(); });
        li.appendChild(qty);

        var remove = document.createElement('button');
        remove.type = 'button'; remove.className = 'link-button'; remove.textContent = 'Remove';
        remove.setAttribute('aria-label', 'Remove ' + product.name + ', ' + product.variants[l.v]);
        remove.addEventListener('click', function () { setQty(l.p, l.v, 0); render(); });
        li.appendChild(remove);
        list.appendChild(li);
      });
      empty.hidden = lines.length > 0;
      summary.hidden = lines.length === 0;
      total.textContent = money(subtotal);
    }

    button.addEventListener('click', function () {
      button.disabled = true;
      note.classList.remove('error');
      note.textContent = 'Opening secure checkout…';
      checkout(read()).catch(function () {
        button.disabled = false;
        note.classList.add('error');
        note.textContent = 'Checkout is unavailable right now. Please try again shortly.';
      });
    });
    window.addEventListener('storage', render);
    window.addEventListener('pageshow', function (e) { if (e.persisted) { button.disabled = false; render(); } });
    render();
  }

  function init() {
    badge();
    var form = document.querySelector('.buy-form');
    if (form) productForm(form);
    var root = document.querySelector('[data-cart-root]');
    if (root) cartPage(root);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
  window.addEventListener('storage', function () { badge(); });
})();
