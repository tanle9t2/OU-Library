const CART_API = '/api/v1/cart'
const ACCOUNT_API = '/api/v1/account/'
const CURRENT_URL = new URL(window.location);
const buttonBuy = document.querySelector('.btn-buy')

const moreDetail = document.querySelector(".item-more-detail")
let toggleMoreDetail = false
moreDetail.addEventListener('click', () => {
    if (!toggleMoreDetail) {
        document.querySelector(".block-gradient").style = "display: none"
        document.querySelector(".item-content").style = "overflow:none;max-height:100%"
    } else {
        document.querySelector(".block-gradient").style = "display: block"
        document.querySelector(".item-content").style = "overflow:hidden;max-height:300px"
    }
    toggleMoreDetail = !toggleMoreDetail
})

const VND = new Intl.NumberFormat('vi-VN', {
    style: 'currency',
    currency: 'VND',
});

function extractCurrencyNumber(currencyString) {
    const numericValue = currencyString.replace(/[^\d,]/g, ''); // Keep digits and comma
    return parseFloat(numericValue.replace(',', '.')); // Convert to float, replace comma with dot
}

const showToast = function (message, isError) {
    const color = isError ? 'var(--red)' : "#6cbf6c"
    Toastify({
        text: message,
        duration: 3000,
        newWindow: true,
        close: true,
        gravity: "top", // `top` or `bottom`
        position: "center", // `left`, `center` or `right`
        stopOnFocus: true, // Prevents dismissing of toast on hover
        style: {
            background: color,
        }
    }).showToast()
}

buttonBuy.addEventListener('click', () => {
    addCartItem(CURRENT_URL.searchParams.get("bookId")).then(res => {
        if (res['status'] === 200)
            window.location.href = "/cart"

        else if (res['status'] === 507) {
            showToast(res['message'], true)
        } else if (res['status'] === 403) {
            window.location.href = "/account/login"
        }
    })

})

const imageItem = document.querySelectorAll('.image-item')
imageItem && imageItem.forEach(item => item.addEventListener('click', () => {
    document.body.insertAdjacentHTML('beforeend', ``)
}))

