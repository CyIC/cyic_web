/*
 * Cypress Investment Club - the only script on the site.
 * Replaces jQuery, Bootstrap JS, wow.js, fittext and easing from the old theme.
 */
(function () {
  'use strict';

  /* --- Theme toggle -------------------------------------------------------
   * The initial class is applied by the inline script in _includes/head.html
   * before first paint; this only handles switching afterwards. A stored
   * choice wins over the OS setting, and clearing storage returns to "follow
   * the OS".
   */
  var STORAGE_KEY = 'cyic-theme';
  var root = document.documentElement;

  function storedTheme() {
    try {
      return localStorage.getItem(STORAGE_KEY);
    } catch (e) {
      return null;
    }
  }

  function applyTheme(isDark, persist) {
    root.classList.toggle('dark', isDark);
    if (persist) {
      try {
        localStorage.setItem(STORAGE_KEY, isDark ? 'dark' : 'light');
      } catch (e) {
        /* private mode - the choice just will not survive a reload */
      }
    }
  }

  document.querySelectorAll('[data-theme-toggle]').forEach(function (button) {
    button.addEventListener('click', function () {
      applyTheme(!root.classList.contains('dark'), true);
    });
  });

  // Follow the OS while the visitor has not made an explicit choice.
  var media = window.matchMedia('(prefers-color-scheme: dark)');
  if (media.addEventListener) {
    media.addEventListener('change', function (event) {
      if (!storedTheme()) applyTheme(event.matches, false);
    });
  }

  /* --- Mobile navigation -------------------------------------------------- */
  var menuButton = document.querySelector('[data-menu-toggle]');
  var menu = document.getElementById('mobile-menu');

  if (menuButton && menu) {
    var openIcon = menuButton.querySelector('[data-menu-open]');
    var closeIcon = menuButton.querySelector('[data-menu-close]');

    var setMenuOpen = function (isOpen) {
      menu.hidden = !isOpen;
      menuButton.setAttribute('aria-expanded', String(isOpen));
      menuButton.setAttribute('aria-label', isOpen ? 'Close navigation menu' : 'Open navigation menu');
      if (openIcon) openIcon.classList.toggle('hidden', isOpen);
      if (closeIcon) closeIcon.classList.toggle('hidden', !isOpen);
    };

    menuButton.addEventListener('click', function () {
      setMenuOpen(menu.hidden);
    });

    // Tapping a link should close the sheet behind it.
    menu.addEventListener('click', function (event) {
      if (event.target.closest('a')) setMenuOpen(false);
    });

    document.addEventListener('keydown', function (event) {
      if (event.key === 'Escape' && !menu.hidden) {
        setMenuOpen(false);
        menuButton.focus();
      }
    });

    // Leaving the mobile breakpoint should not strand the sheet open.
    var wide = window.matchMedia('(min-width: 768px)');
    if (wide.addEventListener) {
      wide.addEventListener('change', function (event) {
        if (event.matches) setMenuOpen(false);
      });
    }
  }

  /* --- FAQ section filter -------------------------------------------------
   * Progressive enhancement: without JS every question is simply visible.
   */
  var filterButtons = document.querySelectorAll('[data-faq-filter]');
  var faqSections = document.querySelectorAll('[data-faq-section]');

  if (filterButtons.length && faqSections.length) {
    filterButtons.forEach(function (button) {
      button.addEventListener('click', function () {
        var wanted = button.getAttribute('data-faq-filter');

        filterButtons.forEach(function (other) {
          var isActive = other === button;
          other.setAttribute('aria-pressed', String(isActive));
          other.classList.toggle('bg-accent', isActive);
          other.classList.toggle('text-accent-fg', isActive);
          other.classList.toggle('border-accent', isActive);
          other.classList.toggle('text-fg-muted', !isActive);
          other.classList.toggle('border-line', !isActive);
          // Without this the hover colour would win over the active fill and
          // drop the label to ~2:1 contrast while the pointer rests on it.
          other.classList.toggle('hover:text-accent-text', !isActive);
        });

        faqSections.forEach(function (section) {
          var match = wanted === 'all' || section.getAttribute('data-faq-section') === wanted;
          section.hidden = !match;
        });
      });
    });
  }
})();
