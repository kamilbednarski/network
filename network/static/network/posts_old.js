document.addEventListener('DOMContentLoaded', function() {

    document.querySelector('#load-all-posts').addEventListener('click' , () => {
        document.querySelector('#posts-view').innerHTML = ''
        document.querySelector('#body-view').style.display = 'none'
        document.querySelector('#posts-view').style.display = 'block'

        getLatestPostId()
        .then(response => loadPosts(response))

        document.querySelector('#navbar-toggler-button').click()
    })

});


async function getLatestPostId() {
    const response = await fetch('/post/all/latestid', { method: 'GET' })
    const latestPostId = (await response.json()).id
    return latestPostId
}


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

        return post['id']
    }
}


async function loadMultiplePosts(startNumber, endNumber) {
    let nextPostId
    for (let i = startNumber; i >= endNumber; i--) {
        const loadedPostId = await loadSinglePost(i)
        console.log('loaded post: ' + loadedPostId)
        nextPostId = loadedPostId - 1
        console.log('startNumber: ' + nextPostId)
    }
    console.log('NEW START NUMBER: ' + nextPostId)
    return nextPostId
}


function loadPosts(firstPostId) {
    console.log('FIRST POST ID!!!!: ' + firstPostId)

    if(firstPostId === 0) {
        return
    } else {
        let startNumber = firstPostId
        let endNumber = startNumber - 9

        if(endNumber < 1) {
            endNumber = 1
        }

        loadMultiplePosts(startNumber, endNumber).then(newStartNumber => {
            console.log('LAST LOADED ID:' + newStartNumber)

        })

        window.addEventListener('scroll', () => {
            if(window.scrollY + window.innerHeight >= document.documentElement.scrollHeight) {
                loadPosts(newStartNumber)
            }
        })
    }
}
