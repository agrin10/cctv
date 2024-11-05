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


