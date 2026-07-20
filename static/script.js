function checkDisease() {
    let name = document.getElementById("farmerName").value.trim();
    let village = document.getElementById("village").value.trim();
    let crop = document.getElementById("crop").value;
    let result = document.getElementById("result");

    if (name === "") {  
        result.innerHTML = "<h3 style='color:red;'>Please enter farmer name!</h3>";
        return;
    }

    let disease = "";
    let solution = "";
    let icon = "🌱";
    let confidence = Math.floor(Math.random() * 40) + 60; // 60-99% confidence
    let severity = "Low";

    switch (crop) {
        case "Wheat":
            disease = "Rust Disease";
            solution = "Spray fungicide and avoid excess moisture.";
            icon = "🌾";
            confidence = 85;
            severity = "Medium";
            break;
        case "Rice":
            disease = "Blast Disease";
            solution = "Use disease-resistant seeds and proper fertilizer.";
            icon = "🌾";
            confidence = 92;
            severity = "High";
            break;
        case "Tomato":
            disease = "Leaf Blight";
            solution = "Remove infected leaves and spray fungicide.";
            icon = "🍅";
            confidence = 88;
            severity = "High";
            break;
        case "Cotton":
            disease = "Boll Rot";
            solution = "Improve drainage and use recommended pesticide.";
            icon = "🌿";
            confidence = 80;
            severity = "Medium";
            break;
        case "Potato":
            disease = "Early Blight";
            solution = "Use certified seeds and apply fungicide.";
            icon = "🥔";
            confidence = 90;
            severity = "High";
            break;
        default:
            disease = "Unknown disease";
            solution = "Please select a valid crop.";
            confidence = 0;
            severity = "Low";
    }

    result.innerHTML = `
        <h3>${icon} Analysis Result</h3>
        <p><b>Date & Time:</b> ${new Date().toLocaleString()}</p>
        <p><b>Farmer:</b> ${name}</p>
        <p><b>Village:</b> ${village}</p>
        <p><b>Crop:</b> ${crop}</p>
        <p><b>Disease:</b> ${disease}</p>
        <p><b>Severity:</b> <span style="color: ${severity === 'High' ? 'red' : severity === 'Medium' ? 'orange' : 'green'}; font-weight: bold;">${severity}</span></p>
        <p><b>Confidence:</b> ${confidence}%</p>
        <p><b>Solution:</b> ${solution}</p>
    `;
}

function resetForm() {
    document.getElementById("farmerName").value = "";
    document.getElementById("village").value = "";
    document.getElementById("crop").selectedIndex = 0;
    document.getElementById("cropImage").value = "";

    let preview = document.getElementById("preview");
    preview.src = "";
    preview.style.display = "none";

    document.getElementById("result").innerHTML = "Result will appear here";
}

// Initialize when DOM is ready
document.addEventListener("DOMContentLoaded", function() {
    let checkButton = document.getElementById("checkDiseaseBtn");
    if (checkButton) {
        checkButton.addEventListener("click", checkDisease);
    }

    let image = document.getElementById("cropImage");
    let preview = document.getElementById("preview");

    if (image && preview) {
        image.onchange = function () {
            if (!image.files || image.files.length === 0) {
                preview.style.display = "none";
                preview.src = "";
                return;
            }

            let file = image.files[0];
            preview.src = URL.createObjectURL(file);
            preview.style.display = "block";
        };
    }
});
