const storedTitle = sessionStorage.getItem('headerTitle');
if (storedTitle) {
    document.addEventListener("DOMContentLoaded", () => {
        const headerText = document.getElementById('nav-title');
        headerText.innerHTML = storedTitle;
    });
}

document.addEventListener("DOMContentLoaded", () => {
    const headerText = document.getElementById('nav-title');
    const items = document.querySelectorAll(".header-title");

    const updateHeaderTitle = (title) => {
        headerText.innerHTML = title;
        sessionStorage.setItem('headerTitle', title); 
    };

    items.forEach((item) => {
        item.addEventListener("click", (event) => {
            const parentLink = event.target.closest('a');

            if (parentLink && parentLink.getAttribute('href')) {
                const newTitle = item.innerHTML;  
                updateHeaderTitle(newTitle);  
            } else {
                event.preventDefault();
                console.log('No valid address for this item. Title will not change.');
            }
        });
    });
});


document.addEventListener("DOMContentLoaded", function() {
    const dashboard = document.getElementById("dashboard");
    const toggleDashboardBtn = document.getElementById("toggleDashboardBtn");
    const container = document.getElementById("mainContainer");
    const mainStyle = document.getElementById("mainStyle");

    if (toggleDashboardBtn && dashboard) { // Ensure elements exist
        toggleDashboardBtn.addEventListener("click", function() {
            // Toggle dashboard visibility
            dashboard.classList.toggle("dashboard-hidden"); // Adds or removes 'dashboard-hidden' class

            // Change icon based on dashboard visibility
            if (dashboard.classList.contains("dashboard-hidden")) {
                toggleDashboardBtn.innerHTML = '<i class="fa fa-bars"></i>'; // "Open" icon
            } else {
                toggleDashboardBtn.innerHTML = '<i class="fa fa-times"></i>'; // "Close" icon
            }

            // Toggle container and mainStyle classes for full-width effect
            container.classList.toggle("container-full");
            mainStyle.classList.toggle("main-style-full");
        });
    } else {
        console.error("Dashboard or toggle button not found.");
    }
});