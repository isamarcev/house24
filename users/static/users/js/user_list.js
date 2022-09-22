
document.getElementById('user').addEventListener('change', ajax_request);
document.getElementById('role').addEventListener('change', ajax_request);
document.getElementById('phone').addEventListener('change', ajax_request);
document.getElementById('email').addEventListener('change', ajax_request);
document.getElementById('status').addEventListener('change', ajax_request);


$('tr[data-href]').on("click", function() {
    document.location = $(this).data('href');
});

document.getElementById('reset').addEventListener('click', function () {
    document.getElementById('user').value = '';
    document.getElementById('role').value = '';
    document.getElementById('phone').value = '';
    document.getElementById('email').value = '';
    document.getElementById('status').value = '';
    var event = new Event("change");
    document.getElementById('status').dispatchEvent(event);
})