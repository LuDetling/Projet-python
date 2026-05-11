document.body.addEventListener("notification", function(evt) {
    const { type, message } = evt.detail;
    const zone = document.getElementById("notifications");

    // Crée le toast
    const toast = document.createElement("div");
    toast.className = `alert ${type === "succes" ? "alert-success" : "alert-error"} shadow-lg`;
    toast.innerHTML = `<span>${message}</span>`;
    zone.appendChild(toast);

    // Supprime automatiquement après 3 secondes
    setTimeout(() => toast.remove(), 3000);
});