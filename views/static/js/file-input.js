const fileInput = document.getElementById("cover");
const previewImg = document.getElementById("coverImagePreview");

if (fileInput) {
  fileInput.addEventListener("change", (event) => {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => (previewImg.src = e.target.result);
      reader.readAsDataURL(file);
    }
  });
}
