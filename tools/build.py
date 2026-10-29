# -*- coding: utf-8 -*-
"""Builds the Sanhita Atlas static site into ./dist."""
import html
import json
import os
import shutil

import data as D

E = lambda s: html.escape(str(s), quote=True)
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dist")

NAV = [
    ("The Sanhita", [
        ("bns/index.html", "Overview"),
        ("bns/chapters.html", "Chapters"),
        ("bns/sections.html", "Section index"),
        ("bns/punishments.html", "Punishments"),
    ]),
    ("Comparison", [
        ("bns/mapping.html", "IPC to BNS"),
        ("bns/changes.html", "What changed"),
    ]),
    ("Procedure", [
        ("procedure/bnss.html", "BNSS"),
        ("procedure/bsa.html", "Evidence Act"),
    ]),
    ("Project", [
        ("research/index.html", "Methodology"),
        ("about.html", "About"),
    ]),
]

ICONS = {
    "book": '<path d="M4 5.5A1.5 1.5 0 015.5 4H10a2 2 0 012 2v13a2 2 0 00-2-2H5.5A1.5 1.5 0 014 15.5v-10z"/><path d="M20 5.5A1.5 1.5 0 0018.5 4H14a2 2 0 00-2 2v13a2 2 0 012-2h4.5a1.5 1.5 0 001.5-1.5v-10z"/>',
    "layers": '<path d="M12 3l8.5 4.5L12 12 3.5 7.5 12 3z"/><path d="M3.5 12L12 16.5 20.5 12M3.5 16.5L12 21l8.5-4.5"/>',
    "list": '<path d="M8 6h12M8 12h12M8 18h12"/><circle cx="4.2" cy="6" r="1.1"/><circle cx="4.2" cy="12" r="1.1"/><circle cx="4.2" cy="18" r="1.1"/>',
    "scale": '<path d="M12 4v16M7 20h10M4 8h16"/><path d="M4 8l-2 5h4L4 8zM20 8l-2 5h4l-2-5z"/>',
    "git": '<circle cx="6" cy="6" r="2.4"/><circle cx="6" cy="18" r="2.4"/><circle cx="18" cy="12" r="2.4"/><path d="M6 8.4v7.2M8.4 6h5.2a2 2 0 012 2v1.6"/>',
    "spark": '<path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8L12 3z"/>',
    "gavel": '<path d="M13.5 4.5l6 6M16.5 7.5l-9 9M4 20h8"/><path d="M9.5 3.5l4 4-2.5 2.5-4-4z"/>',
    "file": '<path d="M13 3H7a2 2 0 00-2 2v14a2 2 0 002 2h10a2 2 0 002-2V9l-6-6z"/><path d="M13 3v6h6"/>',
    "arrow": '<path d="M5 12h13M12.5 6l6 6-6 6"/>',
    "search": '<circle cx="11" cy="11" r="6.5"/><path d="M20 20l-4.2-4.2"/>',
    "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
    "close": '<path d="M6 6l12 12M18 6L6 18"/>',
    "chev": '<path d="M9 6l6 6-6 6"/>',
    "ext": '<path d="M14 4h6v6M20 4l-9 9M18 14v4a2 2 0 01-2 2H6a2 2 0 01-2-2V8a2 2 0 012-2h4"/>',
}

MARK = ('<svg class="brand__mark" viewBox="0 0 32 32" fill="none" aria-hidden="true">'
        '<rect x="1.2" y="1.2" width="29.6" height="29.6" rx="7.5" stroke="#b07d2a" stroke-width="1.6"/>'
        '<path d="M9 11h14M9 16h14M9 21h8" stroke="#fff" stroke-width="1.8" stroke-linecap="round"/></svg>')


def icon(name, cls=""):
    return ('<svg class="%s" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">%s</svg>'
            % (cls, ICONS[name]))


# ── layout ───────────────────────────────────────────────────────────────
def layout(path, title, desc, body, active, wide=False):
    depth = path.count("/")
    rel = "../" * depth
    nav_html = "".join(
        '<div class="hdr__nav__x"><a href="%s%s"%s>%s</a></div>' % ()
        for _ in [0]) if False else "".join(
        '<a href="%s%s"%s>%s</a>' % (rel, h, ' aria-current="true"' if h == active else "", l)
        for h, l in [("bns/index.html", "The Sanhita"), ("bns/mapping.html", "Comparison"),
                     ("procedure/bnss.html", "Procedure"), ("research/index.html", "Research")])

    side = ""
    if not wide:
        groups = []
        for gname, links in NAV:
            items = "".join('<a class="side__a" href="%s%s"%s>%s</a>'
                            % (rel, h, ' aria-current="true"' if h == active else "", E(l))
                            for h, l in links)
            groups.append('<div class="side__grp"><p class="side__k">%s</p>%s</div>' % (E(gname), items))
        side = '<aside class="side">%s</aside>' % "".join(groups)

    drawer_groups = []
    for gname, links in NAV:
        items = "".join('<a class="drawer__link" href="%s%s"%s>%s</a>'
                        % (rel, h, ' aria-current="true"' if h == active else "", E(l))
                        for h, l in links)
        drawer_groups.append('<div class="drawer__group"><p class="drawer__label">%s</p>%s</div>'
                             % (E(gname), items))
    drawer_groups.insert(0, '<div class="drawer__group"><a class="drawer__link" href="%shome" '
                            'style="border-left:0">Home</a></div>' % rel)
    # fix home link: point at index
    drawer_groups[0] = ('<div class="drawer__group"><a class="drawer__link" href="%sindex.html">'
                        'Home</a></div>' % rel)

    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%(title)s</title>
<meta name="description" content="%(desc)s">
<meta name="theme-color" content="#101a16">
<meta property="og:title" content="%(title)s">
<meta property="og:description" content="%(desc)s">
<meta property="og:type" content="website">
<meta name="sa-base" content="%(rel)s">
<link rel="icon" href="%(rel)sassets/img/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@500;600;700&family=Public+Sans:ital,wght@0,400;0,500;0,600;1,400&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="%(rel)sassets/css/app.css">
<script src="https://cdn.jsdelivr.net/npm/fuse.js@7.0.0/dist/fuse.min.js" defer></script>
<script src="%(rel)sassets/js/app.js" defer></script>
<script src="https://cdn.jsdelivr.net/npm/alpinejs@3.14.1/dist/cdn.min.js" defer></script>
</head>
<body>

