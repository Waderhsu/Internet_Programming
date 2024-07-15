var marker2;
var infowindow2;

function initMap() {
    var myLatLng = { lat: 44.9727, lng: -93.23540000000003 };
    /* Create a map and place it on the div */
    var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 14,
        center: myLatLng,
    });
    var geocoder = new google.maps.Geocoder(); // Create a geocoder object

    var centerlocation = "Coffman Memorial Union, 300 Southeast Washington Avenue, Minneapolis, MN 55455"; // This is the location we will search for using the geocoder
    /* For your Homework assignment 3, you will have to create the code to return * the location of the address and use it to put a marker with an infowindow 
    * on the map
    */

    var address = document.getElementsByClassName('address');
    var name = document.getElementsByClassName('name');
    var time = document.getElementsByClassName('time');
    var location = document.getElementsByClassName('location');
    var day = document.getElementsByClassName('day');
    for (i = 0; i < 12; i++) {
        markerAddress(geocoder, map, address[i].innerHTML, day[i].innerHTML, time[i].innerHTML,
            name[i].innerHTML, location[i].innerHTML);
    }
    geocodeAddress(geocoder, map, centerlocation);

}  // end init map function definiton

// This function takes a geocode object, a map object, and an address, and 
// if successful in finding the address, it places a marker with a callback that shows an 
// info window when the marker is "clicked"
function geocodeAddress(geocoder, resultsMap, address) {

    geocoder.geocode({ 'address': address }, function (results, status) {
        if (status === google.maps.GeocoderStatus.OK) {
            resultsMap.setCenter(results[0].geometry.location);
            marker2 = new google.maps.Marker({
                map: resultsMap,
                position: results[0].geometry.location,
                title: address,
            });
            infowindow2 = new google.maps.InfoWindow({
                content: address
            });

            google.maps.event.addListener(marker2, 'click', createWindow(resultsMap, infowindow2, marker2));
        } else {
            alert('Geocode was not successful for the following reason: ' + status);
        } //end if-then-else
    }); // end call to geocoder.geocode function
} // end geocodeAddress function

// This function displays custom markers
function markerAddress(geocoder, resultsMap, address, day, time, name, location) {

    geocoder.geocode({ 'address': address }, function (results, status) {
        if (status === google.maps.GeocoderStatus.OK) {
            const icon = {
                url: "../img/golden-gopher.png", // url
                scaledSize: new google.maps.Size(30, 30), // scaled size
                origin: new google.maps.Point(0, 0), // origin
                anchor: new google.maps.Point(0, 0) // anchor
            };
            marker2 = new google.maps.Marker({
                map: resultsMap,
                position: results[0].geometry.location,
                title: address,
                icon: icon,
            });
            infowindow2 = new google.maps.InfoWindow({
                content: name + '<br>' + day + ',' + time + '<br>' + location
            });

            google.maps.event.addListener(marker2, 'click', createWindow(resultsMap, infowindow2, marker2));
        } else {
            alert('Geocode was not successful for the following reason: ' + status);
        } //end if-then-else
    }); // end call to geocoder.geocode function
}

// Function to return an anonymous function that will be called when the rmarker created in the 
// geocodeAddress function is clicked	
function createWindow(rmap, rinfowindow, rmarker) {
    return function () {
        rinfowindow.open(rmap, rmarker);
    }
}//end create (info) window

// This function search the nearby location.
function searchNearby() {
    map = new google.maps.Map(document.getElementById('map'), {
        center: {
            lat: 44.9727,
            lng: -93.23540000000003
        },
        zoom: 14
    });
    var types = document.getElementById('searchPlace').value;;
    if (types == 'other') {
        // types = document.getElementById('otherPlace').value;
        var request = {
            location: map.getCenter(),
            radius: document.getElementById('radius').value,
            query: document.getElementById('otherPlace').value,
            // types: [document.getElementById('otherPlace').value],
        }
        var service = new google.maps.places.PlacesService(map);

        service.textSearch(request, callback);
    } else {
        // types = document.getElementById('searchPlace').value;
        var request = {
            location: map.getCenter(),
            radius: document.getElementById('radius').value,
            types: [types],
        }
        var service = new google.maps.places.PlacesService(map);

        service.nearbySearch(request, callback);
    }
}

// This function creates the the markers you searched 
function callback(results, status) {
    if (status == google.maps.places.PlacesServiceStatus.OK) {
        console.log(results.length);
        for (var i = 0; i < results.length; i++) {
            createMarker(results[i]);
        }
    }
}

function createMarker(place) {
    var placeLoc = place.geometry.location;
    var marker = new google.maps.Marker({
        map: map,
        position: place.geometry.location,
        title: place.name
    })
    var geocoder = new google.maps.Geocoder();
    var latlng = {
        lat: parseFloat(place.geometry.location.lat()),
        lng: parseFloat(place.geometry.location.lng()),
    }
    var add;
    geocoder.geocode({ location: latlng }).then((response) => {
        if (response.results[0]) {
            add = response.results[0].formatted_address;
            infowindow2 = new google.maps.InfoWindow({
                content: place.name + '<br>' + add,
            });

            google.maps.event.addListener(marker, 'click', createWindow(map, infowindow2, marker));
        }
    })
}
var map, directionsService, directionsRenderer;

function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition);
    } else {
        x.innerHTML = "Geolocation is not supported by this browser.";
    }
}

function showPosition(position) {
    x.innerHTML = "Latitude: " + position.coords.latitude +
        "<br>Longitude: " + position.coords.longitude;
}

// function searchRoute() {
function searchRoute() {
    const directionsRenderer = new google.maps.DirectionsRenderer();
    const directionsService = new google.maps.DirectionsService();
    const map = new google.maps.Map(document.getElementById("map"), {
        zoom: 14,
        center: { lat: 37.77, lng: -122.447 },
    });

    directionsRenderer.setMap(map);
    directionsRenderer.setPanel(document.getElementById("sidebar"));
    calculateAndDisplayRoute(directionsService, directionsRenderer);

    document.querySelector('input[name="travelMode"]:checked').addEventListener("change", () => {
        calculateAndDisplayRoute(directionsService, directionsRenderer);
    });
}
function calculateAndDisplayRoute(directionsService, directionsRenderer) {
    const selectedMode = document.querySelector('input[name="travelMode"]:checked').value;
    var geocoder = new google.maps.Geocoder();

    address = document.getElementById('Directionsplace').value;
    // alert(address);
    geocoder.geocode({ 'address': address }, function (results, status) {
        if (status == google.maps.GeocoderStatus.OK) {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(showPosition);
            } else {
                x.innerHTML = "Geolocation is not supported by this browser.";
            }
            function showPosition(position) {
                currentLat = position.coords.latitude;
                currentLng = position.coords.longitude;
                // alert(currentLat);
                // x.innerHTML = "Latitude: " + position.coords.latitude + 
                // "<br>Longitude: " + position.coords.longitude;
            }

            desLat = results[0].geometry.location.lat();
            desLng = results[0].geometry.location.lng();
            // alert(desLat);
            // alert(currentLat);
            // alert(desLat);
            directionsService
                .route({
                    origin: { lat: currentLat, lng: currentLng },
                    destination: { lat: desLat, lng: desLng },
                    // Note that Javascript allows us to access the constant
                    // using square brackets and a string value as its
                    // "property."
                    travelMode: google.maps.TravelMode[selectedMode],
                })
                .then((response) => {
                    directionsRenderer.setDirections(response);
                })
                .catch((e) => window.alert("Directions request failed due to " + status));
        }
    });
    // alert(selectedMode);

}