function toggleSidebar() {
    document.getElementById("sidebar").classList.toggle("active");
}

// CONFIRMAR ELIMINACIÓN
function confirmDelete() {
    return confirm('¿Estás seguro de que deseas eliminar esto?');
}

// MODALES
function openModal(modalId) {
    document.getElementById(modalId).style.display = "block";
}

function closeModal(modalId) {
    document.getElementById(modalId).style.display = "none";
}

// CERRAR AL HACER CLICK FUERA
window.onclick = function(event) {
    let modals = document.getElementsByClassName("modal");
    for (let i = 0; i < modals.length; i++) {
        if (event.target == modals[i]) {
            modals[i].style.display = "none";
        }
    }
}