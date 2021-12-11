function watchListing(id, ajaxURL, disappear) {
    let listingContainer = document.getElementById("listing-" + id);
    let toastElement = document.getElementById("toast-" + id);
    let toastBody = document.getElementById("toast-body-" + id);
    let buttonText = document.getElementById("toast-button-text-" + id);
    let toastIcon = document.getElementById("toast-icon-" + id);

    let request = new XMLHttpRequest();
    request.onreadystatechange = function() {
        if (request.readyState === 4 && request.status === 200) {
            let r = JSON.parse(request.responseText);
            // set toast text according to server response
            toastBody.innerHTML = r.message;
            // toggle icon and text
            toastIcon.classList.toggle("bi-heart");
            toastIcon.classList.toggle("bi-heart-fill");
            buttonText.innerHTML = r.button_text;
            // create Toast instance
            let toast = new bootstrap.Toast(toastElement);
            // display Toast
            toast.show();

            if (disappear) fadeOut(listingContainer);
            return;
        }
    }
    request.open("POST", ajaxURL);
    request.send();
}


/* 
 * Fade function written by Bruno Vieira
 * https://dev.to/bmsvieira/vanilla-js-fadein-out-2a6o
 */
function fadeOut(el) {
    el.style.opacity = 1;
    (function fade() {
        if ((el.style.opacity -= .05) < 0) {
            el.style.display = "none";
        } else {
            requestAnimationFrame(fade);
        }
    })();
};