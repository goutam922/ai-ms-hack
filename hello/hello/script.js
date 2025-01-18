// API Configuration
const API_BASE_URL = "http://localhost:5000/api";

const messagesContainer = document.getElementById("messages");
const emojiBox = document.getElementById("emojiBox");
const userInput = document.getElementById("userInput");

// Helper function to append messages to the chat
function appendMessage(sender, text, isHTML = false) {
  const messageDiv = document.createElement("div");
  messageDiv.classList.add("message", sender);

  if (isHTML) {
    messageDiv.innerHTML = `<span>${text}</span>`;
  } else {
    const span = document.createElement("span");
    span.textContent = text;
    messageDiv.appendChild(span);
  }

  messagesContainer.appendChild(messageDiv);
  messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

// Format counselors data into readable text
function formatCounselors(counselors) {
  return counselors
    .map(
      (c) => `
    <strong>${c.name}</strong><br>
    Services: ${c.services.join(", ")}<br>
    Location: ${c.location}<br>
    Contact: ${c.contact}<br>
  `
    )
    .join("<br>");
}

// Format resources data into readable text
function formatResources(resources) {
  return resources
    .map(
      (r) => `
    <strong>${r.name}</strong><br>
    Services: ${r.services.join(", ")}<br>
    Contact: ${r.contact}<br>
    Website: <a href="${r.website}" target="_blank">${r.website}</a><br>
    Hours: ${r.hours || r.available}<br>
  `
    )
    .join("<br>");
}

// Format CBT exercises data into readable text
function formatExercises(exercises) {
  return exercises
    .map(
      (e) => `
    <strong>${e.name}</strong><br>
    ${e.description}<br>
    Duration: ${e.recommended_duration}<br>
  `
    )
    .join("<br>");
}

// API Calls
async function sendMessage() {
  const userText = userInput.value.trim();
  if (userText === "") return;

  appendMessage("user", userText);
  userInput.value = "";

  try {
    const response = await axios.post(`${API_BASE_URL}/chat`, {
      message: userText,
    });

    if (response.data.status === "success") {
      appendMessage("bot", response.data.response);
    } else {
      appendMessage(
        "bot",
        "I apologize, but I'm having trouble processing your request."
      );
    }
  } catch (error) {
    console.error("Error:", error);
    appendMessage(
      "bot",
      "I'm sorry, but I'm having technical difficulties. Please try again later."
    );
  }
}

async function fetchNews() {
  try {
    appendMessage("user", "Show me the latest medical news");

    const response = await axios.get(`${API_BASE_URL}/news`);

    if (response.data.status === "success") {
      const newsText = response.data.headlines.join("\n\n");
      appendMessage(
        "bot",
        "Here are the latest medical headlines:\n\n" + newsText
      );
    }
  } catch (error) {
    console.error("Error:", error);
    appendMessage(
      "bot",
      "Sorry, I couldn't fetch the latest news at the moment."
    );
  }
}

async function fetchCounselors() {
  try {
    appendMessage("user", "Show me available counselors");

    const response = await axios.get(`${API_BASE_URL}/counselors`);

    if (response.data.status === "success") {
      const counselorsText = formatCounselors(response.data.counselors);
      appendMessage(
        "bot",
        "Here are some available counselors:<br><br>" + counselorsText,
        true
      );
    }
  } catch (error) {
    console.error("Error:", error);
    appendMessage(
      "bot",
      "Sorry, I couldn't fetch the counselors list at the moment."
    );
  }
}

async function fetchResources() {
  try {
    appendMessage("user", "Show me mental health resources");

    const response = await axios.get(`${API_BASE_URL}/resources`);

    if (response.data.status === "success") {
      const resourcesText = formatResources(response.data.resources);
      appendMessage(
        "bot",
        "Here are some helpful mental health resources:<br><br>" +
          resourcesText,
        true
      );
    }
  } catch (error) {
    console.error("Error:", error);
    appendMessage(
      "bot",
      "Sorry, I couldn't fetch the resources at the moment."
    );
  }
}

async function fetchCBTExercises() {
  try {
    appendMessage("user", "Show me CBT exercises");

    const response = await axios.get(`${API_BASE_URL}/cbt-exercises`);

    if (response.data.status === "success") {
      const exercisesText = formatExercises(response.data.exercises);
      appendMessage(
        "bot",
        "Here are some CBT exercises you can try:<br><br>" + exercisesText,
        true
      );
    }
  } catch (error) {
    console.error("Error:", error);
    appendMessage(
      "bot",
      "Sorry, I couldn't fetch the CBT exercises at the moment."
    );
  }
}

async function assessEmotionalState(message) {
  try {
    const response = await axios.post(`${API_BASE_URL}/emotional-assessment`, {
      message: message,
    });

    if (response.data.status === "success") {
      const assessment = response.data.response;
      let responseText = assessment.message + "\n\n";

      if (assessment.techniques) {
        responseText +=
          "Suggested techniques:\n" + assessment.techniques.join("\n") + "\n\n";
      }

      if (assessment.resources) {
        responseText +=
          "Helpful resources:\n" +
          assessment.resources
            .map((r) => (typeof r === "string" ? r : `${r.name}: ${r.url}`))
            .join("\n");
      }

      appendMessage("bot", responseText);
    }
  } catch (error) {
    console.error("Error:", error);
    appendMessage(
      "bot",
      "I'm having trouble analyzing your message. Could you try rephrasing it?"
    );
  }
}

function handleKeyPress(event) {
  if (event.key === "Enter") {
    sendMessage();
  }
}


