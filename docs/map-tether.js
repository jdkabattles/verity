/* Verity — Directory Maps tether. Vanilla, zero-dependency, no tracking, no external fetches.
   Tab says "Directory Maps". Drawer X top-right closes. Escape + scrim click also close.
   HONESTY RULE: a 'built' entry must link to a URL that actually serves that site today.
   Staged / planned / not-yet-live targets are 'coming_soon', never 'built' with a dead link. */
(function () {
  "use strict";
  var DIRECTORY = [
    { group: "Hub", title: "Gold Is The Receipt", desc: "The hub. Not yet live as its own page. Coming Soon; no link until the hub has its own page.", url: "", status: "coming_soon" },
    { group: "Standard", title: "Algorithmic Gold", desc: "The six-gate verification standard. Done is a claim. GOLD is a receipt.", url: "https://jdkabattles.github.io/algorithmic-gold/", status: "built" },
    { group: "Learn", title: "Blog", desc: "Essays behind the standard.", url: "https://jdkabattles.github.io/algorithmic-gold/blog/index.html", status: "built" },
    { group: "Learn", title: "Pattern Atlas", desc: "49 cited patterns behind the gates.", url: "https://jdkabattles.github.io/algorithmic-gold/patterns/index.html", status: "built" },
    { group: "Products", title: "Products", desc: "Live products under the standard.", url: "https://jdkabattles.github.io/algorithmic-gold/products/index.html", status: "built" },
    { group: "Products", title: "Avcal-Agent", desc: "Sandboxed hidden-suite verification for agent-written code. Site exists as code in its repo; not yet live on this domain.", url: "", status: "coming_soon" },
    { group: "Products", title: "harwatch", desc: "Freeze an API from a HAR. Fail the build when a field disappears. Live at /harwatch/.", url: "https://www.forgingstack.com/harwatch/", status: "built" },
    { group: "Products", title: "mimicplus", desc: "Client-side HAR sanitizer that never uploads data. Live at forgingstack.com (its home).", url: "https://www.forgingstack.com/", status: "built" },
    { group: "Products", title: "Contract Gate", desc: "Contract Gate, its own website. Live at /gate/.", url: "https://www.forgingstack.com/gate/", status: "built" },
    { group: "Products", title: "Governed Agent Engine", desc: "Governed multi-agent engine. Not yet built as a site.", url: "", status: "coming_soon" },
    { group: "Products", title: "EvidenceForge", desc: "Auditable, evidence-citing AI agents. Not yet live on this domain.", url: "", status: "coming_soon" },
    { group: "Products", title: "Verity", desc: "Append-only evidence ledger for agent runs. This site.", url: "index.html", status: "built" }
  ];

  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    return n;
  }

  function buildDrawer() {
    var scrim = el("div", "gt-tether-scrim");
    scrim.setAttribute("data-tether-scrim", "");
    scrim.hidden = true;
    var drawer = el("aside", "gt-tether-drawer");
    drawer.setAttribute("aria-label", "Directory Maps");
    drawer.hidden = true;
    var head = el("div", "gt-tether-head");
    var h2 = el("h2", "gt-tether-title", "Directory Maps");
    var close = el("button", "gt-tether-close-x", "×");
    close.type = "button";
    close.setAttribute("aria-label", "Close Directory Maps");
    close.setAttribute("data-tether-close", "");
    head.appendChild(h2);
    head.appendChild(close);
    drawer.appendChild(head);
    var p = el("p", "gt-tether-intro", "Every site. Built entries link to their page. Unbuilt entries say Coming Soon.");
    drawer.appendChild(p);
    var label = el("label", "gt-tether-search-label", "Search pages");
    label.setAttribute("for", "gt-tether-search");
    var search = el("input", "gt-tether-search");
    search.id = "gt-tether-search";
    search.type = "search";
    search.placeholder = "Search pages, e.g. Atlas, Contract, Verity";
    search.autocomplete = "off";
    drawer.appendChild(label);
    drawer.appendChild(search);
    var groups = {};
    DIRECTORY.forEach(function (e) {
      (groups[e.group] = groups[e.group] || []).push(e);
    });
    var listWrap = el("div", "gt-tether-groups");
    Object.keys(groups).forEach(function (g) {
      var section = el("section", "gt-tether-group");
      section.appendChild(el("h3", "gt-tether-group-title", g));
      var ul = el("ul", "gt-tether-list");
      groups[g].forEach(function (e) {
        var li = el("li", "gt-tether-item");
        if (e.status === "coming_soon") {
          li.appendChild(el("strong", "gt-tether-coming-title", e.title));
          li.appendChild(el("span", "gt-tether-coming-soon", "Coming Soon"));
        } else {
          var a = el("a", "gt-tether-link", e.title);
          a.href = e.url;
          li.appendChild(a);
        }
        li.appendChild(el("span", "gt-tether-desc", e.desc));
        ul.appendChild(li);
      });
      section.appendChild(ul);
      listWrap.appendChild(section);
    });
    drawer.appendChild(listWrap);
    var empty = el("p", "gt-tether-empty", "No pages match that search.");
    empty.hidden = true;
    drawer.appendChild(empty);
    document.body.appendChild(scrim);
    document.body.appendChild(drawer);
    search.addEventListener("input", function () {
      var q = search.value.trim().toLowerCase();
      var any = false;
      listWrap.querySelectorAll(".gt-tether-item").forEach(function (li) {
        var show = !q || li.textContent.toLowerCase().indexOf(q) !== -1;
        li.hidden = !show;
        if (show) any = true;
      });
      empty.hidden = any;
    });
    return { scrim: scrim, drawer: drawer, close: close, search: search };
  }

  function init() {
    var mounts = document.querySelectorAll("[data-tether-mount]");
    var ui = buildDrawer();
    var opener = null;
    function open(op) {
      opener = op || null;
      ui.scrim.hidden = false;
      ui.drawer.hidden = false;
      ui.search.value = "";
      ui.search.dispatchEvent(new Event("input"));
      ui.close.focus();
      document.body.classList.add("gt-tether-open");
    }
    function close() {
      ui.scrim.hidden = true;
      ui.drawer.hidden = true;
      document.body.classList.remove("gt-tether-open");
      if (opener) opener.focus();
    }
    if (mounts.length === 0) {
      var tab = el("button", "gt-tether-fallback-tab", "Directory Maps");
      tab.type = "button";
      tab.setAttribute("aria-label", "Open Directory Maps");
      tab.addEventListener("click", function () { open(tab); });
      document.body.appendChild(tab);
    } else {
      mounts.forEach(function (m) {
        var btn = el("button", "gt-tether-tab", "Directory Maps");
        btn.type = "button";
        btn.setAttribute("aria-label", "Open Directory Maps");
        btn.setAttribute("data-open-map", "");
        btn.addEventListener("click", function () { open(btn); });
        m.appendChild(btn);
      });
    }
    ui.close.addEventListener("click", close);
    ui.scrim.addEventListener("click", close);
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && !ui.drawer.hidden) close();
    });
    document.querySelectorAll("[data-open-map]").forEach(function (b) {
      if (!b.closest("[data-tether-mount]")) b.addEventListener("click", function () { open(b); });
    });
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
