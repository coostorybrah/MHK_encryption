async function runTests() {
    const tbody = document.querySelector("#test-table tbody");
    const summary = document.getElementById("summary");

    tbody.innerHTML = "";
    summary.innerText = "Running...";

    try {
        const res = await fetch("/api/run-tests");
        const data = await res.json();

        let passedCount = 0;

        data.forEach(test => {
            const row = document.createElement("tr");
            const detailRow = document.createElement("tr");

            const isPassed = test.passed === true;
            if (isPassed) passedCount++;

            const icon = (ok) => ok ? "✔️" : "❌";

            let S = "-", bits = "-", cipher = "-", text = "-";

            if (test.checks) {
                S = icon(test.checks.S);
                bits = icon(test.checks.bits);
                cipher = icon(test.checks.cipher);
                text = icon(test.checks.plaintext);
            }

            let resultText = isPassed ? "PASS" : "FAIL";
            let resultClass = isPassed ? "pass" : "fail";

            row.classList.add(resultClass);

            row.innerHTML = `
                <td>${test.id}</td>
                <td>${test.name}</td>
                <td>${S}</td>
                <td>${bits}</td>
                <td>${cipher}</td>
                <td>${text}</td>
                <td><strong>${resultText}</strong></td>
            `;

            row.style.cursor = "pointer";

            const detailContent = `
                <div class="test-details">
                    <div>
                        <h4>Input</h4>
                        <p>${formatObject(test.input)}</p>
                    </div>

                    <div>
                        <h4>Expected Result</h4>
                        <p>${formatObject(test.expected)}</p>
                    </div>

                    <div>
                        <h4>Actual Result</h4>
                        <p>${formatObject(test.actual)}</p>
                    </div>
                </div>
            `;

            detailRow.id = `details-${test.id}`;
            detailRow.style.display = "none";

            detailRow.innerHTML = `
                <td colspan="7">
                    ${detailContent}
                </td>
            `;

            row.addEventListener("click", () => {
                detailRow.style.display =
                    detailRow.style.display === "none" ? "table-row" : "none";
            });

            tbody.appendChild(row);
            tbody.appendChild(detailRow);
        });

        summary.innerText = `Passed ${passedCount} / ${data.length} tests`;

    } catch (err) {
        summary.innerText = "Error running tests";
        console.error(err);
    }
}


function formatValue(value) {
    if (Array.isArray(value)) {
        return value.join(", ");
    }
    return value;
}


function formatObject(obj) {
    let result = "";

    for (const key in obj) {
        if (key === "error_code" || key === "message") continue;

        result += `${key}: `;

        if (Array.isArray(obj[key])) {
            result += formatValue(obj[key]);
        } else {
            result += obj[key];
        }

        result += "\n";
    }

    if (obj.error_code) {
        result += `error_code: ${obj.error_code}\n`;
    }

    if (obj.message) {
        result += `message: ${obj.message}\n`;
    }

    return result;
}