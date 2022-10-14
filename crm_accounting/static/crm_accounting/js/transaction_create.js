function get_personal_accounts (){
            const owner_id = ($("#id_owner").val())
            var empty_value = '<option value="">Выберите...</option>'
            if (owner_id) {
                $.ajax({
                url: urlGet,
                type: 'get',
                data: {
                    'owner_id': owner_id,
                },
                success: (data) => {
                    var id_personal_account = $('#id_personal_account');
                    id_personal_account.empty()
                    id_personal_account.append(empty_value)
                    console.log(data)
                    var accounts = '';
                    $(data.accountList).each(function (index, value) {
                        accounts += "<option value='"+value.id+"'>"+value.account_number+"</option>"
                    })
                    id_personal_account.append(accounts)
                }
            })
            } else {
                $('#id_personal_account').empty()
                $('#id_personal_account').append(empty_value)
            }
        }

$(document).ready(function() {
    $("#id_owner").select2({
        tags: true,
        selectionCssClass: 'form-select'
    });
    $("#id_personal_account").select2({
        tags: true,
        selectionCssClass: 'form-select'
    })
})

$(document).ready(function () {
    $("#id_owner").on('change', get_personal_accounts)
    $('[aria-controls="select2-id_owner-container"]').removeClass("select2-selection select2-selection--single")
    $('body > div.wrapper > div > form > section > div > div > div > div > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > span > span.selection > span').removeClass("select2-selection select2-selection--single")
})

let selects = document.querySelectorAll("select")
for (var x = 0; x < selects.length; ++x) {
    selects[x].addEventListener('blur', function(e) {
        this.parentNode.classList.add('has-success');
        this.parentNode.querySelectorAll('.errorlist')[0].style.display = 'none'
    });
}

let input = document.querySelectorAll("input")
for (var y = 0; y < selects.length; ++y) {
    input[y].addEventListener('blur', function(e) {
        this.parentNode.classList.add('has-success');
        this.parentNode.querySelectorAll('.errorlist')[0].style.display = 'none'

    });
}

$(function () {
        $("#id_date").datepicker({
                showOn: "both",
              dateFormat: "yy-mm-dd"

            });
        $('.ui-datepicker-trigger').html("<i class='fa fa-calendar'></i>").addClass('btn btn-date').before($("#id_date"))

    })


