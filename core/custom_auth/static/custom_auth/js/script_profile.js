document.addEventListener("DOMContentLoaded", function () {
    const toggleButton = document.getElementById("toggle-fields");
    const additionalFields = document.getElementById("additional-fields");

    toggleButton.addEventListener("click", function () {
        if (additionalFields.style.display === "none") {
            additionalFields.style.display = "block";
            toggleButton.textContent = "Hide additional fields";
        } else {
            additionalFields.style.display = "none";
            toggleButton.textContent = "Add more information";
        }
    });
});