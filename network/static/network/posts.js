document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('#load-all-posts').addEventListener('click' , () => {
        document.querySelector('#posts-view').innerHTML = ''
        load_posts(1)
        document.querySelector('#navbar-toggler-button').click()
    })
});

function load_single_post(postId) {
    fetch(`/post/id/${postId}`, {method: 'GET'})
    .then(response => response.json())
    .then(post => {
        console.log(post['id'])
        if(post['id'] != undefined) {
            let mainPostsContainer = document.querySelector('#posts-view')

            let postContainer = document.createElement('div')
            postContainer.classList.add('card', 'm-3')

            let userAndDateContainer = document.createElement('div')
            userAndDateContainer.classList.add('card-header')

            let userContainer = document.createElement('span')
            userContainer.classList.add('fw-bold')

            let dateContainer = document.createElement('span')
            dateContainer.classList.add('small', 'fw-light', 'text-uppercase')

            let contentContainer = document.createElement('div')
            contentContainer.classList.add('p-3')

            userContainer.innerText = '@' + post['user'] + ' · '
            dateContainer.innerText = post['date_added']
            contentContainer.innerText = post['content']

            userAndDateContainer.append(userContainer, dateContainer)
            postContainer.append(userAndDateContainer, contentContainer)
            mainPostsContainer.append(postContainer)
        }
    })
}

function load_posts(startNumber) {
    let endNumber = startNumber + 9
    while(startNumber <= endNumber) {
        load_single_post(startNumber)
        startNumber++
    }

    window.addEventListener('scroll', () => {
        if(window.scrollY + window.innerHeight >= document.documentElement.scrollHeight) {
            load_posts(startNumber)
        }
    })
}