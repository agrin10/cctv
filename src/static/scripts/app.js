// Check if themeSwitch exists before adding an event listener
const themeSwitch = document.querySelector('.fa-moon');
if (themeSwitch) {
  themeSwitch.addEventListener('click', () => {
    document.body.classList.toggle('theme-dark');

    if (document.body.className.includes('theme-dark')) {
      localStorage.setItem('theme', 'dark');
    } else {
      localStorage.setItem('theme', 'light');
    }
  });

  document.addEventListener('DOMContentLoaded', () => {
    let result = localStorage.getItem('theme');
    if (result === 'dark') {
      document.body.classList.add('theme-dark');
    }
  });
}

// Open the Modal
function openModal(src) {
  var modal = document.getElementById("imageModal");
  var modalImg = document.getElementById("modalImage");
  if (modal && modalImg) {
    modal.style.display = "block";
    modalImg.src = src;
  }
}

// Close the Modal
function closeModal() {
  var modal = document.getElementById("imageModal");
  if (modal) modal.style.display = "none";
}

// Popup date picking 
function showPopup() {
  document.getElementById('timePopup').classList.add('show');
}

// Close the popup modal
function closePopup() {
  document.getElementById('timePopup').classList.remove('show');
}

//user pop up 
function showUserPopup() {
  document.getElementById('edit-user-popup').classList.add('show')
}

// Close the popup users
function closeUserPopup() {
  document.getElementById('edit-user-popup').classList.remove('show');
}



// AI properties handling
const selectBox = document.getElementById('selectBox');
const select = document.getElementById('ai_properties');
const selectedItemsContainer = document.getElementById('selectedItems');

if (selectBox && select && selectedItemsContainer) {
  selectBox.addEventListener('click', function () {
    select.style.display = select.style.display === 'none' ? 'block' : 'none';
  });
  
  select.addEventListener('change', function () {
    const selectedOptions = Array.from(select.selectedOptions);
    selectedItemsContainer.innerHTML = ''; // Clear previous selections
    
    selectedOptions.forEach(option => {
      const item = document.createElement('div');
      item.className = 'selected-item';
      item.innerText = option.value;

      const removeIcon = document.createElement('span');
      removeIcon.className = 'remove-item';
      removeIcon.innerHTML = '&times;'; // Close icon
      removeIcon.onclick = function () {
        option.selected = false; // Unselect the option
        item.remove(); // Remove the item from the display
      };
      
      item.appendChild(removeIcon);
      selectedItemsContainer.appendChild(item);
    });
  });
}


// date picker 
function submitForm(event) {
  event.preventDefault(); // Prevent the default form submission
  
  // Get form values
  const ip = document.getElementById('ip').value;
  const name = document.getElementById('name').value;
  const startTime = document.getElementById('startTime').value;
  const endTime = document.getElementById('endTime').value;
  
  const startGregorian = jalaliToGregorian(startTime);
  const endGregorian = jalaliToGregorian(endTime);
  
  // Log or process the data
  console.log("ای پی دوربین:", ip);
  console.log("نام دوربین:", name);
  console.log("زمان شروع (میلادی):", startGregorian);
  console.log("زمان پایان (میلادی):", endGregorian);

  alert('اطلاعات با موفقیت ثبت شد!');
}

function jalaliToGregorian(jalaliDate) {
  const [datePart, timePart] = jalaliDate.split(" ");
  const [year, month, day] = datePart.split('/').map(Number);
  const [hours, minutes] = timePart.split(':').map(Number);
  
  // Convert Jalali date to Gregorian
  const gDate = moment.from([year, month - 1, day, hours, minutes], 'jalali').format('YYYY-MM-DD HH:mm');
  return gDate;
}


