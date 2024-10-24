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




    const toggleDropdown = (selected, options) => {
        selected.addEventListener("click", () => {
            options.style.display = options.style.display === "block" ? "none" : "block";
        });
    };

    // Apply dropdown functionality to Zones and Objects (allowing multiple selection)
    toggleDropdown(document.getElementById("selectedZones"), document.getElementById("zoneOptions"));
    toggleDropdown(document.getElementById("selectedObjects"), document.getElementById("objectOptions"));

    // Apply dropdown functionality for the Recording section (only single selection)
    const recordingOptions = document.getElementById("recordingOptions");
    const selectedRecording = document.getElementById("selectedRecording");

    selectedRecording.addEventListener("click", () => {
        recordingOptions.style.display = recordingOptions.style.display === "block" ? "none" : "block";
    });

    // Handle single selection for recording options
    recordingOptions.querySelectorAll(".single-option").forEach(option => {
        option.addEventListener("click", () => {
            // Set the selected value and close the dropdown
            selectedRecording.textContent = option.textContent;
            recordingOptions.style.display = "none";
        });
    });

    // Checkbox behavior for multiple selection in Zones and Objects
    const setupCheckboxBehavior = (options, selected) => {
        options.querySelectorAll("div").forEach(option => {
            option.addEventListener("click", (event) => {
                const checkbox = option.querySelector(".checkbox");
                checkbox.checked = !checkbox.checked; 

                if (checkbox.checked) {
                    option.style.backgroundColor = "#e9f5ff"; 
                } else {
                    option.style.backgroundColor = "";
                }
                event.stopPropagation(); 
            });
        });
    };

    // Apply checkbox behavior for zones and objects dropdowns
    setupCheckboxBehavior(document.getElementById("zoneOptions"), document.getElementById("selectedZones"));
    setupCheckboxBehavior(document.getElementById("objectOptions"), document.getElementById("selectedObjects"));


// Toggle dropdown visibility
const toggleDropdownEdit = (selected, options) => {
    selected.addEventListener("click", () => {
        options.style.display = options.style.display === "block" ? "none" : "block";
    });
};

// Apply dropdown functionality to Zones and Objects (allowing multiple selection)
toggleDropdownEdit(document.getElementById("camSelectedZones"), document.getElementById("camZoneOptions"));
toggleDropdownEdit(document.getElementById("camSelectedObjects"), document.getElementById("camObjectOptions"));

// Apply dropdown functionality for the Recording section (only single selection)
const camRecordingOptions = document.getElementById("camRecordingOptions");
const camSelectedRecording = document.getElementById("camSelectedRecording");

camSelectedRecording.addEventListener("click", () => {
    camRecordingOptions.style.display = camRecordingOptions.style.display === "block" ? "none" : "block";
});

// Handle single selection for recording options
camRecordingOptions.querySelectorAll(".single-option").forEach(option => {
    option.addEventListener("click", () => {
        // Set the selected value and close the dropdown
        camSelectedRecording.textContent = option.textContent;
        camRecordingOptions.style.display = "none";
    });
});

// Checkbox behavior for multiple selection in Zones and Objects
const setupCheckboxBehaviorEdit = (options) => {
    options.querySelectorAll("div").forEach(option => {
        option.addEventListener("click", (event) => {
            const checkbox = option.querySelector(".cam-checkbox");
            checkbox.checked = !checkbox.checked;

            if (checkbox.checked) {
                option.style.backgroundColor = "#e9f5ff"; // Highlight selected
            } else {
                option.style.backgroundColor = ""; // Remove highlight
            }
            event.stopPropagation(); // Prevent click event from bubbling
        });
    });
};

// Apply checkbox behavior for zones and objects dropdowns
setupCheckboxBehaviorEdit(document.getElementById("camZoneOptions"));
setupCheckboxBehaviorEdit(document.getElementById("camObjectOptions"));



// cameras

    