$('tr[data-href]').on("click", function() {
    document.location = $(this).data('href');
});



let selects = document.querySelectorAll("select")
for (var x = 0; x < selects.length; ++x) {
    selects[x].addEventListener('blur', function(e) {
        this.parentNode.classList.add('has-success');
    });
}

let elemtnts = document.querySelectorAll("input[type='text']")
for (var i = 0; i < elemtnts.length; ++i) {
    elemtnts[i].addEventListener('blur', function(e) {
        if (this.value.length !== 0) {
            this.parentNode.classList.remove('has-error');
            this.parentNode.classList.add('has-success');
            let help = document.getElementById('name-error')
            help.style.display = 'none'
        } else {
            this.parentNode.classList.remove('has-success');
            this.parentNode.classList.add('has-error')
            let help = document.getElementById('name-error')
            help.style.display = 'block'
        }

    });
}

$('.btn-delete').click(function (event) {
	$('#'+ 'instance-'+ this.id).removeAttr('data-href')
	const result = confirm('Вы уверены, что хотите удалить этот элемент?')
	if (result) {
		delete_payment(this.id)
	}
	event.stopPropagation()
})


