// ui/script.js
document.addEventListener("DOMContentLoaded", () => {
  const logoContainer = document.querySelector(".logo-container");
  const suggestion = document.querySelector(".suggestion");
  const chatContainer = document.querySelector(".chat-container");
  const userInput = document.getElementById("user-input");
  const sendBtn = document.getElementById("send-btn");

  // Animación de desaparición del logo
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

    // Simular respuesta de GRIND
    setTimeout(() => {
      let respuesta = "";

      if (text.toLowerCase().includes("cansado")) {
        respuesta = "No estás cansado. Estás cómodo. Y el crecimiento vive fuera de la comodidad.";
      } else if (text.toLowerCase().includes("motivación")) {
        respuesta = "No necesitas motivación. Necesitas acción. Tu mejor entrenamiento fue el que no querías hacer.";
      } else if (text.toLowerCase().includes("suicidarme") || text.toLowerCase().includes("morir")) {
        respuesta = "Escucho tu dolor. No estás solo. Tu vida importa.\n\nPor favor, visita https://findahelpline.com para encontrar ayuda real en tu idioma.";
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
}); // Animación del logo SVG
document.addEventListener("DOMContentLoaded", () => {
  const logo = document.getElementById("grind-logo");
  const circleOuter = logo.querySelector('circle[stroke="#10A37F"]');
  const circleInner = logo.querySelector('circle[stroke="#0c7a5c"]');

  // Animación de pulso en los anillos
  const animateCircles = () => {
    circleOuter.style.transition = "all 1.5s ease-in-out";
    circleInner.style.transition = "all 1.8s ease-in-out";

    circleOuter.style.strokeDasharray = "502, 502"; // Circunferencia = 2πr
    circleInner.style.strokeDasharray = "377, 377";

    setTimeout(() => {
      circleOuter.style.strokeDasharray = "0, 502";
      circleInner.style.strokeDasharray = "0, 377";
    }, 100);

    setTimeout(() => {
      circleOuter.style.strokeDasharray = "502, 502";
      circleInner.style.strokeDasharray = "377, 377";
    }, 1600);
  };

  // Repetir animación
  animateCircles();
  setInterval(animateCircles, 3000);
});