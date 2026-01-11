const BACKEND = "https://ai-secured-training-dashboard.onrender.com";

const params = new URLSearchParams(window.location.search);
const user = params.get("user");

if (!user) {
  alert("No user found in URL. Opening login page...");
  window.location.href = "login.html";
}

// --------------------
// CHART
// --------------------
const ctx = document.getElementById("marketChart");
if (ctx && window.Chart) {
  new Chart(ctx, {
    type: "line",
    data: {
      labels: ["Mon", "Tue", "Wed", "Thu", "Fri"],
      datasets: [{
        label: "NIFTY 50",
        data: [24100, 24250, 24310, 24480, 24510],
        borderWidth: 2,
        tension: 0.4
      }]
    },
    options: {
      plugins: { legend: { display: false } }
    }
  });
} else {
  console.warn("Chart.js not loaded OR marketChart missing");
}

// --------------------
// SESSION (to show banner)
// --------------------
fetch(`${BACKEND}/session?username=${encodeURIComponent(user)}`)
  .then(res => res.json())
  .then(data => {
    if (data.access === "PARTIAL") {
      document.getElementById("securityBanner").innerHTML = `
        <div class="alert">
          ⚠ New device detected. Portfolio access locked until verification.
        </div>
      `;
    }
  })
  .catch(() => console.log("Session fetch failed"));

// --------------------
// PORTFOLIO
// --------------------
fetch(`${BACKEND}/portfolio?username=${encodeURIComponent(user)}`)
  .then(res => res.json())
  .then(data => {
    const box = document.getElementById("portfolioContent");

    if (data.locked) {
      box.innerHTML = `
        <div class="blur">
          <p><b>Balance:</b> ₹4,25,000</p>
          <p><b>Holdings:</b> INFY, TCS, RELIANCE</p>
          <p><b>Last trade:</b> BUY INFY</p>
        </div>

        <div class="overlay">
          <p>New device / risky login detected</p>
          <button onclick="verify()">Verify to Unlock</button>
        </div>
      `;
    } else {
      box.innerHTML = `
        <p><b>Balance:</b> ₹4,25,000</p>
        <p><b>Holdings:</b> INFY, TCS, RELIANCE</p>
        <p><b>Last trade:</b> BUY INFY</p>
      `;
    }
  })
  .catch(() => {
    document.getElementById("portfolioContent").innerText =
      "Unable to load portfolio";
  });

function verify() {
  window.location.href = `verify.html?user=${encodeURIComponent(user)}`;
}

function logout() {
  window.location.href = "landing.html";
}
