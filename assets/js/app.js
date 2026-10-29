(function () {
  'use strict';
  var BASE = (document.querySelector('meta[name="sa-base"]') || {}).content || '';

  function setBody(cls, on) {
    document.body.classList.toggle(cls, on);
    document.body.classList.toggle('locked', on);
  }

  window.addEventListener('toggle-drawer', function () {
    if (!window.Alpine) return;
    var s = Alpine.store('ui'); s.drawer = !s.drawer;
    setBody('drawer-open', s.drawer);
  });
  window.addEventListener('close-drawer', function () {
    if (!window.Alpine) return;
    Alpine.store('ui').drawer = false; setBody('drawer-open', false);
  });
  window.addEventListener('open-search', function () {
    if (!window.Alpine) return;
    Alpine.store('ui').search = true; setBody('search-open', true);
    setTimeout(function () { var i = document.getElementById('sq'); if (i) { i.value = ''; i.focus(); } }, 40);
  });
  window.addEventListener('close-search', function () {
    if (!window.Alpine) return;
    Alpine.store('ui').search = false; setBody('search-open', false);
  });

  document.addEventListener('keydown', function (e) {
    var tag = (e.target.tagName || '').toLowerCase();
    var typing = tag === 'input' || tag === 'textarea' || tag === 'select';
    if ((e.key === '/' || ((e.metaKey || e.ctrlKey) && e.key === 'k')) && !typing) {
      e.preventDefault(); window.dispatchEvent(new Event('open-search'));
    }
    if (e.key === 'Escape') {
      window.dispatchEvent(new Event('close-search'));
      window.dispatchEvent(new Event('close-drawer'));
    }
  });

  document.addEventListener('alpine:init', function () {
    if (!Alpine.store('ui')) Alpine.store('ui', { drawer: false, search: false });

    Alpine.data('searchModal', function () {
      return {
        base: BASE, q: '', results: [], sel: 0, fuse: null, index: [], loaded: false, loading: false,
        open: function () { this.q = ''; this.results = []; this.sel = 0; this.load(); },
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
                  keys: [{ name: 'title', weight: 3 }, { name: 'text', weight: 1 }],
                  threshold: 0.32, ignoreLocation: true, minMatchCharLength: 2
                });
              }
              self.loaded = true; if (self.q) self.run();
            })
            .catch(function () { self.loaded = true; });
        },
        run: function () {
          var q = (this.q || '').trim();
          if (!q) { this.results = []; return; }
          if (this.fuse) { this.results = this.fuse.search(q).slice(0, 25).map(function (r) { return r.item; }); }
          else {
            var t = q.toLowerCase();
            this.results = this.index.filter(function (x) {
              return (x.title + ' ' + x.text).toLowerCase().indexOf(t) > -1;
            }).slice(0, 25);
          }
          this.sel = 0;
        },
        move: function (d) { if (this.results.length) this.sel = (this.sel + d + this.results.length) % this.results.length; },
        go: function () { var r = this.results[this.sel]; if (r) window.location.href = this.base + r.url; },
        close: function () { window.dispatchEvent(new Event('close-search')); }
      };
    });

    Alpine.data('tableFilter', function () {
      return {
        q: '', ch: '', shown: 0,
        init: function () { this.filter(); },
        filter: function () {
          var rows = this.$refs.body.querySelectorAll('tr');
          var q = this.q.trim().toLowerCase(), ch = this.ch, n = 0;
          rows.forEach(function (r) {
            var ok = (!q || r.dataset.s.indexOf(q) > -1) && (!ch || r.dataset.ch === ch);
            r.hidden = !ok; if (ok) n++;
          });
          this.shown = n;
        }
      };
    });
  });
})();
