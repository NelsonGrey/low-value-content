(function () {
  var token = new URLSearchParams(window.location.search).get('token');
  var title = document.getElementById('order-title');
  var message = document.getElementById('order-message');
  var details = document.getElementById('order-details');
  var copy = {
    awaiting_payment: ['Confirming your payment…', 'This usually takes a few seconds. This page updates on its own.'],
    paid: ['Payment received.', 'We are sending your order to the print shop.'],
    submitting: ['Payment received.', 'We are sending your order to the print shop.'],
    on_hold: ['Order received.', 'Your shirt is queued. We review every order before printing begins.'],
    in_production: ['Your shirt is being printed.', 'You will get an email with tracking when it ships.'],
    shipped: ['Your shirt has shipped.', 'Tracking details are below.'],
    delivered: ['Delivered.', 'Thank you for the low-value purchase.'],
    canceled: ['This order was canceled.', 'Contact support if you were not expecting this.'],
    payment_failed: ['Payment did not go through.', 'You have not been charged. You can try again from the drop page.'],
    expired: ['Checkout expired.', 'You have not been charged. You can start again from the drop page.'],
    fulfillment_error: ['Order received.', 'We hit a snag and are on it. No action needed.'],
    needs_review: ['Order received.', 'We are reviewing a detail and will email you if we need anything.']
  };
  var terminal = { shipped: 1, delivered: 1, canceled: 1, payment_failed: 1, expired: 1 };
  var tries = 0;

  function row(label, value) {
    var dt = document.createElement('dt'); dt.textContent = label;
    var dd = document.createElement('dd'); dd.appendChild(value);
    details.append(dt, dd);
  }

  function render(order) {
    var c = copy[order.status] || copy.paid;
    title.textContent = c[0];
    message.textContent = c[1];
    details.textContent = '';
    row('Status', document.createTextNode(order.status.replace(/_/g, ' ')));
    if (order.amountTotal != null) row('Total', document.createTextNode('$' + (order.amountTotal / 100).toFixed(2)));
    if (order.trackingNumber) {
      var node;
      if (/^https:\/\//.test(order.trackingUrl || '')) {
        node = document.createElement('a'); node.href = order.trackingUrl; node.rel = 'noopener';
        node.textContent = order.trackingNumber;
      } else node = document.createTextNode(order.trackingNumber);
      row('Tracking', node);
    }
  }

  function poll() {
    if (!token) { title.textContent = 'Order not found.'; message.textContent = 'Use the link from your checkout confirmation.'; return; }
    fetch('/api/orders/' + encodeURIComponent(token), { cache: 'no-store' })
      .then(function (res) { return res.ok ? res.json() : null; })
      .then(function (order) {
        if (order) { render(order); if (terminal[order.status]) return; }
        if (++tries < 40) setTimeout(poll, 3000);
      })
      .catch(function () { if (++tries < 40) setTimeout(poll, 5000); });
  }
  poll();
})();
