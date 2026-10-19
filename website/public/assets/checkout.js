(function () {
  var form = document.querySelector('.buy-form');
  if (!form) return;
  var note = form.querySelector('.buy-note');
  var button = form.querySelector('button[type="submit"]');
  var idle = note.textContent;

  function fail(message) {
    note.textContent = message;
    note.classList.add('error');
    button.disabled = false;
  }

  form.addEventListener('submit', function (event) {
    event.preventDefault();
    button.disabled = true;
    note.classList.remove('error');
    note.textContent = 'Opening secure checkout…';
    // Only identifiers go to the server; it supplies prices and Printify IDs.
    var item = {
      productId: form.dataset.product,
      variantId: form.dataset.color + '-' + form.elements.size.value,
      quantity: Number(form.elements.quantity.value)
    };
    fetch('/api/checkout-session', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ items: [item] })
    })
      .then(function (res) { return res.json().then(function (data) { return { ok: res.ok, data: data }; }); })
      .then(function (r) {
        if (!r.ok || !r.data.url) throw new Error(r.data.error || 'failed');
        window.location.assign(r.data.url);
      })
      .catch(function () {
        fail('Checkout is unavailable right now. Please try again shortly.');
      });
  });

  // Returning from Stripe with the back button restores the page from cache with the button disabled.
  window.addEventListener('pageshow', function (e) {
    if (e.persisted) { button.disabled = false; note.textContent = idle; note.classList.remove('error'); }
  });
})();
