// Scene Setup
const scene = new THREE.Scene();

// Camera Setup
const camera = new THREE.PerspectiveCamera(
    1000, // FOV for wider view
    window.innerWidth / window.innerHeight,
    0.1,
    2000
);
camera.position.set(500, 500, 500); // Positioned further back

// Renderer Setup
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

//--------------------------------- OrbitControls with Zoom Limits----------------------------------------------------------
const controls = new THREE.OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.1;
controls.enableZoom = true;
controls.minDistance = 100;  // Increased minimum zoom distance
controls.maxDistance = 1000; // Increased maximum zoom distance

// Lighting Setup
const ambientLight = new THREE.AmbientLight(0x555555);
scene.add(ambientLight);

const pointLight = new THREE.PointLight(0xffffff, 2);
pointLight.position.set(100, 100, 100);
scene.add(pointLight);

// Texture Loader for Planets and Background
const textureLoader = new THREE.TextureLoader();

//--------------------------------------------- Background Galaxy Sphere--------------------------------------------------------
const backgroundTexture = textureLoader.load('galaxy/8k_stars_milky_way.jpg'); // Replace with your galaxy texture path
const backgroundGeometry = new THREE.SphereGeometry(1000, 64, 64); // Large sphere to cover the scene
const backgroundMaterial = new THREE.MeshBasicMaterial({
    map: backgroundTexture,
    side: THREE.BackSide 
});

const backgroundSphere = new THREE.Mesh(backgroundGeometry, backgroundMaterial);
scene.add(backgroundSphere); 

//------------------------------------------------------- Planets Data (Updated for All Planets)------------------------------------------
const planets = [];
const planetData = [
    { name: 'Mercury', size: 2, distance: 20, texture: 'galaxy/8k_mercury.jpg' },
    { name: 'Venus', size: 3, distance: 30, texture: 'galaxy/8k_venus_surface.jpg' },
    { name: 'Earth', size: 3, distance: 40, texture: 'galaxy/8k_earth_daymap.jpg', cloudTexture: 'clouds.jpg' },
    { name: 'Mars', size: 2.5, distance: 50, texture: 'galaxy/8k_mars.jpg' },
    { name: 'Jupiter', size: 5, distance: 70, texture: 'galaxy/8k_jupiter.jpg' },
//saturn 
    { name: 'Uranus', size: 4, distance: 140, texture: 'galaxy/2k_uranus.jpg' },
    { name: 'Neptune', size: 4, distance: 160, texture: 'galaxy/2k_neptune.jpg' },
    { name: 'Pluto', size: 1.5, distance: 180, texture: 'galaxy/plutomap1k.jpg' }
];

// Create Planets and Clouds
planetData.forEach(data => {
    // Planet Geometry and Material
    const planetGeometry = new THREE.SphereGeometry(data.size, 64, 64);
    const planetMaterial = new THREE.MeshStandardMaterial({
        map: textureLoader.load(data.texture)
    });
    const planet = new THREE.Mesh(planetGeometry, planetMaterial);
    planet.position.set(data.distance, 0, 0);
    scene.add(planet);

 
    if (data.cloudTexture) {
        const cloudGeometry = new THREE.SphereGeometry(data.size + 0.2, 64, 64); // Slightly larger than the planet for better visibility
        const cloudMaterial = new THREE.MeshStandardMaterial({
            map: textureLoader.load(data.cloudTexture),
            transparent: true,
            opacity: 0.8, 
            blending: THREE.AdditiveBlending,
            depthWrite: false 
        });
        const clouds = new THREE.Mesh(cloudGeometry, cloudMaterial);
        planet.add(clouds); 
    }

    planets.push({ planet: planet, clouds: data.cloudTexture ? true : false, distance: data.distance });
});

//-------------------------------------------------- Star Particles ----------------------------------------------------------------//

const starGeometry = new THREE.SphereGeometry(0.5, 8, 8); 
const starMaterial = new THREE.MeshBasicMaterial({
    color: 0xffffff,
    emissive: 0xffffff,
    emissiveIntensity: 0.5,
    transparent: true,
    opacity: 0.9
});

const starField = new THREE.Group();
const starCount = 50000; 
const galaxyRadius = 500; 

