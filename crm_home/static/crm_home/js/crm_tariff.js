$('tr[data-href]').on("click", function() {
    document.location = $(this).data('href');
});


$('#add_service_update').click(function () {
    var form_idx = $('#id_service_update-TOTAL_FORMS').val();
	$('#formset_tariff_services').append($('#empty_form').html().replace(/__prefix__/g, form_idx));
	$('#id_service_update-TOTAL_FORMS').val(parseInt(form_idx) + 1);
})

$('#add_service').click(function () {
    var form_idx = $('#id_service-TOTAL_FORMS').val();
	$('#formset_tariff_services').append($('#empty_form').html().replace(/__prefix__/g, form_idx));
	$('#id_service-TOTAL_FORMS').val(parseInt(form_idx) + 1);
})

function delete_service(index) {
    console.log(index)
	const result = confirm('Удалить?')
		if (result) {
			// $('#id_' + name + '-name').removeAttr('value').removeAttr('required')
			$('.deleted_tariff_services').append('<input type="hidden" value="on" name="' + index  + '-DELETE" id="id_' + index + '-DELETE">');
			$('#' + index + '-form').css('display', 'none');
		}
		else {
		}
}

