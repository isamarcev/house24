
document.getElementById('user').addEventListener('blur', ajax_request);
document.getElementById('role').addEventListener('blur', ajax_request);
document.getElementById('phone').addEventListener('blur', ajax_request);
document.getElementById('email').addEventListener('blur', ajax_request);
document.getElementById('status').addEventListener('blur', ajax_request);


$('tr[data-href]').on("click", function() {
    document.location = $(this).data('href');
});

document.getElementById('reset').addEventListener('click', function () {
    document.getElementById('user').value = '';
    document.getElementById('role').value = '';
    document.getElementById('phone').value = '';
    document.getElementById('email').value = '';
    document.getElementById('status').value = '';
    var event = new Event("blur");
    document.getElementById('status').dispatchEvent(event);
})