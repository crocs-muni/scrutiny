/**
 * Based on https://www.w3schools.com/howto/tryit.asp?filename=tryhow_js_toggle_hide_show
 * @param {*} id
 */
function hideButton(id) {
  var x = document.getElementById(id);
  if (x.style.display === "none") {
    x.style.display = "block";
  } else {
    x.style.display = "none";
  }
}

function showAll(ids) {
  ids.forEach(function(id) {
    var x = document.getElementById(id);
    x.style.display = "block";
  });
}

function hideAll(ids) {
  ids.forEach(function(id) {
    var x = document.getElementById(id);
    x.style.display = "none";
  });
}
