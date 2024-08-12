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

const video = document.getElementById('video');
const playPauseBtn = document.getElementById('play-pause-btn');
const stopBtn = document.getElementById('stop-btn');
const prevBtn = document.getElementById('prev-btn');
const nextBtn = document.getElementById('next-btn');
const volumeControl = document.getElementById('volume');
const progressBar = document.getElementById('progress');

// let videoList = ['assets/videos/sample-video.mp4', 'assets/videos/another-video.mp4']; // Add your video paths
let currentIndex = 0;

playPauseBtn.onclick = function () {
    if (video.paused) {
        video.play();
        playPauseBtn.innerText = 'Pause';
    } else {
        video.pause();
        playPauseBtn.innerText = 'Play';
    }
};

stopBtn.onclick = function () {
    video.pause();
    video.currentTime = 0;
    playPauseBtn.innerText = 'Play';
};

nextBtn.onclick = function () {
    currentIndex = (currentIndex + 1) % videoList.length;
    video.src = videoList[currentIndex];
    video.play();
    playPauseBtn.innerText = 'Pause';
};

prevBtn.onclick = function () {
    currentIndex = (currentIndex - 1 + videoList.length) % videoList.length;
    video.src = videoList[currentIndex];
    video.play();
    playPauseBtn.innerText = 'Pause';
};

volumeControl.oninput = function () {
    video.volume = this.value;
};

// Update progress bar as video plays
video.ontimeupdate = function () {
    progressBar.value = (video.currentTime / video.duration) * 100; // Update progress bar
};

// Seek video when progress bar is changed
progressBar.oninput = function () {
    video.currentTime = (progressBar.value / 100) * video.duration; // Seek to new position
};

// Handle video end
video.onended = function () {
    currentIndex = (currentIndex + 1) % videoList.length;
    video.src = videoList[currentIndex];
    video.play();
    playPauseBtn.innerText = 'Pause';
};