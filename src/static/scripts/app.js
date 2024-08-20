"use strict";

// side menu 

const dashboardBtn = document.querySelector(".dashboard-moblie");
const dashboard = document.querySelector(".dashboard");
const xBtn=document.querySelector('.icon-x')
const backdrop=document.querySelector('.backdrop')

dashboardBtn.addEventListener("click",showDashboard);
xBtn.addEventListener("click",showDashboard);
backdrop.addEventListener('click',showDashboard)

function showDashboard() {
  dashboardBtn.classList.toggle("menu-active");
  dashboard.classList.toggle("show-menu");
  backdrop.classList.toggle('hidden')
}

// theme
// locatStorage

const themeSwitch=document.querySelector('.bxs-moon')
themeSwitch.addEventListener('click',()=>{
  document.body.classList.toggle('theme-dark')

  if (document.body.className.includes('theme-dark')) {
    localStorage.setItem('theme', 'dark')
  } else {
    localStorage.setItem('theme', 'light')
  }
})


document.addEventListener('DOMContentLoaded', () => {
  let result = localStorage.getItem('theme')  
  if (result === 'dark') {
    document.body.classList.add('theme-dark')
  }
})