<header class="hdr">
  <div class="hdr__in">
    <button class="hdr__menu" id="menuBtn" aria-expanded="false" aria-controls="drawer"
            aria-label="Open menu" x-data @click="$dispatch('toggle-drawer')">
      %(menuicon)s<span>Menu</span>
    </button>
    <a class="brand" href="%(rel)sindex.html">%(mark)s<span>Sanhita <span style="color:#e0b062">Atlas</span></span>
      <span class="brand__sub">BNS 2023</span></a>
    <nav class="hdr__nav" aria-label="Primary">%(nav)s</nav>
    <button class="hdr__search" aria-label="Search" x-data @click="$dispatch('open-search')">
      %(searchicon)s<span>Search</span><kbd>/</kbd>
    </button>
  </div>
</header>

<div class="scrim" id="scrim" x-data @click="$dispatch('close-drawer')"></div>

<aside class="drawer" id="drawer" aria-label="Site menu" aria-hidden="true"
       x-data x-bind:class="$store.ui.drawer ? '' : ''">
  <div class="drawer__top">
    <span class="drawer__brand">%(mark)s Sanhita Atlas</span>
    <button class="drawer__x" aria-label="Close menu" x-data @click="$dispatch('close-drawer')">
      %(closeicon)s
    </button>
  </div>
  <div class="drawer__body">%(drawer)s</div>
  <div class="drawer__foot">Reference edition &middot; October 2026<br>Not legal advice.</div>
</aside>

<div class="smodal" id="smodal" x-data="searchModal()" x-show="$store.ui.search" x-cloak
     @open-search.window="open()" @keydown.escape.window="close()">
  <div class="smodal__box" @click.outside="close()">
    <div class="smodal__in">
      %(searchicon)s
      <input id="sq" type="search" placeholder="Search sections, offences, chapters" autocomplete="off"
             x-model="q" @input.debounce.120ms="q = $event.target.value; run()" @keydown.arrow-down.prevent="move(1)"
             @keydown.arrow-up.prevent="move(-1)" @keydown.enter.prevent="go()" x-ref="inp">
      <kbd>esc</kbd>
    </div>
    <div class="smodal__res">
      <template x-if="!q">
        <p class="smodal__none">Search 150+ sections, offences and chapters of the Sanhita.</p>
      </template>
      <template x-if="q && !results.length">
        <p class="smodal__none">No match. Try a section number, an offence or a chapter.</p>
      </template>
      <template x-for="(r,i) in results" :key="r.url+r.title">
        <a :href="base+r.url" :class="i===sel ? 'sel' : ''" @mouseenter="sel=i" @click="close()">
          <strong x-text="r.title"></strong>
          <span x-text="r.context"></span>
        </a>
      </template>
    </div>
    <div class="smodal__foot"><span>&uarr;&darr; move &middot; &crarr; open</span><span x-text="results.length + ' results'"></span></div>
  </div>
</div>

%(shellopen)s
<main class="content%(wideclass)s" id="main">
%(body)s
</main>
%(shellclose)s

<footer class="ftr">
  <div class="ftr__in">
    <div class="ftr__grid">
      <div>
        <div class="ftr__brand">%(mark)s Sanhita Atlas</div>
        <p>An independent research platform for the Bharatiya Nyaya Sanhita, 2023 — the structure, the
        correspondence with the IPC, and what changed on 1 July 2024.</p>
      </div>
      <div>
        <h4>The Sanhita</h4>
        <ul>
          <li><a href="%(rel)sbns/index.html">Overview</a></li>
          <li><a href="%(rel)sbns/chapters.html">Chapters</a></li>
          <li><a href="%(rel)sbns/sections.html">Section index</a></li>
          <li><a href="%(rel)sbns/punishments.html">Punishments</a></li>
        </ul>
      </div>
      <div>
        <h4>Comparison</h4>
        <ul>
          <li><a href="%(rel)sbns/mapping.html">IPC to BNS</a></li>
          <li><a href="%(rel)sbns/changes.html">What changed</a></li>
          <li><a href="%(rel)sprocedure/bnss.html">BNSS</a></li>
          <li><a href="%(rel)sprocedure/bsa.html">Evidence Act</a></li>
        </ul>
      </div>
      <div>
        <h4>Project</h4>
        <ul>
          <li><a href="%(rel)sresearch/index.html">Methodology</a></li>
          <li><a href="%(rel)sabout.html">About</a></li>
          <li><a href="https://www.indiacode.nic.in/" target="_blank" rel="noopener">India Code</a></li>
          <li><a href="https://github.com/apsideslabs/sanhita-atlas" target="_blank" rel="noopener">GitHub</a></li>
        </ul>
      </div>
    </div>
    <div class="ftr__base">
      <span>Compiled 29 October 2026 &middot; Act No. 45 of 2023</span>
      <span>Independent research &middot; not legal advice</span>
    </div>
  </div>
</footer>

<style>[x-cloak]{display:none!important}</style>
</body>
</html>""" % {
        "title": E(title), "desc": E(desc), "rel": rel, "nav": nav_html, "side": side,
        "body": body, "drawer": "".join(drawer_groups), "mark": MARK,
        "menuicon": icon("menu"), "searchicon": icon("search"), "closeicon": icon("close"),
        "shellopen": "" if wide else '<div class="shell">' + side,
        "shellclose": "" if wide else "</div>",
        "wideclass": " content--wide" if wide else "",
    }


def crumbs(items):
    out = []
    for i, (href, label) in enumerate(items):
        last = i == len(items) - 1
        out.append("<em>%s</em>" % E(label) if last else '<a href="%s">%s</a><i>/</i>' % (href, E(label)))
    return '<nav class="crumbs" aria-label="Breadcrumb">%s</nav>' % "".join(out)


def phead(path, title, lede, meta="", trail=None):
    rel = "../" * path.count("/")
    trail = trail or [(rel + "index.html", "Home"), (path.split("/")[0] + "/index.html", path.split("/")[0])]
    return ('<div class="phead">%s<h1>%s</h1><p class="phead__lede">%s</p>%s</div>'
            % (crumbs(trail), title, lede, meta))


def pager(prev, nxt):
    def cell(item, kind):
        if not item:
            return '<span class="pg pg--%s is-empty"></span>' % kind
        href, label, sub = item
        return ('<a class="pg pg--%s" href="%s"><span>%s</span><strong>%s</strong><small>%s</small></a>'
                % (kind, href, "Previous" if kind == "prev" else "Next", label, sub))
    return '<nav class="pager">%s%s</nav>' % (cell(prev, "prev"), cell(nxt, "next"))


# ── pages ────────────────────────────────────────────────────────────────
def home():
    explore = [
        ("bns/chapters.html", "layers", "Chapters", "All 20 chapters with their exact section ranges and what each one covers.", "20 chapters · 358 sections"),
        ("bns/sections.html", "list", "Section index", "A searchable index of the sections that matter in practice, filterable by chapter.", "%d sections" % len(D.SECTIONS)),
        ("bns/mapping.html", "git", "IPC to BNS", "Section-by-section correspondence between the 1860 Code and the 2023 Sanhita.", "39 mappings"),
        ("bns/changes.html", "spark", "What changed", "Twenty new offences, nineteen provisions dropped, and the penalties that moved.", "20 additions"),
        ("procedure/bnss.html", "file", "Procedure", "How the BNSS changes investigation, bail and trial timelines.", "7 anchors"),
        ("bns/punishments.html", "scale", "Punishments", "The seven punishments, community service, and the minimum sentences.", "7 types"),
    ]
    cards = "".join(
        '<a class="ncard" href="%s"><span class="ncard__i">%s</span><h3>%s</h3><p>%s</p>'
        '<span class="ncard__m">%s</span><span class="ncard__a">%s</span></a>'
        % (h, icon(ic), t, d, m, icon("arrow")) for h, ic, t, d, m in explore)

    chap_rows = "".join(
        '<tr><td class="mono" style="color:var(--brass-2)">%s</td><td><strong>%s</strong></td>'
        '<td class="mono num">%d&ndash;%d</td><td style="color:var(--muted)">%d</td></tr>'
        % (r, E(t), f, l, l - f + 1) for n, r, t, f, l, b in D.CHAPTERS[:8])

    return """
