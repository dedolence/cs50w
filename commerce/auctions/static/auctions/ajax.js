function watchListing(id, ajaxURL) {
        let toastElement = document.getElementById("toast-" + id);
        let toastBody = document.getElementById("toast-body-" + id);
        let timer = toastElement.getAttribute("data-delay");
        // let toastIcon = document.getElementById("toast-icon-" + id);

        let request = new XMLHttpRequest();
        request.onreadystatechange = function() {
            if (request.readyState === 4 && request.status === 200) {
                // set toast text according to server response
                toastBody.innerHTML = request.responseText;
                // toggle icon
                // toastIcon.classList.toggle("bi-heart");
                // toastIcon.classList.toggle("bi-heart-fill");
                // create Toast instance
                let toast = new bootstrap.Toast(toastElement);
                // display Toast
                toast.show();
                window.setTimeout(() => {}, timer);
            }
        }
        request.open("POST", ajaxURL);
        request.send();
}