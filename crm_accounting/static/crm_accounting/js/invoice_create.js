function get_section() {
    var house_id = ($("#id_house"))
    var section_id = ($("#id_section"))
    var flat_id = ($("#id_flat"))
    var owner = ($('#owner'))
    var phone = ($('#phone'))
    var personal_account = ($('#id_personal_account'))
    var empty_value = '<option value="">Выберите...</option>'

    if (house_id) {
        $.ajax({
            url: urlGetSection,
            type: 'get',
            data: {
                'house_id': house_id.val(),
            },
            success: (data) => {
                section_id.empty().append(empty_value)
                flat_id.empty().append(empty_value)
                personal_account.empty()
                owner.html('не выбран')
                phone.html('не выбран')
                console.log(data)
                var sections = "";
                $(data.data).each(function(index, value) {
                    sections += "<option value='"+value.section_id+"'>"+value.section_title+"</option>"
                })
                section_id.append(sections)
            }
        })
    }
}

function get_info_by_flat() {
    var flat_id = ($("#id_flat"))
    var personal_account = ($('#id_personal_account'))
    var owner = ($("#owner"))
    var phone = ($("#phone"))
    owner.html('не выбран')
    phone.html('не выбран')
    personal_account.val('')
    if (flat_id) {
        $.ajax({
                url: urlGetInfoByFlat,
                type: 'get',
                data: {
                    'flat_id': flat_id.val(),
                },
                success: (data) => {
                    console.log(data)
                    if (data.data.owner) {
                        var link = "<a class='link-list' href='../../../users/owner/detail/" + data.data.owner.id + "'>" + data.data.owner.owner + "</a>"
                        owner.html(link)
                        phone.html(data.data.owner.phone)
                    }
                    if (data.data.personal_account) {
                        personal_account.val(data.data.personal_account)
                    }
                }
        }
    )
    }
}


function get_flat() {
    var section_id = ($("#id_section"))
    var flat_id = ($("#id_flat"))
    var personal_account = ($('#id_personal_account'))
    var empty_value = '<option value="">Выберите...</option>'
    flat_id.empty().append(empty_value)
    if (section_id) {
            $.ajax({
                url: urlGetFlat,
                type: 'get',
                data: {
                    'section_id': section_id.val(),
                },
                success: (data) => {
                    console.log(data)
                    var flats = "";
                    $(data.flats).each(function(index, value) {
                    flats += "<option value='"+value.flat_id+"'>"+value.flat_title+"</option>"
                    })
                    flat_id.append(flats)
                    var owner = ($('#owner'))
                    var phone = ($('#phone'))
                    owner.html('ые выбран')
                    phone.html('ые выбран')
                    personal_account.val('')
                }
        }
    )}
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
                          { "name": 'id_flat', "value": $('#id_flat').val() },
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
        $('#id_flat').on('change', function () {
            table.columns(6).search($(this).val()).draw();
        } );

} );

var totalPrice = $('#price-total')
console.log(totalPrice)

function get_total_created(form_idx) {
        var amount = $('#id_form-'+ parseInt(form_idx) + '-amount_id');
        var price = $('#id_form-'+ parseInt(form_idx) + '-price_id');
        if (amount.val() && price.val()) {
            var total = (amount.val() * price.val()).toFixed(2)
        } else {
            total = (0).toFixed(2)
        }
        $('#id_form-'+ parseInt(form_idx) + '-total_id').val(total)
    var TotalAmount = $('#id_amount')
    var nowTotalPrice = 0
    totalPrice.empty()
    $('.total-price').each(function () {
        if ($(this)[0].value) {
            nowTotalPrice += parseFloat($(this)[0].value)
        }

    })
    TotalAmount.val(nowTotalPrice)
    totalPrice.text(nowTotalPrice.toFixed(2))
}

function get_total_row(form_idx) {
        var amount = $('#id_form-'+ parseInt(form_idx.data) + '-amount_id');
        var price = $('#id_form-'+ parseInt(form_idx.data) + '-price_id');
        if (amount.val() && price.val()) {
            var total = (amount.val() * price.val()).toFixed(2)
        } else {
            total = (0).toFixed(2)
        }
        $('#id_form-'+ parseInt(form_idx.data) + '-total_id').val(total)
    var TotalAmount = $('#id_amount')
    var nowTotalPrice = 0
    totalPrice.empty()
    $('.total-price').each(function () {
        if ($(this)[0].value) {
            nowTotalPrice += parseFloat($(this)[0].value)
        }

    })
    TotalAmount.val(nowTotalPrice)
    totalPrice.text(nowTotalPrice.toFixed(2))
}

$("#add_service").click(function () {
    var form_idx = $('#id_form-TOTAL_FORMS').val();
	$('#formset').append($('#empty_form').html().replace(/__prefix__/g, form_idx));
	$('#id_form-TOTAL_FORMS').val(parseInt(form_idx) + 1);
	$('#id_form-'+ form_idx + '-amount_id').change(form_idx, get_total_row)
	$('#id_form-'+ form_idx + '-price_id').change(form_idx, get_total_row)
    $('#id_form-'+ form_idx + '-total_id').addClass('total-price')

})

$(document).ready(function () {
    $("#id_house").on('change', get_section)
    $("#id_section").on('change', get_flat)
    $("#id_flat").on('change', get_info_by_flat)

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

        $('#id_amount').val(parseInt(totalPrice.text()))

    })


function delete_service(index) {
    $('.delete-list-service').append('<input type="hidden" value="on" name="' + index  + '-DELETE" id="id_' + index + '-DELETE">');
    $('#' + index + '-form').css('display', 'none');
    // $('#id_'+ index + '-total_id').val(0)
    $('#id_'+ index + '-amount_id').val(0)
    $('#id_'+ index + '-amount_id').change()
}


$('.set-tariff-services').click(function () {
    var tariff = $('#id_tariff')

    if (tariff.val()) {
            $('.form-row-remove-btn').each(function () {
                if (this.name != 'form-__prefix__') {
                    this.click()
                }});
            $.ajax(
            {
                url: urlSetTariff,
                type: 'get',
                data: {'tariff': tariff.val()},
                success: (data) => {
                    console.log(data)
                    console.log(data.services)
                    console.log(data.services.length)
                    var formset = $('#formset')
                    var add_buttoon = $("#add_service")
                    var form_idx = parseInt($('#id_form-TOTAL_FORMS').val());
                    $(data.services).each(function (index, value) {
                        add_buttoon.click();
                        $('#id_form-'+form_idx+`-service_id`).find(`option[value=${value.service_id}]`).prop('selected', true);;
                        $('#id_form-'+form_idx+`-unit_id`).find(`option[value=${value.unit_id}]`).prop('selected', true);;
                        $('#id_form-'+form_idx+`-price_id`).val(parseFloat(value.price));

                        form_idx += 1

                    })
                    $('#id_form-TOTAL_FORMS').val(form_idx);
                }
            })
        }
         else {
                alert('Выберите тариф.')
                tariff.closest('div').addClass('has-error')
            }

})