<section class="hero">
  <div class="hero__in">
    <div>
      <p class="eyebrow">Bharatiya Nyaya Sanhita &middot; Act 45 of 2023</p>
      <h1>Every section of the Sanhita, <em>mapped</em>.</h1>
      <p class="hero__lede">A research platform for the code that replaced the Indian Penal Code on 1 July 2024 —
      358 sections across 20 chapters, the correspondence with the 1860 Code, and every offence that was added,
      dropped or repriced.</p>
      <div class="hero__act">
        <a class="btn btn--primary" href="bns/chapters.html">Explore the chapters %s</a>
        <a class="btn btn--ghost" href="bns/mapping.html">IPC to BNS mapping</a>
      </div>
    </div>
    <aside class="hero__panel">
      <span class="hero__pk">The Sanhita at a glance</span>
      <dl class="facts">
        <div><dt>358</dt><dd>Sections</dd></div>
        <div><dt>20</dt><dd>Chapters</dd></div>
        <div><dt>20</dt><dd>New offences</dd></div>
        <div><dt>19</dt><dd>Provisions dropped</dd></div>
      </dl>
      <p class="hero__pn">In force 1 July 2024. Repeals the Indian Penal Code, 1860.</p>
    </aside>
  </div>
</section>

<div class="wrap" style="padding-top:2.2rem">
  <div class="stats">
    <div class="stat"><span class="stat__n">33</span><span class="stat__l">Punishments increased</span></div>
    <div class="stat"><span class="stat__n">83</span><span class="stat__l">Fines increased</span></div>
    <div class="stat"><span class="stat__n">23</span><span class="stat__l">Minimum sentences added</span></div>
    <div class="stat"><span class="stat__n">6</span><span class="stat__l">Community service offences</span></div>
  </div>

  <section class="sect">
    <div class="sect__head"><h2>Explore the platform</h2>
      <a class="sect__link" href="bns/index.html">Start with the overview %s</a></div>
    <div class="grid grid--3">%s</div>
  </section>

  <section class="sect">
    <div class="sect__head"><h2>How the Sanhita is organised</h2>
      <a class="sect__link" href="bns/chapters.html">All 20 chapters %s</a></div>
    <div class="tw"><div class="tw__scroll"><table>
      <thead><tr><th style="width:70px">Chapter</th><th>Subject</th><th style="width:110px">Sections</th><th style="width:90px">Count</th></tr></thead>
      <tbody>%s</tbody>
    </table></div></div>
    <p style="font-size:.82rem;color:var(--muted);margin-top:.75rem;max-width:70ch">
      The first eight chapters cover the machinery of the code — definitions, punishments, general exceptions and
      abetment. The substantive offences begin at Chapter V.</p>
  </section>

  <section class="sect">
    <div class="callout callout--warn">
      <div>
        <h4>How to use this platform</h4>
        <p>Sanhita Atlas is an independent index, not a substitute for the Act. Section numbers were renumbered in
        2023 and the correspondence is not one-to-one — always check a provision against the Gazette text before
        relying on it. <a href="research/index.html">Read the methodology</a>.</p>
      </div>
    </div>
  </section>
</div>
""" % (icon("arrow"), icon("arrow"), cards, icon("arrow"), chap_rows)


def bns_overview():
    p = "bns/index.html"
    counts = "".join(
        '<div class="stat"><span class="stat__n">%d</span><span class="stat__l">%s</span></div>'
        % (c, l) for c, l in [("358", "Sections"), ("20", "Chapters"), ("20", "New offences"),
                              ("19", "Provisions dropped")]) if False else ""
    return phead(p, "The Bharatiya Nyaya Sanhita, 2023",
                 "The general penal code of India from 1 July 2024. It consolidates and amends the law relating to "
                 "offences, replacing the Indian Penal Code of 1860 — the statute that had governed Indian criminal "
                 "law for over 160 years.",
                 '<div class="pmeta"><span class="chip chip--ok">In force 1 July 2024</span>'
                 '<span class="chip chip--mono">Act No. 45 of 2023</span>'
                 '<span class="chip">358 sections</span><span class="chip">20 chapters</span></div>',
                 [("../index.html", "Home"), ("index.html", "The Sanhita")]) + """
<div class="prose">
<p>The Sanhita received assent on 25 December 2023 and came into force on 1 July 2024, together with the
Bharatiya Nagarik Suraksha Sanhita (procedure) and the Bharatiya Sakshya Adhiniyam (evidence). The three together
replace the IPC, the Code of Criminal Procedure, 1973 and the Indian Evidence Act, 1872.</p>

<p>Structurally the Sanhita follows the IPC: definitions, then punishments, then general exceptions, then the
substantive offences grouped by subject. What changed is the numbering, the grouping, and a set of new offences
aimed at organised crime, terrorism and offences committed by groups.</p>
</div>

<h2 class="sh">Structure at a glance</h2>
<div class="tw"><div class="tw__scroll"><table>
  <thead><tr><th style="width:80px">Chapter</th><th>Subject</th><th style="width:110px">Sections</th><th style="width:80px">Count</th></tr></thead>
  <tbody>%s</tbody>
</table></div></div>

