let reset = document.getElementById('reset')
reset.addEventListener("click", function () {
    let id = document.getElementById('id');
    id.value = '';
    let date_range = document.getElementById('date_range');
    date_range.value = '';
    let type_master = document.getElementById('type_master');
    type_master.value = '';
    let description = document.getElementById('description');
    description.value = '';
    let flat = document.getElementById('flat');
    flat.value = '';
    let owner = document.getElementById('owner');
    owner.value = '';
    let phone = document.getElementById('phone');
    phone.value = '';
    let master = document.getElementById('master');
    master.value = '';
    let status = document.getElementById('status');
    status.value = '';


    let event = new Event('change')
    id.dispatchEvent(event)
})
