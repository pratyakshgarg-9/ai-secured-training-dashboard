async function register() {
  const msg = document.getElementById("msg");
  msg.innerText = "Registering...";

  try {
    const res = await fetch("https://ai-secured-training-dashboard.onrender.com/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        username: document.getElementById("user").value,
        password: document.getElementById("pass").value,
        fingerprint: fingerprint(),
        location: [28.6, 77.2]
      })
    });

    const data = await res.json();

    if (data.detail) {
      msg.innerText = "❌ " + data.detail;
      return;
    }

    msg.innerText = "✅ Registered successfully";
    setTimeout(() => {
      window.location.href =
        "typing.html?user=" + document.getElementById("user").value;
    }, 1000);

  } catch {
    msg.innerText = "❌ Server error";
  }
}
