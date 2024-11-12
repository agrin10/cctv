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

// Send PATCH request to update camera details
function sendPatchRequest(row) {
    // Collect data from the form inputs
    const newIpAddress = ipAddressInput.value;
    const deviceName = deviceNameInput.value;
    const deviceType = deviceTypeInput.value;
    const zoneName = zoneInput.value;
    const isRecording = document.getElementById('recordingSelectEdit').value === "1";
    const aiProperties = Array.from(document.querySelectorAll('#ObjectEditCameraOptions .checkbox:checked')).map(cb => cb.value);

    // Create data payload based on backend expectations
    const data = {
        oldIpAddress: row.cells[1].innerText,  // original IP from row
        newIpAddress: newIpAddress,
        deviceName: deviceName,
        deviceType: deviceType,
        camera_zones: zoneName,
        recording: isRecording ? "yes" : "no",
        ai_properties: aiProperties
    };

    // Send PATCH request to the Flask endpoint
    fetch('/camera/', {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        if (result.success) {
            // Update the table row with new values
            row.cells[1].innerText = newIpAddress;
            row.cells[2].innerText = deviceName;
            row.cells[3].innerText = deviceType;
            row.cells[4].innerText = zoneName; // Update zone cell
            // row.cells[5].innerText = isRecording ? 'Yes' : 'No';
            // row.cells[6].innerText = aiProperties.join(', ');

            console.log('Camera updated successfully!');
            resetSidebarForm(); // Reset the form after successful edit
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

