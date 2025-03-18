
function flip_card() {
    let keySection = document.getElementById("key-section");
    let valueSection = document.getElementById("value-section");

    if (keySection.style.display !== "none") {
        keySection.style.display = "none";
        valueSection.style.display = "flex";
    } else if (keySection.style.display === "none") {
        keySection.style.display = "flex";
        valueSection.style.display = "none";
    }
}

let currentIndex = 0;
function next_card(pack) {
    let keySection = document.getElementById("key-section");
    let valueSection = document.getElementById("value-section");
    if (keySection.style.display === "none") {
        keySection.style.display = "flex";
        valueSection.style.display = "none";
    }

    if (currentIndex < pack.length - 1) {
        currentIndex = currentIndex + 1;
        let keyText = keySection.querySelector("p");
        let keyImg = keySection.querySelector("img")
        let valueText = valueSection.querySelector("p")
        let valueImg = valueSection.querySelector("img")
        let qheader = document.getElementById("fc-k-header")
        let vheader = document.getElementById("fc-v-header")

        if (Array.isArray(pack[currentIndex].key.key)) {
            keyText.textContent = pack[currentIndex].key.key.join(", ");
            keyImg.src = "../../../../../../static/uploads/pack-" + pack[currentIndex].pack_id + "/" + pack[currentIndex].key.key_file;
            valueText.textContent = pack[currentIndex].value.value;
            valueImg.src = "../../../../../../static/uploads/pack-" + pack[currentIndex].pack_id + "/" + pack[currentIndex].value.value_file;
            qheader.textContent = "Question " + (currentIndex + 1);
            vheader.textContent = "Answer " + (currentIndex + 1);
        } else {
            keyText.textContent = pack[currentIndex].key.key;
            keyImg.src = "../../../../../../static/uploads/pack-" + pack[currentIndex].pack_id + "/" + pack[currentIndex].key.key_file;

            valueText.textContent = pack[currentIndex].value.value;
            valueImg.src = "../../../../../../static/uploads/pack-" + pack[currentIndex].pack_id + "/" + pack[currentIndex].value.value_file;

            qheader.textContent = "Question " + (currentIndex + 1);
            vheader.textContent = "Answer " + (currentIndex + 1);
        }

    }
}

function previous_card(pack) {
    let keySection = document.getElementById("key-section");
    let valueSection = document.getElementById("value-section");
    if (keySection.style.display === "none") {
        keySection.style.display = "flex";
        valueSection.style.display = "none";
    }

    if (currentIndex >= 1) {
        currentIndex = currentIndex - 1;
        let keyText = keySection.querySelector("p");
        let keyImg = keySection.querySelector("img")
        let valueText = valueSection.querySelector("p")
        let valueImg = valueSection.querySelector("img")
        let qheader = document.getElementById("fc-k-header")
        let vheader = document.getElementById("fc-v-header")

        if (Array.isArray(pack[currentIndex].key.key)) {
            keyText.textContent = pack[currentIndex].key.key.join(", ");
            keyImg.src = "../../../../../../static/uploads/pack-" + pack[currentIndex].pack_id + "/" + pack[currentIndex].key.key_file;
            valueText.textContent = pack[currentIndex].value.value;
            valueImg.src = "../../../../../../static/uploads/pack-" + pack[currentIndex].pack_id + "/" + pack[currentIndex].value.value_file;
            qheader.textContent = "Question " + (currentIndex + 1);
            vheader.textContent = "Answer " + (currentIndex + 1);
        } else {
            keyText.textContent = pack[currentIndex].key.key;
            keyImg.src = "../../../../../../static/uploads/pack-" + pack[currentIndex].pack_id + "/" + pack[currentIndex].key.key_file;

            valueText.textContent = pack[currentIndex].value.value;
            valueImg.src = "../../../../../../static/uploads/pack-" + pack[currentIndex].pack_id + "/" + pack[currentIndex].value.value_file;

            qheader.textContent = "Question " + (currentIndex + 1);
            vheader.textContent = "Answer " + (currentIndex + 1);
        }
    }
}

function blur_unblur(id) {
    answer = document.getElementById(id);
    if (answer.style.filter != "none") {
        answer.style.filter = "none";
        return
    } else {
        answer.style.filter = "blur(5px)";
    }
}

