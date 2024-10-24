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

// //user pop up 
// function showUserPopup() {
//   document.getElementById('edit-user-popup').style.display='block'
// }

// // Close the popup users
// function closeUserPopup() {
//   document.getElementById('edit-user-popup').style.display='none';
// }


// Function to show the user popup with existing user details
function showUserPopup(username, email, password) {
  // Populate the inputs with the existing user data
  document.getElementById('firstName').value = ""; // You may want to fetch these values based on your context
  document.getElementById('lastName').value = ""; // You may want to fetch these values based on your context
  document.getElementById('username').value = username;
  document.getElementById('password').value = password;

  // Show the popup
  const popup = document.getElementById('edit-user-popup');
  popup.classList.add('show');
}

// Hide the popup when cancel button is clicked
document.querySelector('.cancel-btn').addEventListener('click', function() {
  const popup = document.getElementById('edit-user-popup');
  popup.classList.remove('show');
});


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
    selectedItemsContainer.innerHTML = ''; 
    
    selectedOptions.forEach(option => {
      const item = document.createElement('div');
      item.className = 'selected-item';
      item.innerText = option.value;

      const removeIcon = document.createElement('span');
      removeIcon.className = 'remove-item';
      removeIcon.innerHTML = '&times;'; 
      removeIcon.onclick = function () {
        option.selected = false; 
        item.remove(); 
      };
      
      item.appendChild(removeIcon);
      selectedItemsContainer.appendChild(item);
    });
  });
}


// date picker 
function submitForm(event) {
  event.preventDefault(); 
  
  const ip = document.getElementById('ip').value;
  const name = document.getElementById('name').value;
  const startTime = document.getElementById('startTime').value;
  const endTime = document.getElementById('endTime').value;
  
  const startGregorian = jalaliToGregorian(startTime);
  const endGregorian = jalaliToGregorian(endTime);
  
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

window.onclick = function(event) {
  const confirmModal = document.getElementById('confirmModal');
  if (event.target === confirmModal) {
      confirmModal.style.display = 'none';
  }
};

let currentUsername = ''; 

function showUserPopup(username, email, password) {
    currentUsername = username; 
    console.log(`Editing user: ${username}`); 


    document.getElementById('new_username').value = username;
    document.getElementById('new_email').value = email;
    document.getElementById('password').value = password;
    document.getElementById('edit-user-popup').classList.add('show');
}

function closeUserPopup() {
    document.getElementById('edit-user-popup').classList.remove('show'); 
}

// Handle form submission
document.getElementById('editUserForm').addEventListener('submit', function(event) {
    event.preventDefault(); 

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

    const url = `/users/profile/${currentUsername}`; 

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


            const userInfoElement = document.querySelector(`.info-value:has(.single-value:contains(${currentUsername}))`);
            if (userInfoElement) {
                userInfoElement.querySelector('.single-value:nth-child(2) p').textContent = newUsername;
                userInfoElement.querySelector('.single-value:nth-child(3) p').textContent = newEmail;
            }

            closeUserPopup(); 
        } else if (data.error) {
            alert(data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
  

/*drop down modification */
 document.addEventListener("DOMContentLoaded", function() {
        const selectedOptions = document.getElementById('selectedOptions');
        const optionsContainer = document.getElementById('optionsContainer');

        selectedOptions.addEventListener('click', function() {
            optionsContainer.style.display = optionsContainer.style.display === 'block' ? 'none' : 'block';
        });

        optionsContainer.addEventListener('change', function(event) {
            if (event.target.tagName === 'INPUT' && event.target.type === 'checkbox') {
                updateSelectedOptions();
            }
        });

        function updateSelectedOptions() {
            const checkboxes = optionsContainer.querySelectorAll('input[type="checkbox"]');
            const selected = Array.from(checkboxes)
                .filter(checkbox => checkbox.checked)
                .map(checkbox => checkbox.parentElement.textContent.trim())
                .join(', ');

            selectedOptions.textContent = selected.length > 0 ? selected : 'Select options...';
        }

        document.addEventListener('click', function(event) {
            if (!event.target.closest('.custom-select')) {
                optionsContainer.style.display = 'none';
            }
        });
    });


    document.addEventListener("DOMContentLoaded", function() {
      const customSelects = document.querySelectorAll('.custom-select');
  
      customSelects.forEach(select => {
          const selectedOptions = select.querySelector('.selected-options');
          const optionsContainer = select.querySelector('.options-container');
  
          selectedOptions.addEventListener('click', function() {
              const isVisible = optionsContainer.style.display === 'block';
              optionsContainer.style.display = isVisible ? 'none' : 'block';
          });
  
          optionsContainer.addEventListener('change', function(event) {
              if (event.target.tagName === 'INPUT' && event.target.type === 'checkbox') {
                  updateSelectedOptions(select);
              }
          });
  
          function updateSelectedOptions(select) {
              const checkboxes = select.querySelectorAll('input[type="checkbox"]');
              const selected = Array.from(checkboxes)
                  .filter(checkbox => checkbox.checked)
                  .map(checkbox => checkbox.nextSibling.textContent.trim())
                  .join(', ');
  
              selectedOptions.textContent = selected.length > 0 ? selected : 'دسترسی ها...';
          }
  
          document.addEventListener('click', function(event) {
              if (!event.target.closest('.custom-select')) {
                  optionsContainer.style.display = 'none';
              }
          });
      });
  });
  


// cameras ************

    
