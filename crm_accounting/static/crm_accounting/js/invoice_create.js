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

$(document).ready( function CreateTable() {
        var table = $('#counters').DataTable(
            {
                "order": [],
                "bSortCellsTop": true,
                "bFilter": false,
                 "iDisplayLength": 10,
                "lengthChange": false,
                "language": {
                    "zeroRecords": "Ничего не найдено",
                    "info": "",
                    'infoFiltered': '',
                    "infoEmpty": "",
                    "paginate": {
                        "next":       "След.",
                        "previous":   "Пред."
                    },
                  },
                "aoColumnDefs": [
                    { 'bSortable': false, 'targets': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] },
                    ],
                "fnServerParams": function ( aoData ) {
                      aoData.push(
                          // { "name": 'number', "value": $('#number').val() },
                          // { "name": 'status', "value": $('#status').val() },
                          // { "name": 'date_range', "value": $('#date_range').val() },
                          // { "name": 'house', "value": $('#house').val() },
                          // { "name": 'section', "value": $('#section').val() },
                          // { "name": 'flat_number', "value": $('#flat_number').val() },
                          // { "name": 'service', "value": $('#service').val() },
                          { "name": 'id_flat', "value": $('#id_flat').val() },
                          // { "name": 'id_service', "value": $('#id_service').val() },
                      );
                },
                processing: true,
                serverSide: true,
                sAjaxSource: urlGetCounters,
                columns: [
                    {name: "number", data: 9},
                    {name: "status", data: null, render: function (data, type, row) {
                            if (row[10] === 'Новое') {
                                this.data = `<small class="label label-success">${row[10]}</small>`
                            } else if (row[10] === 'Учтено') {
                                this.data = `<small class="label label-warning">${row[10]}</small>`
                            } else if (row[10] === 'Учтено и оплачено') {
                                this.data = `<small class="label label-danger">${row[10]}</small>`
                            } else if (row[10] === 'Нулевое') {
                                this.data = `<small class="label label-null">${row[10]}</small>`
                            } else {
                                this.data = 'Не выбрано'
                            }
                            return this.data
                        }},
                    {name: "date_range", data: 11},
                    {name: "month", data: null, render: function(data, type, row) {
                            var months = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
                                "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"];
                            var myDate = new Date(row[11]);
                            var fullDate = months[myDate.getMonth()] + ' ' + myDate.getFullYear()
                            return fullDate
                        }},
                    {name: "house", data: 0},
                    {name: "section", data: 1},
                    {name: "flat_number", data: 2},
                    {name: "service", data: 3},
                    {name: "data", data: 4},
                    {name: "unit", data: 5},
                ],
            });

} );

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
        $('.ui-datepicker-trigger').html("<i class='fa fa-calendar'></i>").addClass('btn btn-date').before($("#id_date"));

        $("#id_period_start").datepicker({
                showOn: "both",
              dateFormat: "yy-mm-dd"

            });
        $('body > div.wrapper > div > form > section > div > div > div > div > div:nth-child(1) > div:nth-child(2) > div.row > div:nth-child(1) > div > div > button').html("<i class='fa fa-calendar'></i>").addClass('btn btn-date').after($("#id_period_start"));
        //
        $("#id_period_end").datepicker({
                showOn: "both",
              dateFormat: "yy-mm-dd"

            });
        $('body > div.wrapper > div > form > section > div > div > div > div > div:nth-child(1) > div:nth-child(2) > div.row > div:nth-child(2) > div > div > button').html("<i class='fa fa-calendar'></i>").addClass('btn btn-date').after($("#id_period_end"));

    })


