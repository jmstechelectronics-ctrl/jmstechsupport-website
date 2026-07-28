/* JMS Tech Support Meta Pixel: PageView, Contact, and form-confirmed Lead events. */
(function (f, b, e, v, n, t, s) {
  if (f.fbq) return;
  n = f.fbq = function () {
    n.callMethod ? n.callMethod.apply(n, arguments) : n.queue.push(arguments);
  };
  if (!f._fbq) f._fbq = n;
  n.push = n;
  n.loaded = true;
  n.version = "2.0";
  n.queue = [];
  t = b.createElement(e);
  t.async = true;
  t.src = v;
  s = b.getElementsByTagName(e)[0];
  s.parentNode.insertBefore(t, s);
})(window, document, "script", "https://connect.facebook.net/en_US/fbevents.js");

fbq("init", "1537482598109576");
fbq("track", "PageView");

if (document.body && document.body.dataset.metaLead === "true") {
  fbq("track", "Lead");
}

document.addEventListener("click", function (event) {
  var link = event.target.closest('a[href^="tel:"], a[href^="sms:"]');
  if (!link) return;
  fbq("track", "Contact", {
    content_name: link.href.indexOf("tel:") === 0 ? "Phone call" : "SMS enquiry"
  });
});
