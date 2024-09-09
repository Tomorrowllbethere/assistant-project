// Function to start a countdown for a given element
function startCountdown(countdownElement, seconds) {
    var interval = setInterval(function() {
        if (seconds > 0) {
            var days = Math.floor(seconds / (3600 * 24));
            var hours = Math.floor((seconds % (3600 * 24)) / 3600);
            var minutes = Math.floor((seconds % 3600) / 60);
            var remainingSeconds = seconds % 60;

            // Format the time as days:hours:minutes:seconds
            countdownElement.innerHTML = days + " days " + hours + " : " + minutes + " : " + remainingSeconds;

            seconds--;  // Decrement the seconds
        } else {
            clearInterval(interval);
            countdownElement.innerHTML = "Time's up!";
        }
    }, 1000);  // Update every second
}

document.addEventListener('DOMContentLoaded', function() {
    // Select all countdown elements by class name
    var countdownElements = document.querySelectorAll(".countdown");
    
    countdownElements.forEach(function(countdownElement) {
        // Get the remaining seconds from the data attribute
        var remainingSeconds = parseInt(countdownElement.getAttribute("data-remaining-seconds"));
        // Start the countdown for this element
        startCountdown(countdownElement, remainingSeconds);
    });
});