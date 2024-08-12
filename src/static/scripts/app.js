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


const videoPlayer = document.getElementById('videoPlayer');

document.getElementById('playButton').addEventListener('click', () => {
    videoPlayer.play();
});

document.getElementById('pauseButton').addEventListener('click', () => {
    videoPlayer.pause();
});

document.getElementById('resumeButton').addEventListener('click', () => {
    videoPlayer.play();
});

// Add functionality for Previous and Next buttons
document.getElementById('prevButton').addEventListener('click', () => {
    // Logic to go to the previous video
    alert('Previous video functionality not implemented.');
});

document.getElementById('nextButton').addEventListener('click', () => {
    // Logic to go to the next video
    alert('Next video functionality not implemented.');
});
