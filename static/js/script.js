document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("dronesTypesCount")?.addEventListener("input", function () {
        updateDroneTypes(parseInt(this.value, 10));
    });
});

// pridanie typov dronov na zaklade vstupu
function updateDroneTypes(countArg = null) {
    const droneTypesContainer = document.getElementById("dronesTypesContainer");
    const droneTypesCount = document.getElementById("dronesTypesCount");

    // droneTypesCount.addEventListener("input", function() {
        // pre istotu
    let count = countArg ?? parseInt(droneTypesCount?.value, 10);
    if (isNaN(count) || count < 1) {
        return;
    }

    droneTypesContainer.innerHTML = "";

    for (let i = 1; i <= count; ++i) {
        const row = document.createElement("div");
        row.classList.add("row", "mt-2");

        const colType = document.createElement("div");
        colType.classList.add("col-8");
        if (i == 1) {
            colType.innerHTML += `<label>Typ dronov</label>`;
        }
        colType.innerHTML += `<select id="droneType${i}" name="droneType${i}" class="form-select">
        <option value="" disabled selected>Vyberte typ</option>
        <option value="type_1">TYP 1</option>
        <option value="type_2">TYP 2</option>
        <option value="type_3">TYP 3</option>
        <option value="type_4">TYP 4</option>
        </select>`;

        const colTypeCount = document.createElement("div");
        colTypeCount.classList.add("col-4");
        if (i == 1) {
            colTypeCount.innerHTML += `<label>Počet dronov</label>`;
        }
        colTypeCount.innerHTML += `<input id="typeCount${i}" name="typeCount${i}" type="number" min="1" required>`;


        row.appendChild(colType);
        row.appendChild(colTypeCount);
        droneTypesContainer.appendChild(row);
    }
    // });
}

document.getElementById("topologySelect").addEventListener("change", function (event) {
    const selectedOption = event.target.value;
    const redundancyInputContainer = document.getElementById("redundancyInputContainer");
    const dronesTypesCountContainer = document.getElementById("dronesTypesCountContainer");
    redundancyInputContainer.innerHTML = "";
    dronesTypesCountContainer.innerHTML = "";

    // pridanie redundancie
    if (selectedOption.includes("hot_stable")) {
        const row = document.createElement("div");
        row.classList.add("row", "mt-2");

        const redundancyLabel = document.createElement("div");
        redundancyLabel.classList.add("col-8");
        redundancyLabel.innerHTML = `<label>Zadaj počet nepracujúcich dronov</label>`;

        const redundancyCount = document.createElement("div");
        redundancyCount.classList.add("col-4");
        // uvazovat nad max poctom
        redundancyCount.innerHTML = `<input id="redundantCount" name="redundantCount" type="number" min="1" required>`;

        row.appendChild(redundancyLabel);
        row.appendChild(redundancyCount);
        redundancyInputContainer.appendChild(row);
    }

    // pocet typov iba ak je heterogenna
    if (selectedOption.includes("heterogenous")) {
        const row = document.createElement("div");
        row.classList.add("row", "mt-2");

        const dronesTypesCountLabel = document.createElement("div");
        dronesTypesCountLabel.classList.add("col-8");
        dronesTypesCountLabel.innerHTML = `<label for="dronesTypesCount">Zadaj počet typov dronov vo flotile</label>`;

        const dronesTypesCount = document.createElement("div");
        dronesTypesCount.classList.add("col-4");
        // uvazovat nad max poctom
        dronesTypesCount.innerHTML = `<input id="dronesTypesCount" name="dronesTypesCount" type="number" min="1" required>`;

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

// pridanie spolahlivosti riadiacej jednotky
document.addEventListener("DOMContentLoaded", function () {
    const connectionType = document.getElementById("connectionType");
    const reliabilityCUContainer = document.getElementById("reliabilityCUContainer");

    connectionType.addEventListener("change", function () {
        reliabilityCUContainer.innerHTML = "";

        if (connectionType.value === "centralizovane") {
            const row = document.createElement("div");
            row.classList.add("row", "mt-2");

            const cuLabel = document.createElement("div");
            cuLabel.classList.add("col-8");
            cuLabel.innerHTML = `<label>Zadaj spoľahlivosť riadaiacej jednotky (%)</label>`;

            const cuReliability = document.createElement("div");
            cuReliability.classList.add("col-4");
            cuReliability.innerHTML = `<input id="cuReliability" name="cuReliability" type="number" min="0" max="100" step="0.01" required>`;

            row.appendChild(cuLabel);
            row.appendChild(cuReliability);
            reliabilityCUContainer.appendChild(row);
        }
    });
});


// document.getElementById("formContainer").addEventListener("submit", async function (event) {
//     event.preventDefault();
//     alert("Form submitted without reloading!"); 
// });