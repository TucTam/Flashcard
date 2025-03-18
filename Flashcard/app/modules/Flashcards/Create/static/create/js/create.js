


function add_inputs(event) {
    let form = document.getElementById("create-flashcard");
    let btn = document.getElementById("add_card_field")
    let template = document.getElementById("inputlabels-template")

    let numofcards = document.querySelectorAll(".card-container").length;

    tempRMBtn = template.content.querySelector("#rm-card-" + numofcards)
    cardContainer = template.content.querySelector('#card-container-' + numofcards)
    let inputTags = template.content.querySelectorAll("input");
    inputTags.forEach((input) => {
        if (input.id.includes("key-file-")) {
            input.id = "key-file-" + (numofcards + 1);
            input.name = "key-file-" + (numofcards + 1);
        } else if (input.id.includes("key-")) {
            input.id = "key-" + (numofcards + 1);
            input.name = "key-" + (numofcards + 1);

        } else if (input.id.includes("value-file-")) {
            input.id = "value-file-" + (numofcards + 1);
            input.name = "value-file-" + (numofcards + 1);
        } else if (input.id.includes("value-")) {
            input.id = "value-" + (numofcards + 1);
            input.name = "value-" + (numofcards + 1);
        }
    });

    cardContainer.id = "card-container-" + (numofcards + 1);
    tempRMBtn.id = "rm-card-" + (numofcards + 1);


    if (template) {
        let snippetContent = template.content.cloneNode(true);

        if (btn && form) {
            // Insert the inputsnippet to the form
            form.insertBefore(snippetContent, btn);

            // Add event listener to the "Remove" button
            let removeButton = document.querySelector("#" + tempRMBtn.id);
            if (removeButton) {
                removeButton.onclick = function (event) { remove_inputs(event, (numofcards + 1)) };
            } else {
                console.error("Remove button not found!");
            }
        } else {
            console.error("Button or form not found!")
        }
    } else {
        console.error("Template not found!");
    }

    console.log("Added a new container numbering " + (numofcards + 1))
}

function remove_inputs(e, id_num) {
    console.log("Trying to remove card no. " + id_num)
    e.preventDefault();
    container2remove = document.getElementById("card-container-" + id_num);
    container2remove.remove();
    console.log("Removed Card Container: " + id_num)

    AllCardContainers = document.querySelectorAll(".card-container");

    template = document.getElementById("inputlabels-template");

    templateRemoveBtn = template.content.querySelector("#rm-card-" + (AllCardContainers.length + 1));
    templateRemoveBtn.id = "rm-card-" + (AllCardContainers.length);

    templateCardContainer = template.content.querySelector("#card-container-" + (AllCardContainers.length + 1));
    templateCardContainer.id = "card-container-" + (AllCardContainers.length);

    templateInputs = template.content.querySelectorAll("input");
    templateInputs.forEach(input => {
        if (input.id.includes("key-file-")) {
            input.id = "key-file-" + (AllCardContainers.length);
            input.name = "key-file-" + (AllCardContainers.length);
        } else if (input.id.includes("key-")) {
            input.id = "key-" + (AllCardContainers.length);
            input.name = "key-" + (AllCardContainers.length);

        } else if (input.id.includes("value-file-")) {
            input.id = "value-file-" + (AllCardContainers.length);
            input.name = "value-file-" + (AllCardContainers.length);
        } else if (input.id.includes("value-")) {
            input.id = "value-" + (AllCardContainers.length);
            input.name = "value-" + (AllCardContainers.length);
        }
    })

    console.log("Changing container and button ids and parameter setups")
    AllCardContainers.forEach((container, index) => {
        if (container.id !== ("card-container-" + (index + 1))) {
            container.id = "card-container-" + (index + 1); // Change the id of container

            // Get all inputs in the container to change their id numbers
            inputTags = container.querySelectorAll("input")
            inputTags.forEach((input) => {
                if (input.id.includes("key-file-")) {
                    input.id = "key-file-" + (index + 1);
                    input.name = "key-file-" + (index + 1);
                } else if (input.id.includes("key-")) {
                    input.id = "key-" + (index + 1);
                    input.name = "key-" + (index + 1);

                } else if (input.id.includes("value-file-")) {
                    input.id = "value-file-" + (index + 1);
                    input.name = "value-file-" + (index + 1);
                } else if (input.id.includes("value-")) {
                    input.id = "value-" + (index + 1);
                    input.name = "value-" + (index + 1);
                }
            });


            // Get removebutton and change the id
            let removeBtn = container.querySelector("button");
            removeBtn.id = "rm-card-" + (index + 1)

            // Dynamically change the removebuttons onclick event parameter
            console.log("The new parameter is " + (index + 1));
            if (removeBtn) {
                removeBtn.onclick = function (event) {
                    remove_inputs(event, (index + 1));
                    console.log("The new parameter is " + (index + 1));
                };
            } else {
                console.error("Remove button not found!");
            }

        }
    });
}

function cancel_create(event) {
    fetch("/Flashcards/create/")
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            window.location.href = "/Flashcards/create/";
        })
        .then(data => {
            console.log('Success:', data);
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
        });
}