const params = new URLSearchParams(window.location.search);
const user = params.get("user"); // ✅ FIXED
const ctx = document.getElementById("marketChart");

if (ctx && window.Chart) {
  new Chart(ctx, {
    type: "line",
    data: {
      labels: ["Mon", "Tue", "Wed", "Thu", "Fri"],
      datasets: [{
        label: "NIFTY 50",
        data: [24100, 24250, 24310, 24480, 24510],
        borderColor: "#2dd36f",
        backgroundColor: "transparent",
        borderWidth: 2,
        tension: 0.4,
        pointRadius: 4
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { display: false }
      },
      scales: {
        x: { grid: { display: false } },
        y: { grid: { color: "#222" } }
      }
    }
  });
}



if (!user) {
  alert("Session expired. Please login again.");
  window.location.href = "login.html";
}

// --------------------
// SESSION CHECK
// --------------------
fetch(`http://127.0.0.1:8000/session?username=${user}`)
  .then(res => res.json())
  .then(data => {
    if (data.access === "VERIFY") {
      document.getElementById("securityBanner").innerHTML = `
        <div class="alert">
          ⚠ New device detected. Portfolio locked until verification.
        </div>
      `;
    }
  });

// --------------------
// PORTFOLIO
// --------------------
fetch(`http://127.0.0.1:8000/portfolio?username=${user}`)
  .then(res => res.json())
  .then(data => {
    const box = document.getElementById("portfolioContent");

    if (data.locked) {
      box.innerHTML = `
        <div class="blur">
          <p>Balance: ₹4,25,000</p>
          <p>INFY · TCS · RELIANCE</p>
          <p>Last trade: BUY INFY</p>
        </div>

        <div class="overlay">
          <p>New device detected</p>
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
  });

function verify() {
  window.location.href = `verify.html?user=${user}`;
}

function logout() {
  window.location.href = "landing.html";
}
