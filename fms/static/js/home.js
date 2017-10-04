$(document).ready(function() {
$('.thumbnail').click(function(){
      $('.modal-body').empty();
  	var title = $(this).parent('a').attr("title");
  	$('.modal-title').html(title);
  	$($(this).parents('div').html()).appendTo('.modal-body');
  	$('#myModal').modal({show:true});
});

});
var counter = 0;
function createNewItem()
{
    ++counter;
    var html = "<input name='food";
    html += counter;
    html +="' required class='itemField form-control' type='text' placeholder='Food item Name'>";
    html += "<select name='item_weight"
    html += counter;
    html += "' class='itemField form-control'>" +
        "<option value='Less than 5Kg'>Less than 5Kg</option>" +
        "<option value='5Kg - 15Kg'>5Kg - 15Kg</option>" +
        "<option value='15Kg - 25Kg'>15Kg - 25Kg</option>" +
        "<option value='Greater than 25Kg'>Greater than 25Kg" +
        "</option></select>" +
        "<input name='food_expiry";
    html += counter;
    html += "' type='datetime-local' class='itemField form-control' placeholder='Expiry Date' required />";
        document.getElementById("itemDetails1").innerHTML += html;
}
function resetItems()
{
    counter = 0;
}
function deleteAllItem()
{
    document.getElementById("itemDetails1").innerHTML = "";
    counter = 0;
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

