document.addEventListener("DOMContentLoaded", function () {
  console.log("JS loaded");

  /* =========================
   MOBILE NAVBAR (FIXED)
========================= */
  const menuToggle = document.getElementById("menuToggle");
  const navMenu = document.getElementById("navMenu");

  if (menuToggle && navMenu) {
    menuToggle.addEventListener("click", () => {
      const isOpen = navMenu.classList.toggle("active");
      menuToggle.setAttribute("aria-expanded", isOpen);
    });

    // Close menu when clicking a link
    navMenu.querySelectorAll("a").forEach((link) => {
      link.addEventListener("click", () => {
        navMenu.classList.remove("active");
        menuToggle.setAttribute("aria-expanded", "false");
      });
    });
  }
  /* =========================
   PASSWORD SHOW / HIDE
========================= */
  document.querySelectorAll(".toggle-password").forEach((toggle) => {
    toggle.addEventListener("click", () => {
      const inputId = toggle.getAttribute("data-target");
      const input = document.getElementById(inputId);

      if (!input) return;

      if (input.type === "password") {
        input.type = "text";
        toggle.textContent = "🙈";
      } else {
        input.type = "password";
        toggle.textContent = "👁️";
      }
    });
  });

  /* =========================
     REGISTER PAGE 
  ========================== */
  function getCookie(name) {
    let cookieValue = null;

    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");

      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();

        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }

    return cookieValue;
  }

  // VERIFY OTP & REGISTER
  const registerBtn = document.getElementById("registerBtn");

  if (registerBtn) {
    registerBtn.addEventListener("click", () => {
      const name = document.getElementById("name").value.trim();
      const email = document.getElementById("email").value.trim();
      const password = document.getElementById("password").value.trim();

      if (!name || !email || !password) {
        alert("Please fill all fields");
        return;
      }

      fetch("/api/register/", {
        method: "POST",
        headers: {
          "X-CSRFToken": getCookie("csrftoken"),
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: new URLSearchParams({
          name: name,
          email: email,
          password: password,
        }),
      })
        .then((res) => res.json())
        .then((res) => {
          if (res.status === "registered") {
            alert("Registration successful");
            window.location.href = "/";
          } else if (res.status === "user_exists") {
            alert("User already exists. Please login.");
            window.location.href = "/login/";
          } else {
            alert("Registration failed");
          }
        })
        .catch(() => {
          alert("Server error");
        });
    });
  }

  /* =========================
     LOGIN PAGE
  ========================== */
  const loginBtn = document.getElementById("loginBtn");

  if (loginBtn) {
    loginBtn.addEventListener("click", () => {
      const email = document.getElementById("loginEmail").value.trim();
      const password = document.getElementById("loginPassword").value.trim();

      fetch("/api/login/", {
        method: "POST",
        body: new URLSearchParams({
          email: email,
          password: password,
        }),
      })
        .then((res) => res.json())
        .then((res) => {
          console.log("LOGIN RESPONSE:", res);

          if (res.status === "logged_in") {
            window.location.href = "/";
          } else {
            alert("Login failed");
          }
        })
        .catch(() => alert("Server error"));
    });
  }

  /* =========================
   TIMELINE SCROLL ANIMATION
========================= */

  // TIMELINE ANIMATION
  const timelineItems = document.querySelectorAll(".timeline-item");
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach(
        (e) => e.isIntersecting && e.target.classList.add("visible"),
      );
    },
    { threshold: 0.3 },
  );
  timelineItems.forEach((item) => observer.observe(item));
});

/* =========================
   BLOG PANEL (GLOBAL)
========================= */
function openBlog(title, date, content) {
  document.getElementById("panelTitle").innerText = title;
  document.getElementById("panelDate").innerText = date;
  document.getElementById("panelContent").innerHTML = content;

  document.getElementById("blogOverlay").style.display = "flex";
  document.body.style.overflow = "hidden";
}

function closeBlog() {
  document.getElementById("blogOverlay").style.display = "none";
  document.body.style.overflow = "auto";
}
