const commentElement = document.querySelectorAll('.comment');
const jsCommentsObj = {}; // create DOM data for Comment object
for (let comment of commentElement.values()) {
    var id = comment.getAttribute('comment-id');
    var likesCount = comment.getAttribute('likes-count');
    jsCommentsObj[id] = parseInt(likesCount);
}

function toggleInlineDisplay(like_id) {
    var elem = document.getElementById(like_id);
    if(window.getComputedStyle(elem).display == "inline") {
        elem.style.display = 'none';
        elem.dataset.previousDisplay = 'inline';
    } else if(window.getComputedStyle(elem).display == "block") {
        elem.style.display = 'none';
        elem.dataset.previousDisplay = 'block';
    } else {
        console.log('prev', elem.dataset.previousDisplay);
        if ( typeof elem.dataset.previousDisplay == 'string' ) {
            elem.style.display = elem.dataset.previousDisplay
        } else {
            elem.style.display = 'inline';
        }
    }
}

function updateLikesCount(url, comment_id) { // update DOM data to reflect Comment object changes
    const likesCountId = 'likes_count_'+comment_id;
    const element = document.getElementById(likesCountId);
    if (url == '/comment/'+comment_id+'/like') {
        prevLikesCount = jsCommentsObj[comment_id];
        newLikesCount = prevLikesCount + 1;
        jsCommentsObj[comment_id] = newLikesCount;
        element.innerHTML = ' <span class="liked-count">'+newLikesCount+'</span>';
    } else {
        prevLikesCount = jsCommentsObj[comment_id];
        newLikesCount = prevLikesCount - 1;
        jsCommentsObj[comment_id] = newLikesCount;
        element.innerHTML = ' <span class="dismissed-like-count">'+newLikesCount+'</span>';
    }
}

function likeComment(url, comment_id) {
    console.log('POSTing to', url);
    fetch(url, { method: 'POST', body: '{}' } )
    .then((response) => {
        console.log(url, 'finished');
        toggleInlineDisplay('not_liked_'+comment_id);
        toggleInlineDisplay('liked_'+comment_id);
        updateLikesCount(url, comment_id)
    }).catch((error) => {
        alert('Url failed with '+error+' '+url);
    });
}