fetch("https://YOUR_BACKEND.onrender.com/admin/logs")
  .then(res => res.json())
  .then(data => {
    document.getElementById("logs").innerHTML =
      data.map(l => `
        <tr>
          <td>${l.user}</td>
          <td>${l.time}</td>
          <td>${l.otp}</td>
          <td>${l.risk}</td>
          <td>${l.decision}</td>
        </tr>
      `).join("");
  });
