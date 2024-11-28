document.addEventListener("DOMContentLoaded", () => {
  const addUserBackdrop = document.getElementById("addUserBackdrop");
  const addUserForm = document.getElementById("AddUserForm");
  const addUserButton = document.getElementById("add-user-button");
  const cancelAddModalButton = document.getElementById("cancelAddModal");

  const editUserBackdrop = document.getElementById("editUserBackdrop");
  const editUserForm = document.getElementById("editUserForm");
  const editButtons = document.querySelectorAll(".edit-user-edit-btn");
  const cancelEditModalButton = document.getElementById("cancelEditModal");

  function openModal(modal, backdrop) {
    modal.style.display = "block";
    backdrop.style.display = "block";
  }

  function closeModal(modal, backdrop) {
    modal.style.display = "none";
    backdrop.style.display = "none";
  }
  if (addUserButton) {
    addUserButton.addEventListener("click", () => openModal(addUserForm, addUserBackdrop));
  }

  if (cancelAddModalButton) {
    cancelAddModalButton.addEventListener("click", () => closeModal(addUserForm, addUserBackdrop));
  }

  editButtons.forEach((button) => {
    button.addEventListener("click", function () {
      const row = this.closest("tr");

      const oldUsername = row.getAttribute("data-username");
      const oldPassword = row.getAttribute("data-password");
      const oldFirstName = row.getAttribute("data-firstname");
      const oldLastName = row.getAttribute("data-lastname");

      document.querySelector('input[name="old_username"]').setAttribute("data-oldusername", oldUsername);
      document.querySelector('input[name="old_password"]').setAttribute("data-oldpassword", oldPassword);
      document.querySelector('input[name="old_firstname"]').setAttribute("data-oldfirstname", oldFirstName);
      document.querySelector('input[name="old_lastname"]').setAttribute("data-oldlastname", oldLastName);

      document.getElementById("EditUserFirstName").value = oldFirstName;
      document.getElementById("EditUserLastName").value = oldLastName;
      document.getElementById("EditUserUsername").value = oldUsername;

      openModal(editUserForm, editUserBackdrop);
    });
  });

  if (cancelEditModalButton) {
    cancelEditModalButton.addEventListener("click", () => closeModal(editUserForm, editUserBackdrop));
  }

  if (addUserBackdrop) {
    addUserBackdrop.addEventListener("click", (event) => {
      if (event.target === addUserBackdrop) closeModal(addUserForm, addUserBackdrop);
    });
  }
  if (editUserBackdrop) {
    editUserBackdrop.addEventListener("click", (event) => {
      if (event.target === editUserBackdrop) closeModal(editUserForm, editUserBackdrop);
    });
  }

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
      closeModal(addUserForm, addUserBackdrop);
      closeModal(editUserForm, editUserBackdrop);
    }
  });
});

document.getElementById('editUserForm').addEventListener('submit', function(event) {
  event.preventDefault(); // Prevent default form submission

  // Disable the submit button to prevent double submission
  const submitButton = document.getElementById('submitEditUserButton');
  submitButton.disabled = true;

  // Gather form data
  const oldFirstName = document.querySelector('input[name="old_firstname"]').getAttribute('data-oldfirstname');
  const oldLastName = document.querySelector('input[name="old_lastname"]').getAttribute('data-oldlastname');
  const oldUsername = document.querySelector('input[name="old_username"]').getAttribute('data-oldusername');
  const oldPassword = document.querySelector('input[name="old_password"]').getAttribute("data-oldpassword"); 

  const newFirstName = document.getElementById('EditUserFirstName').value;
  const newLastName = document.getElementById('EditUserLastName').value;
  const newUsername = document.getElementById('EditUserUsername').value;
  const newPassword = document.getElementById('editUsePassword').value;

  const cameraAccess = Array.from(document.querySelectorAll('input[name="camera_access[]"]:checked')).map(input => input.value);
  const zoneAccess = Array.from(document.querySelectorAll('input[name="zone_access[]"]:checked')).map(input => input.value);
  const userAccess = Array.from(document.querySelectorAll('input[name="user_access[]"]:checked')).map(input => input.value);
  const accessToCamera = Array.from(document.querySelectorAll('input[name="access_to_cameras[]"]:checked')).map(input => input.value);
  const accessToZone = Array.from(document.querySelectorAll('input[name="access_to_zones[]"]:checked')).map(input => input.value);

  const data = {
    old_firstname: oldFirstName,
    firstname: newFirstName || oldFirstName,
    old_lastname: oldLastName,
    lastname: newLastName || oldLastName,
    old_username: oldUsername,
    new_username: newUsername || oldUsername,
    old_password: oldPassword,
    password: newPassword || null , 
    camera_access: cameraAccess,
    zone_access: zoneAccess,
    user_access: userAccess, 
    access_to_cameras : accessToCamera,
    access_to_zones :accessToZone
  };

  // Send PATCH request
  fetch('/users/edit', {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  })
    .then(response => response.json())
    .then(responseData => {
      if (responseData.success) {
        closeEditModal();
        console.log('User updated successfully!');
      } else {
        closeEditModal()
        console.log('Error updating user: ' + responseData.message);
      }
    })
    .catch(error => {
      console.error('Error:', error);
      console.log('An error occurred while updating the user.');
    })
    .finally(() => {      submitButton.disabled = false;
    });
});
document.getElementById('editUserForm').addEventListener('keydown', function(event) {
  if (event.key === 'Enter') {
    event.preventDefault(); 
  }
});

function closeEditModal() {
  document.getElementById('editUserModal').style.display = 'none';
  document.getElementById('editUserBackdrop').style.display = 'none';
}

document.getElementById('cancelEditModal').addEventListener('click', closeEditModal);



/// delete users 
function deleteUser(button) {
  const username = button.getAttribute('data-username'); 
  const url = `/users/delete-users/${username}`;

  fetch(url, {
      method: 'DELETE',
      headers: { 'Content-Type': 'application/json' }
  })
  .then(response => response.json()) 
  .then(data => {
      if (data.success) {
          button.closest('tr').remove();
          console.log(`User ${username} deleted successfully.`);
      } else {
          console.log(`Failed to delete user: ${data.message}`);
      }
  })
  .catch(error => console.error('Error:', error));
}
