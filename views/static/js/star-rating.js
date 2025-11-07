document.addEventListener('DOMContentLoaded', () => {
  const stars = document.querySelectorAll('.star-rating .star');
  const ratingInput = document.getElementById('ratingValue');
  let rating = ratingInput.value;

  stars.forEach((star) => {
    star.addEventListener('click', () => {
      rating = star.dataset.value;
      ratingInput.value = rating;
      stars.forEach(s => s.classList.toggle('filled', s.dataset.value <= rating));
    });
  });
});
