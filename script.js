const form = document.getElementById("questionForm");
const input = document.getElementById("questionInput");
const askButton = document.getElementById("askButton");
const chatArea = document.getElementById("chatArea");
const sourcesPanel = document.getElementById("sourcesPanel");
const sourcesList = document.getElementById("sourcesList");
const emergencyArea = document.getElementById("emergencyArea");
const feedbackPanel = document.getElementById("feedbackPanel");
const feedbackMessage = document.getElementById("feedbackMessage");
const statusMessage = document.getElementById("statusMessage");
let lastAnswerAvailable = false;

function addMessage(text, role) {
  const article = document.createElement("article");
  article.className = `message ${role}`;
  const bubble = document.createElement("div");
  bubble.className = "bubble";
  bubble.textContent = text;
  article.appendChild(bubble);
  chatArea.appendChild(article);
  chatArea.scrollTop = chatArea.scrollHeight;
}
function renderSources(sources) {
  sourcesList.replaceChildren();
  if (!sources || sources.length === 0) {
    sourcesPanel.classList.add("hidden");
    return;
  }
  sources.forEach((source, index) => {
    const item = document.createElement("div");
    item.className = "source-item";
    const heading = document.createElement("strong");
    heading.textContent = `${index + 1}. ${source.topic} — ${source.question}`;
    const answer = document.createElement("p");
    answer.textContent = source.answer;
    const meta = document.createElement("div");
    meta.className = "source-meta";
    const score = document.createElement("span");
    score.textContent = `Cosine similarity: ${(source.score * 100).toFixed(1)}%`;
    const link = document.createElement("a");
    link.href = source.source_url;
    link.target = "_blank";
    link.rel = "noopener noreferrer";
    link.textContent = "Open source ↗";
    meta.append(score, link);
    item.append(heading, answer, meta);
    sourcesList.appendChild(item);
  });
  sourcesPanel.classList.remove("hidden");
}
form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const question = input.value.trim();
  if (!question) {
    statusMessage.textContent = "Please enter a question.";
    return;
  }
  addMessage(question, "user");
  input.value = "";
  askButton.disabled = true;
  askButton.textContent = "Thinking…";
  statusMessage.textContent = "Retrieving educational information…";
  emergencyArea.classList.add("hidden");
  sourcesPanel.classList.add("hidden");
  feedbackPanel.classList.add("hidden");
  lastAnswerAvailable = false;
  try {
    const response = await fetch("/api/ask", {
      method: "POST", headers: {"Content-Type": "application/json"},
      body: JSON.stringify({question})
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "Unable to process the question.");
    addMessage(data.answer, "assistant");
    renderSources(data.sources);
    if (data.emergency) {
      emergencyArea.textContent = data.answer;
      emergencyArea.classList.remove("hidden");
    }
    if (data.mode === "retrieval_fallback") {
      statusMessage.textContent = "Ollama is unavailable. Showing a safe knowledge-base response.";
    } else if (data.mode === "knowledge_base_no_match") {
      statusMessage.textContent = "No sufficiently relevant knowledge-base match was found.";
    } else if (data.mode === "emergency") {
      statusMessage.textContent = "Emergency guidance returned without calling the LLM.";
    } else {
      statusMessage.textContent = "Response mode: Ollama + RAG.";
    }
    if (!data.emergency) {
      lastAnswerAvailable = true;
      feedbackPanel.classList.remove("hidden");
    }
  } catch (error) {
    addMessage(error.message || "A network error occurred. Please try again.", "assistant");
    statusMessage.textContent = "Request failed.";
  } finally {
    askButton.disabled = false;
    askButton.innerHTML = 'Ask <span>➤</span>';
  }
});
document.querySelectorAll(".suggestion").forEach(button => {
  button.addEventListener("click", () => {
    input.value = button.textContent;
    input.focus();
  });
});
feedbackPanel.querySelectorAll("button[data-helpful]").forEach(button => {
  button.addEventListener("click", async () => {
    if (!lastAnswerAvailable) return;
    try {
      const response = await fetch("/api/feedback", {
        method: "POST", headers: {"Content-Type": "application/json"},
        body: JSON.stringify({helpful: button.dataset.helpful === "true"})
      });
      const data = await response.json();
      feedbackMessage.textContent = response.ok ? data.message : (data.error || "Feedback could not be sent.");
    } catch {
      feedbackMessage.textContent = "Feedback could not be sent. Please try again.";
    }
  });
});