<h2 class="sh">Sections per chapter</h2>
<p class="slead">Chapter VI and Chapter XIV carry the most sections; Chapter XX carries one. Hover any bar for the
exact count.</p>
<div class="card" style="padding:1.1rem"><canvas id="chapChart" height="220"></canvas></div>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js" defer></script>
<script>
window.addEventListener('load', function () {
  var el = document.getElementById('chapChart');
  if (!el || typeof Chart === 'undefined') return;
  var labels = %s;
  var vals = %s;
  new Chart(el, {
    type: 'bar',
    data: { labels: labels, datasets: [{
      data: vals, backgroundColor: '#b07d2a', hoverBackgroundColor: '#8d6220',
      borderRadius: 3, barPercentage: 0.72
    }]},
    options: {
      responsive: true, maintainAspectRatio: false,
      plugins: { legend: { display: false },
        tooltip: { callbacks: { label: function (c) { return c.parsed.y + ' sections'; } } } },
      scales: {
        x: { grid: { display: false },
             ticks: { font: { family: 'JetBrains Mono', size: 10 }, color: '#6c6f66' } },
        y: { beginAtZero: true, grid: { color: '#e4e1d8' },
             ticks: { font: { family: 'JetBrains Mono', size: 10 }, color: '#6c6f66', stepSize: 10 } }
      }
    }
  });
});
</script>

<h2 class="sh">What the Sanhita does differently</h2>
<div class="grid grid--2">
  <div class="card"><div class="card__b">
    <span class="card__k">Numbering</span>
    <h3>Renumbered, not reorganised</h3>
    <p>The code runs to 358 sections against the IPC's 511. Much of the substance is carried across, but almost
    every section number moved — which is why old judgments and new FIRs no longer speak the same language.</p>
  </div></div>
  <div class="card"><div class="card__b">
    <span class="card__k">New offences</span>
    <h3>Organised crime and terrorism</h3>
    <p>Sections 111, 112 and 113 create standalone offences of organised crime, petty organised crime and terrorist
    acts — categories the IPC dealt with only indirectly, through conspiracy and unlawful assembly.</p>
  </div></div>
  <div class="card"><div class="card__b">
    <span class="card__k">Sentencing</span>
    <h3>Community service enters the code</h3>
    <p>Section 4 adds community service as a seventh punishment, available for six specified offences including
    small-value theft and defamation.</p>
  </div></div>
  <div class="card"><div class="card__b">
    <span class="card__k">Language</span>
    <h3>Sedition recast</h3>
    <p>Section 124-A of the IPC does not survive. Section 152 punishes acts endangering sovereignty, unity and
    integrity — exciting secession or armed rebellion, or encouraging such feelings.</p>
  </div></div>
</div>

<div class="callout">
  <div>
    <h4>Reading the section ranges</h4>
    <p>Chapter ranges in this platform follow the Act as notified, not the Bill as introduced. The Bill had 356
    clauses; two sections were added during passage, which shifts numbering in the later chapters.</p>
  </div>
</div>
""" % ("".join(
        '<tr><td class="mono" style="color:var(--brass-2)">%s</td><td><strong>%s</strong></td>'
        '<td class="mono num">%d&ndash;%d</td><td class="mono" style="color:var(--muted)">%d</td></tr>'
        % (r, E(t), f, l, l - f + 1) for n, r, t, f, l, b in D.CHAPTERS),
        json.dumps(["Ch %s" % r for n, r, t, f, l, b in D.CHAPTERS]),
        json.dumps([l - f + 1 for n, r, t, f, l, b in D.CHAPTERS]))


def bns_chapters():
    p = "bns/chapters.html"
    items = []
    for n, r, t, f, l, b in D.CHAPTERS:
        items.append("""
<div class="acc__item" x-data="{open:false}">
  <button class="acc__btn" @click="open=!open" :aria-expanded="open ? 'true' : 'false'">
    <span class="acc__n">Ch %s</span>
    <span class="acc__t">%s</span>
    <span class="acc__r">ss. %d&ndash;%d</span>
    <svg class="acc__c" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
         stroke-linecap="round" stroke-linejoin="round"><path d="M9 6l6 6-6 6"/></svg>
  </button>
  <div class="acc__p" x-show="open" x-cloak>
    <p style="margin:0 0 .5rem">%s</p>
    <a href="sections.html?ch=%d">See the sections in this chapter</a>
  </div>
</div>""" % (r, E(t), f, l, E(b), n))
    return phead(p, "The twenty chapters",
                 "The Sanhita is divided into twenty chapters, running from the definitions in Chapter I to the "
                 "repeal of the IPC in Chapter XX. Expand any chapter to see its range and what it covers.",
                 '<div class="pmeta"><span class="chip">358 sections</span>'
                 '<span class="chip chip--mono">ss. 1&ndash;358</span></div>',
                 [("../index.html", "Home"), ("index.html", "The Sanhita"), ("chapters.html", "Chapters")]) + \
        '<div class="acc" x-data>%s</div>' % "".join(items) + """
<div class="callout callout--warn" style="margin-top:1.6rem">
  <div>
    <h4>Chapter numbers are Roman, section numbers are not</h4>
    <p>Chapters are numbered I to XX in the Act. Sections run in a single continuous sequence from 1 to 358 — a
    section's chapter is determined by its number, not printed alongside it in the text.</p>
  </div>
</div>
"""


def bns_sections():
    p = "bns/sections.html"
    rows = "".join(
        '<tr data-ch="%d" data-s="%s"><td class="sec-n">%s</td><td><strong>%s</strong></td>'
        '<td><span class="chip chip--mono">Ch %s</span></td><td style="color:var(--muted)">%s</td></tr>'
        % (ch, E(("%s %s %s %s" % (s, t, ch, b)).lower()), E(s), E(t),
           next((r for n, r, _, _, _, _ in D.CHAPTERS if n == ch), ch), E(b))
        for s, t, ch, b in D.SECTIONS)

    opts = "".join('<option value="%d">Chapter %s &mdash; %s</option>' % (n, r, E(t))
                   for n, r, t, f, l, b in D.CHAPTERS)
    return phead(p, "Section index",
                 "A working index of the sections that carry the most weight in practice — the ones cited in "
                 "chargesheets, judgments and commentary. Filter by chapter or search by offence.",
                 '<div class="pmeta"><span class="chip">%d sections indexed</span>'
                 '<span class="chip">Out of 358</span></div>' % len(D.SECTIONS),
                 [("../index.html", "Home"), ("index.html", "The Sanhita"), ("sections.html", "Section index")]) + """
<div x-data="sectionTable()" x-init="init()">
  <div class="toolbar">
    <div class="field">
      %s
      <input type="search" placeholder="Search by section, offence or keyword" x-model="q" @input="q = $event.target.value; filter()">
    </div>
    <div class="field" style="flex:0 1 240px">
      <select x-model="ch" @change="ch = $event.target.value; filter()">
        <option value="">All chapters</option>%s
      </select>
    </div>
    <span class="count" x-text="shown + ' of %d'"></span>
  </div>
  <div class="tw"><div class="tw__scroll"><table>
    <thead><tr><th style="width:80px">Section</th><th style="width:270px">Title</th>
    <th style="width:110px">Chapter</th><th>What it covers</th></tr></thead>
    <tbody x-ref="body">%s</tbody>
  </table></div></div>
  <p style="font-size:.82rem;color:var(--muted);margin-top:.75rem;max-width:72ch">
    This is a curated index of %d sections, not the full text of all 358. It covers the provisions that account
    for most practical work; the chapter pages give the complete range.</p>
