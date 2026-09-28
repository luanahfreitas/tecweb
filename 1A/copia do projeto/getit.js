// =============================================================================
// getit.js — JavaScript do Desafio CSS (🔹 só reconhecer, não precisa mexer)
// 1) Textareas com class="autoresize" aumentam de altura enquanto você digita
// 2) Sorteia uma cor (card-color-1..5) e uma rotação (card-rotation-1..11) para cada card
// Carregado no fim do index.html: o navegador faz GET /getit.js → is_file() no servidor
// ⚠ No simulado, a cor de fundo NÃO pode ser feita com JavaScript
// README_1A.md → Parte 1 — Estilo da página
// =============================================================================

function getRandomInt(min, max) {
  min = Math.ceil(min);
  max = Math.floor(max);
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

document.addEventListener("DOMContentLoaded", function () {
  // Faz textarea aumentar a altura automaticamente
  // Fonte: https://www.geeksforgeeks.org/how-to-create-auto-resize-textarea-using-javascript-jquery/#:~:text=It%20can%20be%20achieved%20by,height%20of%20an%20element%20automatically.
  let textareas = document.getElementsByClassName("autoresize");
  for (let i = 0; i < textareas.length; i++) {
    let textarea = textareas[i];
    function autoResize() {
      this.style.height = "auto";
      this.style.height = this.scrollHeight + "px";
    }

    textarea.addEventListener("input", autoResize, false);
  }

  // Sorteia classes de cores aleatoriamente para os cards
  let cards = document.getElementsByClassName("card");
  for (let i = 0; i < cards.length; i++) {
    let card = cards[i];
    card.className += ` card-color-${getRandomInt(
      1,
      5
    )} card-rotation-${getRandomInt(1, 11)}`;
  }
});
