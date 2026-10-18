/* Verity — Directory Maps tether. Vanilla, zero-dependency, no tracking, no external fetches.
   Tab says "Directory Maps". Drawer X top-right closes. Escape + scrim click also close.
   HONESTY RULE: a 'built' entry must link to a URL that actually serves that site today.
   Staged / planned / not-yet-live targets are 'coming_soon', never 'built' with a dead link.
   'removed' entries show the page name + "Removed" underneath, NO live link, not clickable. */
(function () {
  "use strict";
  var DIRECTORY = [
    { group: "Hub", title: "Gold Is The Receipt", desc: "Removed.", url: null, status: "removed" },
    { group: "Standard", title: "Algorithmic Gold", desc: "Removed — claims unverified.", url: null, status: "removed" },
    { group: "Learn", title: "Blog", desc: "Removed — claims unverified.", url: null, status: "removed" },
    { group: "Learn", title: "Pattern Atlas", desc: "Removed — claims unverified.", url: null, status: "removed" },
    { group: "Products", title: "Products", desc: "Removed — claims unverified.", url: null, status: "removed" },
    { group: "Products", title: "Avcal-Agent", desc: "Sandboxed hidden-suite verification for agent-written code. Live at /avcal-agent/.", url: "https://www.forgingstack.com/avcal-agent/", status: "built" },
    { group: "Products", title: "harwatch", desc: "Freeze an API from a HAR. Fail the build when a field disappears. Live at /harwatch/.", url: "https://www.forgingstack.com/harwatch/", status: "built" },
    { group: "Products", title: "mimicplus", desc: "Client-side HAR sanitizer that never uploads data. Live at forgingstack.com (its home).", url: "https://www.forgingstack.com/", status: "built" },
    { group: "Products", title: "Contract Gate", desc: "Contract Gate, its own website. Live at /gate/.", url: "https://www.forgingstack.com/gate/", status: "built" },
    { group: "Products", title: "Governed Agent Engine", desc: "Governed multi-agent engine. Live at /governed-agent-engine/.", url: "https://www.forgingstack.com/governed-agent-engine/", status: "built" },
    { group: "Products", title: "EvidenceForge", desc: "Auditable, evidence-citing AI agents. Live at /evidenceforge/.", url: "https://www.forgingstack.com/evidenceforge/", status: "built" },
    { group: "Products", title: "Verity", desc: "Append-only evidence ledger for agent runs. This site.", url: "index.html", status: "built" },
    { group: "Products", title: "Products", desc: "Actual products only.", url: "https://www.forgingstack.com/products/", status: "built" }
  ];