</div>
""" % (icon("search"), opts, len(D.SECTIONS), rows, len(D.SECTIONS))


def bns_mapping():
    p = "bns/mapping.html"
    rows = "".join(
        '<tr data-s="%s"><td class="mono" style="color:var(--muted)">%s</td><td>%s</td>'
        '<td class="sec-n">%s</td><td><strong>%s</strong></td><td style="color:var(--muted)">%s</td></tr>'
        % (E(("%s %s %s %s" % (a, at, b, bt)).lower()), E(a), E(at), E(b), E(bt), E(note))
        for a, at, b, bt, note in D.MAPPING)
    return phead(p, "IPC to BNS: the correspondence",
                 "Forty provisions of the Indian Penal Code and where they landed in the Sanhita. The mapping is "
                 "not one-to-one — several IPC sections were merged, split or reworded rather than carried across.",
                 '<div class="pmeta"><span class="chip">%d mappings</span>'
                 '<span class="chip">IPC 1860 &rarr; BNS 2023</span></div>' % len(D.MAPPING),
                 [("../index.html", "Home"), ("index.html", "The Sanhita"), ("mapping.html", "IPC to BNS")]) + """
<div x-data="rowFilter()">
  <div class="toolbar">
    <div class="field">%s
      <input type="search" placeholder="Search an IPC or BNS section, or an offence" x-model="q" @input="q = $event.target.value; filter()">
    </div>
    <span class="count" x-text="shown + ' of %d'"></span>
  </div>
  <div class="tw"><div class="tw__scroll"><table>
    <thead><tr><th style="width:90px">IPC</th><th style="width:230px">Offence</th>
    <th style="width:90px">BNS</th><th style="width:230px">Offence</th><th>Note</th></tr></thead>
    <tbody x-ref="body">%s</tbody>
  </table></div></div>
  <div class="callout callout--warn" style="margin-top:1.4rem">
    <div>
      <h4>Selected correspondences</h4>
      <p>This table covers the provisions most often looked up. It is not a complete concordance: the official
      comparative table published with the Act runs to every section. Where a provision was substantively rewritten,
      the note says so rather than implying equivalence.</p>
    </div>
  </div>
</div>
""" % (icon("search"), len(D.MAPPING), rows)


def bns_changes():
    p = "bns/changes.html"
    stats = "".join('<div class="stat"><span class="stat__n">%s</span><span class="stat__l">%s</span></div>'
                    % (n, l) for n, l, _ in D.CHANGE_STATS)
    new = "".join("""
<div class="card"><div class="card__b">
  <span class="card__k">Section %s</span>
  <h3>%s</h3>
  <p>%s</p>
</div></div>""" % (E(s), E(t), E(d)) for s, t, d in D.NEW_OFFENCES)
    dropped = "".join('<tr><td class="mono" style="color:var(--muted)">%s</td><td>%s</td></tr>'
                      % (E(a), E(b)) for a, b in D.DROPPED)
    return phead(p, "What changed on 1 July 2024",
                 "The Sanhita is not a rewrite of the IPC so much as a renumbering with a set of deliberate "
                 "changes layered on top. These are the ones that alter outcomes rather than drafting style.",
                 '<div class="pmeta"><span class="chip chip--brass">20 offences added</span>'
                 '<span class="chip">19 dropped</span><span class="chip">33 punishments raised</span></div>',
                 [("../index.html", "Home"), ("index.html", "The Sanhita"), ("changes.html", "What changed")]) + """
<div class="stats" style="margin-bottom:1.8rem">%s</div>

<h2 class="sh">Offences with no IPC equivalent</h2>
<p class="slead">Nine of the most consequential additions. Several respond to conduct the courts had been
struggling to fit into conspiracy, unlawful assembly or abetment.</p>
<div class="grid grid--3">%s</div>

<h2 class="sh">Provisions left behind</h2>
<div class="tw"><div class="tw__scroll"><table>
  <thead><tr><th style="width:150px">IPC</th><th>What happened</th></tr></thead>
  <tbody>%s</tbody>
</table></div></div>

<h2 class="sh">Penalties that moved</h2>
<p class="slead">Three changes matter most in practice.</p>
<div class="grid grid--3">
  <div class="card"><div class="card__b"><span class="card__k">Death by negligence</span>
    <h3>Section 106</h3><p>The base punishment rose from two years to five. A new sub-section (2) punishes a driver
    who causes death by rash driving and then flees without reporting — up to ten years and a fine.</p></div></div>
  <div class="card"><div class="card__b"><span class="card__k">Organised crime</span>
    <h3>Sections 111 and 112</h3><p>A crime syndicate's continuing unlawful activity is now an offence in itself,
    with death or life where it results in death, and a minimum of five years otherwise.</p></div></div>
  <div class="card"><div class="card__b"><span class="card__k">Community service</span>
    <h3>Section 4</h3><p>Added as a seventh punishment, available for six offences including small-value theft,
    defamation, misconduct in public by a drunken person and attempt to suicide.</p></div></div>
</div>
""" % (stats, new, dropped)


def bns_punishments():
    p = "bns/punishments.html"
    kinds = [
        ("Death", "Awarded for a defined set of offences — murder, gang rape in certain cases, terrorism, and "
                  "repeat offences. It is no longer mandatory in any case; the court must record reasons where it "
                  "chooses life instead."),
        ("Imprisonment for life", "The default alternative to death. Its meaning is fixed by the procedure code, "
                                  "and commutation is governed by Section 5."),
        ("Rigorous imprisonment", "Imprisonment with hard labour. Used where the section specifies 'rigorous'."),
        ("Simple imprisonment", "Imprisonment without hard labour, for the offences the code marks as simple."),
        ("Forfeiture of property", "Available only where the section expressly provides for it."),
        ("Fine", "Fixed or discretionary, with the considerations in Section 8 and imprisonment in default."),
        ("Community service", "New in 2023. Ordered for six specified offences, and conceived as an alternative to "
                              "short custodial sentences."),
    ]
    cards = "".join('<div class="card"><div class="card__b"><span class="card__k">%02d</span><h3>%s</h3>'
                    '<p>%s</p></div></div>' % (i + 1, k, d) for i, (k, d) in enumerate(kinds))
    return phead(p, "The punishment framework",
                 "Section 4 lists seven punishments. The Sanhita keeps the IPC's structure but adds community "
                 "service, and introduces statutory minimums for a set of offences that previously had none.",
                 '<div class="pmeta"><span class="chip">7 punishments</span>'
                 '<span class="chip">23 minimum sentences</span>'
                 '<span class="chip chip--ok">Community service added</span></div>',
                 [("../index.html", "Home"), ("index.html", "The Sanhita"),
                  ("punishments.html", "Punishments")]) + """