document.querySelectorAll('.delete-user-btn').forEach(button => {
  button.addEventListener('click', function() {
      const username = this.getAttribute('data-username');
      const confirmModal = document.getElementById('confirmModal');
      const confirmMessage = document.getElementById('confirmMessage');

      // Set the confirmation message
      confirmMessage.textContent = `Are you sure you want to delete ${username}?`;

      // Show the modal
      confirmModal.style.display = 'block';

      // Handle the confirm button
      document.getElementById('confirmYes').onclick = function() {
          console.log(`Attempting to delete user with username: ${username}`);
          const url = `/users/delete-users/${username}`;

          fetch(url, {
              method: 'DELETE'
          })
          .then(response => response.json())
          .then(data => {
              console.log('Delete response:', data);
              if (data.message) {
                  const row = button.closest('.info-value');
                  if (row) {
                      row.remove();
                  }
              } else if (data.error) {
                  alert(data.error);
              }
              // Close the modal
              confirmModal.style.display = 'none';
          })
          .catch(error => {
              console.error('Error:', error);
              confirmModal.style.display = 'none'; // Close modal on error
          });
      };

      // Handle the cancel button
      document.getElementById('confirmNo').onclick = function() {
          confirmModal.style.display = 'none'; // Close the modal
      };
  });
});

// Close the modal if the user clicks outside of it
window.onclick = function(event) {
  const confirmModal = document.getElementById('confirmModal');
  if (event.target === confirmModal) {
      confirmModal.style.display = 'none';
  }
};


document.querySelectorAll('.delete-user-btn').forEach(button => {
  button.addEventListener('click', function() {
      const username = this.getAttribute('data-username');
      const confirmModal = document.getElementById('confirmModal');
      const confirmMessage = document.getElementById('confirmMessage');

      confirmMessage.textContent = `Are you sure you want to delete ${username}?`;
      confirmModal.style.display = 'block';

      document.getElementById('confirmYes').onclick = function() {
          console.log(`Attempting to delete user with username: ${username}`);
          const url = `/users/delete-users/${username}`;

          fetch(url, {
              method: 'DELETE'
          })
          .then(response => response.json())
          .then(data => {
              console.log('Delete response:', data);
              if (data.message) {
                  const row = button.closest('.info-value');
                  if (row) {
                      row.remove();
                  }
              } else if (data.error) {
                  alert(data.error);
              }
              confirmModal.style.display = 'none';
          })
          .catch(error => {
              console.error('Error:', error);
              confirmModal.style.display = 'none';
          });
      };

      document.getElementById('confirmNo').onclick = function() {
          confirmModal.style.display = 'none';
      };
  });
});

// Event listener for the edit user buttons
function showUserPopup(username, email, password) {
  // Populate the form with the user's current data

  console.log(`Editing user: ${username}`); // Debug line

  document.getElementById('new_username').value = username;
  document.getElementById('new_email').value = email;
  document.getElementById('password').value = password; // Optional, depending on your security policy
  document.getElementById('edit-user-popup').classList.add('show'); // Show the popup
}

function closeUserPopup() {
  document.getElementById('edit-user-popup').classList.remove('show'); // Hide the popup
}

// Handle form submission
document.getElementById('editUserForm').addEventListener('submit', function(event) {
  event.preventDefault(); // Prevent the default form submission

  const newUsername = document.getElementById('new_username').value;
  const newEmail = document.getElementById('new_email').value;
  const currentPassword = document.getElementById('password').value;
  const newPassword = document.getElementById('new_password').value;

  const userData = {
      new_username: newUsername,
      new_email: newEmail,
      password: currentPassword,
      new_password: newPassword
  };

  const url = `/users/profile/${username}`; 

  fetch(url, {
      method: 'PUT',
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify(userData)
  })
  .then(response => response.json())
  .then(data => {
      console.log('Update response:', data);
      if (data.message) {
          alert('User updated successfully!');
          closeUserPopup(); 
      } else if (data.error) {
          alert(data.error);
      }
  })
  .catch(error => {
      console.error('Error:', error);
  });
});


/*drop down modiifction */
