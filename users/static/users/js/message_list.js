let DeletionArray = [];


// DATATABLE
$(document).ready( function CreateTable() {
        var table = $('#messages').DataTable(
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
                    { 'bSortable': false, 'targets': [0, 1, 2, 3] },
                ],
                "fnServerParams": function ( aoData ) {
                      aoData.push(
                          { "name": 'search', "value": $('#search').val() },
                      );
                },
                processing: true,
                serverSide: true,
                sAjaxSource: UrlGetAjaxList,
                columns: [
                    {name: "id", data: null, render: function (data, type, row) {
                            console.log(row)
                            console.log(data)
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
                ],
                "createdRow": function( row, data, dataIndex ) {
                    var url = 'detail/'+data[1]
                    $(row).attr( 'data-href', url );
                    $(row).on("click", function() {
                        document.location = $(this).data('href');
                        });
            }
            });
        $('#search').on('change blur', function () {
            table.columns(1).search($(this).val()).draw();
        } );
    } );

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

$(document).ready( function () {
        $('.odd').css('background-color', '#f9f9f9')
    })


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
