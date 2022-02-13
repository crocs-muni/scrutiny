/**
 * Based on https://www.w3schools.com/howto/tryit.asp?filename=tryhow_js_toggle_hide_show
 * @param {*} id id of element to hide
 */
function hideButton(id) {
  var x = document.getElementById(id);
  if (x.style.display === "none") {
    x.style.display = "block";
  } else {
    x.style.display = "none";
  }
}

/**
 * @param {*} ids array of ids of elements to show
 */
function showAll(ids) {
  ids.forEach(function(id) {
    document.getElementById(id).style.display = "block";
  });
}

/**
 * @param {*} ids array of ids of elements to hide
 */
function hideAll(ids) {
  ids.forEach(function(id) {
    document.getElementById(id).style.display = "none";
  });
}

/**
 * 
 * @param {*} shown  array of ids of elements to show
 * @param {*} hidden array of ids of elements to hide
 */
function defaultAll(shown, hidden) {
  showAll(shown);
  hideAll(hidden);
}

// Floating button based on https://www.w3schools.com/howto/howto_js_scroll_to_top.asp
window.onscroll = showHideScrollButton;

function showHideScrollButton() {
  var topButton = document.getElementById("topButton");
  if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
    topButton.style.display = "block";
  } else {
    topButton.style.display = "none";
  }
}

// Taken from https://www.w3schools.com/howto/howto_js_scroll_to_top.asp
function backToTop() {
  document.body.scrollTop = 0; // For Safari
  document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
}

/* Gallery */

function displayImage(imgs, expandedImageID, imageTextID) {
  var expandImg = document.getElementById(expandedImageID);
  var imgText = document.getElementById(imageTextID);
  expandImg.src = imgs.src;
  imgText.innerHTML = imgs.alt;
  expandImg.parentElement.style.display = "block";
}

/* Gallery end */