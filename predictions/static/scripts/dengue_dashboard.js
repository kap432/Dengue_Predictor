// Initialize map
var map = L.map('map').setView([19.0760, 72.8777], 10); // Default location to Mumbai

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

// Location coordinates
var locations = {
    'mulund': [19.17168, 72.956], // Coordinates for Mulund
};

// Function to update map location
function updateMap(location) {
    if (location && locations[location]) {
        map.setView(locations[location], 15); // Zoom level 15 for more detail
        L.circle(locations[location], {
            color: 'red',
            fillColor: '#f03',
            fillOpacity: 0.5,
            radius: 1000 // Radius of 100 meters
        }).addTo(map);
    } else {
        map.setView([19.0760, 72.8777], 10); // Default to Mumbai if no location is selected
    }
}

// Handle dropdown change
document.getElementById('location').addEventListener('change', function() {
    var selectedLocation = this.value;
    updateMap(selectedLocation);
});

// Initialize with default location
updateMap('');