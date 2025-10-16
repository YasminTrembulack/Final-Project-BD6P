const openBtn = document.getElementById('openModal');
const modal = document.getElementById('Modal');
const stars = document.querySelectorAll('.star-rating .star');
let rating = 0;

// Abrir modal
openBtn.addEventListener('click', () => {
  modal.style.display = 'flex';
});

// Fechar modal ao clicar fora
window.addEventListener('click', (e) => {
  if (e.target === modal) {
    modal.style.display = 'none';
  }
});

stars.forEach((star) => {
  star.addEventListener('click', () => {
    rating = star.dataset.value;
    stars.forEach(s => s.classList.toggle('filled', s.dataset.value <= rating));
  });
});
