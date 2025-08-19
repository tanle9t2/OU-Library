
const searchButton = document.querySelector('.icon-search')

searchButton.addEventListener('click', (e) => {
      e.preventDefault();

    const keyword = document.querySelector('input[name="keyword"]').value;

    // Get current URL and params
    const url = new URL(window.location.href);
    const params = url.searchParams;

    params.set('keyword', keyword);


    params.delete('page');

    // Update the URL
    window.location.href = `${url.pathname}?${params.toString()}`;
})

