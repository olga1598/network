console.log("JS is loaded");
document.addEventListener('DOMContentLoaded', function() {
    divs = document.querySelectorAll(".edit-form");
    // console.log("DOM");
    // console.log(divs)
    divs.forEach(div => {
        console.log(div)
        div.style.display = 'none';
    })
    // console.log("DOM loaded");
    editPost();
    savePost();
    add_toggle_likes();
});

function add_toggle_likes() {
    console.log("inside likes")
    document.querySelectorAll(".star").forEach(element => {
        element.addEventListener("click", function (e) {
            console.log("clicked")
            toggle_like(element);
        })
    });
}

function toggle_like(element) {
    // check if post currently liked
    console.log(element.attributes.fill.value.trim());
    const ifLiked = element.attributes.fill.value.trim() === 'red' ? true : false;
    console.log(element.dataset.like);

    // update like/unlike via PUT request
    fetch(`/toggle_like/${element.dataset.like}`, {
        method: "PUT",
        body: JSON.stringify({
            liked: !ifLiked
        })
    })

    // update DOM according to the like post change
    const likes_count = parseInt(document.querySelector(`#like-count-${element.dataset.like}`).innerText);
    console.log(likes_count);
    if(!ifLiked) {
        document.querySelector(`#like-count-${element.dataset.like}`).innerText = likes_count + 1;
        element.setAttribute("fill", "red")
    } else {
        document.querySelector(`#like-count-${element.dataset.like}`).innerText = likes_count - 1;       
        element.setAttribute("fill", "black");
    }
}

function editPost(){
    // Add toggle_edit for each EDIT post button
    const editBtn = document.querySelectorAll(".edit-btn");
    editBtn.forEach(btn => toggle_edit_btn(btn));
}

function toggle_edit_btn(btn) {
    console.log("Inside edit post")
    // add event listener for each EDIT button
    btn.addEventListener("click", function(e) {
        // Pull out the id of the post
        const post_id = e.target.getAttribute("data-post");
        console.log("Inside, HERE post ID")

        console.log(post_id);

        // Hide edit btn
        document.querySelector(`#edit-btn-${ post_id }`).style.display = "none";

        // Hide the post content 
        document.querySelector(`#post-content-${post_id}`).style.display = "none";

        // Show edit form
        document.querySelector(`#edit-form-${post_id}`).style.display = 'block';
    })
}

function savePost() {
    console.log("inside save post");
    // Add toggle_edit for each EDIT post button
    const saveBtn = document.querySelectorAll(".edit-save-btn");
    saveBtn.forEach(btn => toggle_edit_save_btn(btn));
}

function toggle_edit_save_btn(btn){
    // Enable the save button if the content is empty string
    document.querySelector(`#edit-textarea-${ btn.dataset.post }`).onkeyup = () => {
        // Checking the length of the post
        if (document.querySelector(`#edit-textarea-${ btn.dataset.post }`).value.length > 0) {
            // Enable save button
            btn.disabled = false;
        } else {
            // disable save button
            btn.disabled = true;            
        }
    }
    btn.addEventListener("click", function() {
        console.log("saved clicked");
        // Get the button attribute data-post value
        // const post_id = e.target.getAttribute("data-post"); --same as below
        const post_id = btn.dataset.post;
        console.log(post_id);
        console.log("saved clicked");


        // Get the textarea value/text
        let postContent = document.querySelector(`#edit-textarea-${ post_id }`).value;
        console.log(postContent);

        // Make PUT request to update the post content
        fetch(`/edit_post/${post_id}`, {
            method: "PUT",
            body: JSON.stringify({
                content: postContent
            })
        })

        // Update post content in the DOM
        document.getElementById(`post-content-${post_id}`).innerText = postContent;

        // Show the post content 
        document.querySelector(`#post-content-${post_id}`).style.display = "block";

        // Hide edit form
        document.querySelector(`#edit-form-${post_id}`).style.display = 'none';

        // Show edit btn
        document.querySelector(`#edit-btn-${ post_id }`).style.display = "block";


    })
}