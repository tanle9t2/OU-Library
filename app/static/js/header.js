
const searchButton = document.querySelector('.icon-search')

searchButton.addEventListener('click', (e) => {
    e.preventDefault()
    const keyword = document.querySelector('input[name="keyword"]').value
    window.location.href = `${window.location.origin}?keyword=${keyword}`
})

