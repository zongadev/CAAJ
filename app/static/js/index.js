document.addEventListener("DOMContentLoaded", () => {
  let suggestions = [];

  const searchInput = document.getElementById("search");
  const suggestionsBox = document.getElementById("suggestions");

  // Función para normalizar texto (quitar tildes)
  function normalizar(texto) {
    return texto
      .toLowerCase()
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "");
  }

  // Buscar en tiempo real mientras se escribe
  let timeoutId;
  searchInput.addEventListener("input", () => {
    const query = searchInput.value.trim();
    suggestionsBox.innerHTML = "";

    if (!query || query.length < 2) {
      suggestionsBox.style.display = "none";
      return;
    }

    // Debounce: esperar 300ms antes de buscar
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => {
      fetch(`/buscar?q=${encodeURIComponent(query)}`)
        .then((response) => response.json())
        .then((data) => {
          suggestions = data;

          if (suggestions.length > 0) {
            suggestions.forEach((item) => {
              const div = document.createElement("div");

              if (item.tipo === "materia") {
                div.innerHTML = `<strong>📚 ${item.titulo}</strong>`;
                div.dataset.tipo = "materia";
                div.dataset.id = item.materia_id;
              } else {
                div.innerHTML = `<strong>📄 ${item.titulo}</strong><br><small>${
                  item.contenido ? item.contenido + "..." : ""
                }</small>`;
                div.dataset.tipo = "apunte";
                div.dataset.id = item.id;
              }

              div.addEventListener("click", () => {
                if (item.tipo === "materia") {
                  window.location.href = `/buscador?materia=${item.materia_id}`;
                } else {
                  window.location.href = `/apunte?apunte=${item.id}`;
                }
              });
              suggestionsBox.appendChild(div);
            });
            suggestionsBox.style.display = "flex";
          } else {
            suggestionsBox.style.display = "none";
          }
        });
    }, 300);
  });

  const searchBtn = document.getElementById("search-btn");
  if (searchBtn) {
    searchBtn.addEventListener("click", () => {
      const query = searchInput.value.trim();
      if (!query || query.length < 2) return;

      // Si hay sugerencias, usar la primera
      if (suggestions.length > 0) {
        const item = suggestions[0];
        if (item.tipo === "materia") {
          window.location.href = `/buscador?materia=${item.materia_id}`;
        } else {
          window.location.href = `/apunte?apunte=${item.id}`;
        }
      } else {
        alert("No se encontraron resultados.");
      }
    });
  }

  // Permitir buscar con Enter
  searchInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") {
      searchBtn.click();
    }
  });
});
