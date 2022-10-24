let DeletionArray = [];


function delete_invoice(event, elem) {
    const result = confirm('Вы уверены, что хотите удалить эту квитанцию?')
    let newArray = [];
    newArray.push(elem.id)
    if (result) {
        var csrf = $("input[name=csrfmiddlewaretoken]").val();
        $.ajax({
            url: urlInvoiceDelete,
            type: 'post',
            data: {
                'deleted_list': newArray.toString(),
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


// DATATABLE
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
                    "info": "Количество квитанций:  _MAX_",
                    'infoFiltered': '',
                    "infoEmpty": "",
                    "paginate": {
                        "next":       "След.",
                        "previous":   "Пред."
                    },
                  },
                "aoColumnDefs": [
                    { 'bSortable': false, 'targets': [0, 1, 2, 5, 6, 7, 8, 9] },
                ],
                "fnServerParams": function ( aoData ) {
                      aoData.push(
                          { "name": 'number', "value": $('#number').val() },
                          { "name": 'status', "value": $('#status').val() },
                          { "name": 'date', "value": $('#date').val() },
                          { "name": 'month', "value": $('#month').val() },
                          { "name": 'flat', "value": $('#flat').val() },
                          { "name": 'owner', "value": $('#owner').val() },
                          { "name": 'payment_state', "value": $('#payment_state').val() },

                      );
                },
                processing: true,
                serverSide: true,
                sAjaxSource: urlInvoiceList,
                columns: [
                    {name: "id", data: null, render: function (data, type, row) {
                        var id = row[8]
                            this.data = "<input type='checkbox' " + "class='select-alone'" +
                                   " name='selection-" + id + "' value='"+ id +"'>"
                            var element = $(`input[name='selection-` + id +`']`)
                            console.log(element)
                            element.click(event, function () {
                                if (element.is(':checked')) {
                                    DeletionArray.push(element.val());


                            } else if(!element.is(':checked')) {
                                    let i = DeletionArray.indexOf(element.val())
                                    DeletionArray.splice(i, 1);
                                    $('#select-on-check-all').prop('checked', false)
                            }
                                event.stopPropagation()
                            } )

                            return this.data
                        }},
                    {name: "number", data: 0},
                    {name: "status", data: null, render: function (data, type, row) {
                            console.log(row[1])
                        if (row[1] === 'Оплачена') {
                            this.data = `<small class="label label-success">${row[1]}</small>`
                        } else if (row[1] === 'Неоплачена') {
                            this.data = `<small class="label label-danger">${row[1]}</small>`
                        } else if (row[1] === 'Частично оплачена') {
                            this.data = `<small class="label label-warning">${row[1]}</small>`
                        } else {
                            this.data = "Не выбран"
                        }
                            return this.data
                        }},
                    {name: "date", data: 2},
                    {name: "month", data: null, render: function (data, type, row) {
                            var months = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
                                    "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"];
                                var myDate = new Date(row[2]);
                                var fullDate = months[myDate.getMonth()] + ' ' + myDate.getFullYear()
                                return fullDate
                        }},
                    {name: "flat", data: null, render: function (data, type, row) {
                            var flat = row[3] + ', ' + row[4]
                            return flat
                        }},
                    {name: "owner", data: 5},
                    {name: "payment_state", data: null, render: function (data, type, row) {
                            var value = row[6]
                            if (value === 'False') {
                                this.data = "Не проведена"
                            } else if (value === 'True') {
                                this.data = "Проведена"
                            }
                            return this.data
                        }},
                    {name: "amount", data: 7},
                    {name: 'link', data: null, render: function (data, type, row){
                            console.log(row[8])
                        var url = 'update'
                            return '<div class="btn-group pull-right" >'+
                                '<a class="btn btn-default btn-sm" href="'+url+'/'+row[8]+'" title="Редактировать">'+
                                '<i class="fa fa-pencil"></i></a>'+
                                '<a class="btn btn-default btn-sm btn-delete" onclick="delete_invoice(event, this)" id="'+row[8]+'" title="Удалить">'+
                                '<i class="fa fa-trash " ></i></a></div>'
                        }}
                ],
                "createdRow": function( row, data, dataIndex ) {
                    var url = 'detail/'+data[8]
                    $(row).attr( 'data-href', url );
                    $(row).on("click", function() {
                        document.location = $(this).data('href');
                        });
            }
            });
        $('#number').on('change blur', function () {
            table.columns(1).search($(this).val()).draw();
        } );
        $('#status').on('change clear', function () {
            table.columns([2]).search($(this).val()).draw();
        });
        $('#date').on('change clear', function () {
            table.columns([3]).search($(this).val()).draw();
        });
        $('#month').on('change clear', function () {
            table.columns([4]).search($(this).val()).draw();
        });
        $('#flat').on('change clear', function () {
            table.columns([5]).search($(this).val()).draw();
        });
        $('#owner').on('change clear', function () {
            table.columns([6]).search($(this).val()).draw();
        });
        $('#payment_state').on('change clear', function () {
            table.columns([7]).search($(this).val()).draw();
        });
    } );

