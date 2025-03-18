function check_all() {
    let filter_check = document.getElementById("check-all");
    let cardsContainer = document.getElementById("display-packs-container");

    let all_checks = cardsContainer.querySelectorAll("input")

    if (filter_check.checked === true) {
        all_checks.forEach(check => {
            check.checked = true;
        })
    } else {
        all_checks.forEach(check => {
            check.checked = false;
        })
    }
}

function check_pack(id) {
    let filter_check = document.getElementById("check-all");
    let this_check = document.getElementById(id);

    let cardsContainer = document.getElementById("display-packs-container");
    let all_checks = cardsContainer.querySelectorAll("input[type='checkbox']");

    // If the master checkbox is checked but the current checkbox is unchecked, uncheck the master checkbox.
    if (filter_check.checked === true && this_check.checked === false) {
        filter_check.checked = false;
    }
    // If all individual checkboxes are checked, set the master checkbox to checked.
    else if ([...all_checks].every(checkbox => checkbox.checked) && filter_check.checked === false) {
        filter_check.checked = true;
    }
}

function confirmSubmit() {
    const action = document.getElementById('actions').value;
    if (action == "delete") {
        return confirm("Are you sure you want to delete this item?");
    }
}

function remove_edit_pack(id) {
    editContainer = document.getElementById("item-container-" + id)
    if (editContainer) {
        editContainer.remove(); // Remove the element from the DOM
    }

    const formElements = document.querySelectorAll(`#item-container-${id} input, #item-container-${id}  select, #item-container-${id}  textarea`);
    formElements.forEach(el => {
        el.disabled = true;
    });

}