const sentences = [
  "Secure systems adapt to users.",
  "Behavior improves authentication.",
  "Typing patterns reveal identity."
];

let samples = [];
let current = [];
let index = 0;

const box = document.getElementById("box");
const sentenceDiv = document.getElementById("sentence");

sentenceDiv.innerText = sentences[index];

box.addEventListener("keydown", () => {
  current.push(Date.now());
});

function saveSample() {
  if (current.length < 5) {
    alert("Please type the full sentence.");
    return;
  }

  samples.push(current);
  current = [];
  box.value = "";

  index++;
  document.getElementById("count").innerText =
    `Samples: ${samples.length} / 3`;

  if (index < sentences.length) {
    sentenceDiv.innerText = sentences[index];
  } else {
    enroll();
  }
}

function enroll() {
  const params = new URLSearchParams(window.location.search);
  const user = params.get("user");

  fetch("http://127.0.0.1:8000/enroll-typing", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      username: user,
      typing_samples: samples
    })
  }).then(() => {
    alert("Typing enrollment completed.");
    window.location.href = "login.html";
  });
}
