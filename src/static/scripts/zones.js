let selectedRow = null;  // Track selected row for editing
let editMode = false;    // Mode flag to differentiate between add and edit actions

// Sidebar form elements
const formTitle = document.querySelector(".zone-title");
const zoneNameInput = document.getElementById("zoneName");
const zoneDescriptionInput = document.getElementById("zoneDescription");
const buttonGroup = document.getElementById("buttonGroup");

// Function to initialize the sidebar for adding a new zone
function resetSidebarForm() {
  editMode = false;  // Switch to "Add" mode
  formTitle.textContent = "افزودن منطقه جدید";  // Update form title
  zoneNameInput.value = "";
  zoneDescriptionInput.value = "";

  // Update button to "Add"
  buttonGroup.innerHTML = `
    <button type="button" class="zone-add-btn" style="background-color: #124076; color:white;">افزودن</button>
  `;

  // Attach event listener for "Add" button
  document.querySelector(".zone-add-btn").addEventListener("click", addZone);
}

// Function to fill the sidebar with row data for editing
function fillSidebarFormWithRowData(row) {
  selectedRow = row; // Store the selected row for later reference
  editMode = true;   // Switch to "Edit" mode

  // Get data from row attributes
  const zoneName = row.getAttribute("data-zone-name");
  const zoneDescription = row.getAttribute("data-zone-description");

  // Populate form with existing data
  zoneNameInput.value = zoneName;
  zoneDescriptionInput.value = zoneDescription;
  formTitle.textContent = `ویرایش منطقه: ${zoneName}`;  // Update form title

  // Update button to "Edit"
  buttonGroup.innerHTML = `
    <button type="button" class="zone-edit-btn" style="background-color: #124076; color:white;">ویرایش</button>
    <button type="button" class="zone-cancel-btn">انصراف</button>
  `;

  // Attach event listeners for edit and cancel buttons
  document.querySelector(".zone-edit-btn").addEventListener("click", editZone);
  document.querySelector(".zone-cancel-btn").addEventListener("click", resetSidebarForm);
}

// Function to handle adding a new zone (POST request)
function addZone() {
  const zoneName = zoneNameInput.value.trim();
  const zoneDescription = zoneDescriptionInput.value.trim();

  if (zoneName && zoneDescription) {
    // Send POST request to add new zone
    fetch('/zones/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ zone_name: zoneName, zone_desc: zoneDescription })
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        // Optionally, update the UI to show the new zone in the list
        resetSidebarForm();  // Reset sidebar to "Add" mode
      } else {
        console.error(`Failed to add zone: ${data.message}`);
      }
    })
    .catch(error => console.error('Error:', error));
  } else {
    alert("Please fill in all fields.");
  }
}

// Function to handle editing an existing zone (PATCH request)
function editZone() {
  const newZoneName = zoneNameInput.value.trim();
  const newZoneDescription = zoneDescriptionInput.value.trim();

  if (newZoneName && newZoneDescription) {
    const oldZoneName = selectedRow.getAttribute("data-zone-name");
    const oldZoneDescription = selectedRow.getAttribute("data-zone-description");

    // Send PATCH request to update the zone
    fetch('/zones/', {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        old_zone_name: oldZoneName,
        old_zone_desc: oldZoneDescription,
        new_zone_name: newZoneName,
        new_zone_desc: newZoneDescription
      })
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        // Update the selected row in the table
        selectedRow.setAttribute('data-zone-name', newZoneName);
        selectedRow.setAttribute('data-zone-description', newZoneDescription);
        selectedRow.cells[1].innerText = newZoneName;
        selectedRow.cells[2].innerText = newZoneDescription;

        resetSidebarForm();  // Reset sidebar to "Add" mode
      } else {
        console.error(`Failed to edit zone: ${data.message}`);
      }
    })
    .catch(error => console.error('Error:', error));
  } else {
    alert("Please fill in all fields.");
  }
}

// Attach event listeners to table rows for "Edit" mode
document.querySelectorAll(".zone-body-row").forEach(row => {
  row.addEventListener("click", () => fillSidebarFormWithRowData(row));
});

// Initialize the sidebar form on page load for "Add" mode
window.onload = resetSidebarForm;


const modal = document.querySelector(".camera-list-modal");
const backdrop = document.querySelector(".backdrop-modal");
const closeModalBtn = document.querySelector(".close-modal-btn");
const viewBtns = document.querySelectorAll(".view-btn");

document.addEventListener('DOMContentLoaded', function() {
  const viewButtons = document.querySelectorAll('.view-btn');

  viewButtons.forEach(button => {
      button.addEventListener('click', function() {
          const zoneId = this.dataset.zoneId; // Assuming zone ID is stored in a data attribute
          const zoneName = this.closest('tr').dataset.zoneName; // Get the zone name from the row

          fetchCameras(zoneId, zoneName); // Pass the zone name to fetchCameras
      });
  });

  function fetchCameras(zoneId, zoneName) {
      fetch(`/zones/${zoneId}/cameras`) // Adjust the URL based on your route
          .then(response => {
              if (!response.ok) {
                  throw new Error('Zone not found');
              }
              return response.json();
          })
          .then(data => {
              populateCameraList(data);
              // Update the modal header with the zone name
              document.querySelector('.camera-list-modal h2').textContent = `دوربین‌های ${zoneName}`; // Update the header
              // Show the modal
              document.querySelector('.backdrop-modal').style.display = 'block';
              document.querySelector('.zone-camera-list').style.display = 'block';
          })
          .catch(error => {
              console.error('Error:', error);
              console.error(error.message);
          });
  }
});
  function convertToPersianNumber(number) {
    const persianDigits = '۰۱۲۳۴۵۶۷۸۹';
    return number.toString().split('').map(digit => persianDigits[digit]).join('');
}

function populateCameraList(data) {
  const cameraListBody = document.getElementById('cameraListBody'); 
  console.log(cameraListBody);
  if (cameraListBody) { 
      cameraListBody.innerHTML = ''; 

      data.cameras.forEach((camera, index) => {
          const row = document.createElement('tr');
          row.className = 'cam-list-zone-body-row';

          // Convert the index + 1 to Persian
          const persianIndex = convertToPersianNumber(index + 1);

          row.innerHTML = `
              <td class="body-cell-number">
                  <span class="row-number" lang="fa">${persianIndex}</span>
              </td>
              <td>${camera.camera_ip}</td>
              <td>${camera.camera_name}</td>
              <td>${camera.camera_type}</td>
              <td>${data.zone.zone_name}</td>
          `;
          cameraListBody.appendChild(row);
      });
  } else {
      console.error('cameraListBody not found');
  }
} 

// Open and close functions for cam-list modal
function openCamListModal() {
  document.querySelector(".camera-list-modal").style.display = "block";
  document.querySelector(".backdrop-modal").style.display = "block";
}
function closeCamListModal() {
  document.querySelector(".camera-list-modal").style.display = "none";
  document.querySelector(".backdrop-modal").style.display = "none";
}

// Attach open/close events to view buttons for cam-list modal
document.querySelectorAll(".view-btn").forEach((btn) => {
  btn.addEventListener("click", openCamListModal);
});
document.querySelector(".close-modal-btn").addEventListener("click", closeCamListModal);
document.querySelector(".backdrop-modal").addEventListener("click", closeCamListModal);

