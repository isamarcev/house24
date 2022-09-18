let btn = document.getElementById('add_form')
console.log(btn)


$('#add_form').click(function() {
	var form_idx = $('#id_form-TOTAL_FORMS').val();
	$('#form_set').append($('#empty_form').html().replace(/__prefix__/g, form_idx));
	$('#id_form-TOTAL_FORMS').val(parseInt(form_idx) + 1);
});

function delete_form(index) {
	console.log(index)
	$('#id_' + index + '-document')[0].value="";
	$('.delete-list').append('<input type="hidden" value="on" name="' + index  + '-DELETE" id="id_' + index + '-DELETE">');
	$('#' + index + '-form').css('display', 'none');
	$('#' + index + '-title').css('display', 'none');
}


$('#add_service').click(function () {
	var form_idx = $('#id_form-TOTAL_FORMS').val();
	$('#formset').append($('#empty_form').html().replace(/__prefix__/g, form_idx));
	$('#id_form-TOTAL_FORMS').val(parseInt(form_idx) + 1);
	$('#id_form-'+ form_idx +'-text')
	CKEDITOR.replace( 'form-'+ form_idx +'-text' );

})


function delete_service(index) {
	console.log(index)
	$('#id_' + index + '-image')[0].value="";
	$('.delete-list').append('<input type="hidden" value="on" name="' + index  + '-DELETE" id="id_' + index + '-DELETE">');
	$('#' + index + '-form').css('display', 'none');

}



var link = 'https://seeklogo.com/images/A/Adobe_PDF-logo-84B633809C-seeklogo.com.png'

// VALIDATION SIZE AND FORMAT
$('.doc-valid').change(function () {
	var x = $(this)
	var fileExtension = ['jpg', 'pdf'];
	var name = this.files[0].name;
	var size = this.files[0].size;
	console.log($(this).closest('img'));
	if ($.inArray(name.split('.').pop().toLowerCase(), fileExtension)==-1 || 20000000 < size) {
		x.siblings().css('color', 'red')
		$('#btn-save').attr('disabled', 'disabled')
	}
	else {
		x.siblings().css('color', '#333333')
		$('#btn-save').removeAttr('disabled')
		// x.parent().parent().children('img')
	}
})

$(function () {
	var x = $('#form_set img')
	var fileExtension = ['pdf'];
	x.each(function() {
		if ($.inArray($(this).attr('src').split('.').pop().toLowerCase(), fileExtension)!=-1) {
			$(this).attr('src', link);
	}
	})
})






