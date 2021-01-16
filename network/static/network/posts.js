document.addEventListener('DOMContentLoaded', function() {

    document.querySelector('#load-all-posts')
    .addEventListener('click', async function infinitePostLoader() {
        showHideNavbar()
        const latestPostId = await getLatestPostId()
        const lastLoadedPost = await getPosts(latestPostId)
    })
});


function showPostsView() {
    document.querySelector('#posts-view').innerHTML = ''
    document.querySelector('#body-view').style.display = 'none'
    document.querySelector('#posts-view').style.display = 'block'
}

function showHideNavbar() {
    document.querySelector('#navbar-toggler-button').click()
}


async function getLatestPostId() {
    const response = await fetch('/post/all/latestid', { method: 'GET' })
    const latestPostId = (await response.json()).id
    return latestPostId
}


async function getSinglePost(postId) {
    const response = await fetch(`/post/id/${postId}`, { method: 'GET' })
    const post = await response.json()
    let loadedPostId = post['id']

    console.log(post['id'])

    if (loadedPostId != undefined) {
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
    return loadedPostId
}


async function getPosts(startingPostId) {
    const POSTS_PER_PAGE = 10

    showPostsView()

    let firstPostId = startingPostId
    let lastPostId = firstPostId - POSTS_PER_PAGE
    let lastLoadedPostId

    if(lastPostId < 1) {lastPostId = 1}

    if(firstPostId == 1) {
        lastLoadedPostId = await getSinglePost(firstPostId)
    } else {
        for(let i = firstPostId; i > lastPostId; i--) {
            const loadedPostId = await getSinglePost(i)
            lastLoadedPostId = loadedPostId
        }
    }

    if(lastLoadedPostId > 1) {
        window.addEventListener('scroll', () => {
            if(window.scrollY + window.innerHeight >= document.documentElement.scrollHeight) {
                getPosts(lastLoadedPostId - 1, POSTS_PER_PAGE)
            }
        })
    }

    return lastLoadedPostId
}

// window.addEventListener('scroll', () => {
//     if(window.scrollY + window.innerHeight >= document.documentElement.scrollHeight) {
//         getPosts(lastLoadedPostId - 1, POSTS_PER_PAGE)
//     }
// })