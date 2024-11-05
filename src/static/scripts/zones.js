function fillSidebarFormWithRowData(row) {
    selectedRow = row;
    
    const zoneName = row.getAttribute("data-zone-name");
    const zoneDescription = row.getAttribute("data-zone-description");
    
    zoneNameInput.value = zoneName;
    zoneDescriptionInput.value = zoneDescription;
    formTitle.textContent = `ویرایش منطقه: ${zoneName}`;
  
    // Set old values for data attributes
    // openEditModal(zoneName, zoneDescription);
  }

  const modal = document.querySelector(".camera-list-modal");
  const backdrop = document.querySelector(".backdrop-modal");
  const closeModalBtn = document.querySelector(".close-modal-btn");
  const viewBtns = document.querySelectorAll(".view-btn");

  document.addEventListener('DOMContentLoaded', function() {
    const viewButtons = document.querySelectorAll('.view-btn');

    viewButtons.forEach(button => {
        button.addEventListener('click', function() {
            const zoneId = this.dataset.zoneId; 
            const zoneName = this.closest('tr').dataset.zoneName; 
            fetchCameras(zoneId, zoneName); 
        });
    });

    function fetchCameras(zoneId, zoneName) {
        fetch(`/zones/${zoneId}/cameras`) 
            .then(response => {
                if (!response.ok) {
                    throw new Error('Zone not found');
                }
                return response.json();
            })
            .then(data => {
                populateCameraList(data);
                document.querySelector('.camera-list-modal h2').textContent = `دوربین‌های ${zoneName}`; 
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

  document.querySelector(".zone-edit-btn").addEventListener("click", () => {
    openEditZoneModal(zoneName, zoneDescription);
  document.querySelector('.zone-cancel-btn').addEventListener('click', resetSidebarForm);
  });
}



document.querySelectorAll(".zone-body-row").forEach((row) => {
  row.addEventListener("click", () => fillSidebarFormWithRowData(row));
});

function resetSidebarForm() {
  formTitle.textContent = "افزودن منطقه جدید";
  zoneNameInput.value = "";
  zoneDescriptionInput.value = "";
  buttonGroup.innerHTML = `<button type="submit" class="zone-add-btn" style="background-color: #124076; color:white;">افزودن</button>`;
}


window.onload = function () {
  resetSidebarForm();
  closeCamListModal();
};

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



  window.onload = function () {
    closeCamListModal(); 
  };
  
