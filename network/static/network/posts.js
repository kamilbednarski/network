document.addEventListener('DOMContentLoaded', function () {
    var postsViewState = {
        lastLoadedPostId: 0,
        isLoading: false
    };

    document.querySelector('#load-all-posts')
        .addEventListener('click', async function infinitePostLoader() {
            showHideNavbar();
            showPostsView();
            const latestPostId = await getLatestPostId()
            postsViewState.isLoading = true;
            const lastLoadedPost = await getPosts(latestPostId)
            postsViewState.lastLoadedPostId = lastLoadedPost;
            postsViewState.isLoading = false;
        });

    const postsViewElement = document.querySelector('#posts-view');
    postsViewElement.addEventListener('scroll', async () => {
        if (postsViewElement.scrollTop + postsViewElement.clientHeight >= postsViewElement.scrollHeight) {
            const thereAreMorePostsToLoad = postsViewState.lastLoadedPostId > 1;

            if (!postsViewState.isLoading && thereAreMorePostsToLoad) {
                console.log("Get additional posts");
                postsViewState.isLoading = true;
                const lastLoadedPost = await getPosts(postsViewState.lastLoadedPostId - 1)
                postsViewState.lastLoadedPostId = lastLoadedPost;
                postsViewState.isLoading = false;
            }
        }
    });
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
        dateContainer.innerText = post.date_added + ' id:' + post.id
        contentContainer.innerText = post['content']

        userAndDateContainer.append(userContainer, dateContainer)
        postContainer.append(userAndDateContainer, contentContainer)
        mainPostsContainer.append(postContainer)

    }
    return loadedPostId
}


async function getPosts(startingPostId) {
    if(startingPostId < 1) {
        throw new Error("StartingPostId must be greater or equal 0.")
    }

    const POSTS_PER_PAGE = 10

    //showPostsView()

    let firstPostId = startingPostId
    let lastPostId = firstPostId - POSTS_PER_PAGE + 1
    let lastLoadedPostId

    if (lastPostId < 1) { lastPostId = 1 }

    if (firstPostId == 1) {
        lastLoadedPostId = await getSinglePost(firstPostId)
    } else {
        for (let i = firstPostId; i >= lastPostId; i--) {
            const loadedPostId = await getSinglePost(i)
            lastLoadedPostId = loadedPostId
        }
    }

    return lastLoadedPostId
}

// window.addEventListener('scroll', () => {
//     if(window.scrollY + window.innerHeight >= document.documentElement.scrollHeight) {
//         getPosts(lastLoadedPostId - 1, POSTS_PER_PAGE)
//     }
// })