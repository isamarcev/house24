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