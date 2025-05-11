// Select the header element
const header = document.getElementById('header');

// Set the threshold for zoom level or distance when the header should appear
const zoomThreshold = 10; // Adjust based on your desired zoom level

// Use a timer or observer to check the camera's zoom level at regular intervals
setInterval(() => {
    // Assuming `camera` is globally accessible (initialized in galaxy.js)
    if (typeof camera !== 'undefined') {
        // Check the camera's position or zoom level
        if (camera.position.z > zoomThreshold) {
            header.style.opacity = '1';
            header.style.display = 'block';
        } else {
            header.style.opacity = '0';
            header.style.display = 'none';
        }
    }
}, 100); // Check every 100ms or adjust as needed
