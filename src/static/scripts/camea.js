var popup = document.getElementById("specific_camera_popup");

var cameraRows = document.querySelectorAll(".camera-body-row");

cameraRows.forEach(function(row) {
    var viewButton = row.querySelector(".view-btn");  
    if (viewButton) {
        viewButton.addEventListener("click", function(event) {
            event.stopPropagation();

            var deviceName = row.querySelector('td:nth-child(3)').innerText; 
            var zoneName = row.querySelector('td:nth-child(5)').innerText;  

            var currentDate = new Date();
            var timestamp = currentDate.getFullYear() + '/' + (currentDate.getMonth() + 1) + '/' + currentDate.getDate() + ' ' + currentDate.getHours() + ':' + currentDate.getMinutes() + ':' + currentDate.getSeconds();

            document.getElementById("modal-camera-name").innerText = deviceName;  
            document.getElementById("modal-camera-zone").innerText = zoneName;   
            document.getElementById("modal-camera-timestamp").innerText = timestamp; 


            document.getElementById("modal-camera-name-header").innerText = 'دوربین ' + deviceName;


            popup.style.display = "block";
        });
    }
});


document.querySelector(".popup-return-btn").addEventListener("click", function() {
    popup.style.display = "none"; 
});

window.onclick = function(event) {
    if (event.target == popup) {
        popup.style.display = "none";
    }
};

// Get form elements for sidebar form
const formTitle = document.querySelector('.camera-title'); 
const ipAddressInput = document.getElementById('ipAddress'); 
const deviceNameInput = document.getElementById('deviceName'); 
const deviceTypeInput = document.getElementById('deviceType'); 
const cameraUsernameInput = document.getElementById('cameraUsername'); 
const cameraPasswordInput = document.getElementById('cameraPassword'); 
const buttonGroup = document.getElementById('buttonGroup');

function fillSidebarFormWithRowData(row) {
    // Get values from the clicked row
    const ipAddress = row.cells[1].innerText;        
    const deviceName = row.cells[2].innerText;      
    const deviceType = row.cells[3].innerText;      
    const zoneName = row.cells[4].innerText;      
    const cameraUsername = '';
    const cameraPassword = ''; 

    // Fill the sidebar form fields
    ipAddressInput.value = ipAddress;
    deviceNameInput.value = deviceName;
    deviceTypeInput.value = deviceType;
    cameraUsernameInput.value = cameraUsername;
    cameraPasswordInput.value = cameraPassword;

    formTitle.textContent = 'ویرایش دوربین: ' + deviceName;

    buttonGroup.innerHTML = `
        <button type="button" class="camera-edit-btn">ویرایش</button>
        <button type="button" class="camera-cancel-btn">انصراف</button>
    `;

    document.querySelector('.camera-edit-btn').addEventListener('click', openCameraEditModal); 
    document.querySelector('.camera-cancel-btn').addEventListener('click', resetSidebarForm); 
}
document.querySelectorAll('.camera-body-row').forEach(row => {
    row.addEventListener('click', () => fillSidebarFormWithRowData(row));
});

function resetSidebarForm() {
    formTitle.textContent = 'افزودن دوربین جدید'; 
    ipAddressInput.value = '';
    deviceNameInput.value = '';
    deviceTypeInput.value = '';
    cameraUsernameInput.value = '';
    cameraPasswordInput.value = '';
    buttonGroup.innerHTML = '';  

    buttonGroup.innerHTML = `<button type="submit" class="zone-add-btn">افزودن</button>`;
}

window.onload = () => {
    resetSidebarForm();
};

const cameraEditModal = document.getElementById('editCameraModal');
    const modalBackdrop = document.querySelector('.cam-backdrop');

    console.log(cameraEditModal, modalBackdrop); 

    const camIpAddressInput = document.getElementById('camIpAddress');
    const camDeviceNameInput = document.getElementById('camDeviceName');
    const camDeviceTypeInput = document.getElementById('camDeviceType');
    const camCameraUsernameInput = document.getElementById('camCameraUsername');
    const camCameraPasswordInput = document.getElementById('camCameraPassword');



    function openCameraEditModal() {
        console.log('Opening modal...'); // Debugging log

        camIpAddressInput.value = ipAddressInput.value;
        camDeviceNameInput.value = deviceNameInput.value;
        camDeviceTypeInput.value = deviceTypeInput.value;
        camCameraUsernameInput.value = cameraUsernameInput.value;
        camCameraPasswordInput.value = cameraPasswordInput.value;

        cameraEditModal.style.display = 'flex';  
        modalBackdrop.style.display = 'block';
        console.log('Modal should be visible now');  
    }

    function closeCameraEditModal() {
        cameraEditModal.style.display = 'none';
        modalBackdrop.style.display = 'none';
    }


    modalBackdrop.addEventListener('click', closeCameraEditModal);

    document.querySelector('.cam-cancel-btn').addEventListener('click', closeCameraEditModal);



