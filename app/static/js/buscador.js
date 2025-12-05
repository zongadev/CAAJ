document.addEventListener('DOMContentLoaded', function() {
  const input = document.querySelector('.busqueda-input');
  const cards = document.querySelectorAll('.card');

  if (!input) return;

  input.addEventListener('input', function() {
    const q = input.value.trim().toLowerCase();
    cards.forEach(card => {
      const titulo = card.querySelector('.card-title')?.textContent.toLowerCase() || '';
      const autor = card.querySelector('.card-author')?.textContent.toLowerCase() || '';
      const tags = card.querySelector('.card-tags')?.textContent.toLowerCase() || '';
      if (titulo.includes(q) || autor.includes(q) || tags.includes(q)) {
        card.style.display = '';
      } else {
        card.style.display = 'none';
      }
    });
  });
});