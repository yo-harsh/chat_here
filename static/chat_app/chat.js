document.addEventListener("DOMContentLoaded", function() {
    const chatLog = document.getElementById("chat-log");
    const userInput = document.getElementById("user-input");
    const key = document.getElementById("keyInput");
    const sendButton = document.getElementById("send-button");

    sendButton.addEventListener("click", function() {
        var userMessage = userInput.value;
        if (userMessage.trim() !== "") {
            displayMessage("You", userMessage);

            // Get the send URL from the data attribute
            // const sendUrl = sendButton.getAttribute("data-send-url");

            userInput.value = "";
            // You can add AJAX code here to send the user message to the server
                // Send user message to server using AJAX
                sendUserMessageToServer(userMessage,key.value);
            }
        });

                // Example POST method implementation:
        // async function postData(url = "http://localhost:8000/bot/", data = {"messagee": message}) { 
        //     const response = await fetch(url, {
        //     method: "POST", headers: {
        //         "Content-Type": "application/json", 
        //     }, body: JSON.stringify(data),  
        //     });
        //     return response.json(); 
        // }

        // sendButton.addEventListener("click", async ()=>{ 
        //     userMessage = document.getElementById("user-input").value;
        //     document.getElementById("user-input").value = "";
        //     document.querySelector(".right2").style.display = "block"
        //     document.querySelector(".right1").style.display = "none"
        
        //     question1.innerHTML = userMessage;
        //     question2.innerHTML = userMessage;
        
        //     // Get the answer and populate it! 
        //     let result = await postData("http://127.0.0.1:8000/bot/", {"question": userMessage})
        //     solution.innerHTML = result.answer
        // })

        userInput.addEventListener("keydown", function(event) {
            if (event.key === "Enter") {
                event.preventDefault(); // Prevent the default Enter key behavior (e.g., new line)
                sendButton.click();
            }
        });
        
    
        function displayMessage(sender, message) {
            const messageDiv = document.createElement("div");
            // messageDiv.style.paddingTop = '20px'
            
            console.log(sender);
            if(sender == 'You'){
                messageDiv.className = "message_you";
                messageDiv.style.backgroundColor = "#69B4AD"; 
                
            }
            else if(sender == 'bot'){
                messageDiv.className = "message_bot";
                messageDiv.style.borderBottom = "1px solid black";
                messageDiv.style.marginBottom = "20px";

                
            }
            else{
            messageDiv.className = "else_section";
            }
            messageDiv.style.fontSize = "20px";
            messageDiv.innerHTML = `<strong>${sender}:</strong> ${message}`;
            chatLog.appendChild(messageDiv);

            // chatLog.scrollTop = chatLog.scrollHeight;
        }
    


        function sendUserMessageToServer(message,key) {
            console.log(message);
            fetch("http://localhost:8000/message/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCookie("csrftoken")
                },
                body: JSON.stringify({
                    "messagee": message,
                    'key':key
                    
                
                })
            })
            .then(response => response.json())
            .then(data => {
                console.log(data);
                console.log('done');
                console.log(data.response);
                displayMessage('bot' , data.response);




                // console.log(data);
                // console.log('hhhhh');
                // console.log(data.response);
                // displayMessage('bot' , data.response);
                // document.getElementById('chat').innerHTML = data.response;
                // Handle the response from the server if needed
                // For example, you can display the bot's response
            })
            .catch(error => {
                console.error("Error:", error);
            });
        }


        
        // Function to get CSRF token from cookies
        function getCookie(name) {
            let cookieValue = null;
            if (document.cookie && document.cookie !== "") {
                const cookies = document.cookie.split(";");
                for (let i = 0; i < cookies.length; i++) {
                    const cookie = cookies[i].trim();
                    if (cookie.substring(0, name.length + 1) === name + "=") {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
    });