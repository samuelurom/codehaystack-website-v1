// Get the menu button and menu
const menuButton = document.getElementById('mobile-menu-button');
const menu = document.getElementById('mobile-menu');

const userMenuButton = document.getElementById('user-menu-button')
const userMenu = document.getElementById('user-menu')

// Add event listener to menu button
menuButton.addEventListener('click', () => {
    // Toggle the menu visibility class
    menu.classList.toggle('hidden');
});

// Add event listener to user menu
userMenuButton.addEventListener('click', () => {
    // Toggle the visibility of userMenu
    userMenu.classList.toggle('hidden');
})