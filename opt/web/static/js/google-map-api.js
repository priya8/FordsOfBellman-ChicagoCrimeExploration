var map;

function initMap() {
    map = new google.maps.Map(
        document.getElementById("map"),
        {
            center: {lat: 41.881832, lng: -87.623177},
            zoom: 11
        }
    );
}

// initialize array of markers that will be used to clear markers from the map
var crimeMarkers = [];
//function that adds marker to the map where the crime was commited, takes longitude, latitude
function addMarker(lat,lng){
    //this will hold the path to the icon image
    var markerIcon = null;

    marker = new google.maps.Marker({
            position: new google.maps.LatLng(lat,lng),
            map: map,
            icon: markerIcon
         
        }
    );
    crimeMarkers.push(marker);
    //sets the zoom to the location that the map is
    map.setZoom(20);
    map.panTo(marker.position);
}

// Removes the markers from the map,
function clearOverlays() {
  for (var i = 0; i < crimeMarkers.length; i++ ) {
    crimeMarkers[i].setMap(null);
  }
  crimeMarkers.length = 0;

}

// Add info windows to each marker for crime info
function addCrimeInfo(number, marker, date, address, description, crimeType){
    //adding info
    
    var crimeInfo = "<p> #" + number + "</p><p> Description: " + crimeType 
    + " " + description + "</p> <p> Block: " + address + "</p><p> Date: " + date + "</p>";
    	var infowindow = new google.maps.InfoWindow({
        content: crimeInfo
    });
    
    
  //  window.alert(date);
    
    //added mouseover to see the info window
    marker.addListener("mouseover", function(){
        
        	infowindow.open(map, marker);
       // 	marker.setIcon('http://maps.google.com/mapfiles/ms/icons/blue-dot.png');
        
        
    });
    marker.addListener("mouseout", function() {
    infowindow.close(map, marker);
    marker.setIcon(null);
});
}

