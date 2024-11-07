
// Dropdown elements and toggle functionality
function setupDropdownToggle(dropdownButton, dropdownOptions, svgIcon) {
    dropdownButton.addEventListener("click", () => {
        dropdownOptions.style.display = dropdownOptions.style.display === "block" ? "none" : "block";
        svgIcon.style.transform = svgIcon.style.transform === "rotate(180deg)" ? "rotate(0deg)" : "rotate(180deg)";
    });

    // Close dropdown on clicking outside
    document.addEventListener("click", (event) => {
        if (!dropdownButton.contains(event.target) && !dropdownOptions.contains(event.target)) {
            dropdownOptions.style.display = "none";
        }
    });
}

// Checkbox selection behavior in dropdown
function setupCheckboxSelection(dropdownOptions) {
    dropdownOptions.querySelectorAll(".custom-checkbox").forEach((option) => {
        option.addEventListener("click", (event) => {
            const checkbox = option.querySelector(".checkbox");
            checkbox.checked = !checkbox.checked;
            option.style.backgroundColor = checkbox.checked ? "#e9f5ff" : "";
            event.stopPropagation();
        });
    });
}

// Initialize the dropdown for both sections
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

