document.addEventListener("DOMContentLoaded", () => {
  let suggestions = [];
  fetch("/api/materias") ///ESTO ES EL AJAX, EL FETCH ES ASINCRONIC
    .then(response => response.json())
    .then(data => {
      suggestions = data;
    });

  const searchInput = document.getElementById("search");
  const suggestionsBox = document.getElementById("suggestions");

  searchInput.addEventListener("input", () => {
    const query = searchInput.value.toLowerCase();
    suggestionsBox.innerHTML = "";

    if (!query) {
      suggestionsBox.style.display = "none";
      return;
    }

    // Si suggestions es una lista de objetos con 'nombre'
    const filtered = suggestions.filter((item) =>
      (item.nombre || item).toLowerCase().includes(query)
    );

    if (filtered.length) {
      filtered.forEach((item) => {
        const nombre = item.nombre || item;
        const div = document.createElement("div");
        div.textContent = nombre;
        div.addEventListener("click", () => {
          searchInput.value = nombre;
          suggestionsBox.style.display = "none";
        });
        suggestionsBox.appendChild(div);
      });
      suggestionsBox.style.display = "flex";
    } else {
      suggestionsBox.style.display = "none";
    }
  });
  
  const searchBtn = document.getElementById("search-btn");
  if (searchBtn) {
    searchBtn.addEventListener("click", () => {
      const query = searchInput.value.trim().toLowerCase();
      if (!query) return;

      // Busca la materia seleccionada en suggestions
      const materia = suggestions.find(item =>
        (item.nombre || item).toLowerCase() === query
      );

      if (materia) {
        // Redirige usando el uuid o id según tu sistema
        window.location.href = `/buscador?materia=${materia.uuid || materia.id}`;
      } else {
        alert("Materia no encontrada.");
      }
    });
  }

});
