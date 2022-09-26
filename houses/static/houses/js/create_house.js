$('#add_section').click(function () {
    var form_idx = $('#id_section-TOTAL_FORMS').val();
	$('#form_set_section').append($('#empty_form_section').html().replace(/__prefix__/g, form_idx));
	$('#id_section-TOTAL_FORMS').val(parseInt(form_idx) + 1);
	$('#id_section-'+ form_idx + '-title').val(`Секция ` + (parseInt(form_idx) + 1))
})


function delete_section(index) {
    console.log(index)
	const result = confirm('Удалить?')
		if (result) {
			$('.delete-list-section').append('<input type="hidden" value="on" name="' + index  + '-DELETE" id="id_' + index + '-DELETE">');
			$('#' + index + '-form').css('display', 'none');
		}
		else {
		}
}

$('#add_users').click(function () {
    var form_idx = $('#id_users-TOTAL_FORMS').val();
	$('#form_set_users').append($('#empty_form_users').html().replace(/__prefix__/g, form_idx));
	$('#id_users-TOTAL_FORMS').val(parseInt(form_idx) + 1);
	$('#id_users-'+ form_idx +'-name').on('change', function () {

		console.log(this.value)
		console.log(this.name)
		get_role(this.value, this.name)
	})
})

$('#nav-users select').on('change', function () {
	console.log(this.value)
	console.log(this.name)
	get_role(this.value, this.name)
})

function delete_user(index) {
	console.log(index)
	const result = confirm('Удалить?')
		if (result) {
			$('.delete-list-users').append('<input type="hidden" value="on" name="' + index  + '-DELETE" id="id_' + index + '-DELETE">');
			$('#' + index + '-form').css('display', 'none');
		}
		else {
		}
}

$('#add_floor').click(function () {
    var form_idx = $('#id_floor-TOTAL_FORMS').val();
	$('#form_set_floor').append($('#empty_form_floor').html().replace(/__prefix__/g, form_idx));
	$('#id_floor-TOTAL_FORMS').val(parseInt(form_idx) + 1);
	$('#id_floor-'+ form_idx + '-title').val(`Этаж ` + (parseInt(form_idx) + 1))
})

function delete_floor(index) {
    console.log(index)
	const result = confirm('Удалить?')
		if (result) {
			$('.delete-list-floor').append('<input type="hidden" value="on" name="' + index  + '-DELETE" id="id_' + index + '-DELETE">');
			$('#' + index + '-form').css('display', 'none');
		}
		else {
		}
}


let elemtnts = document.querySelectorAll("#house_form input[type='text']")
for (var i = 0; i < elemtnts.length; ++i) {
    elemtnts[i].addEventListener('blur', function(e) {
        this.parentNode.classList.add('has-success');
    });
}

let files = document.querySelectorAll("#house_form input[type='file']")
for (var s = 0; s < files.length; ++s) {
    files[s].addEventListener('blur', function(e) {
        this.parentNode.classList.add('has-success');
    });
}



