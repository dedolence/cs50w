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
            let comment_input = document.getElementById("commentInput");
            switch (action) {
                case 'dismiss':
                    let el = document.getElementById("notification-" + id);
                    $(el).fadeOut();
                    break;
                case 'watch_listing':
                    watchListing(id, disappear);
                    break;
                case 'generate_comment':
                    comment_input.innerHTML = r.message;
                    comment_input.style.height = 'auto';
                    comment_input.style.height = comment_input.scrollHeight + 10 + "px";
                    break;
                case 'reply_comment':
                    let comment = document.getElementById("commentText-" + id);
                    let o_c_t = comment.innerText;
                    let r_b = document.getElementById("reply_block");
                    let r_a_l = document.getElementById("reply_author_link");
                    let r_o_c = document.getElementById("reply_original_comment");
                    r_b.classList.remove("d-none");
                    r_o_c.innerText = o_c_t;
                    break;
                case 'edit_comment':
                    editComment(id);
                    break;
                case 'delete_comment':
                    let card = document.getElementById("comment-" + id);
                    let alert = document.createElement("div");
                        alert.classList.add("alert");
                        alert.classList.add("alert-warning");
                        alert.ariaRoleDescription = "alert";
                        alert.innerHTML = r.message;
                    let parent = card.parentElement;
                    parent.replaceChild(alert, card);
                    setTimeout(function() {
                        $(alert).fadeOut();
                    }, 1000);
                    break;
                default:
                    break;
            }
            return;
        });
}

function editComment(id) {
    let anchor = document.getElementById("commentInputAnchor");
    let comment_text = document.getElementById("commentText-" + id);
    let comment_box = document.getElementById("commentInput");
    let submit_button = document.getElementById("commentSubmitButton");
    let hidden_id = document.getElementById("commentId");
    comment_box.innerHTML = comment_text.innerText;
    submit_button.value = "Save Changes";
    hidden_id.value = id;
    // set height to show entire comment
    comment_box.style.height = 'auto';
    comment_box.style.height = comment_box.scrollHeight + 10 + "px";
    anchor.scrollIntoView();
}

function watchListing(id, disappear) { 
    let listing = document.getElementById("listing-" + id);
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
    if (disappear) {
        disappear(listing);
    }
}
