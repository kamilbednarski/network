document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('#load-all-posts').addEventListener('click' , () => {
        document.querySelector('#posts-view').innerHTML = ''
        document.querySelector('#body-view').style.display = 'none'
        document.querySelector('#posts-view').style.display = 'block'
        loadPosts(1)
        document.querySelector('#navbar-toggler-button').click()
    })
});

async function loadSinglePost(postId) {
    const response = await fetch(`/post/id/${postId}`, { method: 'GET' })
    const post = await response.json()
    console.log(post['id'])
    if (post['id'] != undefined) {
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
}

function loadPosts(postId) {
    let startNumber = postId
    let endNumber = startNumber + 9

    const loadMultiplePosts = async _ => {
        for(let i = startNumber; i <= endNumber; i++) {
            const loadedPost = await loadSinglePost(startNumber)
            startNumber++
        }
    }

    loadMultiplePosts()

    window.addEventListener('scroll', () => {
        if(window.scrollY + window.innerHeight >= document.documentElement.scrollHeight) {
            loadPosts(startNumber)
        }
    })
}