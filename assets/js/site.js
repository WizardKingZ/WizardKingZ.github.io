// Theme toggle and the "On this page" list for articles.
(function () {
  var root = document.documentElement;
  var btn = document.getElementById('themeBtn');
  function isDark() {
    var t = root.getAttribute('data-theme');
    if (t) return t === 'dark';
    return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
  }
  function label() { if (btn) btn.textContent = isDark() ? 'Light mode' : 'Dark mode'; }
  if (btn) {
    btn.addEventListener('click', function () {
      var next = isDark() ? 'light' : 'dark';
      root.setAttribute('data-theme', next);
      try { localStorage.setItem('jz-theme', next); } catch (e) {}
      label();
    });
    label();
  }

  var prose = document.getElementById('prose');
  var toc = document.getElementById('toc');
  if (!prose || !toc) return;
  var heads = prose.querySelectorAll('h1[id], h2[id]');
  if (heads.length < 3) return;
  var links = [];
  heads.forEach(function (h) {
    var a = document.createElement('a');
    a.href = '#' + h.id;
    a.textContent = h.textContent;
    toc.appendChild(a);
    links.push(a);
  });
  toc.hidden = false;
  if (!('IntersectionObserver' in window)) return;
  var current = null;
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting) {
        var i = Array.prototype.indexOf.call(heads, e.target);
        if (current) current.classList.remove('on');
        current = links[i]; current.classList.add('on');
      }
    });
  }, { rootMargin: '0px 0px -70% 0px' });
  heads.forEach(function (h) { io.observe(h); });
})();
