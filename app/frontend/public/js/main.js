// ---------------- MAIN.JS ----------------

// ----------- LOGIN PAGE -----------
document.addEventListener("DOMContentLoaded", () => {
  const loginForm = document.getElementById("loginForm");
  const goSignup = document.getElementById("goSignup");

  if (loginForm) {
    loginForm.addEventListener("submit", (e) => {
      e.preventDefault();
      const email = document.getElementById("email").value;
      const password = document.getElementById("password").value;

      if (email === "test@example.com" && password === "1234") {
        window.location.href = "Dashboard.html";
      } else {
        alert("Invalid credentials! Use test@example.com / 1234");
      }
    });
  }

  if (goSignup) {
    goSignup.addEventListener("click", (e) => {
      e.preventDefault();
      window.location.href = "Signup.html";
    });
  }
});

// ----------- SIGNUP PAGE -----------
if (document.getElementById("full-name") && document.getElementById("email-address")) {
  const signupBtn = document.querySelector("#signupBtn");
  const loginLinkSignup = document.querySelector("#loginLinkSignup");

  signupBtn.addEventListener("click", (e) => {
    e.preventDefault();

    const fullName = document.getElementById("full-name").value;
    const email = document.getElementById("email-address").value;
    const password = document.getElementById("password").value;
    const confirmPassword = document.getElementById("confirm-password").value;

    if (!fullName || !email || !password || !confirmPassword) {
      alert("Please fill all the fields!");
      return;
    }

    if (password !== confirmPassword) {
      alert("Passwords do not match!");
      return;
    }

    alert(`Account created for ${fullName}. Redirecting to Dashboard...`);
    window.location.href = "Dashboard.html";
  });

  loginLinkSignup.addEventListener("click", (e) => {
    e.preventDefault();
    window.location.href = "Login.html";
  });
}

// ----------- DASHBOARD PAGE -----------
const logoutBtn = document.getElementById("logoutBtn");
if (logoutBtn) {
  logoutBtn.addEventListener("click", () => {
    window.location.href = "Login.html";
  });
}

const uploadArea = document.getElementById("uploadArea");
const fileInput = document.getElementById("fileInput");
const fileListContainer = document.getElementById("fileList");

// Upload area click → file input click
if (uploadArea && fileInput) {
  uploadArea.addEventListener("click", () => {
    fileInput.click();
  });

  fileInput.addEventListener("change", uploadFile);
}

// Upload file to server
async function uploadFile() {
  if (!fileInput || !fileInput.files.length) return;
  const file = fileInput.files[0];
  const formData = new FormData();
  formData.append("file", file);

  try {
    const response = await fetch("http://localhost:5000/upload", {
      method: "POST",
      body: formData
    });
    const result = await response.json();
    alert(result.message || result.error);
    loadFiles();
  } catch (err) {
    console.error("Upload error:", err);
    alert("Failed to upload file.");
  }
}

// Fetch files and update table
async function loadFiles() {
  try {
    const res = await fetch("http://localhost:5000/files");
    const files = await res.json();
    fileListContainer.innerHTML = "";

    files.forEach((filename) => {
      const row = `
        <tr class="border-b border-[var(--border-color)] hover:bg-white/5 transition-colors">
          <td class="px-6 py-4 whitespace-nowrap">
            <a href="http://localhost:5000/uploads/${filename}" target="_blank" class="text-[var(--primary-color)]">${filename}</a>
          </td>
          <td class="px-6 py-4 whitespace-nowrap text-[var(--text-secondary)]">Me</td>
          <td class="px-6 py-4 whitespace-nowrap text-[var(--text-secondary)]">${new Date().toLocaleDateString()}</td>
          <td class="px-6 py-4 whitespace-nowrap text-[var(--text-secondary)]">-</td>
        </tr>
      `;
      fileListContainer.insertAdjacentHTML("beforeend", row);
    });
  } catch (err) {
    console.error("Error loading files:", err);
  }
}

// Initialize
document.addEventListener("DOMContentLoaded", () => {
  if (fileListContainer) {
    loadFiles();
  }
});
