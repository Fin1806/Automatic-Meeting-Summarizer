function updateWordCount() {

    const transcriptBox =
        document.getElementById("transcript");

    const words =
        transcriptBox.value
            .trim()
            .split(/\s+/)
            .filter(Boolean);

    document.getElementById("wordCount").innerText =
        `Words: ${words.length}`;
}

function loadFile() {

    const file =
        document.getElementById("fileInput").files[0];

    if (!file) {
        alert("Select a file first.");
        return;
    }

    const reader = new FileReader();

    reader.onload = function(event) {
        document.getElementById("transcript").value =
            event.target.result;

        updateWordCount()
    };

    reader.readAsText(file);
}


async function summarizeText() {

    const transcript =
        document.getElementById("transcript").value;

    if (!transcript.trim()) {
        alert("Transcript is empty.");
        return;
    }

    document.getElementById("result").innerHTML =
        "Generating summary...";

    try {

        const response = await fetch(
            "/summarize",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    text: transcript
                })
            }
        );

        const data = await response.json();

        document.getElementById("result").innerHTML =
            data.summary;

    } catch (err) {

        document.getElementById("result").innerHTML =
            "Error generating summary.";

        console.error(err);

    }
}

const transcriptBox =
    document.getElementById("transcript");

transcriptBox.addEventListener("input", updateWordCount);