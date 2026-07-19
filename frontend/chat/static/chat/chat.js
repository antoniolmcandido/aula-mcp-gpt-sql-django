const chatMessages = document.getElementById("chatMessages");
const chatForm = document.getElementById("chatForm");
const messageInput = document.getElementById("messageInput");
const sendButton = document.getElementById("sendButton");
const suggestionChips = document.querySelectorAll(".suggestion-chip");

// URL do endpoint de chat informada pelo template Django.
const backendChatUrl = window.BACKEND_CHAT_URL;

function scrollToBottom() {
  // Mantem a ultima mensagem visivel apos cada atualização.
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

function createMessage(role, text, isTyping = false) {
  // Cria a estrutura visual de uma mensagem para usuario ou assistente.
  const wrapper = document.createElement("article");
  wrapper.className = `message message--${role}`;

  const bubble = document.createElement("div");
  bubble.className = "message-bubble";

  const meta = document.createElement("div");
  meta.className = "message-meta";
  meta.textContent = role === "user" ? "Você" : "Assistente";

  bubble.appendChild(meta);

  if (isTyping) {
    // Exibe o indicador animado enquanto o backend processa a resposta.
    const typing = document.createElement("div");
    typing.className = "typing-dots";
    typing.innerHTML = "<span></span><span></span><span></span>";
    bubble.appendChild(typing);
  } else {
    // Insere o texto de forma segura sem interpretar HTML.
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
  // Bloqueia o formulario durante a requisicao para evitar envios duplicados.
  sendButton.disabled = isLoading;
  messageInput.disabled = isLoading;
  sendButton.textContent = isLoading ? "Processando..." : "Enviar comando";
}

function appendBotMessage(text) {
  // Adiciona uma resposta simples do assistente na conversa.
  createMessage("assistant", text || "Sem resposta do backend.");
}

async function sendMessage(text) {
  // Normaliza a mensagem antes do envio.
  const typedMessage = text.trim();
  if (!typedMessage) {
    return;
  }

  // Exibe a mensagem do usuario e limpa o campo de entrada.
  createMessage("user", typedMessage);
  messageInput.value = "";

  // Mostra o estado visual de processamento.
  const typingIndicator = createMessage("assistant", "", true);
  setLoading(true);

  try {
    // Envia o comando para o endpoint do backend usando JSON.
    const response = await fetch(backendChatUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message: typedMessage }),
    });

    // Lê a resposta do backend como objeto JavaScript.
    const payload = await response.json();
    typingIndicator.remove();

    if (!response.ok) {
      // Exibe mensagens de erro retornadas pela API.
      appendBotMessage(payload.error || "Não foi possível processar sua solicitação.");
      return;
    }

    // Mostra a resposta final gerada pelo backend.
    appendBotMessage(payload.reply);
  } catch (error) {
    // Trata falhas de rede ou indisponibilidade do backend.
    typingIndicator.remove();
    appendBotMessage("Falha de comunicação com o backend.");
  } finally {
    // Restaura o formulario para nova interação.
    setLoading(false);
    messageInput.focus();
  }
}

chatForm.addEventListener("submit", (event) => {
  // Intercepta o envio padrao do formulario e dispara o fluxo do chat.
  event.preventDefault();
  sendMessage(messageInput.value);
});

messageInput.addEventListener("keydown", (event) => {
  // Enter envia a mensagem e Shift mais Enter insere quebra de linha.
  if (event.key === "Enter" && !event.shiftKey) {
    event.preventDefault();
    chatForm.requestSubmit();
  }
});

suggestionChips.forEach((chip) => {
  // Preenche o campo com o texto da sugestao selecionada.
  chip.addEventListener("click", () => {
    messageInput.value = chip.dataset.message || "";
    messageInput.focus();
  });
});

// Mensagem inicial que orienta o usuario ao abrir a pagina.
createMessage(
  "assistant",
  "Olá. Posso cadastrar, atualizar, listar e remover alunos. Experimente um comando na caixa abaixo."
);
