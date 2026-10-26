// Adds a thin "back to the site" strip to the top of a standalone page.
// Usage, before </body>:
// <script src="/assets/js/return-strip.js" data-section="Culture" data-section-url="/culture/" data-title="Johnew's Kitchen" defer></script>
(function () {
  var me = document.currentScript;
  var section = (me && me.getAttribute('data-section')) || '';
  var sectionUrl = (me && me.getAttribute('data-section-url')) || '/';
  var title = (me && me.getAttribute('data-title')) || document.title;
  var note = (me && me.getAttribute('data-note')) || '';
  var css = '' +
    '.jz-strip{display:flex;align-items:center;gap:10px;padding:0 max(16px,env(safe-area-inset-left,0px));min-height:38px;' +
    'background:#f5f5f1;border-bottom:1px solid #d5d7d0;font:12px/1.2 Arial,Helvetica,sans-serif;color:#0f1a2b;position:relative;z-index:50}' +
    '.jz-strip a{color:inherit;text-decoration:none}' +
    '.jz-strip .jz-m{flex:none;width:20px;height:20px;border:1.25px solid currentColor;display:grid;place-items:center;font:10px/1 "DM Serif Display",Georgia,serif}' +
    '.jz-strip .jz-n{font-size:11px;letter-spacing:.16em;text-transform:uppercase;font-weight:700;display:flex;align-items:center;gap:10px;min-height:38px}' +
    '.jz-strip .jz-c{color:#5d6672;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;min-width:0}' +
    '.jz-strip .jz-b{margin-left:auto;font-weight:700;letter-spacing:.04em;color:#1f4e8c;white-space:nowrap;min-height:38px;display:inline-flex;align-items:center}' +
    '.jz-strip a:hover{text-decoration:underline}' +
    '.jz-strip .jz-note{margin-left:auto;color:#5d6672;font-size:11px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;min-width:0}.jz-strip .jz-note+.jz-b{margin-left:16px}' +
    '@media (max-width:1000px){.jz-strip .jz-note{display:none}.jz-strip .jz-note+.jz-b{margin-left:auto}}' +
    '@media (max-width:560px){.jz-strip .jz-c{display:none}}' +
    '@media (prefers-color-scheme:dark){:root:not([data-theme="light"]) .jz-strip{background:#0f1319;border-color:#2c3440;color:#e3e8ef}:root:not([data-theme="light"]) .jz-strip .jz-c{color:#8f99a7}:root:not([data-theme="light"]) .jz-strip .jz-b{color:#6ea3e6}}' +
    ':root[data-theme="dark"] .jz-strip{background:#0f1319;border-color:#2c3440;color:#e3e8ef}:root[data-theme="dark"] .jz-strip .jz-c{color:#8f99a7}:root[data-theme="dark"] .jz-strip .jz-b{color:#6ea3e6}' +
    '@media print{.jz-strip{display:none}}';
  var st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);
  var bar = document.createElement('nav');
  bar.className = 'jz-strip';
  bar.setAttribute('aria-label', 'Johnew Zhang site');
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  bar.innerHTML =
    '<a class="jz-n" href="/"><span class="jz-m" aria-hidden="true">JZ</span>Johnew Zhang</a>' +
    '<span class="jz-c">' + (section ? '/ <a href="' + esc(sectionUrl) + '">' + esc(section) + '</a> ' : '') + '/ ' + esc(title) + '</span>' +
    (note ? '<span class="jz-note">' + esc(note) + '</span>' : '') +
    '<a class="jz-b" href="/">← Back to the site</a>';
  document.body.insertBefore(bar, document.body.firstChild);
  // Google Analytics on standalone pages, live site only (not local previews).
  var GA = 'G-ZBQ25JW26B';
  if (/\.github\.io$/.test(location.hostname) && !window.gtag) {
    var g = document.createElement('script'); g.async = true;
    g.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA; document.head.appendChild(g);
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    window.gtag('js', new Date()); window.gtag('config', GA);
  }
})();
