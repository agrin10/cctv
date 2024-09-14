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

// Popup form
function showPopup() {
  document.getElementById('timePopup').classList.add('show');
}

// Close the popup modal
function closePopup() {
  document.getElementById('timePopup').classList.remove('show');
}
// function showPopup() {
//   const timePopup = document.getElementById("timePopup");
//   if (timePopup) timePopup.style.display = "block";
// }

// function closePopup() {
//   const timePopup = document.getElementById("timePopup");
//   if (timePopup) timePopup.style.display = "none";
// }

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

