$(document).ready(function () {
    const $btnCancel = $(`.cancel-btn`);
    $btnCancel.on('click', function () {
        const id = $(this).attr('value');
        // Gán lại action cho form
        const form = document.getElementById('cancelForm');
        form.action = `/employee/cancel-request/${id}`;

        // Mở modal bằng Bootstrap 5
        const modal = new bootstrap.Modal(document.getElementById('cancelModal'));
        modal.show();
    })

});
