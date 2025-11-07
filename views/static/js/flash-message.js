const flashes = document.querySelectorAll(".flash");

flashes.forEach((flash) => {
  // Tempo antes de iniciar a animação de saída (ex: 3s)
  setTimeout(() => {
    flash.classList.add("hide");

    // Remove do DOM após a animação (0.4s = duração da animação)
    flash.addEventListener("animationend", () => {
      flash.remove();
    });
  }, 3000); // 3 segundos
});
