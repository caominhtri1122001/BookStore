var updateBtns = document.getElementsByClassName('update-cart')

for (var i = 0; i < updateBtns.length ; i++) {
    updateBtns[i].addEventListener('click', function() {
        var bookID = this.dataset.book
        var action = this.dataset.action
        console.log('bookID', bookID, 'action', action);

        console.log('User : ',user);
        if (user === 'AnonymousUser') {
            addCookieItem(bookID, action);
        }
        else {
            updateUserOrder(bookID,action);
        }
    })
}

function addCookieItem(bookID, action) {
    console.log('Not logged in...');
    console.log('Action : ', action);
    if( action == 'add') {
        if (cart[bookID] === undefined) {
            cart[bookID] = {'quantity':1}
        }else {
            cart[bookID]['quantity'] += 1
        }
    }

    if ( action == 'remove') {
        cart[bookID]['quantity'] -= 1;

        if (cart[bookID]['quantity'] <= 0) {
            console.log('Remove Item');
            delete cart[bookID]
        }
    }
    console.log('Cart:' , cart);
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
    location.reload()
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
        location.reload()
    })
}