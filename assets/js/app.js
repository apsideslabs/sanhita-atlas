/* Sanhita Atlas — UI layer
   Alpine components for the drawer, the search modal and the table filters. */

(function () {
  'use strict';

  window.__SA = {loaded:true, events:[]};
  var meta = document.querySelector('meta[name="sa-base"]');
  var BASE = meta ? meta.getAttribute('content') : '';

  function setBody(cls, on) {
    document.body.classList.toggle(cls, on);
    document.body.classList.toggle('is-locked', on);
  }

  /* ── global drawer ─────────────────────────────────────────────────── */
  window.addEventListener('toggle-drawer', function () {
    window.__SA.events.push('toggle:'+(typeof window.Alpine));
    if (!window.Alpine) return;
    var s = Alpine.store('ui');
    s.drawer = !s.drawer;
    setBody('drawer-open', s.drawer);
    var btn = document.getElementById('menuBtn');
    if (btn) btn.setAttribute('aria-expanded', String(s.drawer));
    var dr = document.getElementById('drawer');
    if (dr) dr.setAttribute('aria-hidden', String(!s.drawer));
  });

  window.addEventListener('close-drawer', function () {
    if (!window.Alpine) return;
    Alpine.store('ui').drawer = false;
    setBody('drawer-open', false);
    var btn = document.getElementById('menuBtn');
    if (btn) btn.setAttribute('aria-expanded', 'false');
    var dr = document.getElementById('drawer');
    if (dr) dr.setAttribute('aria-hidden', 'true');
  });

  window.addEventListener('open-search', function () {
    if (!window.Alpine) return;
    Alpine.store('ui').search = true;
    setBody('search-open', true);
    setTimeout(function () {
      var i = document.getElementById('sq');
      if (i) { i.value = ''; i.focus(); }
    }, 40);
  });

  window.addEventListener('close-search', function () {
    if (!window.Alpine) return;
    Alpine.store('ui').search = false;
    setBody('search-open', false);
  });

  /* keyboard: / or cmd+k opens search, esc closes */
  document.addEventListener('keydown', function (e) {
    var tag = (e.target.tagName || '').toLowerCase();
    var typing = tag === 'input' || tag === 'textarea' || tag === 'select';
    if ((e.key === '/' || ((e.metaKey || e.ctrlKey) && e.key === 'k')) && !typing) {
      e.preventDefault();
      window.dispatchEvent(new Event('open-search'));
    }
    if (e.key === 'Escape') {
      window.dispatchEvent(new Event('close-search'));
      window.dispatchEvent(new Event('close-drawer'));
    }
  });

  /* ── Alpine components ─────────────────────────────────────────────── */
  document.addEventListener('alpine:init', function () {
    Alpine.store('ui', { drawer: false, search: false });

    Alpine.data('searchModal', function () {
      return {
        base: BASE,
        q: '',
        results: [],
        sel: 0,
        fuse: null,
        index: [],
        loaded: false,
        loading: false,

        open: function () {
          this.q = '';
          this.results = [];
          this.sel = 0;
          this.load();
        },
        load: function () {
          var self = this;
          if (this.loaded || this.loading) return;
          this.loading = true;
          fetch(BASE + 'assets/data/search.json')
            .then(function (r) { return r.json(); })
            .then(function (data) {
              self.index = data;
              if (window.Fuse) {
                self.fuse = new Fuse(data, {
                  keys: [{ name: 'title', weight: 2 }, { name: 'text', weight: 1 }],
                  threshold: 0.36, ignoreLocation: true, minMatchCharLength: 2
                });
              }
              self.loaded = true;
              if (self.q) self.run();
            })
            .catch(function () { self.loaded = true; });
        },
        run: function () {
          var q = (this.q || '').trim();
          if (!q) { this.results = []; return; }
          var out;
          if (this.fuse) {
            out = this.fuse.search(q).slice(0, 30).map(function (r) { return r.item; });
          } else {
            var t = q.toLowerCase();
            out = this.index.filter(function (x) {
              return (x.title + ' ' + x.text).toLowerCase().indexOf(t) > -1;
            }).slice(0, 30);
          }
          this.results = out;
          this.sel = 0;
        },
        move: function (d) {
          if (!this.results.length) return;
          this.sel = (this.sel + d + this.results.length) % this.results.length;
        },
        go: function () {
          var r = this.results[this.sel];
          if (!r) return;
          window.location.href = this.base + r.url;
        },
        close: function () {
          window.dispatchEvent(new Event('close-search'));
        }
      };
    });

    Alpine.data('sectionTable', function () {
      return {
        q: '',
        ch: '',
        shown: 0,
        init: function () {
          var m = new URLSearchParams(window.location.search).get('ch');
          if (m) this.ch = m;
          this.filter();
        },
        filter: function () {
          var rows = this.$refs.body.querySelectorAll('tr');
          var q = this.q.trim().toLowerCase();
          var ch = this.ch;
          var n = 0;
          rows.forEach(function (r) {
            var ok = (!q || r.dataset.s.indexOf(q) > -1) && (!ch || r.dataset.ch === ch);
            r.hidden = !ok;
            if (ok) n++;
          });
          this.shown = n;
        }
      };
    });

    Alpine.data('rowFilter', function () {
      return {
        q: '',
        shown: 0,
        init: function () { this.filter(); },
        filter: function () {
          var rows = this.$refs.body.querySelectorAll('tr');
          var q = this.q.trim().toLowerCase();
          var n = 0;
          rows.forEach(function (r) {
            var ok = !q || r.dataset.s.indexOf(q) > -1;
            r.hidden = !ok;
            if (ok) n++;
          });
          this.shown = n;
        }
      };
    });
  });
})();
