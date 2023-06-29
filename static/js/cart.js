var buttons = document.getElementsByClassName('update-cart');
var quantity = document.getElementById('quantity');
var checkoutBtn = document.getElementById('checkout');
var sizeBtns = document.getElementsByClassName('size-update');
var selectedSize;


function randomNumber() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
      var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
      return v.toString(16);
    });
  }

for (i = 0; i < sizeBtns.length; i++) {
	sizeBtns[i].onclick = function() {
		selectedSize = this.dataset.size

		console.log('size: ', selectedSize)
	}
}

for (i = 0; i < buttons.length; i++) {
	buttons[i].onclick = function() {
		var productId = this.dataset.product
		var action = this.dataset.action
		var size = parseInt(selectedSize)
		code = productId + '-' + size
		
		console.log('productId: ', productId, 'size: ', size,'action: ', action)
		addCookieItem(productId, action, size)
	}
}

function addCookieItem(productId, action, size) {
	if (isNaN(size)) {
		code = productId + '-' + smallest_id
	} else {
		code = productId + '-' + size
	}

	if (action == 'add') {
	  if (cart[code] === undefined) {
		if (quantity.value == '') {
		  cart[code] = {'quantity': 0};
		} else {
			cart[code] = {'quantity': parseInt(quantity.value)};
		}
	  } else {
		if (quantity.value == '' || quantity.value == null) {
			cart[code] = {'quantity': 0};
		} else {
			cart[code]['quantity'] += parseInt(quantity.value)
		}
	  }

	  if (quantity.value !== '' && quantity.value != 0) {
		location.replace('/products/cart/');
	  }
	}
	
	if (action == 'remove') {
		code = productId;
		cart[code] = {'quantity':0};
		location.reload()
	}

	document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
}

checkoutBtn.onclick = function() {
	location.replace('/products/details/');
}
