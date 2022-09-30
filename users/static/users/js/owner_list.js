
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