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
     REGISTER PAGE – OTP FLOW
  ========================== */
  const sendOtpBtn = document.getElementById("sendOtpBtn");
  const registerBtn = document.getElementById("registerBtn");
  const otpSection = document.getElementById("otpSection");

  // SEND OTP
  if (sendOtpBtn) {
    sendOtpBtn.addEventListener("click", () => {
      const email = document.getElementById("email")?.value.trim();

      if (!email) {
        alert("Please enter your email first");
        return;
      }

      const data = new FormData();
      data.append("email", email);

      fetch("/api/send-otp/", {
        method: "POST",
        body: data,
      })
        .then((res) => res.json())
        .then((res) => {
          console.log("OTP RESPONSE:", res);

          if (res.status === "otp_sent") {
            alert("OTP has been sent to your email");
            otpSection.style.display = "block";
          } else if (res.status === "already_registered") {
            alert("This email is already registered. Please login.");
            window.location.href = "/login/";
          } else {
            alert("Failed to send OTP. Please try again.");
          }
        })
        .catch(() => {
          alert("Server error while sending OTP");
        });
    });
  }

  // VERIFY OTP & REGISTER
  if (registerBtn) {
    registerBtn.addEventListener("click", () => {
      const name = document.getElementById("name")?.value.trim();
      const email = document.getElementById("email")?.value.trim();
      const otp = document.getElementById("otp")?.value.trim();

      if (!name || !email || !otp) {
        alert("Please fill all fields");
        return;
      }

      const data = new FormData();
      data.append("name", name);
      data.append("email", email);
      data.append("otp", otp);

      fetch("/api/verify-register/", {
        method: "POST",
        body: data,
      })
        .then((res) => res.json())
        .then((res) => {
          if (res.status === "verified") {
            alert("Registration successful. Please login.");
            window.location.href = "/login/";
          } else if (res.status === "wrong_otp") {
            alert("Incorrect OTP. Please try again.");
          } else {
            alert("Registration failed. Please retry.");
          }
        })
        .catch(() => {
          alert("Server error during registration");
        });
    });
  }

  /* =========================
     LOGIN PAGE
  ========================== */
  const loginBtn = document.getElementById("loginBtn");

  if (loginBtn) {
    loginBtn.addEventListener("click", () => {
      const name = document.getElementById("loginName")?.value.trim();
      const email = document.getElementById("loginEmail")?.value.trim();

      if (!name || !email) {
        alert("Please fill all fields");
        return;
      }

      const data = new FormData();
      data.append("name", name);
      data.append("email", email);

      fetch("/api/login-user/", {
        method: "POST",
        body: data,
      })
        .then((res) => res.json())
        .then((res) => {
          if (res.status === "logged_in") {
            alert("Login successful");
            window.location.href = "/";
          } else if (res.status === "temporarily_blocked") {
            alert(
              "Your account is temporarily blocked. Please try again later."
            );
          } else if (res.status === "not_registered") {
            alert("Email not registered or not verified");
          } else {
            alert("Login failed");
          }
        })

        .catch(() => {
          alert("Server error during login");
        });
    });
  }
  /* =========================
   TIMELINE SCROLL ANIMATION
========================= */

  // TIMELINE ANIMATION
  const timelineItems = document.querySelectorAll(".timeline-item");
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((e) => e.isIntersecting && e.target.classList.add("visible"));
    },
    { threshold: 0.3 }
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

