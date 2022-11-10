CKEDITOR.replace( 'id_comment' );

document.getElementById("id_time").addEventListener("clocklet.opening", function (event) {
    if (DO_NOT_NEED_TIMEPICKER) {
        event.preventDefault();
    }
});


$(function () {
        $("#id_date").datepicker({
            showOn: "both",
            dateFormat: "yy-mm-dd"
        });
        $('.ui-datepicker-trigger').html("<i class='fa fa-calendar'></i>").addClass('btn btn-date').before($("#id_date"))

})


$(document).ready(function() {
    $("#id_owner").select2({
        tags: true,
        selectionCssClass: 'form-select'
    });
    ajax_get_flat()
})

$(document).ready(function () {
    // $('#id_owner').change()
    $('[aria-controls="select2-id_owner-container"]').removeClass("select2-selection select2-selection--single")
})

let elemtnts = document.querySelectorAll("input[type='text']")
for (var i = 0; i < elemtnts.length; ++i) {
    elemtnts[i].addEventListener('change', function(e) {
        this.parentNode.classList.add('has-success');
    });
}

$('#id_owner').on('change', function () {
    ajax_get_flat()
    if ($(this).val()) {
        this.parentNode.classList.remove('has-error')
        this.parentNode.classList.add('has-success')
    } else {
        this.parentNode.classList.remove('has-success')
        this.parentNode.classList.add('has-error')
    }
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


$(document).ready(function(){
    let form = document.getElementsByTagName('form')
    $('form').attr('action', window.location.pathname )
    console.log($('form'))
});

// AJAX
$(document).ready(function (){
            var flat = $(`#id_flat`);
            flat.value = flat_id
            console.log(flat)
            console.log(flat_id)

        })

