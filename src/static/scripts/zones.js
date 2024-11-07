function fillSidebarFormWithRowData(row) {
    selectedRow = row;
    
    const zoneName = row.getAttribute("data-zone-name");
    const zoneDescription = row.getAttribute("data-zone-description");
    
    zoneNameInput.value = zoneName;
    zoneDescriptionInput.value = zoneDescription;
    formTitle.textContent = `ویرایش منطقه: ${zoneName}`;
  
    // Set old values for data attributes
    openEditModal(zoneName, zoneDescription);
  }
  
  // Open the edit modal with current data
  function openEditModal(zoneName, zoneDescription) {
    newZoneNameInput.value = zoneName;
    newZoneDescriptionInput.value = zoneDescription;
    
    newZoneNameInput.setAttribute("data-old-zone-name", zoneName);
    newZoneDescriptionInput.setAttribute("data-old-zone-desc", zoneDescription);
  
    editModal.style.display = "flex";
    modalBackdrop.style.display = "block";
  }
  document.querySelector('.confirm-edit-btn').addEventListener('click', function() {
    const newZoneNameInput = document.getElementById("newZoneName");
    const newZoneDescriptionInput = document.getElementById("newZoneDescription");

    // Get old values from data attributes
    const oldZoneName = newZoneNameInput.getAttribute('data-old-zone-name');
    const oldZoneDescription = newZoneDescriptionInput.getAttribute('data-old-zone-desc');

    // Get new values from input fields
    const newZoneName = newZoneNameInput.value;
    const newZoneDescription = newZoneDescriptionInput.value;

    // Define the data to send in the request
    const data = {
        old_zone_name: oldZoneName,
        old_zone_desc: oldZoneDescription,
        new_zone_name: newZoneName,
        new_zone_desc: newZoneDescription
    };

    // Send data to backend with PATCH method
    fetch('/zones/', {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Update the selected row with the new values
            selectedRow.setAttribute('data-zone-name', newZoneName);
            selectedRow.setAttribute('data-zone-description', newZoneDescription);
            selectedRow.cells[1].innerText = newZoneName;
            selectedRow.cells[2].innerText = newZoneDescription;

            // Close the modal and reset the sidebar form
            closeEditZoneModal();
            resetSidebarForm();
        } else {
            console.error(`Failed to edit zone: ${data.message}`);
        }
    })
    .catch(error => console.error('Error:', error));
});

  


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
    function convertToPersianNumber(number) {
      const persianDigits = '۰۱۲۳۴۵۶۷۸۹';
      return number.toString().split('').map(digit => persianDigits[digit]).join('');
  }
  function populateCameraList(data) {
    const cameraListBody = document.getElementById('cameraListBody'); // Use the correct ID for camera list body
    console.log(cameraListBody); // Check if the element is found
    if (cameraListBody) { // Check if element exists
        cameraListBody.innerHTML = ''; // Clear existing rows

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
                <td class="view-btn zone-view-btn"></td>
            `;
            cameraListBody.appendChild(row);
        });
    } else {
        console.error('cameraListBody not found');
    }
}    // Close modal functionality
    document.querySelector('.close-modal-btn').addEventListener('click', function() {
        document.querySelector('.backdrop-modal').style.display = 'none';
        document.querySelector('.zone-camera-list').style.display = 'none';
    });
});

let selectedRow = null;
const formTitle = document.querySelector(".zone-title");
const zoneNameInput = document.getElementById("zoneName");
const zoneDescriptionInput = document.getElementById("zoneDescription");
const buttonGroup = document.getElementById("buttonGroup");

function fillSidebarFormWithRowData(row) {
  selectedRow = row; 
  
  const zoneName = row.getAttribute("data-zone-name");
  const zoneDescription = row.getAttribute("data-zone-description");

  zoneNameInput.value = zoneName;
  zoneDescriptionInput.value = zoneDescription;
  formTitle.textContent = `ویرایش منطقه: ${zoneName}`;

  buttonGroup.innerHTML = `
    <button type="button" class="zone-edit-btn">ویرایش</button>
    <button type="button" class="zone-cancel-btn">انصراف</button>
  `;

  // Inside the fillSidebarFormWithRowData function where the cancel button is set:
document.querySelector(".zone-edit-btn").addEventListener("click", () => {
  openEditZoneModal(zoneName, zoneDescription);
});

document.querySelector('.zone-cancel-btn').addEventListener('click', resetSidebarForm);  // Fix here

}

// Function to open the edit-zone modal with the selected data
function openEditZoneModal(zoneName, zoneDescription) {
  const newZoneNameInput = document.getElementById("newZoneName");
  const newZoneDescriptionInput = document.getElementById("newZoneDescription");

  // Set modal inputs with the current zone data
  newZoneNameInput.value = zoneName;
  newZoneDescriptionInput.value = zoneDescription;

  // Set data attributes to store the old values for the backend
  newZoneNameInput.setAttribute("data-old-zone-name", zoneName);
  newZoneDescriptionInput.setAttribute("data-old-zone-desc", zoneDescription);

  // Show the modal
  document.getElementById("editFormModal").style.display = "flex";
  document.getElementById("modalBackdrop").style.display = "block";
}

// Attach click event to each table row to populate the sidebar
document.querySelectorAll(".zone-body-row").forEach((row) => {
  row.addEventListener("click", () => fillSidebarFormWithRowData(row));
});

// Reset sidebar form to "Add New Zone" state
function resetSidebarForm() {
  formTitle.textContent = "افزودن منطقه جدید";
  zoneNameInput.value = "";
  zoneDescriptionInput.value = "";
  buttonGroup.innerHTML = `<button type="submit" class="zone-add-btn" style="background-color: #124076; color:white;">افزودن</button>`;
}


// Initialize sidebar form and close modals on page load
window.onload = function () {
  resetSidebarForm();
  closeCamListModal();
  closeEditZoneModal();
};

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

// Close the edit-zone modal
function closeEditZoneModal() {
  document.getElementById("editFormModal").style.display = "none";
  document.getElementById("modalBackdrop").style.display = "none";
}

// Attach the close event to the backdrop and cancel button for the edit-zone modal
document.querySelector(".cancel-edit-btn").addEventListener("click", closeEditZoneModal);
document.getElementById("modalBackdrop").addEventListener("click", closeEditZoneModal);


  closeEditZoneModal(); 

  cancelEditBtn.addEventListener("click", closeEditZoneModal);

  modalBackdrop.addEventListener("click", function () {
    closeCamListModal();
    closeEditZoneModal()
  });

  window.onload = function () {
    closeCamListModal(); 
    closeEditZoneModal(); 
  };
  
