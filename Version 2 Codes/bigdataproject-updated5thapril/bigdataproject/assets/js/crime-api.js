// Radomizes team member list order
var ul = document.querySelector("#random");
for (var i = ul.children.length; i >= 0; i--) {
    ul.appendChild(ul.children[Math.random() * i | 0]);
}

$(document).ready(function(){
    // the "href" attribute of the modal trigger must specify the modal ID that wants to be triggered
    $("#modal-results").modal();
    $("#modal-previous").modal();

    // Initialize Firebase
    var config = {
      apiKey: "AIzaSyDz4cNlkfWQVwV4sJBXgIOtITjeKexIjy0",
      authDomain: "isitsafe-4ce15.firebaseapp.com",
      databaseURL: "https://isitsafe-4ce15.firebaseio.com",
      projectId: "isitsafe-4ce15",
      storageBucket: "isitsafe-4ce15.appspot.com",
      messagingSenderId: "366399254426"
    };
    firebase.initializeApp(config);

    var dataRef = firebase.database();

    //initialize address
    var address;

    //latitude and longitude
    var latitude;
    var longitude;

    // add scrolling to anchors
    $(".animate").on("click", function(event) {
        //getting the address from the input box
        address = $("#location").val();
        // Code for the push
        dataRef.ref().push({
            address: address,
            dateAdded: firebase.database.ServerValue.TIMESTAMP
        });

        $("#address-list").empty();
        queryFirebase();

        // Make sure this.hash has a value before overriding default behavior
        if (this.hash !== "") {
            // Prevent default anchor click behavior
            event.preventDefault();
            var hash = this.hash;

            // Using jQuery"s animate() method to add smooth page scroll
            // The optional number (800) specifies the number of milliseconds it takes to scroll to the specified area
            $("html, body").animate({
            scrollTop: $(hash).offset().top
            }, 500, function(){

            // Add hash (#) to URL when done scrolling (default click behavior)
            //window.location.hash = hash;
            });
        }
    });

    //queryFirebase
    function queryFirebase() {

        var query = dataRef.ref().orderByChild("dateAdded").limitToLast(3);
        query.on("child_added", function(snapshot){
            var address = snapshot.val();
            $("#address-list").append("<a href='#!' class='collection-item'>" + snapshot.val().address + "</a>");
        });
    }

    queryFirebase();


    //initiallize geocoder
    var geocoder = new google.maps.Geocoder();
            $("#location").keypress(function(e){
            if(e.which == 13){//Enter key pressed
                $("#submit-input").click();//Trigger search button click event
            }
        });

    // grabs user input from location search
    $("#submit-input").click(function() {

        //clear the markers on map before getting new data
        clearOverlays();

        //getting the address from the input box
        var address = $("#location").val();

        // converts user submitted address to longitude and latitude coordinates
        geocoder.geocode( { "address": address}, function(results, status) {

            if (status == google.maps.GeocoderStatus.OK) {
                latitude = results[0].geometry.location.lat();
                longitude = results[0].geometry.location.lng();
            }

            var queryURL = "https://data.cityofchicago.org/resource/6zsd-86xi.json?$where=within_circle(location," + latitude + ", " + longitude + ", 50)";

               // Performing an AJAX request with the queryURL
            $.ajax({
                url: queryURL,
                type: "GET",
                data: {
                    "$limit" : 5000,
                    "$$app_token" : "pyfrFl35spogEJeGI7iTphR2y"
                }
            })
			// After data comes back from the request
            .done(function(response) {

                // storing the data from the AJAX request in the results variable
                var results = response;

                //clears the table for the new input
                $("#results-table").empty();

                //adding the markers for each crime to the map
                for(var i = 0; i < results.length; i++){
                    //get latitude and longitude from data
                    var a=((moment(results[i].date).format("MMMM Do YYYY, h:mm:ss a")).split(" ")[2])
                    if(a>="2012" && a<="2017"){
                    latitude = results[i].latitude;
                    longitude = results[i].longitude;
                    //use addMarker function from the google-map-api js file
                    }
                    //adding markers
                    addMarker(latitude, longitude);

                    //getting the data from the returned json object
                    var block = results[i].block;
                    var description = results[i].description;
                    //format date using moment js
                    var date = moment(results[i].date).format("MMMM Do YYYY, h:mm:ss a");
                    //get type of crime
                   //document.write(date.split(" ")[2])
                    var crimeType = results[i].primary_type;
                    //number for each crime has to be i + 1
                    var number = (i + 1)%3+1;
                    //adding crime info
                    addCrimeInfo(number, crimeMarkers[i], date,block,description,crimeType);

                    //add the table
                    $("#results-table").append("<tr><td>"+number+"</td><td>"+block+"</td><td>"+crimeType+" "+description+"</td><td>"+date+"</td></tr>");
                }
            });  //end .done function
        });//end of geocode function?? for some reason all of the code regarding the api has to be inside here
    }); //on click end

    //this enables the Google Map API Autocomplete function for addresses
    var autocomplete = new google.maps.places.Autocomplete((document.getElementById("location")),
    {
        types: ["geocode"]
    });
});

 