document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('#load-all-posts').addEventListener(
        'click',
        load_all_posts())
});

function load_single_post() {
    document.querySelector('#body-view').style.display = 'none'
    document.querySelector('#posts-view').style.display = 'none'
    document.querySelector('#post-view').style.display = 'block'

    let postId = Number(event.target.dataset.postId)
    console.log(postId)
    fetch(`/post/id/${postId}`, {method: 'GET'})
    .then(response => response.json())
    .then(post => {
        console.log(post)
        // // Main container for extended view of single post
        // let mainPostContainer = document.querySelector('#post-view')

        // // Container for exteded single post view
        // let postContainer = document.createElement('div')
        // postContainer.classList.add('card', 'm-3')

        // // Container for 'user' and 'date_added' fields
        // let userAndDateContainer = document.createElement('div')
        // userAndDateContainer.classList.add('card-header')
        // let userContainer = document.createElement('span')
        // userContainer.classList.add('fw-bold')
        // let dateContainer = document.createElement('span')
        // dateContainer.classList.add('small', 'fw-light', 'text-uppercase')

        // // Container for 'content' field
        // let contentContainer = document.createElement('div')
        // contentContainer.classList.add('p-3')

        // userContainer.innerText = '@' + post['user'] + ' · '
        // dateContainer.innerText = post['date_added']
        // contentContainer.innerText = post['content']
    })

}

function load_all_posts() {
    document.querySelector('#body-view').style.display = 'none'
    document.querySelector('#posts-view').style.display = 'block'
    document.querySelector('#post-view').style.display = 'none'

    fetch('/post/all', {method: 'GET'})
    .then(response => response.json())
    .then(posts => {
        if (posts.length === 0) {
            let messageContainer = document.createElement('div')
            messageContainer.append("There's no posts yet.")
            messageContainer.classList.add('text-center', 'py-5')
            emailsView.append(messageContainer)
            // TODO create separate container for all messages.
        }

        let i = 0
        for (i = 0; i < posts.length; i++) {
            // Main container for all posts view
            let mainPostsContainer = document.querySelector('#posts-view')

            // Container for single post
            let postContainer = document.createElement('div')
            postContainer.classList.add('card', 'm-3')

            // Container for 'user' and 'date_added' fields
            let userAndDateContainer = document.createElement('div')
            userAndDateContainer.classList.add('card-header')
            let userContainer = document.createElement('span')
            userContainer.classList.add('fw-bold')
            let dateContainer = document.createElement('span')
            dateContainer.classList.add('small', 'fw-light', 'text-uppercase')

            // Container for 'content' field
            let contentContainer = document.createElement('div')
            contentContainer.classList.add('p-3')

            postContainer.dataset.postId = `${posts[i]['id']}`
            userContainer.dataset.postId = `${posts[i]['id']}`
            userAndDateContainer.dataset.postId = `${posts[i]['id']}`
            userContainer.dataset.postId = `${posts[i]['id']}`
            dateContainer.dataset.postId = `${posts[i]['id']}`
            contentContainer.dataset.postId = `${posts[i]['id']}`

            userContainer.innerText = '@' + posts[i]['user'] + ' · '
            dateContainer.innerText = posts[i]['date_added']
            contentContainer.innerText = posts[i]['content']

            userAndDateContainer.append(userContainer)
            userAndDateContainer.append(dateContainer)
            postContainer.append(userAndDateContainer)
            postContainer.append(contentContainer)
            mainPostsContainer.append(postContainer)

            postContainer.addEventListener('click', () => load_single_post())
        }
    })
}