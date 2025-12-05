// Limpiar símbolos de Markdown del contenido
function cleanMarkdown(text) {
  if (!text) return "";

  // Eliminar enlaces pero mantener el texto [texto](url) -> texto
  text = text.replace(/\[([^\]]+)\]\([^\)]+\)/g, "$1");

  // Eliminar imágenes ![alt](url) -> ''
  text = text.replace(/!\[([^\]]*)\]\([^\)]+\)/g, "");

  // Eliminar símbolos de Markdown
  text = text
    .replace(/#/g, "")
    .replace(/\*/g, "")
    .replace(/`/g, "")
    .replace(/>/g, "")
    .replace(/_/g, "")
    .replace(/^- /gm, "");

  return text.trim();
}

// Procesar todas las descripciones de cards al cargar la página
document.addEventListener("DOMContentLoaded", function () {
  const descriptions = document.querySelectorAll(".card-description");

  descriptions.forEach((desc) => {
    const content = desc.getAttribute("data-content");
    if (content) {
      const cleaned = cleanMarkdown(content);
      const truncated =
        cleaned.length > 120 ? cleaned.substring(0, 120) + "..." : cleaned;
      desc.textContent = truncated;
    }
  });
});
