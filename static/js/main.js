// Mobile menu toggle
document.addEventListener("DOMContentLoaded", () => {
  const mobileBtn = document.querySelector(".mobile-menu-btn");
  const navLinks = document.querySelector(".nav-links");

  if (mobileBtn && navLinks) {
    mobileBtn.addEventListener("click", () => {
      const isVisible = navLinks.style.display === "flex";
      navLinks.style.display = isVisible ? "none" : "flex";
      navLinks.style.flexDirection = "column";
      navLinks.style.position = "absolute";
      navLinks.style.top = "72px";
      navLinks.style.left = "0";
      navLinks.style.right = "0";
      navLinks.style.background = "#ffffff";
      navLinks.style.padding = "20px";
      navLinks.style.borderBottom = "1px solid #e2e8f0";
      navLinks.style.boxShadow = "0 10px 25px rgba(0,0,0,0.1)";
      navLinks.style.zIndex = "99";
    });
  }

  // Live search redirection if pressed Enter in navbar
  const searchInput = document.querySelector(".nav-search input");
  if (searchInput) {
    searchInput.addEventListener("keypress", (e) => {
      if (e.key === "Enter" && searchInput.value.trim()) {
        window.location.href = `/blog?q=${encodeURIComponent(searchInput.value.trim())}`;
      }
    });
  }
});