let reset = document.getElementById('reset')
reset.addEventListener("click", function () {
    let number = document.getElementById('number');
    number.value = '';
    let status = document.getElementById('status');
    status.value = '';
    let flat = document.getElementById('flat');
    flat.value = '';
    let owner = document.getElementById('owner');
    owner.value = '';
    let payment_state = document.getElementById('payment_state');
    payment_state.value = '';
    let date = document.getElementById('date');
    date.value = '';
    let month = document.getElementById('month');
    month.value = '';
    let checkbox = document.getElementById('select-on-check-all')
    checkbox.checked = false;
    let event = new Event('change')
    number.dispatchEvent(event);
    checkbox.dispatchEvent(event);
})

$('#select-on-check-all').change(function () {
    if ($(this).is(':checked')) {
        DeletionArray = [];
        $('.select-alone').prop('checked', true);
        $('.select-alone').each(function () {
            DeletionArray.push($(this).val());
        })
        console.log(DeletionArray)
    } else {
        $('.select-alone').prop('checked', false);
        DeletionArray = [];
    }
})

$('tr[data-href]').on("click", function() {
    document.location = $(this).data('href');
});



$('.btn-delete').click(function (event) {
	$('#'+ 'instance-'+ this.id).removeAttr('data-href')
	const result = confirm('Вы уверены, что хотите удалить этот дом?')
	console.log(result)
	if (result) {
		delete_house(this.id)
	}
	event.stopPropagation()
})


$(document).ready( function () {
        $('.odd').css('background-color', '#f9f9f9')
    })

$(function() {
            $('#month').datepicker( {
            changeMonth: true,
            changeYear: true,
            showButtonPanel: true,
            dateFormat: 'MM yy',

            onClose: function(dateText, inst) {
                $(this).datepicker(
                    'setDate',
                    new Date(inst.selectedYear,
                    inst.selectedMonth, 1)
                );
                $(this).change()
            }
            });
            $('#ui-datepicker-div > table').css('display', 'none')
        });

function delete_selected() {
    const result = confirm('Вы уверены, что хотите удалить выбранные?')
    let Del = DeletionArray
    if (result) {
        var csrf = $("input[name=csrfmiddlewaretoken]").val();
        $.ajax({
            url: urlInvoiceDelete,
            type: 'post',
            data: {
                'deleted_list': Del.toString(),
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
}

$(function() {
              $('#date').daterangepicker({
                  autoUpdateInput: false,
                  locale: {
                      cancelLabel: 'Clear'
                  }
              });

              $('#date').on('apply.daterangepicker', function(ev, picker) {
                  $(this).val(picker.startDate.format('MM-DD-YYYY') + ' - ' + picker.endDate.format('MM-DD-YYYY'));
                  $(this).change()
              });

              $('#date').on('cancel.daterangepicker', function(ev, picker) {
                  $(this).val('');
                  $(this).change()
              });

            });
