document.addEventListener("DOMContentLoaded", function () {
    const fileUploadForm = document.getElementById("fileUploadForm");
    const fileInput = document.getElementById("fileInput");
    const chatMessages = document.getElementById("chatMessages");
    const messageInput = document.getElementById("messageInput");
    const sendMessageButton = document.getElementById("sendMessage");

    fileUploadForm.addEventListener("submit", function (e) {
        e.preventDefault();
        const formData = new FormData();
        formData.append("file", fileInput.files[0]);

        // Send the PDF file to the server
        fetch("http://localhost:8000/upload_csv/", { // Update the URL as needed
            method: "POST",
            body: formData,
            headers: {
                "X-CSRFToken": getCookie("csrftoken"),
            },
        })
            .then((response) => response.json())
            .then((data) => {
                // Display the response from the server in the chat
                chatMessages.innerHTML += `<div><strong>User:</strong> Uploaded CSV successfully</div>`;
            })
            .catch((error) => {
                console.error("Error uploading PDF:", error);
            });
    });

    sendMessageButton.addEventListener("click", function () {
        const message = messageInput.value;
        if (message.trim() === "") {
            return;
        }

        console.log(message)

        // Send the user's message to the server
        fetch("http://localhost:8000/csv_agent/", { // Update the URL as needed
            method: "POST",
            body: JSON.stringify({ message }),
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie("csrftoken"),
            },
        })
            .then((response) => response.json())
            .then((data) => {
                // Display the response from the server in the chat
                chatMessages.innerHTML += `<div><strong>User:</strong> ${message}</div>`;
                chatMessages.innerHTML += `<div><strong>Bot:</strong> ${data.output}</div>`;
                messageInput.value = "";
            })
            .catch((error) => {
                console.error("Error sending message:", error);
            });
    });

    // Function to get CSRF token from cookies
    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(";").shift();
    }
});
