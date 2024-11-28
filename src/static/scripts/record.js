document.addEventListener("DOMContentLoaded", function () {
  // Select the elements
  const closeModalBtn = document.getElementById("closeModalBtn");
  const calendarModal = document.getElementById("calendarModal");
  const backdropModal = document.getElementById("recordBackdrop");

  // Add click event listener to the cancel button
  closeModalBtn.addEventListener("click", function () {
    // Hide the modal and backdrop
    calendarModal.style.display = "none";
    backdropModal.style.display = "none";
  });
});




document.addEventListener("DOMContentLoaded", function () {
  const openCalendarButton1 = document.getElementById("openCalendarButton1");
  const openCalendarButton2 = document.getElementById("openCalendarButton2");
  const calendarPopUp = document.getElementById("calendarPopUp");
  const startDateDisplay = document.getElementById("startDate");
  const endDateDisplay = document.getElementById("endDate");
  const confirmDateBtn = document.getElementById("calendarSubmitBtn");
  let currentTarget = null; 

 
  function openCalendar(event) {
    
    currentTarget = event.target.id === "openCalendarButton1" ? "start" : "end";
    
    const rect = event.target.getBoundingClientRect();
    calendarPopUp.style.top = `${rect.bottom + -230}px`; 
    calendarPopUp.style.left = `${rect.left - +330}px`; 
    calendarPopUp.style.display = "block";
  }
  


  function confirmDate() {
    const selectedDate = document.getElementById("q-app").__vue__.date;
    if (currentTarget === "start") {
      startDateDisplay.textContent = selectedDate;
    } else if (currentTarget === "end") {
      endDateDisplay.textContent = selectedDate;
    }
    calendarPopUp.style.display = "none"; 
  }

  openCalendarButton1.addEventListener("click", openCalendar);
  openCalendarButton2.addEventListener("click", openCalendar);
  confirmDateBtn.addEventListener("click", confirmDate);

  let isSubmitting = false;

function submitDateData() {
  if (isSubmitting) return; // Prevent multiple submissions
  isSubmitting = true;

  const selectedDateStart = startDateDisplay.textContent;
  const selectedDateEnd = endDateDisplay.textContent;
  const startTime = document.getElementById("startTime").value;
  const endTime = document.getElementById("endTime").value;

  const data = {
    start_date: selectedDateStart,
    start_time: startTime,
    end_date: selectedDateEnd,
    end_time: endTime,
  };

  // Show loading indicator (e.g., a spinner or text)
  document.querySelector(".record-save-btn").textContent = "در حال ذخیره...";

  fetch("/camera/records", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  })
    .then((response) => response.json())
    .then((result) => {
      console.log("Data sent successfully:", result);
    })
    .catch((error) => {
      console.error("Error sending data:", error);
    })
    .finally(() => {
      isSubmitting = false;
      document.querySelector(".record-save-btn").textContent = "ذخیره شد";
    });
}


  document.querySelector(".record-save-btn").addEventListener("click", submitDateData);
});
