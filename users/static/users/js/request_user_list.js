
// DATATABLE
$(document).ready( function CreateTable() {
        var table = $('#requests').DataTable(
            {
                "order": [],
                "bSortCellsTop": true,
                "bFilter": false,
                 "iDisplayLength": 10,
                "lengthChange": false,
                // 'bPaginate': false,
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
                    { 'bSortable': false, 'targets': [0, 1, 2, 3, 4, 5] },
                ],
                "fnServerParams": function ( aoData ) {
                      aoData.push(
                          { "name": 'reboot', "value": $('#reboot').val() },
                      );
                },
                processing: true,
                serverSide: true,
                sAjaxSource: RequestListUrl,
                columns: [
                    {name: "id", data: 0},
                    {name: "sender", data: 1},
                    {name: "text", data: 2},
                    {name: "date", data: null, render: function (data, type, row) {
                            console.log(row);
                            var myDate = row[3].split('-');
                            var myTime = row[4].split(':');
                            var fullDate = myDate[2] + '.' + myDate[1] + '.' + myDate[0] +
                                ' - ' + myTime[0] + ':' + myTime[1]
                            return fullDate
                        }},
                    {name: "status", data: null, render: function (data, type, row) {
                        var status = row[5];
                        if (status === 'Новое') {
                            this.data = `<small class="label label-null">${status}</small>`
                        } else if (status === 'В работе') {
                            this.data = `<small class="label label-warning">${status}</small>`
                        } else if (status === 'Выполнено') {
                            this.data = `<small class="label label-success">${status}</small>`
                        } else {
                            this.data = "Не выбрано"
                        }
                        return this.data
                        }},
                    {name: "delete", data: null, render: function (data, type, row) {
                            return '<div class="btn-group pull-right">' +
                                '<a class="btn btn-default btn-sm btn-delete" onclick="delete_request(event, this)" id="' + row[0] + '" title="Удалить">' +
                                '<i class="fa fa-trash"></i>' +
                                '</a></div>'
                        }},


                ],
            });
            $('#reboot').on('change clear', function () {
                table.search($(this).val()).draw();
            });
    } );


function delete_request(event, elem) {
            const result = confirm('Вы уверены, что хотите удалить эту заявку?')
            if (result) {
                var csrf = $("input[name=csrfmiddlewaretoken]").val();
                $.ajax({
                    url: RequestDeleteUrl,
                    type: 'post',
                    data: {
                        'id': elem.id,
                        csrfmiddlewaretoken: csrf,
                    },
                    success: (data) => {
                        if (data.success === 'success') {
                            $('#reboot').change()
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


$(document).ready( function () {
        $('.odd').css('background-color', '#f9f9f9')
    })

