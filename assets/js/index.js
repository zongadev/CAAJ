document.addEventListener("DOMContentLoaded", () => { //DOM, Document Object model. es decir, cuando ya cargo el html.
  const suggestions = [ //claramente esta lista no va a ser estatica
    "Calculo Elementeal",
    "Calculo Avanzado",
    "Algebra y Geometria",
    "Programacion Web y Movil",
    "Informatica General",
    "Fisica I",
  ];
  const searchInput = document.getElementById("search"); //en la barra
  const suggestionsBox = document.getElementById("suggestions");

  searchInput.addEventListener("input", () => {
    const query = searchInput.value.toLowerCase();
    suggestionsBox.innerHTML = "";

    if (!query) {
      suggestionsBox.style.display = "none";
      return;
    }

    const filtered = suggestions.filter((item) =>
      item.toLowerCase().includes(query)
    );

    if (filtered.length){
      filtered.forEach((item) => {
        const div = document.createElement("div");
        div.textContent = item;
        div.addEventListener("click", () => {
          searchInput.value = item;
          suggestionsBox.style.display = "none"; //mover a clases
        });
        suggestionsBox.appendChild(div);
      });
      suggestionsBox.style.display = "flex";
    } else {
      suggestionsBox.style.display = "none";
    }
  });
});
