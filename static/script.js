document.getElementById("task").addEventListener("change", function () {
    const task = this.value;
    document.getElementById("translationFields").style.display = task === "translation" ? "block" : "none";
});

document.getElementById("generateReference").addEventListener("click", async function () {
    const task = document.getElementById("task").value;
    let inputText = document.getElementById("inputText").value;

    if (!inputText) {
        alert("Please enter input text!");
        return;
    }

    let requestData = { task, text: inputText };

    if (task === "translation") {
        requestData.sourceLang = document.getElementById("sourceLang").value;
        requestData.targetLang = document.getElementById("targetLang").value;
        if (!requestData.sourceLang || !requestData.targetLang) {
            alert("Please enter source and target languages!");
            return;
        }
    }

    const response = await fetch("/generate_reference", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(requestData)
    });

    const data = await response.json();
    document.getElementById("referenceText").textContent = data.reference;
});

document.getElementById("aiForm").addEventListener("submit", async function (event) {
    event.preventDefault();

    const referenceText = document.getElementById("referenceText").textContent;
    const userOutput = document.getElementById("userOutput").value;

    if (!referenceText) {
        alert("Please generate the reference output first!");
        return;
    }

    const response = await fetch("/evaluate_output", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ reference: referenceText, user_output: userOutput })
    });

    const data = await response.json();
    document.getElementById("rougeScore").textContent = `ROUGE Score: ${data.rouge_score.toFixed(4)}`;
});