<h2 class="sh">The seven punishments — Section 4</h2>
<div class="grid grid--2">%s</div>

<h2 class="sh">How the sentence is computed</h2>
<div class="tw"><div class="tw__scroll"><table>
  <thead><tr><th style="width:100px">Section</th><th style="width:260px">Provision</th><th>Effect</th></tr></thead>
  <tbody>
    <tr><td class="sec-n">5</td><td><strong>Commutation</strong></td>
      <td>The appropriate Government may commute a death sentence, and may commute life imprisonment in the
      cases listed — for example where the offender is a woman or a person under eighteen.</td></tr>
    <tr><td class="sec-n">6</td><td><strong>Fractions of a term</strong></td>
      <td>Where the code refers to a portion of a maximum term, the portion is calculated on that maximum.</td></tr>
    <tr><td class="sec-n">8</td><td><strong>Fine and default</strong></td>
      <td>Fixing a fine turns on the offender's means and the injury caused; non-payment converts to imprisonment
      within statutory limits.</td></tr>
    <tr><td class="sec-n">9&ndash;10</td><td><strong>Several offences</strong></td>
      <td>The limit on punishment where an act constitutes several offences, and the rule where the judgment is
      doubtful as to which offence was committed.</td></tr>
    <tr><td class="sec-n">11&ndash;12</td><td><strong>Solitary confinement</strong></td>
      <td>Permitted only in the listed cases, and barred for women and for persons sentenced to simple
      imprisonment.</td></tr>
    <tr><td class="sec-n">13</td><td><strong>Repeat offenders</strong></td>
      <td>Enhanced punishment after a previous conviction in the specified cases.</td></tr>
  </tbody>
</table></div></div>

<h2 class="sh">Minimum sentences</h2>
<p class="slead">Twenty-three offences acquired a statutory floor. The ones most often encountered:</p>
<div class="tw"><div class="tw__scroll"><table>
  <thead><tr><th style="width:100px">Section</th><th style="width:240px">Offence</th><th>Minimum</th></tr></thead>
  <tbody>
    <tr><td class="sec-n">64</td><td>Rape</td><td>Ten years rigorous imprisonment, extendable to life</td></tr>
    <tr><td class="sec-n">65</td><td>Rape causing death or a persistent vegetative state</td><td>Twenty years, extendable to life</td></tr>
    <tr><td class="sec-n">66</td><td>Rape of a child under twelve</td><td>Twenty years, extendable to life, or death</td></tr>
    <tr><td class="sec-n">70</td><td>Gang rape</td><td>Twenty years, extendable to life</td></tr>
    <tr><td class="sec-n">103</td><td>Murder</td><td>Death or life, and a fine</td></tr>
    <tr><td class="sec-n">111</td><td>Organised crime</td><td>Five years; death or life where it causes death</td></tr>
    <tr><td class="sec-n">113</td><td>Terrorist act</td><td>Five years; death or life where it causes death</td></tr>
    <tr><td class="sec-n">124</td><td>Acid attack</td><td>Ten years, extendable to life</td></tr>
  </tbody>
</table></div></div>

<div class="callout">
  <div>
    <h4>Community service in practice</h4>
    <p>Section 4(f) makes community service a punishment, but the code does not define it. The procedure code and
    the rules made under it supply the mechanics — the court orders the work, and non-compliance is treated as a
    breach of the order.</p>
  </div>
</div>
""" % cards


def bnss():
    p = "procedure/bnss.html"
    rows = "".join(
        '<tr><td class="sec-n">%s</td><td><strong>%s</strong></td><td style="color:var(--muted)">%s</td></tr>'
        % (E(s), E(t), E(d)) for s, t, d in D.BNSS_POINTS)
    return phead(p, "Bharatiya Nagarik Suraksha Sanhita, 2023",
                 "The procedure code that replaced the CrPC on 1 July 2024. It governs arrest, investigation, bail "
                 "and trial — and it is where most of the practical change for a client actually sits.",
                 '<div class="pmeta"><span class="chip chip--ok">In force 1 July 2024</span>'
                 '<span class="chip chip--mono">Act No. 46 of 2023</span></div>',
                 [("../index.html", "Home"), ("bnss.html", "Procedure")]) + """
<div class="prose">
<p>The BNSS is the companion statute to the Sanhita: the Sanhita defines the offence, the BNSS supplies the
machinery. Its stated aim is time-bound investigation and trial, and much of the drafting is directed at delay
rather than at substantive rights.</p>
</div>

<h2 class="sh">The anchors that matter</h2>
<div class="tw"><div class="tw__scroll"><table>
  <thead><tr><th style="width:100px">Section</th><th style="width:270px">Provision</th><th>What it does</th></tr></thead>
  <tbody>%s</tbody>
</table></div></div>

<h2 class="sh">What changes for a client</h2>
<div class="grid grid--3">
  <div class="card"><div class="card__b"><span class="card__k">Filing</span><h3>Zero FIR and e-FIR</h3>
    <p>A first information report can be filed at any police station regardless of where the offence happened, and
    transmitted to the station with jurisdiction. Electronic filing is expressly permitted.</p></div></div>
  <div class="card"><div class="card__b"><span class="card__k">Arrest</span><h3>Notice instead of arrest</h3>
    <p>For offences punishable with less than seven years, the officer must ordinarily issue a notice of appearance
    rather than arrest — codifying the <em>Arnesh Kumar</em> guidelines.</p></div></div>
  <div class="card"><div class="card__b"><span class="card__k">Bail</span><h3>Half the sentence served</h3>
    <p>An undertrial who has served half the maximum sentence for a non-bailable offence is entitled to be released
    on bond, subject to the exceptions in the section.</p></div></div>
</div>

<div class="callout callout--warn">
  <div>
    <h4>Verify before relying</h4>
    <p>The BNSS has been amended and supplemented by rules and notifications since commencement, and several
    provisions are being implemented in phases. Check the current text on India Code.</p>
  </div>
