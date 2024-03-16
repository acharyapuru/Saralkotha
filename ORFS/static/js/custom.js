//review form togg
document.addEventListener('DOMContentLoaded', function() {
    var reviewFormContainer = document.getElementById('review-form-container');
    var toggleReviewFormBtn = document.getElementById('toggle-review-form-btn');

    toggleReviewFormBtn.addEventListener('click', function() {
        if (reviewFormContainer.style.display === 'none') {
            reviewFormContainer.style.display = 'block';
        } else {
            reviewFormContainer.style.display = 'none';
        }
    });
});

//review toggle
document.addEventListener('DOMContentLoaded', function() {
    var toggleReviewsBtn = document.getElementById('toggle-reviews-btn');
    var reviewsSection = document.getElementById('reviews-section');

    toggleReviewsBtn.addEventListener('click', function() {
        if (reviewsSection.style.display === 'none') {
            reviewsSection.style.display = 'block';
        } else {
            reviewsSection.style.display = 'none';
        }
    });
});

//auto calculate lat long
document.addEventListener('DOMContentLoaded', function() {
    const autoFillLocationBtn = document.getElementById('auto-fill-location');
    const latField = document.getElementById('id_latitude');
    const lonField = document.getElementById('id_longitude');

    autoFillLocationBtn.addEventListener('click', function() {
        // Check if Geolocation is supported by the browser
        if (navigator.geolocation) {
            // Get current position
            navigator.geolocation.getCurrentPosition(function(position) {
                const latitude = position.coords.latitude;
                const longitude = position.coords.longitude;

                // Set latitude and longitude in the location field
                latField.value = latitude;
                lonField.value = longitude
                // locationField.value = `${latitude}, ${longitude}`;
            }, function(error) {
                console.error('Error getting current position:', error);
                alert('Error getting current position. Please try again.');
            });
        } else {
            alert('Geolocation is not supported by your browser.');
        }
    });
});




function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

//find nearby function
document.querySelector('.findbtn').addEventListener('click', function(event) {
    event.preventDefault(); // Prevent default form submission behavior
  
    navigator.geolocation.getCurrentPosition(function(position) {
      const latitude = position.coords.latitude;
      const longitude = position.coords.longitude;
  
      // Send the latitude and longitude to the backend (explained next section)
      sendLocationData(latitude, longitude);
    }, function(error) {
      console.error("Error getting location:", error);
      // Handle location access error (optional: display a message to the user)
    });
  });
  
  function sendLocationData(latitude, longitude) {

    const csrftoken = getCookie('csrftoken'); 
    // Use AJAX, Fetch API, or a suitable method to send data to the backend view
    // Example using Fetch API (replace with your preferred method)
    fetch('http://127.0.0.1:8000/findnearby/',  // Replace with your actual view URL
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken
      },
      body: JSON.stringify({
        latitude: latitude,
        longitude: longitude
      })
    })
    .then(response => response.json())
    .then(data => {
      // Handle the response from the backend (optional: update the UI)
      console.log("Data from backend:", data);
    })
    .catch(error => {
      console.error("Error sending location data:", error);
      // Handle errors during data transmission (optional)
    });
  }