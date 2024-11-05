document.addEventListener("DOMContentLoaded", () => {
  const addUserBackdrop = document.getElementById("addUserBackdrop");
  const addUserForm = document.getElementById("AddUserForm");
  const addUserButton = document.getElementById("add-user-button");
  const cancelAddModalButton = document.getElementById("cancelAddModal");

    
  
  const editUserBackdrop = document.getElementById("editUserBackdrop");
  const editUserForm = document.getElementById("editUserForm");
  const editButtons = document.querySelectorAll(".edit-user-edit-btn");
  const cancelEditModalButton = document.getElementById("cancelEditModal");

  let currentUsername = ""; // Store the username of the row clicked for editing

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
      currentUsername = this.closest("tr").querySelector(".body-cell").textContent.trim();
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

  // Gather form data
  const oldUsername = document.querySelector('input[name="old_username"]').value;
  const oldPassword = document.querySelector('input[name="old_password"]').value;
  const newUsername = document.getElementById('EditUserUsername').value;
  const newPassword = document.getElementById('editUsePassword').value;
  const firstName = document.getElementById('EditUserFirstName').value;
  const lastName = document.getElementById('EditUserLastName').value;

  // Collect checked permissions for each category
  const cameraAccess = Array.from(document.querySelectorAll('input[name="camera_access[]"]:checked'))
                            .map(input => input.value);
  const zoneAccess = Array.from(document.querySelectorAll('input[name="zone_access[]"]:checked'))
                          .map(input => input.value);
  const userAccess = Array.from(document.querySelectorAll('input[name="user_access[]"]:checked'))
                          .map(input => input.value);

  console.log("Old Username:", document.querySelector('input[name="old_username"]').value);
  console.log("Old Password:", document.querySelector('input[name="old_password"]').value);
  console.log("New Username:", document.getElementById('EditUserUsername').value);
  console.log("New Password:", document.getElementById('editUsePassword').value);
  
  // Prepare data to send
  const data = {
      old_username: oldUsername,
      old_password: oldPassword,
      new_username: newUsername || oldUsername,  
      password: newPassword || oldPassword,      
      first_name: firstName,
      last_name: lastName,
      camera_access: cameraAccess,
      zone_access: zoneAccess,
      user_access: userAccess
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
  .then(data => {
      if (data.message) {
          alert('User updated successfully!');
          closeEditModal(); // Close modal if you have this function
      } else {
          alert('Error updating user: ' + data.message);
      }
  })
  .catch(error => {
      console.error('Error:', error);
      alert('An error occurred while updating the user.');
  });
});

// Close the modal
function closeEditModal() {
  document.getElementById('editUserModal').style.display = 'none';
  document.getElementById('editUserBackdrop').style.display = 'none';
}

// Event listener for cancel button
document.getElementById('cancelEditModal').addEventListener('click', closeEditModal);



/// delete users 
function deleteUser(button) {
  const username = button.getAttribute('data-username'); // Get the username from the button's data attribute
  const url = `/users/delete-users/${username}`; // Construct the URL for the DELETE request

  // Send DELETE request to the backend
  fetch(url, {
      method: 'DELETE',
      headers: { 'Content-Type': 'application/json' }
  })
  .then(response => response.json()) // Parse the JSON response
  .then(data => {
      if (data.success) {
          // If deletion is successful, remove the corresponding row from the table
          button.closest('tr').remove();
          console.log(`User ${username} deleted successfully.`);
      } else {
          console.log(`Failed to delete user: ${data.message}`);
      }
  })
  .catch(error => console.error('Error:', error)); // Handle any errors
}
