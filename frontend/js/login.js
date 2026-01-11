const BACKEND = "https://ai-secured-training-dashboard.onrender.com";

// --------------------
// GENERATE OTP
// --------------------
async function generateOTP() {
  const username = document.getElementById("username").value;

  if (!username) {
    document.getElementById("otpStatus").innerText =
      "❌ Please enter username first";
    return;
  }

  try {
    const res = await fetch(`${BACKEND}/generate-otp`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username })
    });

    const data = await res.json();

    if (data.status === "blocked") {
      document.getElementById("otpStatus").innerText =
        "❌ Too many OTP requests. User blocked for 1 hour.";
      return;
    }

    document.getElementById("otpStatus").innerText =
      "✅ OTP generated. Please check admin panel.";

    document.getElementById("otpSection").style.display = "block";

  } catch (err) {
    document.getElementById("otpStatus").innerText =
      "❌ Backend not reachable";
  }
}


// --------------------
// LOGIN
// --------------------
async function login() {
  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;
  const otp = document.getElementById("otp").value;

  if (!username || !password || !otp) {
    document.getElementById("loginStatus").innerText = "❌ Fill all fields";
    return;
  }

  const payload = {
    username: username,
    password: password,
    otp: parseInt(otp),
    fingerprint: fingerprint(),
    location: getLocation(),
    hours: 24
  };

  try {
    const res = await fetch(`${BACKEND}/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    const data = await res.json();

    if (!res.ok) {
      document.getElementById("loginStatus").innerText =
        "❌ " + (data.detail || "Login failed");
      return;
    }

    if (data.access === "BLOCK") {
      document.getElementById("loginStatus").innerText =
        "❌ Login blocked due to suspicious activity";
      return;
    }

    document.getElementById("loginStatus").innerText = "✅ Login successful";

    setTimeout(() => {
      window.location.href = `dashboard.html?user=${username}`;
    }, 800);

  } catch (err) {
    document.getElementById("loginStatus").innerText =
      "❌ Backend not reachable";
  }
}
