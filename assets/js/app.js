/* Sanhita Atlas — PWA app */
(function () {
  'use strict';

  var DATA = null, FUSE = null, CH = {}, SECS = [];
  var view = document.getElementById('view');
  var store = {
    get: function (k, d) { try { return JSON.parse(localStorage.getItem('sa:' + k)) || d; } catch (e) { return d; } },
    set: function (k, v) { try { localStorage.setItem('sa:' + k, JSON.stringify(v)); } catch (e) {} }
  };
  var saved = store.get('saved', []);
  var last = store.get('last', null);

  var IC = {
    home: '<path d="M4 10.5L12 4l8 6.5V20H4z"/><path d="M9.5 20v-5h5v5"/>',
    list: '<path d="M8 6h12M8 12h12M8 18h12"/><circle cx="4.2" cy="6" r="1.1"/><circle cx="4.2" cy="12" r="1.1"/><circle cx="4.2" cy="18" r="1.1"/>',
    bookmark: '<path d="M6 4h12v16l-6-4.2L6 20V4z"/>',
    more: '<circle cx="12" cy="12" r="8.5"/><path d="M12 11v5M12 8h.01"/>',
    search: '<circle cx="11" cy="11" r="6.5"/><path d="M20 20l-4.2-4.2"/>',
    back: '<path d="M15 6l-6 6 6 6"/>',
    chev: '<path d="M9 6l6 6-6 6"/>',
    book: '<path d="M4 5.5A1.5 1.5 0 015.5 4H10a2 2 0 012 2v13a2 2 0 00-2-2H5.5A1.5 1.5 0 014 15.5v-10z"/><path d="M20 5.5A1.5 1.5 0 0018.5 4H14a2 2 0 00-2 2v13a2 2 0 012-2h4.5a1.5 1.5 0 001.5-1.5v-10z"/>',
    layers: '<path d="M12 3l8.5 4.5L12 12 3.5 7.5 12 3z"/><path d="M3.5 12L12 16.5 20.5 12M3.5 16.5L12 21l8.5-4.5"/>',
    scale: '<path d="M12 4v16M7 20h10M4 8h16"/><path d="M4 8l-2 5h4L4 8zM20 8l-2 5h4l-2-5z"/>',
    gavel: '<path d="M13.5 4.5l6 6M16.5 7.5l-9 9M4 20h8"/><path d="M9.5 3.5l4 4-2.5 2.5-4-4z"/>',
    git: '<circle cx="6" cy="6" r="2.4"/><circle cx="6" cy="18" r="2.4"/><circle cx="18" cy="12" r="2.4"/><path d="M6 8.4v7.2M8.4 6h5.2a2 2 0 012 2v1.6"/>',
    spark: '<path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8L12 3z"/>',
    download: '<path d="M12 4v11M7 11l5 5 5-5M5 20h14"/>',
    trash: '<path d="M4 7h16M9 7V4h6v3M6 7l1 13h10l1-13"/>'
  };
  function ic(n, cls) {
    return '<svg class="' + (cls || '') + '" viewBox="0 0 24 24" fill="none" stroke="currentColor" ' +
      'stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + IC[n] + '</svg>';
  }
  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c];
    });
  }
  function toast(msg) {
    var t = document.getElementById('toast');
    t.textContent = msg; t.classList.add('on');
    clearTimeout(t._t); t._t = setTimeout(function () { t.classList.remove('on'); }, 1800);
  }

  /* ── data ───────────────────────────────────────────────────────────── */
  function load() {
    return fetch('assets/data/sections.json').then(function (r) { return r.json(); }).then(function (d) {
      DATA = d; SECS = d.sections;
      d.chapters.forEach(function (c) { CH[c.n] = c; });
      if (window.Fuse) {
        FUSE = new Fuse(SECS, {
          keys: [{ name: 't', weight: 3 }, { name: 'x', weight: 1 }],
          threshold: .34, ignoreLocation: true, minMatchCharLength: 2
        });
      }
      return d;
    });
  }

  /* ── router ─────────────────────────────────────────────────────────── */
  function parse() {
    var h = (location.hash || '#/home').replace(/^#\/?/, '');
    var p = h.split('/');
    return { name: p[0] || 'home', arg: p[1] || '' };
  }
  function go(path) { location.hash = '#/' + path; }
  function route() {
    var r = parse();
    var html = '';
    if (r.name === 'section' && r.arg) html = vSection(+r.arg);
    else if (r.name === 'chapter' && r.arg) html = vChapter(+r.arg);
    else if (r.name === 'browse') html = vBrowse();
    else if (r.name === 'saved') html = vSaved();
    else if (r.name === 'more') html = vMore();
    else html = vHome();
    view.innerHTML = '<div class="fade">' + html + '</div>';
    document.querySelectorAll('[data-tab]').forEach(function (t) {
      var n = t.getAttribute('data-tab');
      var on = (n === 'home' && (r.name === 'home' || r.name === 'section' || r.name === 'chapter')) ||
        n === r.name;
      t.classList.toggle('on', on);
    });
    window.scrollTo(0, 0);
    afterRender(r);
  }
  function afterRender(r) {
    var s = view.querySelector('#q');
    if (s) { s.value = q; s.addEventListener('input', function () { q = this.value; paintList(); }); }
    view.querySelectorAll('[data-chip]').forEach(function (c) {
      c.addEventListener('click', function () {
        chip = c.getAttribute('data-chip');
        view.querySelectorAll('[data-chip]').forEach(function (x) { x.classList.toggle('on', x === c); });
        paintList();
      });
    });
    if (r.name === 'section') {
      var b = view.querySelector('#bm');
      if (b) b.addEventListener('click', function () { toggleSave(+r.arg); });
    }
  }

  /* ── views ──────────────────────────────────────────────────────────── */
  function vHome() {
    var cont = last ? SECS.filter(function (s) { return s.n === last; })[0] : null;
    var chapters = DATA.chapters.map(function (c) {
      return '<a class="tile" href="#/chapter/' + c.n + '" style="--lc:' + c.c + '">' +
        '<span class="tile__k"><span class="dot" style="background:' + c.c + '"></span>Ch ' + c.r + '</span>' +
        '<h3>' + esc(c.t) + '</h3><p>ss. ' + c.f + '–' + c.l + '</p></a>';
    }).join('');
    var ann = SECS.filter(function (s) { return s.a; }).slice(0, 6).map(function (s) {
      return '<a class="tile" href="#/section/' + s.n + '" style="--lc:' + s.col + '">' +
        '<span class="tile__k"><span class="dot" style="background:' + s.col + '"></span>' + s.n + '</span>' +
        '<h3>' + esc(s.t) + '</h3></a>';
    }).join('');
    return '' +
      '<section class="hero">' +
      '<span class="orb orb--1"></span><span class="orb orb--2"></span>' +
      '<div class="hero__in">' +
      '<p class="hero__k">Bharatiya Nyaya Sanhita &middot; 2023</p>' +
      '<h1>The penal code, <em>annotated</em>.</h1>' +
      '<p>All 358 sections with the text, an explanation, a worked example and the case law that still governs it.</p>' +
      '<div class="hero__act">' +
      '<a class="btn btn--primary" href="#/browse">Browse sections</a>' +
      '<a class="btn btn--ghost" href="#/section/103">s. 103 &rarr;</a>' +
      '</div>' +
      '<div class="hstats">' +
      '<div class="hstat"><b>358</b><span>Sections</span></div>' +
      '<div class="hstat"><b>20</b><span>Chapters</span></div>' +
      '<div class="hstat"><b>21</b><span>Annotated</span></div>' +
      '<div class="hstat"><b>37</b><span>IPC maps</span></div>' +
      '</div></div></section>' +
      (cont ? '<div class="sect"><div class="sect__head"><h2>Continue reading</h2></div>' +
        '<a class="row" href="#/section/' + cont.n + '">' +
        '<span class="row__n">' + cont.n + '</span><span class="row__t">' + esc(cont.t) + '</span>' +
        '<span class="row__chev">' + ic('chev') + '</span></a></div>' : '') +
      '<div class="sect"><div class="sect__head"><h2>Chapters</h2>' +
      '<a href="#/browse">All sections</a></div><div class="grid grid--3">' + chapters + '</div></div>' +
      '<div class="sect"><div class="sect__head"><h2>Annotated</h2></div>' +
      '<div class="grid grid--3">' + ann + '</div></div>' +
      '<div class="note">Independent reference, not legal advice. Text extracted from the Gazette ' +
      'notification of 25 December 2023.</div>';
  }

  var q = '', chip = '';
  function vBrowse() {
    var chips = '<button class="chip' + (chip === '' ? ' on' : '') + '" data-chip="">All</button>' +
      DATA.chapters.map(function (c) {
        return '<button class="chip' + (chip === String(c.n) ? ' on' : '') + '" data-chip="' + c.n + '">' +
          c.r + ' &middot; ' + esc(c.t.split(' ').slice(0, 2).join(' ')) + '</button>';
      }).join('');
    return '<h1 style="margin:0 0 .7rem">All 358 sections</h1>' +
      '<div class="searchbar">' + ic('search') +
      '<input id="q" type="search" placeholder="Search sections, offences, phrases" value="' + esc(q) + '">' +
      '</div><div class="chips">' + chips + '</div>' +
      '<p class="count" id="count"></p><div id="list"></div>';
  }
  function paintList() {
    var box = document.getElementById('list');
    if (!box) return;
    var t = q.trim();
    var rows;
    if (t && FUSE) rows = FUSE.search(t).slice(0, 60).map(function (r) { return r.item; });
    else if (t) rows = SECS.filter(function (s) {
      return (s.t + ' ' + s.x).toLowerCase().indexOf(t.toLowerCase()) > -1;
    }).slice(0, 60);
    else rows = chip ? SECS.filter(function (s) { return String(s.ch) === chip; }) : SECS;
    document.getElementById('count').textContent = rows.length + ' of 358';
    box.innerHTML = rows.map(function (s) {
      return '<a class="row" href="#/section/' + s.n + '">' +
        '<span class="row__n" style="color:' + s.col + '">' + s.n + '</span>' +
        '<span class="row__t">' + esc(s.t) + '</span>' +
        (s.a ? '<span class="row__m">A</span>' : '') +
        '<span class="row__chev">' + ic('chev') + '</span></a>';
    }).join('');
  }

  function vChapter(n) {
    var c = CH[n];
    if (!c) return vHome();
    var rows = SECS.filter(function (s) { return s.ch === n; }).map(function (s) {
      return '<a class="row" href="#/section/' + s.n + '">' +
        '<span class="row__n" style="color:' + s.col + '">' + s.n + '</span>' +
        '<span class="row__t">' + esc(s.t) + '</span>' +
        (s.a ? '<span class="row__m">A</span>' : '') +
        '<span class="row__chev">' + ic('chev') + '</span></a>';
    }).join('');
    return '<a class="btn btn--light btn--sm" href="#/home" style="margin-bottom:.9rem">' +
      ic('back') + ' Home</a>' +
      '<div class="sec-top"><span class="sec-num" style="color:' + c.c + '">' + c.r + '</span>' +
      '<span class="sec-crumb" style="color:' + c.c + '">Chapter &middot; ss. ' + c.f + '–' + c.l + '</span></div>' +
      '<h1 class="sec-title">' + esc(c.t) + '</h1>' +
      '<p style="color:var(--dim);font-size:.88rem;margin-bottom:1.1rem">' + esc(c.b) + '</p>' + rows;
  }

  function vSection(n) {
    var s = SECS.filter(function (x) { return x.n === n; })[0];
    if (!s) return vHome();
    last = n; store.set('last', n);
    var isSaved = saved.indexOf(n) > -1;
    var body = s.x.split(/(?<=[;:.,—])\s+(?:or\s+)?(?=\([a-z0-9]{1,3}\)\s)|(?=\([ivx]{1,4}\)\s)|(?=(?:Explanation|Illustration|Exception)\s?[0-9]?\.?—)/)
      .filter(function (p) { return p.trim(); })
      .map(function (p) { return '<p>' + esc(p.trim()) + '</p>'; }).join('');
    var a = s.a;
    var annHtml = '';
    if (a) {
      annHtml += '<div class="block"><p class="block__k">What it means</p>' +
        a.why.map(function (w) { return '<p>' + esc(w) + '</p>'; }).join('') + '</div>';
      if (a.ex) annHtml += '<div class="block"><p class="block__k">Worked example</p>' +
        '<div class="example"><span class="lbl">Illustration</span><p>' + esc(a.ex) + '</p></div></div>';
      if (a.cases && a.cases.length) annHtml += '<div class="block"><p class="block__k">Case law</p>' +
        a.cases.map(function (c) {
          return '<article class="case"><h4>' + esc(c[0]) + '</h4><span>' + esc(c[1]) + '</span>' +
            '<p>' + esc(c[2]) + '</p></article>';
        }).join('') + '</div>';
    }
    var refs = (s.refs || []).map(function (r) {
      var t = SECS.filter(function (x) { return x.n === r; })[0];
      return '<a href="#/section/' + r + '">' + r + ' &middot; ' + esc((t ? t.t : '').slice(0, 26)) + '</a>';
    }).join('');
    var prev = SECS.filter(function (x) { return x.n === n - 1; })[0];
    var next = SECS.filter(function (x) { return x.n === n + 1; })[0];
    return '<a class="btn btn--light btn--sm" href="#/chapter/' + s.ch + '" style="margin-bottom:.9rem">' +
      ic('back') + ' Ch ' + s.cr + '</a>' +
      '<div class="sec-top"><span class="sec-num" style="color:' + s.col + '">' + s.n + '</span>' +
      '<span class="sec-crumb" style="color:' + s.col + '">Chapter ' + s.cr + '</span>' +
      '<button class="iconbtn" id="bm" style="margin-left:auto" aria-label="Save">' +
      '<svg viewBox="0 0 24 24" fill="' + (isSaved ? 'currentColor' : 'none') + '" stroke="currentColor" ' +
      'stroke-width="1.7" stroke-linejoin="round"><path d="M6 4h12v16l-6-4.2L6 20V4z"/></svg></button></div>' +
      '<h1 class="sec-title">' + esc(s.t) + '</h1>' +
      '<div class="pills"><span class="pill pill--m">s. ' + s.n + '</span>' +
      (a ? '<span class="pill pill--b">Annotated</span>' : '') +
      (s.ipc && s.ipc !== '—' ? '<span class="pill">IPC ' + esc(s.ipc) + '</span>' : '') +
      '<span class="pill">In force 1 Jul 2024</span></div>' +
      '<div class="statute">' + body + '</div>' + annHtml +
      '<div class="meta">' +
      '<div><dt>Chapter</dt><dd>' + s.cr + ' — ' + esc(s.ct) + '</dd></div>' +
      '<div><dt>IPC equivalent</dt><dd>' + (s.ipc ? (s.ipc === '—' ? 'None — new offence' : 'Section ' + esc(s.ipc)) : '—') + '</dd></div>' +
      (s.pun ? '<div style="grid-column:1/-1"><dt>Punishment</dt><dd>' + esc(s.pun) + '</dd></div>' : '') +
      '</div>' +
      (refs ? '<div class="block" style="margin-top:1.1rem"><p class="block__k">Cross-references</p>' +
        '<div class="refs">' + refs + '</div></div>' : '') +
      '<div class="nav2">' +
      (prev ? '<a href="#/section/' + prev.n + '"><span>Previous</span><b>' + prev.n + '. ' + esc(prev.t) + '</b></a>' : '<span></span>') +
      (next ? '<a class="n2" href="#/section/' + next.n + '"><span>Next</span><b>' + next.n + '. ' + esc(next.t) + '</b></a>' : '') +
      '</div>' +
      '<div class="note">Text extracted from the Gazette notification of 25 December 2023. Check the official ' +
      'copy before relying on it.</div>';
  }

  function vSaved() {
    if (!saved.length) {
      return '<h1 style="margin:0 0 .7rem">Saved</h1><div class="empty">' + ic('bookmark') +
        '<h3>Nothing saved yet</h3><p>Tap the bookmark on any section to keep it here.</p></div>';
    }
    var rows = saved.slice().sort(function (a, b) { return a - b; }).map(function (n) {
      var s = SECS.filter(function (x) { return x.n === n; })[0];
      if (!s) return '';
      return '<a class="row" href="#/section/' + s.n + '">' +
        '<span class="row__n" style="color:' + s.col + '">' + s.n + '</span>' +
        '<span class="row__t">' + esc(s.t) + '</span>' +
        '<span class="row__chev">' + ic('chev') + '</span></a>';
    }).join('');
    return '<h1 style="margin:0 0 .7rem">Saved</h1>' +
      '<p class="count">' + saved.length + ' section' + (saved.length === 1 ? '' : 's') + '</p>' + rows;
  }

  function vMore() {
    return '<h1 style="margin:0 0 .9rem">More</h1>' +
      '<div class="card" style="margin-bottom:.6rem"><h3 style="margin:0 0 .3rem">Sanhita Atlas</h3>' +
      '<p style="margin:0;font-size:.85rem;color:var(--dim)">A reference to the Bharatiya Nyaya Sanhita, 2023 — ' +
      'all 358 sections with annotations and case law. Independent, unaffiliated, not legal advice.</p></div>' +
      '<button class="row" id="install" style="width:100%;text-align:left;cursor:pointer">' +
      '<span class="row__n">' + ic('download') + '</span><span class="row__t">Install as an app</span>' +
      '<span class="row__chev">' + ic('chev') + '</span></button>' +
      '<a class="row" href="https://www.indiacode.nic.in/" target="_blank" rel="noopener">' +
      '<span class="row__n">' + ic('book') + '</span><span class="row__t">India Code (official source)</span>' +
      '<span class="row__chev">' + ic('chev') + '</span></a>' +
      '<button class="row" id="clear" style="width:100%;text-align:left;cursor:pointer">' +
      '<span class="row__n">' + ic('trash') + '</span><span class="row__t">Clear saved sections</span>' +
      '<span class="row__chev">' + ic('chev') + '</span></button>' +
      '<div class="note">Offline ready — the whole code is cached after first load. ' +
      'Version 1.0 &middot; updated October 2026.</div>';
  }

  function toggleSave(n) {
    var i = saved.indexOf(n);
    if (i > -1) { saved.splice(i, 1); toast('Removed from saved'); }
    else { saved.push(n); toast('Saved'); }
    store.set('saved', saved);
    route();
  }

  /* ── boot ───────────────────────────────────────────────────────────── */
  function bind() {
    var gs = document.getElementById('goSearch');
    if (gs) gs.addEventListener('click', function () {
      go('browse');
      setTimeout(function () { var i = document.getElementById('q'); if (i) i.focus(); }, 80);
    });
    document.querySelectorAll('[data-tab]').forEach(function (t) {
      t.addEventListener('click', function () {
        var n = t.getAttribute('data-tab');
        go(n === 'home' ? 'home' : n);
      });
    });
    window.addEventListener('hashchange', route);
    document.addEventListener('click', function (e) {
      var i = e.target.closest('#install'); if (i) { promptInstall(); return; }
      var c = e.target.closest('#clear');
      if (c) { saved = []; store.set('saved', []); toast('Cleared'); route(); }
    });
  }

  var deferred = null;
  window.addEventListener('beforeinstallprompt', function (e) {
    e.preventDefault(); deferred = e;
  });
  function promptInstall() {
    if (deferred) { deferred.prompt(); deferred = null; }
    else toast('Use your browser menu → Add to Home Screen');
  }

  function offline() {
    document.body.classList.toggle('is-offline', !navigator.onLine);
  }
  window.addEventListener('online', offline);
  window.addEventListener('offline', offline);

  load().then(function () {
    bind(); route(); paintList(); offline();
    if ('serviceWorker' in navigator) {
      navigator.serviceWorker.register('sw.js').catch(function () {});
    }
  }).catch(function () {
    view.innerHTML = '<div class="empty"><h3>Could not load the code</h3>' +
      '<p>Check your connection and reload.</p></div>';
  });
})();
