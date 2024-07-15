function initMap() {
    var myLatLng = {lat: 44.9727, lng: -93.23540000000003};
    /* Create a map and place it on the div */
    var map = new google.maps.Map(document.getElementById('map'), {
            zoom: 14,
            center: myLatLng,
        });

    google.maps.event.addListener(map, 'click', function(event) {
        // Get the latitude and longitude of the clicked location
        var clickedLocation = event.latLng;

        // Call the geocode function to convert the coordinates to an address
        geocodeLatLng(clickedLocation, map);
    });
    initAutocomplete();
    
}  // end init map function definiton

function geocodeLatLng(location, map) {
    var geocoder = new google.maps.Geocoder;

    // Perform reverse geocoding
    geocoder.geocode({'location': location}, function(results, status) {
        if (status === 'OK') {
            if (results[0]) {
                // Set the value of the location input field to the address
                document.getElementById('location').value = results[0].formatted_address;
            } else {
                window.alert('No results found');
            }
        } else {
            window.alert('Geocoder failed due to: ' + status);
        }
    });
}

let autocomplete;
let address1Field;

function initAutocomplete() {
  address1Field = document.querySelector("#location");
  // Create the autocomplete object, restricting the search predictions to
  // addresses in the US and Canada.
  autocomplete = new google.maps.places.Autocomplete(address1Field, {
    componentRestrictions: { country: ["us", "ca"] },
    fields: ["address_components", "geometry"],
    types: ["address"],
  });
  address1Field.focus();
  // When the user selects an address from the drop-down, populate the
  // address fields in the form.
  autocomplete.addListener("place_changed", fillInAddress);
}

function fillInAddress() {
  // Get the place details from the autocomplete object.
  const place = autocomplete.getPlace();
  let address1 = "";
  let postcode = "";

  // Get each component of the address from the place details,
  // and then fill-in the corresponding field on the form.
  // place.address_components are google.maps.GeocoderAddressComponent objects
  // which are documented at http://goo.gle/3l5i5Mr
  for (const component of place.address_components) {
    // @ts-ignore remove once typings fixed
    const componentType = component.types[0];

    switch (componentType) {
      case "street_number": {
        address1 = `${component.long_name} ${address1}`;
        break;
      }

      case "route": {
        address1 += component.short_name;
        break;
      }

      case "postal_code": {
        postcode = `${component.long_name}${postcode}`;
        break;
      }

      case "postal_code_suffix": {
        postcode = `${postcode}-${component.long_name}`;
        break;
      }
      case "locality":
        document.querySelector("#locality").value = component.long_name;
        break;
      case "administrative_area_level_1": {
        document.querySelector("#state").value = component.short_name;
        break;
      }
      case "country":
        document.querySelector("#country").value = component.long_name;
        break;
    }
  }

  address1Field.value = address1;
  // After filling the form with address components from the Autocomplete
  // prediction, set cursor focus on the second address line to encourage
  // entry of subpremise information such as apartment, unit, or floor number.
}

window.initAutocomplete = initAutocomplete;