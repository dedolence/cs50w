function ajax(full_url, disappear = false) {
    // params[0] will be a leading '/'; params[1] will be 'ajax'
    let params = full_url.split('/');
    let action = params[2];
    let id = params[3];
    let csrf_token = document.querySelector('[name=csrfmiddlewaretoken]').value
    fetch(full_url, {
        method: 'POST',
        headers: {'X-CSRFToken': csrf_token}
        })
        .then(res => res.json())
        .then(r => {
            // set the toast message, if any
            if (action == 'watch_listing') {
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
            else if (action == 'generate_comment') {
                let comment_box = document.getElementById("commentInput");
                comment_box.innerHTML = r.message;
            }
            else if (action == 'reply_comment') {}
            else if (action == 'edit_comment') {
                let comment_card = document.getElementById("comment-" + id);
                let comment_text = document.getElementById("commentText-" + id);
                let comment_box = document.getElementById("commentInput");
                let submit_button = document.getElementById("commentSubmitButton");
                
            }
            else if (action == 'delete_comment') {}

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
        });
}
