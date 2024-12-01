// Dropdown elements and toggle functionality
function setupDropdownToggle(dropdownButton, dropdownOptions, svgIcon) {
    dropdownButton.addEventListener("click", (event) => {
        event.stopPropagation(); 
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
            option.classList.toggle("selected", checkbox.checked); 
            event.stopPropagation(); 
        });
    });
}

// Initialize dropdowns for specified sections
setupDropdownToggle(
    document.getElementById("selectedObjectCameras"),
    document.getElementById("ObjectCameraOptions"),
    document.getElementById("selectedObjectCameras").querySelector("svg")
);

setupCheckboxSelection(document.getElementById("ObjectCameraOptions"));

const selectedZones = document.getElementById("selectedZones");
const zonesOptions = document.getElementById("zonesOptions");

// Toggle dropdown display
selectedZones.addEventListener("click", () => {
  const isDropdownVisible = zonesOptions.style.display === "block";
  zonesOptions.style.display = isDropdownVisible ? "none" : "block";
});

// Close dropdown when clicking outside
document.addEventListener("click", (event) => {
  if (
    !selectedZones.contains(event.target) &&
    !zonesOptions.contains(event.target)
  ) {
    zonesOptions.style.display = "none";
  }
});

// Handle radio selection
zonesOptions.querySelectorAll(".custom-radio-camera").forEach((option) => {
  option.addEventListener("click", (event) => {
    const radio = option.querySelector("input[type='radio']");
    if (!radio.checked) {
      radio.checked = true; // Select the clicked radio
      selectedZones.textContent = option.querySelector("span").textContent; 
    }
    zonesOptions.style.display = "none"; 
    event.stopPropagation();
  });
});

// Rotate the dropdown icon
selectedZones.addEventListener("click", () => {
  const svg = selectedZones.querySelector("svg");
  const isRotated = svg.style.transform === "rotate(180deg)";
  svg.style.transform = isRotated ? "rotate(0deg)" : "rotate(180deg)";
});
const selectedRecording = document.getElementById("selectedRecording");
const recordingOptions = document.getElementById("recordingOptions");

// Toggle dropdown display for recording
selectedRecording.addEventListener("click", () => {
const isDropdownVisible = recordingOptions.style.display === "block";
recordingOptions.style.display = isDropdownVisible ? "none" : "block";

// Rotate the dropdown icon
const svg = selectedRecording.querySelector("svg");
const isRotated = svg.style.transform === "rotate(180deg)";
svg.style.transform = isRotated ? "rotate(0deg)" : "rotate(180deg)";
});

// Close dropdown when clicking outside
document.addEventListener("click", (event) => {
if (
!selectedRecording.contains(event.target) &&
!recordingOptions.contains(event.target)
) {
recordingOptions.style.display = "none";

// Reset icon rotation
const svg = selectedRecording.querySelector("svg");
if (svg) svg.style.transform = "rotate(0deg)";
}
});

// Handle radio selection for recording
recordingOptions.querySelectorAll(".custom-radio-recording").forEach((option) => {
option.addEventListener("click", (event) => {
const radio = option.querySelector("input[type='radio']");
if (!radio.checked) {
  radio.checked = true; // Select the clicked radio
  selectedRecording.querySelector("span").textContent =
    option.querySelector("span").textContent; // Update dropdown label
}
recordingOptions.style.display = "none"; // Close dropdown immediately
event.stopPropagation();
});
});

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


const popup = document.getElementById("specific_camera_popup");
const closeButton = document.querySelector(".cameraPopup-return-btn");
document.querySelectorAll(".camera-body-row").forEach(row => {
    const viewButton = row.querySelector(".view-btn");
    viewButton?.addEventListener("click", (event) => {
        event.stopPropagation();
        document.getElementById("modal-camera-name").innerText = row.querySelector('td:nth-child(3)').innerText;
        document.getElementById("modal-camera-zone").innerText = row.querySelector('td:nth-child(5)').innerText;
        document.getElementById("modal-camera-timestamp").innerText = new Date().toLocaleString();
        popup.style.display = "block";
    });
});

// Popup close behavior
function closePopup() {
    popup.style.display = "none";
}

// Attach close event to the close button
closeButton.addEventListener("click", closePopup);


closeButton.addEventListener("click", closePopup);



const formTitle = document.querySelector('.camera-title'); 
const ipAddressInput = document.getElementById('ipAddress'); 
const deviceNameInput = document.getElementById('deviceName'); 
const deviceTypeInput = document.getElementById('deviceType'); 
const zoneInput = document.getElementById('zoneSelect');
const buttonGroup = document.getElementById('buttonGroup');

// Fill form with selected row data
function fillSidebarFormWithRowData(row) {
    ipAddressInput.value = row.cells[1].innerText;
    deviceNameInput.value = row.cells[2].innerText;
    deviceTypeInput.value = row.cells[3].innerText;
    zoneInput.value = row.cells[4].innerText; // Assigning zone data
    formTitle.textContent = 'ویرایش دوربین: ' + deviceNameInput.value;

    // Populate button group with edit and cancel buttons
    buttonGroup.innerHTML = `
        <button type="button" class="camera-edit-btn">ویرایش</button>
        <button type="button" class="camera-cancel-btn">انصراف</button>
    `;

    // Attach event listeners to the new buttons
    document.querySelector('.camera-edit-btn').addEventListener('click', () => sendPatchRequest(row));
    document.querySelector('.camera-cancel-btn').addEventListener('click', resetSidebarForm);
}
function sendPatchRequest(row) {
    // Collect data from the form inputs
    const newIpAddress = ipAddressInput.value;
    const deviceName = deviceNameInput.value;
    const deviceType = deviceTypeInput.value;
    const zoneName = zoneInput.value; 
    const isRecording = document.getElementById('recordingSelect').value === "1";
    
    const aiProperties = Array.from(document.querySelectorAll('#ObjectCameraOptions .checkbox:checked')).map(cb => cb.value);

    const data = {
        oldIpAddress: row.cells[1].innerText,
        newIpAddress: newIpAddress,
        deviceName: deviceName,
        deviceType: deviceType,
        camera_zones: zoneName,  
        recording: isRecording ? "yes" : "no", 
        ai_properties: aiProperties
    };

    fetch('/camera/', {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)  // Send JSON payload
    })
    .then(response => response.json())
    .then(result => {
        if (result.success) {
            // Update the table row with new values
            row.cells[1].innerText = newIpAddress;
            row.cells[2].innerText = deviceName;
            row.cells[3].innerText = deviceType;
            row.cells[4].innerText = zoneName.join(', ');  // Update zone cell (if it's an array, join into a string)

            console.log('Camera updated successfully!');
            resetSidebarForm();  // Reset the form after successful edit
        } else {
            console.log(`Error: ${result.message}`);
        }
    })
    .catch(error => console.error('Error:', error));
}

// Reset sidebar form to initial state
function resetSidebarForm() {
    formTitle.textContent = 'افزودن دوربین جدید';
    [ipAddressInput, deviceNameInput, deviceTypeInput, zoneInput].forEach(input => input.value = '');
    buttonGroup.innerHTML = `<button type="submit" class="zone-add-btn">افزودن</button>`;
}

// Attach event listeners to each row for sidebar form filling
document.querySelectorAll('.camera-body-row').forEach(row => 
    row.addEventListener('click', () => fillSidebarFormWithRowData(row))
);

