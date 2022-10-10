let reset = document.getElementById('reset')
reset.addEventListener("click", function () {
    let house = document.getElementById('house');
    house.value = '';
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
		delete_house(this.id)
	}
	event.stopPropagation()
})