</div>
""" % rows


def bsa():
    p = "procedure/bsa.html"
    rows = "".join(
        '<tr><td class="sec-n">%s</td><td><strong>%s</strong></td><td style="color:var(--muted)">%s</td></tr>'
        % (E(s), E(t), E(d)) for s, t, d in D.BSA_POINTS)
    return phead(p, "Bharatiya Sakshya Adhiniyam, 2023",
                 "The evidence code that replaced the Indian Evidence Act, 1872. Its most consequential change is "
                 "the treatment of electronic records as primary evidence.",
                 '<div class="pmeta"><span class="chip chip--ok">In force 1 July 2024</span>'
                 '<span class="chip chip--mono">Act No. 47 of 2023</span></div>',
                 [("../index.html", "Home"), ("bnss.html", "Procedure"), ("bsa.html", "Evidence")]) + """
<div class="prose">
<p>The BSA keeps the architecture of the 1872 Act — relevance, admissibility, proof, and the examination of
witnesses — and rewrites it for a document environment that is now largely digital. The provisions that litigators
actually argue about are the ones dealing with electronic records.</p>
</div>

<h2 class="sh">Electronic records</h2>
<div class="tw"><div class="tw__scroll"><table>
  <thead><tr><th style="width:100px">Section</th><th style="width:270px">Provision</th><th>What it does</th></tr></thead>
  <tbody>%s</tbody>
</table></div></div>

<h2 class="sh">Why it matters</h2>
<div class="grid grid--2">
  <div class="card"><div class="card__b"><span class="card__k">Before</span><h3>Section 65-B certificates</h3>
    <p>Under the 1872 Act an electronic record was secondary evidence, admissible only with a certificate
    identifying the device, the custodian and the process. Disputes over the certificate were a routine source of
    acquittals.</p></div></div>
  <div class="card"><div class="card__b"><span class="card__k">After</span><h3>Primary evidence</h3>
    <p>The BSA treats the electronic record itself as primary evidence, while retaining a certificate requirement
    where the record is produced by a device. The practical effect is to shift argument from admissibility to
    authenticity.</p></div></div>
</div>

<div class="callout">
  <div>
    <h4>Read the section, not the summary</h4>
    <p>The certificate requirement is the most litigated provision in the new code. The wording of Section 63 and
    the form of the certificate in the Schedule govern whether a record is admitted.</p>
  </div>
</div>
""" % rows


def research():
    p = "research/index.html"
    src = "".join(
        '<tr><td><strong><a href="%s" target="_blank" rel="noopener">%s</a></strong></td>'
        '<td style="color:var(--muted)">%s</td></tr>' % (u, E(t), E(d)) for t, d, u in D.SOURCES)
    return phead(p, "Methodology and sources",
                 "How this platform was compiled, what it covers, and where its limits are. Every section number "
                 "here traces to the Act as notified, not to secondary commentary.",
                 '<div class="pmeta"><span class="chip">Compiled October 2026</span>'
                 '<span class="chip">6 primary sources</span></div>',
                 [("../index.html", "Home"), ("index.html", "Research")]) + """
<h2 class="sh">What this is</h2>
<div class="prose">
<p>Sanhita Atlas indexes the Bharatiya Nyaya Sanhita, 2023 and its two companion codes. It is built for people who
need to find a provision quickly — a section number, the offence it creates, its punishment, and the IPC section it
corresponds to — and for people trying to understand what actually changed on 1 July 2024.</p>

<p>It is deliberately not a commentary. There is no case law digest and no editorial opinion on how a provision
should be read; the judgments that interpret the Sanhita are still being written.</p>
</div>

<h2 class="sh">Editorial rules</h2>
<div class="tw"><div class="tw__scroll"><table>
  <thead><tr><th style="width:220px">Rule</th><th>What it means in practice</th></tr></thead>
  <tbody>
    <tr><td><strong>Numbers come from the Act</strong></td>
      <td>Section and chapter ranges follow the Act as notified on 25 December 2023, not the Bill as introduced.
      Two sections were added during passage, which shifts numbering in the later chapters.</td></tr>
    <tr><td><strong>Mappings are selective</strong></td>
      <td>The IPC&ndash;BNS table covers the provisions most often looked up. Where a provision was substantively
      rewritten, the note says so rather than implying equivalence.</td></tr>
    <tr><td><strong>No inference of punishment</strong></td>
      <td>Where a punishment is not stated in a summary, it is because the section was not verified against the
      text — not because the offence is unpunished.</td></tr>
    <tr><td><strong>Currency</strong></td>
      <td>The platform reflects the position as at 29 October 2026. Amendments after that date are not
      reflected.</td></tr>
  </tbody>
</table></div></div>

<h2 class="sh">Sources</h2>
<div class="tw"><div class="tw__scroll"><table>
  <thead><tr><th style="width:320px">Source</th><th>Use</th></tr></thead>
  <tbody>%s</tbody>
</table></div></div>

<h2 class="sh">Known limits</h2>
<div class="callout callout--warn">
  <div>
    <h4>This is an index, not the statute</h4>
    <p>The section index covers %d of the 358 sections — the ones that carry most practical weight. The full text of
    every provision is available on India Code and in the Gazette notification. Nothing here is legal advice.</p>
  </div>
</div>
""" % (src, len(D.SECTIONS))


def about():
    p = "about.html"
    return phead(p, "About Sanhita Atlas",
                 "An independent research platform for the Bharatiya Nyaya Sanhita, 2023, built as an open static "
                 "site with no tracking and no login.",
                 '<div class="pmeta"><span class="chip">Open source</span>'
                 '<span class="chip chip--mono">MIT</span></div>',
                 [("index.html", "Home"), ("about.html", "About")]) + """
<h2 class="sh">Why it exists</h2>
<div class="prose">
<p>On 1 July 2024 India replaced three statutes that had governed its criminal justice system for over a century.
Every section number moved. Practitioners, students and journalists spent the following months converting
references in their heads — 302 to 103, 420 to 318, 124-A to 152.</p>
<p>This platform is a reference for that conversion, and for the structure of the new code. It is not affiliated
with the Government of India, any court, or any law firm.</p>
</div>

<h2 class="sh">What it is built with</h2>
<div class="grid grid--2">
  <div class="card"><div class="card__b"><span class="card__k">Stack</span><h3>Static, no server</h3>
    <p>Hand-written HTML and CSS, with Alpine.js for the interactive parts, Fuse.js for search, and Chart.js for
    the chapter distribution. No framework, no build runtime, no database.</p></div></div>
  <div class="card"><div class="card__b"><span class="card__k">Hosting</span><h3>GitHub Pages</h3>
    <p>The site is served directly from the repository. Every page is a plain HTML file, so it loads without
    JavaScript and prints cleanly.</p></div></div>
  <div class="card"><div class="card__b"><span class="card__k">Privacy</span><h3>No tracking</h3>
    <p>No analytics, no cookies, no third-party scripts beyond a font CDN and the libraries above. Search runs
    entirely in the browser against a static index.</p></div></div>
  <div class="card"><div class="card__b"><span class="card__k">Licence</span><h3>MIT</h3>
    <p>The code is MIT licensed. The statutory text it indexes is published by the Government of India and is not
    claimed by this project.</p></div></div>
