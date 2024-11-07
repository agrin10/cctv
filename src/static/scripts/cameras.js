// Dropdown elements and toggle functionality
function setupDropdownToggle(dropdownButton, dropdownOptions, svgIcon) {
    dropdownButton.addEventListener("click", (event) => {
        event.stopPropagation(); // Prevent click from bubbling to document
        const isVisible = dropdownOptions.style.display === "block";
        
        // Close all dropdowns before opening the clicked one
        document.querySelectorAll(".dropdown-options").forEach(option => option.style.display = "none");
        
        // Toggle current dropdown
        dropdownOptions.style.display = isVisible ? "none" : "block";
        svgIcon.style.transform = isVisible ? "rotate(0deg)" : "rotate(180deg)";
    });
}

// Close dropdown on clicking outside any dropdown
document.addEventListener("click", () => {
    document.querySelectorAll(".dropdown-options").forEach(option => option.style.display = "none");
    document.querySelectorAll(".dropdown-button svg").forEach(icon => icon.style.transform = "rotate(0deg)");
});

// Checkbox selection behavior in dropdown
function setupCheckboxSelection(dropdownOptions) {
    dropdownOptions.querySelectorAll(".custom-checkbox").forEach((option) => {
        option.addEventListener("click", (event) => {
            const checkbox = option.querySelector(".checkbox");
            checkbox.checked = !checkbox.checked;
            option.classList.toggle("selected", checkbox.checked); // Apply a 'selected' CSS class
            event.stopPropagation(); // Stop bubbling to avoid toggling dropdown
        });
    });
}

// Initialize dropdowns for specified sections
setupDropdownToggle(
    document.getElementById("selectedObjectCameras"),
    document.getElementById("ObjectCameraOptions"),
    document.getElementById("selectedObjectCameras").querySelector("svg")
);
setupDropdownToggle(
    document.getElementById("selectedObjectEditCameras"),
    document.getElementById("ObjectEditCameraOptions"),
    document.getElementById("selectedObjectEditCameras").querySelector("svg")
);
setupCheckboxSelection(document.getElementById("ObjectCameraOptions"));
setupCheckboxSelection(document.getElementById("ObjectEditCameraOptions"));

// Zone dropdown behavior with icon rotation
const zoneSelect = document.getElementById("zoneSelect");
const svgIcon = document.querySelector(".select-location-box svg");
zoneSelect.addEventListener("focus", () => svgIcon.style.transform = "rotate(180deg)");
zoneSelect.addEventListener("blur", () => svgIcon.style.transform = "rotate(0deg)");

// Delete camera functionality
function deleteCamera(button) {
    const cameraIp = button.getAttribute('data-camera-ip');
    const cameraName = button.getAttribute('data-camera-name');
    const url = `/camera/delete-camera/ip=${cameraIp}&name=${cameraName}`;

    fetch(url, { method: 'DELETE', headers: { 'Content-Type': 'application/json' } })
        .then(response => {
            if (!response.ok) throw new Error(`Failed to delete camera: ${response.statusText}`);
            return response.json();
        })
        .then(data => {
            if (data.success) {
                button.closest('tr').remove();
                console.log(`Camera ${cameraName} deleted successfully.`);
            } else {
                console.log(`Failed to delete camera: ${data.message}`);
            }
        })
        .catch(error => console.error('Error:', error));
}
