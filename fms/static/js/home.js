var counter = 0;
function createNewItem()
{
    ++counter;
    var html = "<input name='food";
    html += counter;
    html +="' required class='itemField form-control' type='text' placeholder='Food item Name'>";
    html += "<select class='itemField form-control'><option value='Countable'>Countable</option><option value='Uncountable'>Uncountable</option></select><br>";
    document.getElementById("itemDetails1").innerHTML += html;
}
function deleteAllItem()
{
    document.getElementById("itemDetails1").innerHTML = "";
}