</div>

<h2 class="sh">Corrections</h2>
<div class="prose">
<p>If a section number, punishment or mapping is wrong, the correction is welcome — open an issue on the
repository with the provision and the source. Corrections are reviewed against the Gazette text.</p>
</div>
"""


def not_found():
    return """<div style="padding:4rem 0;text-align:center;max-width:520px;margin:0 auto">
<p class="eyebrow" style="justify-content:center">Error 404</p>
<h1 style="margin-bottom:.6rem">That page is not in the code</h1>
<p style="color:var(--muted);margin-bottom:1.6rem">The link may be out of date, or the section may have moved when
the Sanhita was renumbered.</p>
<a class="btn btn--dark" href="index.html">Back to the overview</a>
</div>"""


# ── search index ─────────────────────────────────────────────────────────
def search_index():
    items = []
    for s, t, ch, b in D.SECTIONS:
        items.append({"url": "bns/sections.html", "title": "Section %s — %s" % (s, t),
                      "context": "Chapter %s · %s" % (ch, b[:70]), "text": "%s %s %s" % (s, t, b)})
    for a, at, b, bt, note in D.MAPPING:
        items.append({"url": "bns/mapping.html", "title": "IPC %s → BNS %s" % (a, b),
                      "context": "%s → %s" % (at, bt), "text": "%s %s %s %s %s" % (a, at, b, bt, note)})
    for n, r, t, f, l, bl in D.CHAPTERS:
        items.append({"url": "bns/chapters.html", "title": "Chapter %s — %s" % (r, t),
                      "context": "Sections %d to %d" % (f, l), "text": "%s %s %s" % (t, r, bl)})
    for s, t, d in D.NEW_OFFENCES:
        items.append({"url": "bns/changes.html", "title": "%s — Section %s" % (t, s),
                      "context": "New offence", "text": "%s %s %s" % (t, s, d)})
    for url, title, ctx in [
        ("bns/index.html", "Overview of the Sanhita", "The code, its commencement and structure"),
        ("bns/punishments.html", "The punishment framework", "Seven punishments and minimum sentences"),
        ("procedure/bnss.html", "BNSS — procedure", "FIR, arrest, bail and trial"),
        ("procedure/bsa.html", "Evidence Act — BSA", "Electronic records and proof"),
        ("research/index.html", "Methodology and sources", "How this platform was compiled"),
        ("about.html", "About Sanhita Atlas", "The project, stack and licence"),
    ]:
        items.append({"url": url, "title": title, "context": ctx, "text": title + " " + ctx})
    return items


# ── write ────────────────────────────────────────────────────────────────
PAGES = [
    ("index.html", "Sanhita Atlas — the Bharatiya Nyaya Sanhita, 2023, mapped",
     "A research platform for the BNS 2023: 358 sections, 20 chapters, the IPC correspondence and every offence "
     "that changed on 1 July 2024.", home, "", True),
    ("bns/index.html", "Overview — Sanhita Atlas",
     "The Bharatiya Nyaya Sanhita, 2023: structure, commencement and what it does differently.",
     bns_overview, "bns/index.html", False),
    ("bns/chapters.html", "The twenty chapters — Sanhita Atlas",
     "All 20 chapters of the BNS with their section ranges and subject matter.",
     bns_chapters, "bns/chapters.html", False),
    ("bns/sections.html", "Section index — Sanhita Atlas",
     "A searchable index of the BNS sections that matter in practice, filterable by chapter.",
     bns_sections, "bns/sections.html", False),
    ("bns/mapping.html", "IPC to BNS mapping — Sanhita Atlas",
     "Section-by-section correspondence between the Indian Penal Code, 1860 and the BNS, 2023.",
     bns_mapping, "bns/mapping.html", False),
    ("bns/changes.html", "What changed — Sanhita Atlas",
     "New offences, dropped provisions and the penalties that moved when the BNS replaced the IPC.",
     bns_changes, "bns/changes.html", False),
    ("bns/punishments.html", "Punishments — Sanhita Atlas",
     "The seven punishments under Section 4, the fine regime and the statutory minimum sentences.",
     bns_punishments, "bns/punishments.html", False),
    ("procedure/bnss.html", "BNSS — Sanhita Atlas",
     "The Bharatiya Nagarik Suraksha Sanhita, 2023: FIR, arrest, bail and trial timelines.",
     bnss, "procedure/bnss.html", False),
    ("procedure/bsa.html", "Evidence — Sanhita Atlas",
     "The Bharatiya Sakshya Adhiniyam, 2023 and the treatment of electronic records.",
     bsa, "procedure/bsa.html", False),
    ("research/index.html", "Methodology — Sanhita Atlas",
     "How Sanhita Atlas was compiled, its editorial rules and its sources.",
     research, "research/index.html", False),
    ("about.html", "About — Sanhita Atlas",
     "An independent, open research platform for the Bharatiya Nyaya Sanhita, 2023.",
     about, "about.html", False),
]


def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(os.path.join(OUT, "assets/css"), exist_ok=True)
    os.makedirs(os.path.join(OUT, "assets/js"), exist_ok=True)
    os.makedirs(os.path.join(OUT, "assets/img"), exist_ok=True)
    os.makedirs(os.path.join(OUT, "assets/data"), exist_ok=True)

    for path, title, desc, fn, active, wide in PAGES:
        full = os.path.join(OUT, path)
        os.makedirs(os.path.dirname(full) or OUT, exist_ok=True)
        with open(full, "w", encoding="utf-8") as f:
            f.write(layout(path, title, desc, fn(), active, wide))

    with open(os.path.join(OUT, "404.html"), "w", encoding="utf-8") as f:
        f.write(layout("404.html", "Page not found — Sanhita Atlas",
                       "That page is not in the code.", not_found(), "", True))

    with open(os.path.join(OUT, "assets/data/search.json"), "w", encoding="utf-8") as f:
        json.dump(search_index(), f, ensure_ascii=False, separators=(",", ":"))

    with open(os.path.join(OUT, ".nojekyll"), "w") as f:
        f.write("")

    here = os.path.dirname(os.path.abspath(__file__))
    shutil.copy(os.path.join(here, "src/app.js"), os.path.join(OUT, "assets/js/app.js"))
    shutil.copy(os.path.join(here, "src/favicon.svg"), os.path.join(OUT, "assets/img/favicon.svg"))
    if os.path.exists(os.path.join(here, "README.md")):
        shutil.copy(os.path.join(here, "README.md"), os.path.join(OUT, "README.md"))

    print("built", len(PAGES) + 1, "pages →", OUT)
    print("search entries:", len(search_index()))


if __name__ == "__main__":
    main()
