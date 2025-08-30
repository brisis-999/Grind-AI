// script.js
document.addEventListener("DOMContentLoaded", () => {
  const logoContainer = document.getElementById("logo-container");
  const suggestion = document.getElementById("suggestion");
  const chatContainer = document.getElementById("chat-container");
  const userInput = document.getElementById("user-input");
  const sendBtn = document.getElementById("send-btn");

  // Animación del logo SVG (dibujo progresivo)
  const logoObject = document.getElementById("logo-object");
  logoObject.addEventListener("load", () => {
    const svg = logoObject.contentDocument;
    const circleOuter = svg.querySelector('circle[stroke="#10A37F"]');
    const circleInner = svg.querySelector('circle[stroke="#0c7a5c"]');
    const letterG = svg.querySelector('path[fill="white"]');

    const animate = () => {
      circleOuter.style.strokeDasharray = "502, 502";
      circleInner.style.strokeDasharray = "377, 377";
      letterG.style.opacity = "0";

      setTimeout(() => {
        circleOuter.style.strokeDasharray = "0, 502";
        circleInner.style.strokeDasharray = "0, 377";
      }, 100);

      setTimeout(() => {
        letterG.style.transition = "opacity 0.5s";
        letterG.style.opacity = "1";
      }, 800);
    };

    animate();
    setInterval(animate, 3000);
  });

  // Desaparecer logo después de 2 segundos
  setTimeout(() => {
    logoContainer.style.opacity = "0";
    setTimeout(() => {
      logoContainer.style.display = "none";
    }, 800);
  }, 2000);

  // Mostrar pregunta sugerida
  setTimeout(() => {
    if (suggestion) {
      suggestion.style.opacity = "1";
      suggestion.onclick = () => {
        addMessage("Estoy cansado.", "user");
        setTimeout(() => {
          addMessage("No estás cansado. Estás cómodo. Y el crecimiento vive fuera de la comodidad.", "assistant");
        }, 800);
        suggestion.style.display = "none";
      };
    }
  }, 2200);

  // Añadir mensaje con efecto typing
  function addMessage(text, role) {
    const messageDiv = document.createElement("div");
    messageDiv.className = `message ${role}`;
    chatContainer.appendChild(messageDiv);

    let i = 0;
    const timer = setInterval(() => {
      messageDiv.textContent = text.slice(0, i);
      i++;
      if (i > text.length) clearInterval(timer);
      chatContainer.scrollTop = chatContainer.scrollHeight;
    }, 30);
  }

  // Enviar mensaje
  function sendMessage() {
    const text = userInput.value.trim();
    if (!text) return;

    addMessage(text, "user");
    userInput.value = "";

    setTimeout(() => {
      let respuesta = "";

      if (text.toLowerCase().includes("cansado")) {
        respuesta = "No estás cansado. Estás cómodo. Y el crecimiento vive fuera de la comodidad.";
      } else if (text.toLowerCase().includes("motivación")) {
        respuesta = "No necesitas motivación. Necesitas acción. Tu mejor entrenamiento fue el que no querías hacer.";
      } else if (text.toLowerCase().includes("suicidarme") || text.toLowerCase().includes("morir")) {
        respuesta = "🌟 Escucho tu dolor. No estás solo. Tu vida importa.\n\nPor favor, visita https://findahelpline.com para encontrar ayuda real en tu idioma.";
      } else {
        respuesta = "¿Qué vamos a entrenar hoy? Recuerda: el grind no es sufrimiento. Es elección.";
      }

      addMessage(respuesta, "assistant");
    }, 800);
  }

  sendBtn.addEventListener("click", sendMessage);
  userInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") sendMessage();
  });

  // Nueva conversación
  document.querySelector(".new-chat").addEventListener("click", () => {
    chatContainer.innerHTML = "";
    suggestion.style.display = "block";
    suggestion.style.opacity = "1";
  });
});