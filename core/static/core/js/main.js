/**
 * Bairava Groups Corporate Portal - Interactive JavaScript
 */

document.addEventListener('DOMContentLoaded', function() {
  // Mobile drawer controls
  const burgerBtn = document.getElementById('burgerBtn');
  const mobileDrawer = document.getElementById('mobileDrawer');
  const mobileBackdrop = document.getElementById('mobileBackdrop');
  const drawerCloseBtn = document.getElementById('drawerCloseBtn');

  function openDrawer() {
    if (mobileDrawer) mobileDrawer.classList.add('open');
    if (mobileBackdrop) mobileBackdrop.classList.add('open');
    document.body.style.overflow = 'hidden';
  }

  function closeDrawer() {
    if (mobileDrawer) mobileDrawer.classList.remove('open');
    if (mobileBackdrop) mobileBackdrop.classList.remove('open');
    document.body.style.overflow = '';
  }

  if (burgerBtn) {
    burgerBtn.addEventListener('click', openDrawer);
  }

  if (drawerCloseBtn) {
    drawerCloseBtn.addEventListener('click', closeDrawer);
  }

  if (mobileBackdrop) {
    mobileBackdrop.addEventListener('click', closeDrawer);
  }

  // Mobile drawer accordion items
  const accordionToggles = document.querySelectorAll('.mobile-accordion-toggle');
  accordionToggles.forEach(function(btn) {
    btn.addEventListener('click', function() {
      const targetId = this.getAttribute('data-target');
      const content = document.getElementById(targetId);
      if (content) {
        const isOpen = content.classList.toggle('open');
        const arrow = this.querySelector('.accordion-arrow');
        if (arrow) {
          arrow.style.transform = isOpen ? 'rotate(180deg)' : 'rotate(0deg)';
        }
      }
    });
  });

  // Close drawer on internal link click
  const drawerLinks = document.querySelectorAll('.mobile-drawer a:not(.mobile-accordion-toggle)');
  drawerLinks.forEach(function(link) {
    link.addEventListener('click', closeDrawer);
  });
});
