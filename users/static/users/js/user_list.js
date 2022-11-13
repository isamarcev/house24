

$('tr[data-href]').on("click", function() {
    document.location = $(this).data('href');
});

let reset = document.getElementById('reset')
reset.addEventListener("click", function () {
    let user = document.getElementById('user');
    user.value = '';
    let role = document.getElementById('role');
    role.value = '';
    let phone = document.getElementById('phone');
    phone.value = '';
    let email = document.getElementById('email');
    email.value = '';
    let status = document.getElementById('status');
    status.value = '';
    let event = new Event('change')
    role.dispatchEvent(event)
})


$('.btn-delete').on('click', function (event){
    var result = confirm('Вы действительно хотите удалить пользователя?')
    if (!result) {
        event.preventDefault()
        event.stopImmediatePropagation()
        return false
    }
})