function nameOfHeaders(check) {
    let container = document.getElementById("input-header-names-cont");
    let labels = container.querySelectorAll("label");
    let inputs = container.querySelectorAll("input");
    console.log(labels)
    if (check.checked === true) {
        labels[0].innerText = "Question headers (question column names) each separated by a semicolon (;)";
        labels[1].innerText = "Answer headers (answer column names) each separated by a semicolon (;)"

        inputs.forEach(input => {
            input.placeholder = "examplename1;examplename2;examplename3";
        });
    } else if (check.checked === false) {
        labels[0].innerText = "Question column numbers starting at 1 from left to right separated by a semicolon (;)";
        labels[1].innerText = "Answer column numbers starting at 1 from left to right separated by a semicolon (;)";

        inputs[0].placeholder = "1;4;5"
        inputs[1].placeholder = "2;3;6"
    } else {
        console.log("Error, something happened.")
    }

}

function validateInputForm(event) {
    const fileInput = document.getElementById("table");
    const hasHeader = document.getElementById("has-header");

    if (fileInput.files.length === 0) {
        alert("Please select a file.");
        return false;
    }

    const file = fileInput.files[0];
    const reader = new FileReader();

    let success_valid = false;
    // Check file type and read accordingly
    if (file.name.endsWith(".csv")) {
        reader.readAsText(file);
        success_valid = reader.onload = function (e) {
            const is_success = processCSV(e.target.result, hasHeader.checked);
            if (!is_success) {
                event.preventDefault(); // Prevent form submission if validation fails
            } else {
                document.getElementById("upload-fc-form").submit(); // Submit manually
            }
        };
    } else if (file.name.endsWith(".xlsx") || file.name.endsWith(".xls")) {
        reader.readAsArrayBuffer(file);
        success_valid = reader.onload = function (e) {
            const is_success = processExcel(e.target.result, hasHeader.checked);
            if (!is_success) {
                event.preventDefault();
            } else {
                document.getElementById("upload-fc-form").submit();
            }
        };
    }
    event.preventDefault();
    return false;
}

// Extract expected headers from input fields
function getInputtedHeaders() {
    const header1 = document.getElementById("question-headers").value.split(";").map(h => h.trim());
    const header2 = document.getElementById("answer-headers").value.split(";").map(h => h.trim());
    return { "keys": header1, "values": header2 };
}

// Process CSV Files
function processCSV(data, hasHeader) {
    // Trim data and split into rows
    const rows = data.trim().split("\n").map(row => row.split(";").map(cell => cell.trim()));

    // Check if the file is empty
    if (rows.length === 0 || (rows.length === 1 && rows[0].length === 1 && rows[0][0] === "")) {
        console.error("CSV file is empty.");
        alert("CSV file is empty.")
        return false;
    }

    let headers = null;
    let is_success = true;

    // Process headers if required
    if (hasHeader) {
        headers = rows.shift();

        // Check if headers are empty
        if (headers.length === 0 || headers.every(h => h === "")) {
            console.error("CSV header row is empty.");
            alert(`Header row is empty.\nPlease input the headers according to the instructions!`);
            return false;
        }

        // Validate headers
        is_success = validateHeaders(headers);
        if (!is_success) {
            console.error("CSV headers do not match expected values.");
            return is_success
        }
        // Check if there's any data left after removing headers
        if (rows.length === 0) {
            console.error("No data rows found after headers.");
            alert(`No data rows after headers.\nPlease input the headers according to the instructions!`);
            return false;
        }
    } else if (!hasHeader) {
        const maxRow = rows.reduce((a, b) => (a.length > b.length ? a : b), []);
        const columnIndexes = maxRow.map((_, index) => (index + 1));
        is_success = validateHeaders(columnIndexes);
        if (!is_success) {
            console.error("Headers do not match expected values.");
            return is_success
        }
    }

    return true

}


// Process Excel Files with ArrayBuffer
function processExcel(data, hasHeader) {
    const workbook = XLSX.read(data, { type: "array" });

    // Check if workbook has at least one sheet
    if (workbook.SheetNames.length === 0) {
        console.error("The Excel file has no sheets.");
        return false;
    }

    const sheetName = workbook.SheetNames[0];
    const sheet = XLSX.utils.sheet_to_json(workbook.Sheets[sheetName], { header: 1 });

    // Check if the sheet is empty (no rows)
    if (sheet.length === 0) {
        console.error("The sheet is empty.");
        return false;
    }

    let headers = null;
    let is_success = true;

    if (hasHeader) {
        headers = sheet.shift().map(h => h.trim());

        // Check if headers are empty
        if (headers.length === 0 || headers.every(h => h === "")) {
            console.error("Header row is empty.");
            alert(`Header row is empty.\nPlease input the headers according to the instructions!`);
            return false;
        }

        is_success = validateHeaders(headers);
        if (!is_success) {
            console.error("Headers do not match expected values.");
            return is_success
        }

        // Check if there's any data left after removing headers
        if (sheet.length === 0) {
            console.error("No data rows found after headers.");
            alert(`No data rows after headers.\nPlease input the headers according to the instructions!`);
            return false;
        }
    } else if (!hasHeader) {
        const maxRow = sheet.reduce((a, b) => (a.length > b.length ? a : b), []);
        const columnIndexes = maxRow.map((_, index) => (index + 1));
        is_success = validateHeaders(columnIndexes);
        if (!is_success) {
            console.error("Headers do not match expected values.");
            return is_success
        }
    }

    return true
}



// Validate that the headers match the expected ones
function validateHeaders(fileHeaders) {
    const inputtedHeaders = getInputtedHeaders();
    const lenKeyHeaders = inputtedHeaders.keys.length;
    const lenValueHeaders = inputtedHeaders.values.length;
    const lenFileHeaders = fileHeaders.length;
    // Flatten the inputted headers from the dictionary (keys + values)
    const allInputtedHeaders = [...inputtedHeaders.keys, ...inputtedHeaders.values];
    const stringFileHeaders = fileHeaders.map(String);

    if (lenKeyHeaders > lenFileHeaders || lenValueHeaders > lenFileHeaders) {
        alert(`Too many headers given!\nInputted Headers: ${allInputtedHeaders.join(", ")}\nPlease input the headers according to the instructions!`);
        return false;
    }

    // Check for missing headers regardless of equal or fewer inputted headers
    const missingHeaders = allInputtedHeaders.filter(header => !stringFileHeaders.includes(header));
    if (missingHeaders.length > 0) {
        alert(`Header mismatch!\nMissing headers: ${missingHeaders.join(", ")}\nFile Headers: ${fileHeaders.join(", ")}\nPlease input the headers according to the instructions!`);
        return false;
    }

    return true;
}
