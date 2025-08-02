$(document).ready(function () {
    handleSelectOrder('order', 'order');
    handleSelectOrder('pagination', 'limit');
    handleSelectPrevButton()
    handleSelectNextButton()
    handleSelectPaginateButton()
    handeSelectFilter("group-filter-genre", "genre")
    handleExpandFilter("group-filter-genre")

    handeSelectFilter("group-filter-publisher", "publisher")
    handleExpandFilter("group-filter-publisher")
});

const url = new URL(window.location.href);

function handleExpandFilter(groupFilter) {
    const $group = $(`#${groupFilter}`)

    $group.find("p").on('click', function () {
        const $ul = $group.find("ul");
        const isCollapsed = $ul.css("height") === "150px" || $ul.height() <= 150;

        if (isCollapsed) {
            $ul.css("height", "auto");
            $(this).text("Thu hẹp");
        } else {
            $ul.css("height", "150px");
            $(this).text("Mở rộng");
        }
    });
}

function handeSelectFilter(groupFilter, param) {
    const $group = $(`#${groupFilter}`)

    $group.find('li').on('click', function () {
        const value = $(this).find('input').attr('value'); // or .val() for form input values
        if (!value) return; // safeguard if no input or value

        const url = new URL(window.location.href);
        let urlValue = url.searchParams.get(param); // assumes param is defined

        if (urlValue) {
            let values = urlValue.split(',');
            if (values.includes(value)) {
                values = values.filter(v => v !== value);
            } else {
                // Add the value
                values.push(value);
            }
            urlValue = values.join(',');
        } else {
            urlValue = value;
        }
        url.searchParams.set(param, urlValue);
        url.searchParams.delete('page');
        window.location.href = url.toString();

    });


}

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



