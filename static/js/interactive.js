// Handles JavaScript interactions

document.addEventListener("DOMContentLoaded", function () {

  const form = document.querySelector("form");
  const titleInput = document.getElementById("title");
  const dueDateInput = document.getElementById("deadline");
  const errorMessage = document.getElementById("error-message");

  if (form) {
      form.addEventListener("submit", function (event) {

          let errors = [];

          // Title validation
          if (titleInput && titleInput.value.trim() === "") {
              errors.push("Title cannot be empty.");
          }

          //  date validation
          if (DateInput && dueDateInput.value) {
              const selectedDate = new Date(dueDateInput.value);
              const today = new Date();

              today.setHours(0, 0, 0, 0);

              if (selectedDate < today) {
                  errors.push("Due date cannot be in the past.");
              }
          }
          if (errors.length > 0) {
              event.preventDefault();

              if (errorMessage) {
                errorMessage.classList.remove("d-none");
                errorMessage.innerHTML = errors.join("<br>");
            }
          }
      });
  }


  const filter = document.getElementById("course-filter");

  if (filter) {
      filter.addEventListener("change", function () {
          const courseId = this.value;
          window.location = "?course=" + courseId;
      });
  }

});


function toggleComplete(id) {

  fetch(`/assignment/${id}/complete/`, {
      method: "POST",
      headers: {
          "X-CSRFToken": csrftoken
      }
  })
  .then(response => response.json())
  .then(data => {
      if (data.success) {
          location.reload();
      }
  })
  .catch(error => {
      console.error("Error:", error);
  });

}
document.addEventListener("DOMContentLoaded", function () {

  const form = document.querySelector("#assignment-form");

  if (form) {
      form.addEventListener("submit", function (e) {
          e.preventDefault(); 

          console.log("Form submitted via AJAX");

          const data = {
              title: document.querySelector("#title").value,
              course: document.querySelector("#course").value,
              dueDate: document.querySelector("#deadline").value
          };

          console.log("Data sent:", data);

          alert("Assignment saved successfully (simulated)");

          const tableBody = document.querySelector("#assignment-table-body");

if (tableBody) {
    const newRow = `
        <tr>
            <td>${data.title}</td>
            <td>${data.course}</td>
            <td>${data.dueDate}</td>
            <td><span class="badge bg-warning text-dark">Pending</span></td>
        </tr>
    `;

    tableBody.innerHTML += newRow;
}

form.reset();
      });
  }

});
document.addEventListener("DOMContentLoaded", function () {

  const buttons = document.querySelectorAll(".complete-btn");

  buttons.forEach(function(button){

      button.addEventListener("click", function(){

          const row = this.closest("tr");
          const badge = row.querySelector(".status-badge");
          if (badge.innerText === "Pending") {
              badge.innerText = "Completed";
              badge.classList.remove("bg-warning", "text-dark");
              badge.classList.add("bg-success");
          } else {
              badge.innerText = "Pending";
              badge.classList.remove("bg-success");
              badge.classList.add("bg-warning", "text-dark");
          }

      });

  });

});