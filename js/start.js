// Initial camera position
camera.position.set(0, 50, 150);

// Function to animate the camera position smoothly
function animateZoomOut() {
    const targetPosition = new THREE.Vector3(600, 600, 600); // Target position
    const duration = 10; // Duration in seconds for the zoom effect
    const startPosition = camera.position.clone(); // Starting position
    const startTime = performance.now(); // Track start time for interpolation

    function zoomAnimation() {
        const elapsed = (performance.now() - startTime) / 1000; // Time elapsed in seconds
        const progress = Math.min(elapsed / duration, 1); // Calculate the progress of animation

        // Interpolate between the starting position and target position
        camera.position.lerpVectors(startPosition, targetPosition, progress);

        // If animation is not yet finished, request next frame
        if (progress < 1) {
            requestAnimationFrame(zoomAnimation);
        }
    }

    zoomAnimation(); // Start the animation
}

// Set timeout to trigger the zoom after 10 seconds
setTimeout(animateZoomOut, 2000); // 10 seconds delay