// Mobile navigation toggle
document.addEventListener('DOMContentLoaded', function() {
  const burger = document.getElementById('burgerBtn');
  const navMobile = document.getElementById('navMobile');

  burger.addEventListener('click', function() {
    const open = navMobile.classList.toggle('open');
    burger.setAttribute('aria-expanded', open);
  });

  navMobile.querySelectorAll('a').forEach(function(a) {
    a.addEventListener('click', function() {
      navMobile.classList.remove('open');
      burger.setAttribute('aria-expanded', false);
    });
  });
});
