

document.addEventListener('DOMContentLoaded', function () {
    const dateField = document.getElementById('id_date');  // Adjust the ID based on your form
    const timeField = document.getElementById('id_time');  // Adjust the ID based on your form

    dateField.addEventListener('change', function () {
        const selectedDate = dateField.value;

        // Data to be sent in the POST request
        const postData = {
            selected_date: selectedDate,
            // Add other data if needed
        };

        const csrfToken = document.cookie.split('; ')
            .find(row => row.startsWith('csrftoken='))
            .split('=')[1];

        // Make a POST request to the Django view
        fetch('/api/available_times/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify(postData),
        })
        .then(response => response.json())
        .then(data => {
    if (data.available_times) {
        // Update the time field options based on the response
        timeField.innerHTML = data.available_times.map(time => `<option value="${time}">${time}</option>`).join('');
    } else {
        console.error('Available times data is undefined or null.');
    }
})
        .catch(error => console.error('Error fetching available times:', error));
    });
});


        function showBookingForm() {
    var bookingForm = document.getElementById("booking-form");

    if (bookingForm.style.display === "none" || bookingForm.style.display === "") {
        bookingForm.style.display = "block";
    } else {
        bookingForm.style.display = "none";
    }
}
