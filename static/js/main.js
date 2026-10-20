// Mobile menu toggle
document.addEventListener("DOMContentLoaded", () => {
  const mobileBtn = document.querySelector(".mobile-menu-btn");
  const navLinks = document.querySelector(".nav-links");

  if (mobileBtn && navLinks) {
    mobileBtn.addEventListener("click", () => {
      const isOpen = navLinks.classList.toggle("nav-links--open");
      mobileBtn.setAttribute("aria-expanded", String(isOpen));
      mobileBtn.setAttribute("aria-label", isOpen ? "মেনু বন্ধ করুন" : "মেনু খুলুন");
    });

    navLinks.addEventListener("click", (event) => {
      if (event.target.closest("a")) {
        navLinks.classList.remove("nav-links--open");
        mobileBtn.setAttribute("aria-expanded", "false");
        mobileBtn.setAttribute("aria-label", "মেনু খুলুন");
      }
    });

    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape" && navLinks.classList.contains("nav-links--open")) {
        navLinks.classList.remove("nav-links--open");
        mobileBtn.setAttribute("aria-expanded", "false");
        mobileBtn.setAttribute("aria-label", "মেনু খুলুন");
        mobileBtn.focus();
      }
    });
  }

  // Live search redirection if pressed Enter in navbar
  const searchInput = document.querySelector(".nav-search input");
  if (searchInput) {
    searchInput.addEventListener("keypress", (e) => {
      if (e.key === "Enter" && searchInput.value.trim()) {
        window.location.href = `/courses?q=${encodeURIComponent(searchInput.value.trim())}`;
      }
    });
  }
});
