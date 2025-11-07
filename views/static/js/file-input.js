const input = document.getElementById("cover");
const label = document.getElementById("cover-label");

input.addEventListener("change", () => {
  if (input.files.length > 0) {
    label.textContent = input.files[0].name;
  } else {
    label.textContent = "Selecione uma capa para o livro...";
  }
});
