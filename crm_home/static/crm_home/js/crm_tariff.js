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

$('.select-choose').change(function () {
	var textOption = $(this).find('option:selected').text()
	if (textOption === '---------') {
		$(`.`+this.id).text('Выберите...')
	} else {
		console.log(this.id)
		return get_unit(this.value[0], this.id)
	}
})

function changeUnit(self) {
	var textOption = $(self).find('option:selected').text()
	if (textOption === 'Выберите...') {
		$(`.`+self.id).text('Выберите...')
	} else {
		console.log(self.id)
		return get_unit(self.value[0], self.id)
	}
}




$('.btn-delete').click(function (event) {
	$('#'+ 'instance-'+ this.id).removeAttr('data-href')
	const result = confirm('Вы уверены, что хотите удалить этот элемент?')
	console.log(result)
	if (result) {
		delete_tariff(this.id)
	}
	event.stopPropagation()
})
