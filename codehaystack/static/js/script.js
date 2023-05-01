// Get the menu button and menu
const menuButton = document.getElementById('mobile-menu-button');
const menu = document.getElementById('mobile-menu');

const userMenuButton = document.getElementById('user-menu-button')
const userMenu = document.getElementById('user-menu')

// Get close button for flash messages
const closeButton = document.getElementById('close-button')
const flashMessage = document.getElementById('flash-message')

if (menuButton) {
    // Add event listener to menu button if present
    menuButton.addEventListener('click', () => {
        // Toggle the menu visibility class
        menu.classList.toggle('hidden');
    });
}

if (userMenuButton) {
    // Add event listener to user menu if present
    userMenuButton.addEventListener('click', () => {
        // Toggle the visibility of userMenu
        userMenu.classList.toggle('hidden');
    })
}

if (closeButton) {
    // Add event listener to close-button if present
    closeButton.addEventListener('click', () => {
        flashMessage.classList.toggle('hidden');
    })
}