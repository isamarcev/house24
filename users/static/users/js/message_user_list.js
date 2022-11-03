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
                'bPaginate': false,
                "language": {
                    "zeroRecords": "Ничего не найдено",
                    "info": "",
                    'infoFiltered': '',
                    "infoEmpty": "",
                  },
                "aoColumnDefs": [
                    { 'bSortable': false, 'targets': [0, 1, 2, 3] },
                ],
                "fnServerParams": function ( aoData ) {
                      aoData.push(
                          { "name": 'search', "value": $('#id_search_field').val() },
                      );
                },
                processing: true,
                serverSide: true,
                sAjaxSource: UrlGetAjaxList,
                columns: [
                    {name: "id", data: null, render: function (data, type, row) {
                            console.log(row)
                        var id = row[0]
                            this.data = "<input type='checkbox' " + "class='select-alone'" +
                                   " name='selection-" + id + "' value='"+ id +"'>"
                            var element = $(`input[name='selection-` + id +`']`)
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
                    {name: "sender", data: 4},
                    {name: "text", data: null, render: function (data, type, row) {
                        let header = row[2];
                        let text = document.createElement('span');
                        text.innerHTML = row[1];
                        this.data = '<b>' + header + '</b>' + text.innerText;
                        return this.data
                        }},
                    {name: "date", data: null, render: function (data, type, row) {

                            var myDate = new Date(row[3]);
                            var minutes = myDate.getMinutes().toString()
                            if (minutes.length === 1) {
                                minutes = '0' + minutes
                            }
                            var fullDate = myDate.getDate() + '.' + myDate.getMonth() + '.' + myDate.getFullYear() +
                                ' - ' + myDate.getHours() + ':' + minutes
                            return fullDate
                        }},
                ],
                "createdRow": function( row, data, dataIndex ) {
                    var url = './'+data[0]
                    $(row).attr( 'data-href', url );
                    $(row).on("click", function() {
                        document.location = $(this).data('href');
                        });
            }
            });
        $('#id_search_field').on('change blur', function () {
            table.columns(1).search($(this).val()).draw();
        } );
    } );

$('#select-on-check-all').click(function (event) {
    if ($(this).is(':checked')) {
        DeletionArray = [];
        $('.select-alone').prop('checked', true);
        $('.select-alone').each(function () {
            DeletionArray.push($(this).val());
        })
        $('#select-on-check-all-bottom').prop('checked', true);
        console.log(DeletionArray)
    } else {
        $('.select-alone').prop('checked', false);
        $('#select-on-check-all-bottom').prop('checked', false);
        DeletionArray = [];
        console.log(DeletionArray)
    }
    event.stopPropagation()

})

$('#select-on-check-all-bottom').click(function (event) {
    if ($(this).is(':checked')) {
        DeletionArray = [];
        $('.select-alone').prop('checked', true);
        $('.select-alone').each(function () {
            DeletionArray.push($(this).val());
        })
        $('#select-on-check-all').prop('checked', true);
        console.log(DeletionArray)
    } else {
        $('.select-alone').prop('checked', false);
        $('#select-on-check-all').prop('checked', false);
        DeletionArray = [];
        console.log(DeletionArray)
    }
    event.stopPropagation()

})

$('.btn-select').on('click', function () {
    var child = $(this).children('input');
    child.click()

})

$(document).ready( function () {
        $('.odd').css('background-color', '#f9f9f9')
    })


function delete_selected() {
    const result = confirm('Вы уверены, что хотите удалить выбранные сообщения?')
    let Del = DeletionArray
    if (result) {
        var csrf = $("input[name=csrfmiddlewaretoken]").val();
        $.ajax({
            url: UrlMessageDelete,
            type: 'post',
            data: {
                'deleted_list': Del.toString(),
                csrfmiddlewaretoken: csrf,
            },
            success: (data) => {
                if (data.success === 'success') {
                    $('#id_search_field').change()
                } else {
                    alert(data.success)
                }
            },
            errors: (errors) => {
            console.log(errors)
        }
    })}
}
