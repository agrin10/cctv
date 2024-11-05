document.addEventListener("DOMContentLoaded", () => {
  const addUserBackdrop = document.getElementById("addUserBackdrop");
  const addUserForm = document.getElementById("AddUserForm");
  const addUserButton = document.getElementById("add-user-button");
  const cancelAddModalButton = document.getElementById("cancelAddModal");



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

  if (addUserBackdrop) {
    addUserBackdrop.addEventListener("click", (event) => {
      if (event.target === addUserBackdrop) closeModal(addUserForm, addUserBackdrop);
    });
  }

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
      closeModal(addUserForm, addUserBackdrop);
    }
  });      
});