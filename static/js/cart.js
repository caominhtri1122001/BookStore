var updateBtns = document.getElementsByClassName('update-cart')

for (var i = 0; i < updateBtns.length ; i++) {
    updateBtns[i].addEventListener('click', function() {
        var bookID = this.dataset.book
        var action = this.dataset.action
        console.log('bookID', bookID, 'action', action);

        console.log('User : ',user);
        if (user === 'AnonymousUser') {
            console.log('Not logged in');
        }
        else {
            updateUserOrder(bookID,action);
        }
    })
}

function updateUserOrder(bookID, action) {
    console.log('User is logged in, sending data...');

    var url = '/update_item/';
    fetch(url, {
        method:'POST',
        headers: {
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({'bookID':bookID, 'action':action})
    })

    .then((response) => {
        return response.json()
    })
    .then((data) => {
        console.log('data:', data);
    })
}