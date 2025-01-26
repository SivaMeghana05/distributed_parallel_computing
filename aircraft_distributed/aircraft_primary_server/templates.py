ADD_AIRCRAFT_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
    <title>Add Aircraft</title>
</head>
<body>
    <h2>Add New Aircraft</h2>
    <form id="aircraftForm">
        Aircraft ID: <input type="text" id="aircraft_id"><br><br>
        Model: <input type="text" id="model"><br><br>
        Altitude: <input type="number" id="altitude"><br><br>
        Speed: <input type="number" id="speed"><br><br>
        Latitude: <input type="number" step="0.0001" id="latitude"><br><br>
        Longitude: <input type="number" step="0.0001" id="longitude"><br><br>
        <button type="button" onclick="submitForm()">Add Aircraft</button>
    </form>

    <script>
    function submitForm() {
        const data = {
            aircraft_id: document.getElementById('aircraft_id').value,
            model: document.getElementById('model').value,
            altitude: parseFloat(document.getElementById('altitude').value),
            speed: parseFloat(document.getElementById('speed').value),
            latitude: parseFloat(document.getElementById('latitude').value),
            longitude: parseFloat(document.getElementById('longitude').value)
        };

        fetch('/primary/add/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => alert(data.message))
        .catch(error => alert('Error: ' + error));
    }
    </script>
</body>
</html>"""