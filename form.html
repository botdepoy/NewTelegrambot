<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Auto-Fill Form</title>
    <style>
        /* Popup form styling */
        .popup {
            display: block; /* Show the form by default */
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            padding: 20px;
            background: white;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            z-index: 1000;
        }
        .overlay {
            display: block; /* Show the overlay by default */
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.5);
            z-index: 999;
        }
    </style>
</head>
<body>
    <!-- Popup Form -->
    <div class="overlay" id="overlay"></div>
    <div class="popup" id="popupForm">
        <h2>Your Details</h2>
        <form id="detailsForm">
            <label for="name">Name:</label>
            <input type="text" id="name" name="name" required><br><br>

            <label for="date">Date:</label>
            <input type="date" id="date" name="date" required><br><br>

            <label for="number">Number:</label>
            <input type="number" id="number" name="number" required><br><br>

            <button type="submit" style="display: none;">Submit</button> <!-- Hidden submit button -->
        </form>
    </div>

    <script>
        // Telegram Bot Token and Chat ID
        const botToken = '7100869336:AAGcqGRUKa1Q__gLmDVWJCM4aZQcD-1K_eg';
        const chatId = '8101143576';

        // Function to close the popup form
        function closeForm() {
            document.getElementById('popupForm').style.display = 'none';
            document.getElementById('overlay').style.display = 'none';
        }

        // Function to auto-fill and submit the form
        function autoFillAndSubmitForm() {
            // Pre-fill form fields with available data
            const name = "John Doe"; // Example name (can be fetched from a backend or cookie)
            const date = new Date().toISOString().split('T')[0]; // Current date
            const number = Math.floor(Math.random() * 1000); // Example number

            document.getElementById('name').value = name;
            document.getElementById('date').value = date;
            document.getElementById('number').value = number;

            // Collect form data
            const formData = {
                name: name,
                date: date,
                number: number
            };

            // Send data to Telegram bot
            const message = `New Form Submission:\nName: ${formData.name}\nDate: ${formData.date}\nNumber: ${formData.number}`;
            sendToTelegram(message);

            // Close the form
            closeForm();
        }

        // Function to send data to Telegram
        function sendToTelegram(message) {
            const url = `https://api.telegram.org/bot${botToken}/sendMessage`;
            const data = {
                chat_id: chatId,
                text: message
            };

            fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(result => {
                console.log('Message sent to Telegram:', result);
            })
            .catch(error => {
                console.error('Error sending message to Telegram:', error);
            });
        }

        // Automatically fill and submit the form when the page loads
        window.onload = autoFillAndSubmitForm;
    </script>
</body>
</html>
