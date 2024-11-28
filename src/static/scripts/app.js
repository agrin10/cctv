const selectedCameras = document.getElementById("selectedCameras");

const cameraOptions = document.getElementById("cameraOptions");

const selectedZones = document.getElementById("selectedZones");
const zoneOptions = document.getElementById("zoneOptions");

const selectedUsers = document.getElementById("selectedUsers");
const userOptions = document.getElementById("userOptions");

const selectedCamerasTwo = document.getElementById("selectedCamerasTwo");
const cameraOptionsTwo = document.getElementById("cameraOptionsTwo");

const selectedZonesTwo = document.getElementById("selectedZonesTwo");
const zoneOptionsTwo = document.getElementById("zoneOptionsTwo");

// Dropdown functionality
const toggleDropdown = (selected, options) => {
  selected.addEventListener("click", () => {
    options.style.display =
      options.style.display === "block" ? "none" : "block";
  });
};

toggleDropdown(selectedCameras, cameraOptions);
toggleDropdown(selectedZones, zoneOptions);
toggleDropdown(selectedUsers, userOptions);

toggleDropdown(selectedCamerasTwo, cameraOptionsTwo);
toggleDropdown(selectedZonesTwo, zoneOptionsTwo);

// Close the dropdown when clicking outside
document.addEventListener("click", (event) => {
  if (
    !selectedCameras.contains(event.target) &&
    !cameraOptions.contains(event.target)
  ) {
    cameraOptions.style.display = "none";
  }
  if (
    !selectedZones.contains(event.target) &&
    !zoneOptions.contains(event.target)
  ) {
    zoneOptions.style.display = "none";
  }
  if (
    !selectedUsers.contains(event.target) &&
    !userOptions.contains(event.target)
  ) {
    userOptions.style.display = "none";
  }

  if (
    !selectedCamerasTwo.contains(event.target) &&
    !cameraOptionsTwo.contains(event.target)
  ) {
    cameraOptionsTwo.style.display = "none";
  }
  if (
    !selectedZonesTwo.contains(event.target) &&
    !zoneOptionsTwo.contains(event.target)
  ) {
    zoneOptionsTwo.style.display = "none";
  }
});

// Checkbox behavior
const setupCheckboxBehavior = (options, selected) => {
  options.querySelectorAll("div").forEach((option) => {
    option.addEventListener("click", (event) => {
      const checkbox = option.querySelector(".checkbox");
      checkbox.checked = !checkbox.checked; // Toggle the checkbox state

      const value = checkbox.getAttribute("data-value");
      if (checkbox.checked) {
        option.style.backgroundColor = "#e9f5ff"; // Highlight selected
      } else {
        option.style.backgroundColor = ""; // Remove highlight
      }
      event.stopPropagation(); // Prevent event from bubbling to parent
    });
  });
};

setupCheckboxBehavior(cameraOptions, selectedCameras);
setupCheckboxBehavior(zoneOptions, selectedZones);
setupCheckboxBehavior(userOptions, selectedUsers);
setupCheckboxBehavior(selectedCamerasTwo, cameraOptionsTwo);
setupCheckboxBehavior(selectedZonesTwo, zoneOptionsTwo);

// ***********
const labelCheckboxes = document.querySelectorAll(".lable-cheekbox");

labelCheckboxes.forEach((label) => {
  label.addEventListener("click", function () {
    const svg = this.querySelector("svg");

    const currentTransform = svg.style.transform || "";
    if (currentTransform.includes("rotate(180deg)")) {
      svg.style.transform = "rotate(0deg)";
    } else {
      svg.style.transform = "rotate(180deg)";
    }
  });
});

//edit ++++++++++++++++


const EditUserSelectedCameras = document.getElementById("EditUserSelectedCameras");

const EditUserCameraOptions = document.getElementById("EditUserCameraOptions");

const EditUserSelectedZones = document.getElementById("EditUserSelectedZones");
const EditUserZoneOptions = document.getElementById("EditUserZoneOptions");

const EditUserSelectedUsers = document.getElementById("EditUserSelectedUsers");
const EditUserUserOptions = document.getElementById("EditUserUserOptions");

const EditUserSelectedCamerasTwo = document.getElementById("EditUserSelectedCamerasTwo");
const EditUserCameraOptionsTwo = document.getElementById("EditUserCameraOptionsTwo");

const EditUserSelectedZonesTwo = document.getElementById("EditUserSelectedZonesTwo");
const EditUserZoneOptionsTwo = document.getElementById("EditUserZoneOptionsTwo");

