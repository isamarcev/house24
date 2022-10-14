$(function() {
      $('#date').daterangepicker({
          autoUpdateInput: false,
          locale: {
              cancelLabel: 'Clear'
          }
      });

      $('#date').on('apply.daterangepicker', function(ev, picker) {
          $(this).val(picker.startDate.format('MM-DD-YYYY') + ' - ' + picker.endDate.format('MM-DD-YYYY'));
          $(this).blur()
      });

      $('#date').on('cancel.daterangepicker', function(ev, picker) {
          $(this).val('');
          $(this).click()
      });

});
    <!-- AJAX -->
function delete_transaction(event, elem) {
            const result = confirm('Вы уверены, что хотите удалить этоу квартиру?')
            if (result) {
                var csrf = $("input[name=csrfmiddlewaretoken]").val();
                $.ajax({
                    url: UrlDeleteTransaction,
                    type: 'post',
                    data: {
                        'account': elem.id,
                        csrfmiddlewaretoken: csrf,
                    },
                    success: (data) => {
                        if (data.success === 'success') {
                            $('#reset').click()
                        } else {
                            alert(data.success)
                        }
                    },
                    errors: (errors) => {
                    console.log(errors)
                }
            })}
            event.stopPropagation()

        }

$(document).ready( function CreateTable() {
    var table = $('#flats').DataTable(
        {
            "order": [],
            "bSortCellsTop": true,
            "bFilter": false,
            "iDisplayLength": 10,
            "lengthChange": false,
            "language": {
                "zeroRecords": "Ничего не найдено",
                "info": "Количество квартир:  _MAX_",
                'infoFiltered': '',
                "infoEmpty": "",
                "paginate": {
                    "next":       "След.",
                    "previous":   "Пред."
                },
            },
            "aoColumnDefs": [
                { 'bSortable': false, 'targets': [0, 2, 3, 4, 5, 6, 7, 8] },
            ],
            "fnServerParams": function ( aoData ) {
                aoData.push(
                    { "name": 'number', "value": $('#number').val() },
                    { "name": 'date', "value": $('#date').val() },
                    { "name": 'completed', "value": $('#completed').val() },
                    { "name": 'paymentstate', "value": $('#paymentstate').val() },
                    { "name": 'owner', "value": $('#owner').val() },
                    { "name": 'personal_account', "value": $('#personal_account').val() },
                    { "name": 'type_of_payment', "value": $('#type_of_payment').val() },
                      );},
            processing: true,
            serverSide: true,
            sAjaxSource: UrlTransactionList,
            columns: [
                {name: "number", data: 0},
                {name: "date_range", data: 1},
                {name: "completed", data: null, render: function (data, type, row) {
                    let status = row[2];
                    if (status === 'False') {
                        this.data = 'Не проведен';
                    } else if (status === 'True') {
                        this.data = 'Проведен';
                    }
                    return this.data
                    } },
                {name: "paymentstate", data: 3},
                {name: "owner", data: 4},
                {name: "personal_account", data: 5},
                {name: "type_of_payment", data: null, render: function (data, type, row) {
                    let type_of_payment = row[6];
                    if (type_of_payment === 'Приход') {
                        this.data = `<p style='color: #00a65a'>${type_of_payment}</p>`;
                    } else {
                        this.data = `<p style='color: #dd4b39'>${type_of_payment}</p>`;
                    }
                    return this.data
                    }},
                {name: "amount", data: null, render: function (data, type, row) {
                            let amount = row[7];
                            if (row[6] === 'Приход') {
                                this.data = `<p style="color: #00a65a">${amount}</p>`
                            } else if (row[6] === 'Расход') {
                                this.data = `<p style="color: #dd4b39">-${amount}</p>`
                            }
                            return this.data
                        }
                    },
                {name: 'link', data: null, render: function (data, type, row){
                        var url = 'update'
                            return '<div class="btn-group pull-right" >'+
                                '<a class="btn btn-default btn-sm" href="'+url+'/'+row[8]+'" title="Редактировать">'+
                                '<i class="fa fa-pencil"></i></a>'+
                                '<a class="btn btn-default btn-sm btn-delete" onclick="delete_transaction(event, this)" id="'+row[8]+'" title="Удалить">'+
                                '<i class="fa fa-trash " ></i></a></div>'
                        }}
                ],
                "createdRow": function( row, data, dataIndex ) {
                    console.log(data)
                    console.log(row)
                    var url = 'detail/'+data[8]
                    $(row).attr( 'data-href', url );
                    $(row).on("click", function() {
                        document.location = $(this).data('href');
                        });
            }
            });
        $('#number').on('change blur click', function () {
            table.columns(0).search($(this).val()).draw();
        } );
        $('#date').on('change blur clear', function () {
            table.columns([1]).search($(this).val()).draw();
        });
        $('#completed').on('change clear', function () {
            table.columns([2]).search($(this).val()).draw();
        });
        $('#paymentstate').on('change clear', function () {
            table.columns([3]).search($(this).val()).draw();
        });
        $('#owner').on('change clear', function () {
            table.columns([4]).search($(this).val()).draw();
        });
        $('#personal_account').on('change clear', function () {
            table.columns([5]).search($(this).val()).draw();
        });
        $('#type_of_payment').on('change clear', function () {
            table.columns([6]).search($(this).val()).draw();
        });
    } );

let reset = document.getElementById('reset')
reset.addEventListener("click", function () {
    let number = document.getElementById('number');
    number.value = '';
    let date = document.getElementById('date');
    date.value = '';
    let completed = document.getElementById('completed');
    completed.value = '';
    let paymentstate = document.getElementById('paymentstate');
    paymentstate.value = '';
    let owner = document.getElementById('owner');
    owner.value = '';
    let personal_account = document.getElementById('personal_account');
    personal_account.value = '';
    let type_of_payment = document.getElementById('type_of_payment');
    type_of_payment.value = '';
    let event = new Event('blur')
    number.dispatchEvent(event)
})


$('tr[data-href]').on("click", function() {
    document.location = $(this).data('href');
});


