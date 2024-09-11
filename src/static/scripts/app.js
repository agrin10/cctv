"use strict";

// side menu 
const dashboardBtn = document.querySelector(".dashboard-moblie");
const dashboard = document.querySelector(".dashboard");
const xBtn = document.querySelector('.icon-x');
const backdrop = document.querySelector('.backdrop');
const mainStyle = document.querySelector('.main-style');

// dashboardBtn.addEventListener("click", showDashboard);
// xBtn.addEventListener("click", showDashboard);
// backdrop.addEventListener('click', showDashboard);

// function showDashboard() {
//   dashboardBtn.classList.toggle("menu-active");
//   dashboard.classList.toggle("show-menu");
//   backdrop.classList.toggle('hidden');
//   mainStyle.classList.toggle('show-menu');


  // theme
  // locatStorage

  const themeSwitch = document.querySelector('.fa-moon');
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
// Open the Modal
function openModal(src) {
  var modal = document.getElementById("imageModal");
  var modalImg = document.getElementById("modalImage");
  modal.style.display = "block";
  modalImg.src = src;
}

// Close the Modal
function closeModal() {
  var modal = document.getElementById("imageModal");
  modal.style.display = "none";
}

// pop up form 

function showPopup(){
  document.getElementById("timePopup").style.display = "block";

}
function closePopup(){
  document.getElementById("timePopup").style.display = "none";
}


//ai properties


const selectBox = document.getElementById('selectBox');
const select = document.getElementById('ai_properties');
const selectedItemsContainer = document.getElementById('selectedItems');

selectBox.addEventListener('click', function() {
    select.style.display = select.style.display === 'none' ? 'block' : 'none';
});

select.addEventListener('change', function() {
    const selectedOptions = Array.from(select.selectedOptions);
    selectedItemsContainer.innerHTML = ''; // Clear previous selections

    selectedOptions.forEach(option => {
        const item = document.createElement('div');
        item.className = 'selected-item';
        item.innerText = option.value;

        const removeIcon = document.createElement('span');
        removeIcon.className = 'remove-item';
        removeIcon.innerHTML = '&times;'; // Close icon
        removeIcon.onclick = function() {
            option.selected = false; // Unselect the option
            item.remove(); // Remove the item from the display
        };

        item.appendChild(removeIcon);
        selectedItemsContainer.appendChild(item);
    });
});