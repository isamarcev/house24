function generatePassword(){
    var len = 10
    var password = "";
    var symbols = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789;"
    for (var i = 0; i < len; i++){
        password += symbols.charAt(Math.floor(Math.random() * symbols.length));
    }
    $('#id_password').val(password);
    $('#id_password2').val(password);
    $('#id_password').parent().parent().removeClass('has-error')
    $('#id_password2').parent().parent().removeClass('has-error')
    $('#id_password').parent().parent().addClass('has-success')
    $('#id_password2').parent().parent().addClass('has-success');
    $('.errorlist-password').css('display', 'none')
    return password;
}

$('#showPass').click(function () {
    var password1 = $('#id_password');
    var password2 = $('#id_password2');
    if (password1.attr('type') === 'password') {
        password1.attr('type', 'text');
        password2.attr('type', 'text');
    } else {
        password1.attr('type', 'password');
        password2.attr('type', 'password');
    }
})
$(document).ready(function(){
    $('#id_role > option:nth-child(1)').remove()
});


let elemtnts = document.querySelectorAll("input[type='text']")
for (var i = 0; i < elemtnts.length; ++i) {
    elemtnts[i].addEventListener('blur', function(e) {
        this.parentNode.classList.add('has-success');
    });
}

let areas = document.getElementById("id_about")
areas.addEventListener('blur', function(e) {
        this.parentNode.classList.add('has-success');
    });

// let btnDate = document.getElementById('btn-date')
// btnDate.addEventListener('click', function (e) {
//     var event = new Event('click')
//     var foc = new Event('focus')
//     document.getElementById('id_birthday').dispatchEvent(event)
//     document.getElementById('id_birthday').dispatchEvent(foc)
    // $('#id_birthday').click();
    // $('#id_birthday').click();

// })

let selects = document.querySelectorAll("select")
for (var x = 0; x < selects.length; ++x) {
    selects[x].addEventListener('blur', function(e) {
        this.parentNode.classList.add('has-success');
    });
}

let passwords = document.querySelectorAll("input[type='password']")
for (var y = 0; y < passwords.length; ++y) {
    passwords[y].addEventListener('change', function(e) {
        if (this.value.length > 0 && this.value.length < 6) {
            this.closest('.form-group').classList.add('has-error');
        } else {
            this.closest('.form-group').classList.remove('has-error');
            this.closest('.form-group').classList.add('has-success');
        }
    });
}


