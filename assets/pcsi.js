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
