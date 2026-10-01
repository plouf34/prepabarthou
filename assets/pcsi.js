// Met en surbrillance l'onglet (Cours/Exercices/DS) correspondant à la
// section actuellement visible pendant le défilement de la page matière.
document.addEventListener("DOMContentLoaded", function () {
  var tabLinks = document.querySelectorAll("nav.tab-bar a");
  var sections = Array.prototype.slice
    .call(document.querySelectorAll("main > section"))
    .filter(function (s) { return s.id; });
  if (!tabLinks.length || !sections.length) return;

  function setActive(id) {
    tabLinks.forEach(function (a) {
      a.classList.toggle("active", a.getAttribute("href") === "#" + id);
    });
  }
  setActive(sections[0].id);

  var observer = new IntersectionObserver(
    function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) setActive(entry.target.id);
      });
    },
    { rootMargin: "-110px 0px -70% 0px", threshold: 0 }
  );
  sections.forEach(function (s) { observer.observe(s); });

  tabLinks.forEach(function (a) {
    a.addEventListener("click", function () {
      setActive(a.getAttribute("href").slice(1));
    });
  });
});

// Section « Colles » : 3 pavés (Colles passées / colle en cours / Colles à
// venir), reclassés ici à la date du jour (le HTML généré l'est à la date de
// génération). Une semaine reste « en cours » du début jusqu'au dimanche qui
// suit sa date de fin. Les pavés restent repliés ; la colle en cours est
// seulement surlignée.
document.addEventListener("DOMContentLoaded", function () {
  function iso(d) {
    return d.getFullYear() + "-" + String(d.getMonth() + 1).padStart(2, "0") + "-" + String(d.getDate()).padStart(2, "0");
  }
  var today = iso(new Date());
  document.querySelectorAll("#colles .colle-plan").forEach(function (plan) {
    var passees = plan.querySelector('[data-groupe="passees"]');
    var avenir = plan.querySelector('[data-groupe="avenir"]');
    var encours = plan.querySelector(".colle-encours");
    if (!passees || !avenir || !encours) return;
    var items = Array.prototype.slice.call(plan.querySelectorAll("[data-debut]"))
      .sort(function (a, b) { return a.dataset.debut < b.dataset.debut ? -1 : 1; });
    var g = { passees: [], encours: [], avenir: [] };
    items.forEach(function (el) {
      var fin = new Date(el.dataset.fin + "T12:00:00");
      fin.setDate(fin.getDate() + 2);
      var k = today > iso(fin) ? "passees" : (el.dataset.debut <= today ? "encours" : "avenir");
      el.classList.toggle("is-now", k === "encours");
      g[k].push(el);
    });
    [[passees, g.passees, true], [avenir, g.avenir, false]].forEach(function (x) {
      var box = x[0], list = x[1];
      var dest = box.querySelector(".colle-group-list");
      list.forEach(function (el) { dest.appendChild(el); });
      var ref = list.length ? list[x[2] ? list.length - 1 : 0] : null;
      box.querySelector(".colle-n").textContent = list.length;
      box.querySelector(".colle-gdate").textContent = ref ? ref.querySelector(".colle-dates").textContent : "";
      box.hidden = !list.length;
    });
    g.encours.forEach(function (el) { encours.appendChild(el); });
    encours.hidden = !g.encours.length;
  });
});
