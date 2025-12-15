// site_app/static/site_app/js/script.js
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        target.scrollIntoView({
          behavior: 'smooth'
        });
      }
    });
  });
});




// Alerts
setTimeout(() => {
const alerts = document.querySelectorAll('[role="alert"]');
alerts.forEach(alert => {
  alert.style.transition = "opacity 0.5s ease";
  alert.style.opacity = '0';
  setTimeout(() => alert.remove(), 500); // يحذف الإشعار بعد التلاشي
});
}, 4000);

// Loading
window.addEventListener("load", function() {
const loader = document.getElementById("preloader");
loader.style.opacity = "0";
setTimeout(() => loader.style.display = "none", 500);
});


