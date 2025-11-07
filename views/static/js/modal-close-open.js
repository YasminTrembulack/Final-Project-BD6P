const openBtn = document.getElementById('openModal');
const modal = document.getElementById('Modal');

// Abrir modal
openBtn.addEventListener('click', () => {
  modal.style.display = 'flex';
});

// Fechar modal ao clicar fora
window.addEventListener('click', (e) => {
  if (e.target === modal) {
    modal.classList.remove('active');
    modal.style.display = 'none';

    //  Remove o parâmetro update_review_id da URL
    const url = new URL(window.location);
    url.search = ''; // limpa toda a parte de ?param=valor
    window.history.replaceState({}, '', url);
  }
});
