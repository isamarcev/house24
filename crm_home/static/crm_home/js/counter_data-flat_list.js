let reset = document.getElementById('reset')
reset.addEventListener("click", function () {
    let house = document.getElementById('house');
    house.value = '';
    let date_range = document.getElementById('date_range')
    date_range.value = '';
    let flat_number = document.getElementById('flat_number');
    let status = document.getElementById('status');
    status.value = '';

    flat_number.value = '';
    let number = document.getElementById('flat_number');
    number.value = '';
    let section = document.getElementById('section');
    section.value = '';
    let service = document.getElementById('service');
    service.value = '';
    let event = new Event('change')
    house.dispatchEvent(event)
})


$('tr[data-href]').on("click", function() {
    document.location = $(this).data('href');
});



$('.btn-delete').click(function (event) {
	$('#'+ 'instance-'+ this.id).removeAttr('data-href')
	const result = confirm('Вы уверены, что хотите удалить этот дом?')
	console.log(result)
	if (result) {
		delete_counter(this.id)
	}
	event.stopPropagation()
})