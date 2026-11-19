document.addEventListener("DOMContentLoaded", () => {
    const overlay = document.getElementById("logout-modal-overlay");
    const cancelBtn = document.getElementById("logout-cancel-btn");
    const confirmBtn = document.getElementById("logout-confirm-btn");

    // Select ONLY navigation links that trigger logout, excluding the modal's own confirm button
    const logoutTriggers = document.querySelectorAll('a[href*="/logout/"]:not(#logout-confirm-btn)');

    if (overlay && confirmBtn && logoutTriggers.length) {
        logoutTriggers.forEach((link) => {
            link.addEventListener("click", (e) => {
                e.preventDefault();
                overlay.classList.add("active");
            });
        });

        if (cancelBtn) {
            cancelBtn.addEventListener("click", () => {
                overlay.classList.remove("active");
            });
        }

        // When user clicks 'Yes, Sign Out', navigate directly to /logout/
        confirmBtn.addEventListener("click", (e) => {
            e.stopPropagation();
            window.location.href = "/logout/";
        });

        // Close on backdrop click
        overlay.addEventListener("click", (e) => {
            if (e.target === overlay) {
                overlay.classList.remove("active");
            }
        });

        // Close on Escape key
        document.addEventListener("keydown", (e) => {
            if (e.key === "Escape" && overlay.classList.contains("active")) {
                overlay.classList.remove("active");
            }
        });
    }
});
