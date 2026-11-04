// Wires links from js/links.js, then fills the blog and reviews from data/*.json.
// Everything has a working fallback in the HTML, so the page reads fine without it.
(function () {
  var L = window.BBG_LINKS || {};

  // 1. Links. data-link="key" takes its href from links.js.
  //    Missing link: data-missing="hide" hides it, otherwise it becomes "Coming soon".
  var gumroad = false;
  document.querySelectorAll("[data-link]").forEach(function (a) {
    var url = L[a.getAttribute("data-link")];
    if (url) {
      a.href = url;
      if (/^https?:\/\//.test(url) && !/gumroad\.com/.test(url)) a.rel = "noopener";
      if (/gumroad\.com/.test(url)) gumroad = true;
      return;
    }
    if (a.getAttribute("data-missing") === "hide") { a.hidden = true; return; }
    a.removeAttribute("href");
    a.setAttribute("aria-disabled", "true");
    a.classList.add("soon");
    var label = a.querySelector(".label") || a;
    label.textContent = "Coming soon";
  });
  // Gumroad's overlay opens checkout on this page instead of sending people away.
  if (gumroad) {
    var s = document.createElement("script");
    s.src = "https://gumroad.com/js/gumroad.js";
    s.async = true;
    document.body.appendChild(s);
  }

  function el(tag, cls, text) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text != null) e.textContent = text;
    return e;
  }
  function getJSON(url) {
    return fetch(url, { cache: "no-cache" }).then(function (r) {
      if (!r.ok) throw new Error(r.status);
      return r.json();
    });
  }

  // 2. Blog: newest posts from livebalancefit.com.
  var blog = document.getElementById("posts");
  if (blog) {
    getJSON("data/blog.json").then(function (d) {
      var posts = (d.posts || []).slice(0, 4);
      if (!posts.length) return;
      blog.textContent = "";
      posts.forEach(function (p) {
        var a = el("a", "post");
        a.href = p.link;
        if (p.image) {
          var img = el("img");
          img.src = p.image; img.alt = ""; img.loading = "lazy"; img.width = 640; img.height = 400;
          img.onerror = function () { img.remove(); };
          a.appendChild(img);
        }
        var body = el("span", "post-body");
        if (p.date) {
          var dt = new Date(p.date + "T12:00:00");
          body.appendChild(el("span", "post-date",
            dt.toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" })));
        }
        body.appendChild(el("span", "post-title", p.title));
        if (p.summary) body.appendChild(el("span", "post-sum", p.summary));
        a.appendChild(body);
        blog.appendChild(a);
      });
    }).catch(function () {});
  }

  // 3. Reviews from Google.
  var rev = document.getElementById("reviews");
  if (rev) {
    getJSON("data/reviews.json").then(function (d) {
      if (d.url && !L.google) {
        document.querySelectorAll('[data-link="google"]').forEach(function (a) {
          a.href = d.url; a.hidden = false; a.classList.remove("soon"); a.removeAttribute("aria-disabled");
        });
      }
      if (d.rating) {
        var sum = document.getElementById("rating");
        sum.querySelector("b").textContent = Number(d.rating).toFixed(1);
        sum.querySelector(".n").textContent = d.count ? d.count + " Google reviews" : "on Google";
        sum.hidden = false;
      }
      var list = d.reviews || [];
      if (!list.length) return;
      rev.textContent = "";
      list.forEach(function (r) {
        var f = el("figure", "rv");
        f.appendChild(el("span", "stars", "★★★★★".slice(0, Math.round(r.rating || 5))));
        f.lastChild.setAttribute("aria-label", (r.rating || 5) + " stars");
        f.appendChild(el("blockquote", null, r.text));
        var cap = el("figcaption");
        if (r.photo) {
          var img = el("img");
          img.src = r.photo; img.alt = ""; img.width = 32; img.height = 32; img.loading = "lazy";
          img.referrerPolicy = "no-referrer";
          img.onerror = function () { img.remove(); };
          cap.appendChild(img);
        }
        var who = el("span", null, r.author);
        if (r.when) who.appendChild(el("small", null, " · " + r.when + " on Google"));
        cap.appendChild(who);
        f.appendChild(cap);
        rev.appendChild(f);
      });
    }).catch(function () {});
  }
})();
