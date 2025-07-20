$(document).ready(function () {
    handleSelectOrder('order', 'order');
    handleSelectOrder('pagination', 'limit');
    handleSelectPrevButton()
    handleSelectNextButton()
    handleSelectPaginateButton()
});

const url = new URL(window.location.href);

function handleSelectOrder(nameNode, param) {
    const $menu = $(`.dropdown-menu-${nameNode}`);

    $menu.find('.dropdown-item').on('click', function () {
        const value = $(this).attr('value');
        $(`.dropdown-toggle-${nameNode}`).text($(this).text());

        const url = new URL(window.location.href);
        url.searchParams.set(param, value);
        url.searchParams.delete('page');

        // ✅ Reload page with new parameters
        window.location.href = url.toString();
    });
}



function handleSelectPrevButton() {
    const $prevButton = $('.prev-button');
    $prevButton.on('click', function () {
        let page = parseInt(url.searchParams.get('page') || '1');
        url.searchParams.set("page", Math.max(page - 1, 1)); // prevent page < 1
        window.location.href = url.toString();
    });
}

function handleSelectNextButton() {
    const $nextButton = $('.next-button');
    $nextButton.on('click', function () {
        let page = parseInt(url.searchParams.get('page') || '1');
        url.searchParams.set("page", page + 1);
        window.location.href = url.toString();
    });
}

function handleSelectPaginateButton() {
    const $itemButton = $('.item-button .page-link');
    $itemButton.on('click', function () {
        const page = $(this).attr('aria-label');
        url.searchParams.set("page", page);
        window.location.href = url.toString();
    });
}



