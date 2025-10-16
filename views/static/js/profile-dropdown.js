// profile-dropdown.js
const profileMenu = document.getElementById('profileMenu');
const profileTrigger = document.getElementById('profileTrigger');
const dropdown = document.getElementById('profileDropdown');

// alterna o menu ao clicar no ícone
profileTrigger.addEventListener('click', (e) => {
    e.stopPropagation();
    profileMenu.classList.toggle('active');
});

// fecha ao clicar fora
document.addEventListener('click', (e) => {
    if (!profileMenu.contains(e.target)) {
        profileMenu.classList.remove('active');
    }
});
