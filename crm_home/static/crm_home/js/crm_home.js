

$('#add_service').click(function () {
    var form_idx = $('#id_service-TOTAL_FORMS').val();
	$('#form_set_services').append($('#empty_form_services').html().replace(/__prefix__/g, form_idx));
	$('#id_service-TOTAL_FORMS').val(parseInt(form_idx) + 1);
})


$('#add_unit').click(function () {
    var form_idx = $('#id_unit-TOTAL_FORMS').val();
	$('#form_set_unit').append($('#empty_form_unit').html().replace(/__prefix__/g, form_idx));
	$('#id_unit-TOTAL_FORMS').val(parseInt(form_idx) + 1);
})



function delete_service(name) {
	console.log(name)
	const result = confirm('Удалить?')
		if (result) {
			$('#id_' + name + '-name').removeAttr('value').removeAttr('required')
			$('.delete-list-service').append('<input type="hidden" value="on" name="' + name  + '-DELETE" id="id_' + name + '-DELETE">');
			$('#' + name + '-form').css('display', 'none');
		}
		else {
		}
}

function delete_unit(index) {
	const result = confirm('Удалить?')
	console.log(result)
		if (result) {
			$('.delete-list-unit').append('<input type="hidden" value="on" name="' + index  + '-DELETE" id="id_' + index + '-DELETE">');
			$('#' + index + '-form').css('display', 'none');
		}
		else {

		}
}


function cannotDelete() {
	alert("Эта единица измерения используется в услугах. Удаление невозможно.")
}

function cannotDeleteService() {
	alert("Эта услуга используется в услугах. Удаление невозможно.")
}