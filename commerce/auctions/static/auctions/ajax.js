/**
 * Toggle the addition/deletion of a listing from a user's watchlist.
 * @param {number} id - the listing's primary key ID 
 * @param {string} ajaxURL - the URL that the AJAX call should use; provided by Django so as to avoid hard-coding. 
 * @param {true|false} disappear - binary flag for whether the listing DOM element should be removed from the document after toggling.
 */
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
            if (!r.undo) {
                toastIcon.classList.toggle("bi-heart");
                toastIcon.classList.toggle("bi-heart-fill");
                buttonText.innerHTML = r.button_text;
            }
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

function ajax(full_url, disappear) {
    let params = full_url.split('/');
    let action = params[2];
    let id = params[3];
    fetch(full_url, {method: 'POST'})
        .then(res => res.json())
        .then(r => {
            // set the toast message, if any
            if (action == 'watch_listing'){
                let toastElement = document.getElementById("toast-" + id);
                let toastBody = document.getElementById("toast-body-" + id);
                let buttonText = document.getElementById("toast-button-text-" + id);
                let toastIcon = document.getElementById("toast-icon-" + id);
                
                toastBody.innerHTML = r.message;
                // toggle icon and text
                if (!r.undo) {
                    toastIcon.classList.toggle("bi-heart");
                    toastIcon.classList.toggle("bi-heart-fill");
                    buttonText.innerHTML = r.button_text;
                }
                // create Toast instance
                let toast = new bootstrap.Toast(toastElement);
                // display Toast
                toast.show();
            }

            // hide the notification
            if (disappear) {
                switch (action) {
                    case "dismiss":
                        identifier = 'notification-';
                        break;
                    case "watch_listing":
                        identifier = 'listing-';
                        break;
                    default:
                        break;
                }
                let element = document.getElementById(identifier + id);
                $(element).fadeOut()
                return;
            }
            else return;
        });
}


/* 
 * Fade function written by Bruno Vieira
 * https://dev.to/bmsvieira/vanilla-js-fadein-out-2a6o
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

 */