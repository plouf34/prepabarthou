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

// Section « Colles » : surligne la quinzaine en cours (data-debut/data-fin,
// dates incluses, week-end suivant compris) et ouvre son programme détaillé.
document.addEventListener("DOMContentLoaded", function () {
  var now = new Date();
  var today = now.getFullYear() + "-" + String(now.getMonth() + 1).padStart(2, "0") + "-" + String(now.getDate()).padStart(2, "0");
  document.querySelectorAll("#colles [data-debut]").forEach(function (el) {
    var fin = new Date(el.dataset.fin + "T12:00:00");
    fin.setDate(fin.getDate() + 2);
    var finWe = fin.toISOString().slice(0, 10);
    if (el.dataset.debut <= today && today <= finWe) {
      el.classList.add("is-now");
      if (el.tagName === "DETAILS") el.open = true;
    }
  });
});
