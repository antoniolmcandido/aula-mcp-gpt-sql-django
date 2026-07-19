const chatMessages = document.getElementById("chatMessages");
const chatForm = document.getElementById("chatForm");
const messageInput = document.getElementById("messageInput");
const sendButton = document.getElementById("sendButton");
const suggestionChips = document.querySelectorAll(".suggestion-chip");

const backendChatUrl = window.BACKEND_CHAT_URL;

function scrollToBottom() {
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

function createMessage(role, text, isTyping = false) {
  const wrapper = document.createElement("article");
  wrapper.className = `message message--${role}`;

  const bubble = document.createElement("div");
  bubble.className = "message-bubble";

  const meta = document.createElement("div");
  meta.className = "message-meta";
  meta.textContent = role === "user" ? "Você" : "Assistente";

  bubble.appendChild(meta);

  if (isTyping) {
    const typing = document.createElement("div");
    typing.className = "typing-dots";
    typing.innerHTML = "<span></span><span></span><span></span>";
    bubble.appendChild(typing);
  } else {
    const content = document.createElement("div");
    content.textContent = text;
    bubble.appendChild(content);
  }

  wrapper.appendChild(bubble);
  chatMessages.appendChild(wrapper);
  scrollToBottom();
  return wrapper;
}

function setLoading(isLoading) {
  sendButton.disabled = isLoading;
  messageInput.disabled = isLoading;
  sendButton.textContent = isLoading ? "Processando..." : "Enviar comando";
}

function appendBotMessage(text) {
  createMessage("assistant", text || "Sem resposta do backend.");
}

async function sendMessage(text) {
  const typedMessage = text.trim();
  if (!typedMessage) {
    return;
  }

  createMessage("user", typedMessage);
  messageInput.value = "";

  const typingIndicator = createMessage("assistant", "", true);
  setLoading(true);

  try {
    const response = await fetch(backendChatUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message: typedMessage }),
    });

    const payload = await response.json();
    typingIndicator.remove();

    if (!response.ok) {
      appendBotMessage(payload.error || "Não foi possível processar sua solicitação.");
      return;
    }

    appendBotMessage(payload.reply);
  } catch (error) {
    typingIndicator.remove();
    appendBotMessage("Falha de comunicação com o backend.");
  } finally {
    setLoading(false);
    messageInput.focus();
  }
}

chatForm.addEventListener("submit", (event) => {
  event.preventDefault();
  sendMessage(messageInput.value);
});

messageInput.addEventListener("keydown", (event) => {
  if (event.key === "Enter" && !event.shiftKey) {
    event.preventDefault();
    chatForm.requestSubmit();
  }
});

suggestionChips.forEach((chip) => {
  chip.addEventListener("click", () => {
    messageInput.value = chip.dataset.message || "";
    messageInput.focus();
  });
});

createMessage(
  "assistant",
  "Olá. Posso cadastrar, atualizar, listar e remover alunos. Experimente um comando na caixa abaixo."
);
