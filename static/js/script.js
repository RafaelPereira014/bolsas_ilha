document.getElementById('dataForm').addEventListener('submit', function(e) {
    e.preventDefault();

    const dataInput = document.getElementById('dataInput').value;
    if (!dataInput) {
        alert("Please enter some data.");
        return;
    }

    fetch('/receive_data', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ data: dataInput }),
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('responseMessage').innerText = data.message;
    })
    .catch((error) => {
        document.getElementById('responseMessage').innerText = "Error sending data";
        console.error('Error:', error);
    });
});