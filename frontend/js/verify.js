const params = new URLSearchParams(window.location.search);
const user = params.get("user");

if (!user) {
  alert("Invalid session");
  window.location.href = "login.html";
}

async function verifyDevice() {
  try {
    const res = await fetch("http://127.0.0.1:8000/verify-device", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        username: user,
        fingerprint: fingerprint()
      })
    });

    const data = await res.json();

    if (data.status === "verified") {
      document.getElementById("msg").innerText = "✅ Device verified";
      setTimeout(() => {
        window.location.href = `dashboard.html?user=${user}`;
      }, 800);
    } else {
      document.getElementById("msg").innerText = "❌ Verification failed";
    }

  } catch (e) {
    document.getElementById("msg").innerText = "❌ Server error";
  }
}
