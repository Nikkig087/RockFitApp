/* jslint esversion: 6 */
document.addEventListener('DOMContentLoaded', function() {
    var modal = document.getElementById('contactModal');
    var openButton = document.getElementById('openModalButton');
    var closeButton = document.getElementById('closeModalButton');

    if (openButton) {
        openButton.addEventListener('click', function() {
            if (modal) {
                modal.style.display = 'block';
                modal.removeAttribute('inert');
            }
        });
    }

    if (closeButton) {
        closeButton.addEventListener('click', function() {
            if (modal) {
                modal.style.display = 'none';
                modal.setAttribute('inert', '');
            }
        });
    }
});