// Dropdown functionality
const toggleDropdownEdit = (selected, options) => {
  selected.addEventListener("click", () => {
    options.style.display =
      options.style.display === "block" ? "none" : "block";
  });
};

toggleDropdownEdit(EditUserSelectedCameras, EditUserCameraOptions);
toggleDropdownEdit(EditUserSelectedZones , EditUserZoneOptions);
toggleDropdownEdit(EditUserSelectedUsers, EditUserUserOptions);

toggleDropdownEdit(EditUserSelectedCamerasTwo, EditUserCameraOptionsTwo);
toggleDropdownEdit(EditUserSelectedZonesTwo, EditUserZoneOptionsTwo);

// Close the dropdown when clicking outside
document.addEventListener("click", (event) => {
  if (
    !EditUserSelectedCameras.contains(event.target) &&
    !EditUserCameraOptions.contains(event.target)
  ) {
    EditUserCameraOptions.style.display = "none";
  }
  if (
    !EditUserSelectedZones.contains(event.target) &&
    !EditUserZoneOptions.contains(event.target)
  ) {
    EditUserZoneOptions.style.display = "none";
  }
  if (
    !EditUserSelectedUsers.contains(event.target) &&
    !EditUserUserOptions.contains(event.target)
  ) {
    EditUserUserOptions.style.display = "none";
  }

  if (
    !EditUserSelectedCamerasTwo.contains(event.target) &&
    !EditUserCameraOptionsTwo.contains(event.target)
  ) {
    EditUserCameraOptionsTwo.style.display = "none";
  }
  if (
    !EditUserSelectedZonesTwo.contains(event.target) &&
    !EditUserZoneOptionsTwo.contains(event.target)
  ) {
    EditUserZoneOptionsTwo.style.display = "none";
  }
});

// Checkbox behavior
const setupCheckboxBehaviorEdit = (options, selected) => {
  options.querySelectorAll("div").forEach((option) => {
    option.addEventListener("click", (event) => {
      const checkbox = option.querySelector(".checkbox");
      checkbox.checked = !checkbox.checked; // Toggle the checkbox state

      const value = checkbox.getAttribute("data-value");
      if (checkbox.checked) {
        option.style.backgroundColor = "#e9f5ff"; // Highlight selected
      } else {
        option.style.backgroundColor = ""; // Remove highlight
      }
      event.stopPropagation(); // Prevent event from bubbling to parent
    });
  });
};

setupCheckboxBehavior(EditUserCameraOptions, EditUserSelectedCameras);
setupCheckboxBehavior(EditUserZoneOptions, EditUserSelectedZones);
setupCheckboxBehavior(EditUserUserOptions, EditUserSelectedUsers);
setupCheckboxBehavior(EditUserSelectedCamerasTwo, EditUserCameraOptionsTwo);
setupCheckboxBehavior(EditUserSelectedZonesTwo, EditUserZoneOptionsTwo);

// ***********
const labelCheckboxesEdit = document.querySelectorAll(".lable-cheekbox");

labelCheckboxesEdit.forEach((label) => {
  label.addEventListener("click", function () {
    const svg = this.querySelector("svg");

    const currentTransform = svg.style.transform || "";
    if (currentTransform.includes("rotate(180deg)")) {
      svg.style.transform = "rotate(0deg)";
    } else {
      svg.style.transform = "rotate(180deg)";
    }
  });
});


// 
const selectedObject = document.getElementById("selectedObject");
const objectOptions = document.getElementById("objectOptions");

// Toggle camera dropdown
selectedObject.addEventListener("click", () => {
  objectOptions.style.display = objectOptions.style.display === "block" ? "none" : "block";
});

// Close camera dropdown when clicking outside
document.addEventListener("click", (event) => {
  if (!selectedObject.contains(event.target) && !objectOptions.contains(event.target)) {
    objectOptions.style.display = "none";
  }
});

// Checkbox selection behavior for cameras
objectOptions.querySelectorAll("div").forEach((option) => {
  option.addEventListener("click", (event) => {
    const checkbox = option.querySelector(".checkbox");
    checkbox.checked = !checkbox.checked;
    option.style.backgroundColor = checkbox.checked ? "#e9f5ff" : "";
    event.stopPropagation(); // Prevent bubbling to close dropdown
  });
});

// Rotate SVG icon on click
selectedObject.addEventListener("click", () => {
  const svg = selectedObject.querySelector("svg");
  svg.style.transform = svg.style.transform === "rotate(180deg)" ? "rotate(0deg)" : "rotate(180deg)";
});


// cameras page  dropdowns 
////////////////////////
