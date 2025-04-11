document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("dronesTypesCount")?.addEventListener("input", function () {
        updateDroneTypes(parseInt(this.value, 10));
    });

    // pridanie spolahlivosti riadiacej jednotky
    const connectionType = document.getElementById("connectionType");
    const reliabilityCUContainer = document.getElementById("reliabilityCUContainer");

    connectionType.addEventListener("change", function () {
        reliabilityCUContainer.innerHTML = "";

        if (connectionType.value === "centralized") {
            const row = document.createElement("div");
            row.classList.add("row", "mt-2");

            const cuLabel = document.createElement("div");
            cuLabel.classList.add("col-8");
            cuLabel.innerHTML = `<label>Zadaj spoľahlivosť riadiacej jednotky </label>`;

            const cuReliability = document.createElement("div");
            cuReliability.classList.add("col-4");
            cuReliability.innerHTML = `<input id="cuReliability" name="cuReliability" type="number" min="0" max="1" step="0.01" required>`;

            row.appendChild(cuLabel);
            row.appendChild(cuReliability);
            reliabilityCUContainer.appendChild(row);
        }
    });
});

// pridanie typov dronov na zaklade vstupu
async function updateDroneTypes(countTypesArg = null) {
    const droneTypesContainer = document.getElementById("dronesTypesContainer");
    const droneTypesCount = document.getElementById("dronesTypesCount");
    const structureType = document.getElementById("topologySelect").value;
    const isRedundant = structureType.includes("hot_stable");

    // pre istotu
    let count = countTypesArg ?? parseInt(droneTypesCount?.value, 10);
    if (isNaN(count) || count < 1) {
        return;
    }

    droneTypesContainer.innerHTML = "";

    try {
        const response = await fetch("/api/drones");
        const dronesOptions = await response.json();

        for (let i = 1; i <= count; ++i) {
            const row = document.createElement("div");
            row.classList.add("row", "mt-2");

            const colType = document.createElement("div");
            colType.classList.add("col-6");
            if (i == 1) {
                colType.innerHTML += `<label>Typ dronov</label>`;
            }
            
            let options = '<option value="" disabled selected>Vyberte typ</option>';
                dronesOptions.forEach(drone => {
                    options += `<option value="${drone.name}">${drone.name}   (${drone.description}) p:${drone.reliability}</option>`;
                });
            
            const selectType = document.createElement("select");
            selectType.id = "droneType" + i;
            selectType.name = "droneType" + i;
            selectType.classList.add("form-select");
            selectType.required = true;
            selectType.innerHTML = options;
            colType.appendChild(selectType);

            const customSwitch = document.createElement("div");
            customSwitch.classList.add("form-check", "form-switch");
            customSwitch.innerHTML = `<input class="form-check-input" type="checkbox" id="customTypeSwitch${i}">
                                           <label class="form-check-label" for="customTypeSwitch${i}">Vlastná spoľahlivosť</label>`;
            colType.appendChild(customSwitch);

            customSwitch.querySelector(`#customTypeSwitch${i}`).addEventListener("change", function () {
                const customInput = document.getElementById("customReliability" + i);
                const select = document.getElementById("droneType" + i);

                if (this.checked) {
                    if (select) { select.remove(); }

                    const customInputReliability = document.createElement("input");
                    customInputReliability.id = "customReliability" + i;
                    customInputReliability.name = "customReliability" + i;
                    customInputReliability.type = "number";
                    customInputReliability.min = "0";
                    customInputReliability.max = "1";
                    customInputReliability.step = "0.01";
                    customInputReliability.required = true;
                    customInputReliability.classList.add("form-control");

                    colType.insertBefore(customInputReliability, customSwitch);
                } else {
                    if (customInput) { customInput.remove(); }

                    const select = document.createElement("select");
                    select.id = "droneType" + i;
                    select.name = "droneType" + i;
                    select.classList.add("form-select");
                    select.required = true;
                    select.innerHTML = options;

                    colType.insertBefore(select, customSwitch);
                }
            });

            const colTypeCount = document.createElement("div");
            colTypeCount.classList.add("col-3");
            if (i == 1) {
                colTypeCount.innerHTML += `<label>Počet dronov</label>`;
            }
            colTypeCount.innerHTML += `<input id="typeCount${i}" name="typeCount${i}" type="number" min="1" required>`;

            row.appendChild(colType);
            row.appendChild(colTypeCount);

            if (isRedundant) {
                const colRedundantCount = document.createElement("div");
                colRedundantCount.classList.add("col-3");
                if (i == 1) {
                    colRedundantCount.innerHTML += `<label>Počet dronov v MDF</label>`;
                }
                colRedundantCount.innerHTML += `<input id="redundantCount${i}" name="redundantCount${i}" type="number" min="1" required>`;
                row.appendChild(colRedundantCount);
            }

            droneTypesContainer.appendChild(row);
        }
    } catch {
        console.error("Error fetching drone options:", error);
    }
}

document.getElementById("topologySelect").addEventListener("change", function (event) {
    const selectedOption = event.target.value;
    const dronesTypesCountContainer = document.getElementById("dronesTypesCountContainer");
    dronesTypesCountContainer.innerHTML = "";

    // pocet typov iba ak je heterogenna
    if (selectedOption.includes("heterogenous")) {
        const row = document.createElement("div");
        row.classList.add("row", "mt-2");

        const dronesTypesCountLabel = document.createElement("div");
        dronesTypesCountLabel.classList.add("col-8");
        dronesTypesCountLabel.innerHTML = `<label for="dronesTypesCount">Zadaj počet typov dronov v roji</label>`;

        const dronesTypesCount = document.createElement("div");
        dronesTypesCount.classList.add("col-4");
        dronesTypesCount.innerHTML = `<input id="dronesTypesCount" name="dronesTypesCount" type="number" min="2" required>`;

        row.appendChild(dronesTypesCountLabel);
        row.appendChild(dronesTypesCount);
        dronesTypesCountContainer.appendChild(row);

        document.getElementById("dronesTypesCount").addEventListener("input", function () {
            updateDroneTypes(parseInt(this.value, 10));
        });
    } else {
        dronesTypesCountContainer.innerHTML = `<input id="dronesTypesCount" name="dronesTypesCount" type="number" value="1" hidden>`;
        updateDroneTypes(1);
    }
});

document.getElementById("formContainer").addEventListener("submit", async function (event) {
    event.preventDefault();
    // alert("Form submitted!");

    const formData = new FormData(event.target);
    
    try {
        const response = await fetch('/', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();
        if (!response.ok) {
            console.log('Response is not ok, errors! ' + result.errors);
            showErrors(result.errors)
        } else {
            console.log('Response is ok, ' + result.result);
            showResult(result.result);
        }

    } catch (error) {
        console.error('Nepodarilo sa fetchnut response. :' + error);
    }
});

function showResult(result) {
    const resultContainer = document.getElementById('resultsContainer');
    result.innerHTML = "";
    resultContainer.innerHTML = `<p>Spoľahlivosť, respektíve dostupnosť roja dronov je ${result}.</p>`;
}

function showErrors(errors) {
    const errorContainer = document.getElementById('resultsContainer');
    errorContainer.innerHTML = "";
    const ul = document.createElement('ul');
    ul.classList.add('text-danger')
    ul.innerHTML = errors.map(error => `<li>${error}</li>`).join('');
    errorContainer.appendChild(ul);
}