var counter = 0;


function createNewItem()
{
    ++counter;
    var html = "<input name='food";
    html += counter;
    html +="' required class='itemField form-control' type='text' placeholder='Food item Name'>";
    html += "<select class='itemField form-control'>" +
        "<option value='Less than 5Kg'>Less than 5Kg</option>" +
        "<option value='5Kg - 15Kg'>5Kg - 15Kg</option>" +
        "<option value='15Kg - 25Kg'>15Kg - 25Kg</option>" +
        "<option value='Greater than 25Kg'>Greater than 25Kg" +
        "</option></select>" +
        "<input type='datetime-local' class='itemField form-control' placeholder='Expiry Date' required />";
        document.getElementById("itemDetails1").innerHTML += html;
}
function deleteAllItem()
{
    document.getElementById("itemDetails1").innerHTML = "";
}
function fetchImage(input) {
    if(input.files && input.files[0])
    {
        var reader = new FileReader();
        reader.onload = function (e) {
            $("#imagePreview").attr('src', e.target.result).width(600).height(450);

        };
    }
    reader.readAsDataURL(input.files[0]);
}
var map, infoWindow;
      function initMap() {
        map = new google.maps.Map(document.getElementById('map'), {
          center: {lat: -34.397, lng: 150.644},
          zoom: 14
        });
        infoWindow = new google.maps.InfoWindow;

        // Try HTML5 geolocation.
        if (navigator.geolocation) {
          navigator.geolocation.getCurrentPosition(function(position) {
            var pos = {
              lat: position.coords.latitude,
              lng: position.coords.longitude
            };

            infoWindow.setPosition(pos);
            infoWindow.setContent('Location found.');
            infoWindow.open(map);
            map.setCenter(pos);
          }, function() {
            handleLocationError(true, infoWindow, map.getCenter());
          });
        } else {
          // Browser doesn't support Geolocation
          handleLocationError(false, infoWindow, map.getCenter());
        }
      }

      function handleLocationError(browserHasGeolocation, infoWindow, pos) {
        infoWindow.setPosition(pos);
        infoWindow.setContent(browserHasGeolocation ?
                              'Error: The Geolocation service failed.' :
                              'Error: Your browser doesn\'t support geolocation.');
        infoWindow.open(map);
      }

