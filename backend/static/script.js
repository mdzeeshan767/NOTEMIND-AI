document.getElementById("uploadForm").addEventListener("submit", function (e) {
    e.preventDefault(); // stop page refresh

    const fileInput = document.getElementById("fileInput");
    const resultBox = document.getElementById("result");

    if (fileInput.files.length === 0) {
        alert("Please select a PDF file");
        return;
    }

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    resultBox.style.display = "block";
    resultBox.innerText = "⏳ Uploading and processing...";

    fetch("/upload", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        resultBox.innerText =
            data.extracted_text_preview || data.message;
    })
    .catch(error => {
        resultBox.innerText = "❌ Something went wrong";
        console.error(error);
    });
});
