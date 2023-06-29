const buttons = document.querySelectorAll('.button-size');
const containers = document.querySelectorAll('.options-container');

buttons.forEach((button) => {
    button.addEventListener('click', () => {
        const container = button.nextElementSibling;
        containers.forEach((c) => {
            if (c !== container) {
                c.style.display = 'none';
            }
        });
        container.style.display = container.style.display === 'none' ? 'block' : 'none';
    });
});