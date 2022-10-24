let DeletionArray = [];


// DATATABLE
$(document).ready( function CreateTable() {
        var table = $('#invoices').DataTable(
            {
                "order": [],
                "bSortCellsTop": true,
                "bFilter": false,
                 "iDisplayLength": 10,
                "lengthChange": false,
                'bPaginate': false,
                "language": {
                    "zeroRecords": "Ничего не найдено",
                    "info": "",
                    'infoFiltered': '',
                    "infoEmpty": "",
                  },
                "aoColumnDefs": [
                    { 'bSortable': false, 'targets': [0, 2, 3] },
                ],
                "fnServerParams": function ( aoData ) {
                      aoData.push(
                          { "name": 'date', "value": $('#date').val() },
                          { "name": 'flat', "value": $('#id_flat').val() },
                          { "name": 'status', "value": $('#status').val() },
                          { "name": 'user', "value": $('#id_user').val() },
                      );
                },
                processing: true,
                serverSide: true,
                sAjaxSource: InvoiceAjaxUrl,
                columns: [
                    {name: "number", data: 1},
                    {name: "date", data: 2},
                    {name: "status", data: null, render: function (data, type, row) {
                            console.log(row[3])
                        if (row[3] === 'Оплачена') {
                            this.data = `<small class="label label-success">${row[3]}</small>`
                        } else if (row[3] === 'Неоплачена') {
                            this.data = `<small class="label label-danger">${row[3]}</small>`
                        } else if (row[3] === 'Частично оплачена') {
                            this.data = `<small class="label label-warning">${row[3]}</small>`
                        } else {
                            this.data = "Не выбран"
                        }
                            return this.data
                        }},
                    {name: "amount", data: 4},
                ],
                "createdRow": function( row, data, dataIndex ) {
                    var url = './'+data[0]
                    $(row).attr( 'data-href', url );
                    $(row).on("click", function() {
                        document.location = $(this).data('href');
                        });
            }
            });
        $('#status').on('change clear', function () {
            table.columns([2]).search($(this).val()).draw();
        });
        $('#date').on('change clear', function () {
            table.columns([3]).search($(this).val()).draw();
        });
    } );


$('tr[data-href]').on("click", function() {
    document.location = $(this).data('href');
});

$(document).ready( function () {
        $('.odd').css('background-color', '#f9f9f9')
    })


let reset = document.getElementById('reset')
reset.addEventListener("click", function () {
    let status = document.getElementById('status');
    status.value = '';
    let date = document.getElementById('date');
    date.value = '';
    let event = new Event('change')
    status.dispatchEvent(event);
})

$(function() {
            $('#date').datepicker( {
            })
});