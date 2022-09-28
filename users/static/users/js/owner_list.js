
// document.getElementById('username').addEventListener('change', ajax_request);
// document.getElementById('user').addEventListener('change', ajax_request);
// document.getElementById('phone').addEventListener('change', ajax_request);
// document.getElementById('email').addEventListener('change', ajax_request);
// document.getElementById('house').addEventListener('change', ajax_request);
// document.getElementById('flat').addEventListener('change', ajax_request);
// document.getElementById('date_joined').addEventListener('change', ajax_request);
// document.getElementById('status').addEventListener('change', ajax_request);
// document.getElementById('dolg').addEventListener('change', ajax_request);


$('tr[data-href]').on("click", function() {
    document.location = $(this).data('href');
});

document.getElementById('reset').addEventListener('click', function () {
    document.getElementById('username').value = '';
    document.getElementById('user').value = '';
    document.getElementById('phone').value = '';
    document.getElementById('email').value = '';
    document.getElementById('house').value = '';
    document.getElementById('flat').value = '';
    document.getElementById('date_joined').value = '';
    document.getElementById('status').value = '';
    document.getElementById('dolg').value = '';
    // var event = new Event("change");
    // document.getElementById('flat').dispatchEvent(event);
    var table = $('#users').DataTable();
    table.search('');
    table.columns().search('').draw();
})

$('.btn-delete').on('click', function (event){
    var result = confirm('Вы действительно хотите удалить пользователя?')
    if (!result) {
        event.preventDefault()
        event.stopImmediatePropagation()
        return false
    }
})