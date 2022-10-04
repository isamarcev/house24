let reset = document.getElementById('reset')
reset.addEventListener("click", function () {
    let house = document.getElementById('house');
    house.value = '';
    let number = document.getElementById('number');
    number.value = '';
    let section = document.getElementById('section');
    section.value = '';
    let dolg = document.getElementById('dolg');
    dolg.value = '';
    let floor = document.getElementById('floor');
    floor.value = '';
    let owner = document.getElementById('owner');
    owner.value = '';


    let event = new Event('blur')
    number.dispatchEvent(event)
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