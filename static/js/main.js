/**
 * Chathurya Student Developers Club — Main JavaScript
 * Handles Navigation, Mobile Drawer, Theme Toggle, Smooth Section Redirects & Scroll Spy
 */

document.addEventListener('DOMContentLoaded', () => {
  // 1. Initialize Theme Switcher
  initThemeToggle();

  // 2. Initialize Mobile Navigation Drawer
  initMobileNav();

  // 3. Smooth Scroll for Internal Anchors & Section Redirects
  initSmoothScroll();

  // 4. Scroll Spy for Active Navigation Highlight on Single Page
  initScrollSpy();
});

/**
 * Handles Dark/Light Theme Switching with localStorage persistence
 */
function initThemeToggle() {
  const themeToggleButtons = document.querySelectorAll('.theme-toggle-btn');
  const htmlElement = document.documentElement;

  const savedTheme = localStorage.getItem('chathurya_website_theme') || 'dark';
  htmlElement.setAttribute('data-theme', savedTheme);
  updateThemeIcons(savedTheme);

  themeToggleButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      const currentTheme = htmlElement.getAttribute('data-theme');
      const newTheme = currentTheme === 'light' ? 'dark' : 'light';

      htmlElement.setAttribute('data-theme', newTheme);
      localStorage.setItem('chathurya_website_theme', newTheme);
      updateThemeIcons(newTheme);
    });
  });
}

function updateThemeIcons(theme) {
  const toggleButtons = document.querySelectorAll('.theme-toggle-btn');
  toggleButtons.forEach(btn => {
    btn.innerHTML = theme === 'light' ? '🌙' : '☀️';
    btn.setAttribute('title', theme === 'light' ? 'Switch to Dark Mode' : 'Switch to Light Mode');
  });
}

/**
 * Mobile Hamburger Navigation Drawer Toggle
 */
function initMobileNav() {
  const mobileToggle = document.querySelector('.mobile-toggle');
  const mobileDrawer = document.querySelector('.mobile-nav-drawer');

  if (!mobileToggle || !mobileDrawer) return;

  mobileToggle.addEventListener('click', () => {
    const isOpen = mobileDrawer.classList.contains('open');
    if (isOpen) {
      mobileDrawer.classList.remove('open');
      mobileToggle.innerHTML = '☰';
      mobileToggle.setAttribute('aria-expanded', 'false');
    } else {
      mobileDrawer.classList.add('open');
      mobileToggle.innerHTML = '✕';
      mobileToggle.setAttribute('aria-expanded', 'true');
    }
  });

  const mobileLinks = mobileDrawer.querySelectorAll('.nav-link, .btn');
  mobileLinks.forEach(link => {
    link.addEventListener('click', () => {
      mobileDrawer.classList.remove('open');
      mobileToggle.innerHTML = '☰';
      mobileToggle.setAttribute('aria-expanded', 'false');
    });
  });
}

/**
 * Smooth Scrolling for Section Redirects (e.g., #about, #courses, #fullstack, #data-analytics, #register)
 */
function initSmoothScroll() {
  document.querySelectorAll('a[href*="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      const href = this.getAttribute('href');
      if (!href) return;

      const hashIndex = href.indexOf('#');
      if (hashIndex === -1) return;

      const targetId = href.substring(hashIndex);
      if (targetId === '#' || targetId === '') return;

      // Check if target section exists on current page
      const targetElement = document.querySelector(targetId);
      if (targetElement) {
        // If on same page or index.html
        const isSamePage = window.location.pathname.endsWith('index.html') || window.location.pathname.endsWith('/') || !href.includes('.html');
        if (isSamePage) {
          e.preventDefault();
          const headerOffset = 85;
          const elementPosition = targetElement.getBoundingClientRect().top;
          const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

          window.scrollTo({
            top: offsetPosition,
            behavior: 'smooth'
          });

          // Update active link class manually
          const targetSection = targetId.replace('#', '');
          document.querySelectorAll('.nav-link, .mobile-nav-item').forEach(link => {
            const linkHref = link.getAttribute('href') || '';
            const linkNav = link.getAttribute('data-nav') || '';
            if (linkNav === targetSection || linkHref === href || linkHref === targetId || linkHref.endsWith(targetId)) {
              link.classList.add('active');
            } else {
              link.classList.remove('active');
            }
          });
        }
      }
    });
  });
}

/**
 * Scroll Spy to dynamically update nav active state as user scrolls
 */
function initScrollSpy() {
  const sections = document.querySelectorAll('section[id], main section[id]');
  const allNavItems = document.querySelectorAll('.nav-menu .nav-link, .mobile-floating-nav .mobile-nav-item');

  if (sections.length === 0 || allNavItems.length === 0) return;

  function updateActiveState() {
    const pathname = window.location.pathname;
    const isHomePage = pathname === '/' || pathname.endsWith('index.html') || pathname === '';
    if (!isHomePage) return;

    let currentSectionId = 'home';
    const hash = window.location.hash.replace('#', '');
    if (hash && ['about', 'events', 'courses'].includes(hash) && window.pageYOffset < 100) {
      currentSectionId = hash;
    } else {
      const scrollPosition = window.pageYOffset + 140;
      sections.forEach(section => {
        const sectionTop = section.offsetTop;
        const sectionHeight = section.offsetHeight;
        const sectionId = section.getAttribute('id');

        if (scrollPosition >= sectionTop && scrollPosition < sectionTop + sectionHeight) {
          if (['home', 'about', 'events', 'courses'].includes(sectionId)) {
            currentSectionId = sectionId;
          }
        }
      });
    }

    allNavItems.forEach(link => {
      link.classList.remove('active');
      const dataNav = link.getAttribute('data-nav');
      const href = link.getAttribute('href') || '';

      if (dataNav === currentSectionId) {
        link.classList.add('active');
      } else if (!dataNav && (href.endsWith('#' + currentSectionId) || (currentSectionId === 'home' && (href === '/' || href.endsWith('/'))))) {
        link.classList.add('active');
      }
    });
  }

  window.addEventListener('scroll', updateActiveState);
  window.addEventListener('load', updateActiveState);
  updateActiveState();
}
