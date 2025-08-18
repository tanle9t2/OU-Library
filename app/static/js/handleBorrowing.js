$(document).ready(function () {
    const $listRequest = $(`.book-row`);

    $listRequest.each(function (index, row) {
        const $btnCancel = $(row).find('.cancel-btn');
        const $btnUndo = $(row).find('.btn-undo');
        const $modal = $(row).find("#modalOverlay")

        function onCloseModal() {
            $modal.removeClass("active");
        }

        $btnCancel.on('click', function () {
            $modal.addClass("active");
        });

        $btnUndo.on('click', function () {
            onCloseModal();
        });
        $modal.on('click', function () {
            onCloseModal();
        });
    });


    $(".dropdown-menu-order .dropdown-item").on("click", function () {
        let value = $(this).attr("value");
        let params = new URLSearchParams(window.location.search);
        params.delete("page");
        params.set("order",value)
        let newUrl = window.location.pathname;
        if (params.toString()) {
            newUrl += "?" + params.toString();
        }

        window.location.href = newUrl;
    });


});
