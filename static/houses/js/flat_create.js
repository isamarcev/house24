
let elemtnts = document.querySelectorAll("input[type='text']")
for (var i = 0; i < elemtnts.length; ++i) {
    elemtnts[i].addEventListener('change', function(e) {
        this.parentNode.classList.add('has-success');
    });
}

$('#id_owner').on('change', function () {
    console.log(this)
    console.log(this.closest("div"))
    this.parentNode.classList.add('has-success')
})

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

// function checkLength () {
//     if ($('#id_number'))
// }


$(document).ready(function(){
    let form = document.getElementsByTagName('form')
    $('form').attr('action', window.location.pathname )
    console.log($('form'))
});