// Create multiple stars
for (let i = 0; i < starCount; i++) {
    const star = new THREE.Mesh(starGeometry, starMaterial);
    const phi = Math.acos(2 * Math.random() - 1);
    const theta = Math.random() * 2 * Math.PI;
    const r = galaxyRadius * Math.cbrt(Math.random());

    star.position.set(
        r * Math.sin(phi) * Math.cos(theta),
        r * Math.sin(phi) * Math.sin(theta),
        r * Math.cos(phi)
    );

    starField.add(star); 
}

scene.add(starField); 

//-------------------------------------------- Sun with Glowing Effect and Texture-------------------------------------------------------

const sunGeometry = new THREE.SphereGeometry(10, 32, 32);
const sunTexture = textureLoader.load('galaxy/8k_sun.jpg'); // 
const sunMaterial = new THREE.MeshBasicMaterial({
    map: sunTexture, 
    emissive: 0xffcc00, // Glowing effect (yellowish)
    emissiveIntensity: 1.5 // Intensity of the glow
});
const sun = new THREE.Mesh(sunGeometry, sunMaterial);
scene.add(sun);

//------------------------------------------------------ Nebula Clouds (Cosmic Gas Clouds)---------------------------------------

const nebulaGeometry = new THREE.SphereGeometry(490, 64, 64);
const nebulaMaterial = new THREE.MeshBasicMaterial({
    map: textureLoader.load('galaxy/nebula.jpg'), 
    side: THREE.BackSide,
    transparent: true,
    opacity: 0.2 
});
const nebula = new THREE.Mesh(nebulaGeometry, nebulaMaterial);
scene.add(nebula);

//--------------------------------------------------------------- Saturn and Ring-----------------------------------------------------------//

const saturn = new THREE.Mesh(
    new THREE.SphereGeometry(5.5, 64, 64), 
    new THREE.MeshStandardMaterial({
        map: textureLoader.load('galaxy/8k_saturn.jpg')
    })
);
saturn.position.set(120, 0, 0); // Position Saturn
scene.add(saturn);

//  Ring to Saturn
const ringGeometry = new THREE.RingGeometry(6.5, 8.5, 64); // radius
const ringMaterial = new THREE.MeshBasicMaterial({
    map: textureLoader.load('galaxy/ring.png'), 
    side: THREE.DoubleSide,
    transparent: true,
    opacity: 0.8
});
const ring = new THREE.Mesh(ringGeometry, ringMaterial);
ring.rotation.x = Math.PI / 2; // Align the ring horizontally
saturn.add(ring); // Attach the ring to Saturn

planets.push({ planet: saturn, clouds: false, distance: 120 }); // Add Saturn to the planets array

//----------------------------- Earth's Moon-----------------------------------------------------

const moonGeometry = new THREE.SphereGeometry(5, 32, 32); // Moon size
const moonTexture = textureLoader.load('galaxy/moon.jpg');
const moonMaterial = new THREE.MeshStandardMaterial({
    map: moonTexture
});
const moon = new THREE.Mesh(moonGeometry, moonMaterial);
scene.add(moon);

//------------------------------------------ Black Hole (Positioned Between Planets)--------------------------------------------

//will be added in future update

//------------------------------------------------------------ Animation Loop----------------------------------------------------
function animate() {
    requestAnimationFrame(animate);

//--------------------------------------------- Update star movement for slight motion effect-------------------------------------
    starField.children.forEach(star => {
        star.position.x += Math.random() * 0.01 - 0.0000005; //  random horizontal movement
        star.position.y += Math.random() * 0.01 - 0.0000005; //  random vertical movement
        star.position.z += Math.random() * 0.01 - 0.0000005; //  random depth movement
    });

// Rotate planets on their axis
    planets.forEach(planet => {
        if (planet.planet.children[0]) {
            planet.planet.children[0].rotation.y += 0.01; // Rotate clouds
        }
        planet.planet.rotation.y += 0.01; // Rotate planet itself
    });

// Move planets in their orbits
    const time = Date.now() * 0.001; // Time multiplier for movement
    planets.forEach((planet, index) => {
        const distance = planet.distance;
        const orbitSpeed = 1 / (index + 1); // Planet closer to the sun moves faster, farther planets move slower
        planet.planet.position.x = Math.cos(time * orbitSpeed) * distance;
        planet.planet.position.z = Math.sin(time * orbitSpeed) * distance;
    });   

      
    
    controls.update(); // Update controls
    renderer.render(scene, camera); // Render the scene
}
animate();

// Resize Handling
window.addEventListener('resize', () => {
    renderer.setSize(window.innerWidth, window.innerHeight);
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
});
