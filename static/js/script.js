const bar = document.getElementById('bar');
const close = document.getElementById('close');
const nav = document.getElementById('navbar');
if (bar) {
    bar.addEventListener('click', () => {
        nav.classList.add('active');
    })
}
if (close) {
    close .addEventListener('click', () => {
        nav.classList.remove('active');
    })
}

document.getElementById("dataButton").addEventListener("click", function() {
    var dataContent = document.getElementById("dataContent");
    if (dataContent.style.display === "none") {
        dataContent.style.display = "block";
    } else {
        dataContent.style.display = "none";
    }
});


        // Function to show a pop-up notification
        function showNotification(message) {
            let notification = document.createElement('div');
            notification.textContent = message;
            notification.style.position = 'fixed';
            notification.style.top = '50%';
            notification.style.left = '50%';
            notification.style.transform = 'translate(-50%, -50%)';
            notification.style.backgroundColor = '#f44336';
            notification.style.color = 'white';
            notification.style.padding = '10px';
            notification.style.borderRadius = '5px';
            document.body.appendChild(notification);
            setTimeout(function() {
                document.body.removeChild(notification);
            }, 3000); // Remove the notification after 3 seconds
        }

        
        // let video = document.getElementById('video');
        let recordattendButton = document.getElementById('recordattend');
        // let websocket = new WebSocket('ws://localhost:5000/camera');

        recordattendButton.onclick = function() {
            if (video.style.display === 'none') {
                // Show the camera feed
                navigator.mediaDevices.getUserMedia({ video: true })
                    .then(function (mediaStream) {
                        video.srcObject = mediaStream;
                        video.style.display = 'block';
                    })
                    .catch(function (err) {
                        console.error('Error accessing the camera: ' + err.message);
                    });
            } else {
                // Hide the camera feed
                video.srcObject.getTracks().forEach(track => track.stop());
                video.srcObject = null;
                video.style.display = 'none';
            }
        };
        // document.getElementById("recordattendButton").addEventListener("click", function() {
        //     var recordattendContent = document.getElementById("recordattendContent");
        //     if (recordattendContent.style.display === "none") {
        //         recordattendContent.style.display = "block";
        //     } else {
        //         recordattendContent.style.display = "none";
        //     }
        // });

        // recordattendButton.onclick = function() {
        //     if (video.style.display === 'none') {
        //         // Show the camera feed
        //         fetch('/camera_feed') // Assuming this is the endpoint that provides the camera feed
        //             .then(response => response.blob())
        //             .then(blob => {
        //                 const video = document.getElementById('camera-feed');
        //                 video.src = URL.createObjectURL(blob);
        //                 video.style.display = 'block';
        //             })
        //             .catch(function (err) {
        //                 console.error('Error accessing the camera: ' + err.message);
        //             });
        //     } else {
        //         // Hide the camera feed
        //         video.src = '';
        //         video.style.display = 'none';
        //     }
        // };
       
        document.getElementById("databutton").addEventListener("submit", async function(event) {
            event.preventDefault();
        
            const form = event.target;
            const formData = new FormData(form);
        
            try {
                const response = await fetch('/admin', {
                    method: 'POST',
                    body: formData
                });
        
                const data = await response.json();
        
                if (data.message) {
                    const messageDiv = document.getElementById('message');
                    messageDiv.textContent = data.message;
                    messageDiv.style.display = 'block'; // Show the message div
                
                } else {
                    alert('Failed to add student. Please try again.');
                }
        
            } catch (error) {
                console.error('Error:', error);
                alert('An error occurred. Please try again.');
            }
        });

        
        async function stopCamera() {
    const closeBtn = document.getElementById('closeCamera');
    const errorDiv = document.getElementById('camera-error');
    
    try {
        closeBtn.disabled = true;
        closeBtn.textContent = 'Stopping Camera...';
        errorDiv.style.display = 'none';
        
        const response = await fetch("{{ url_for('stop_camera') }}");
        const result = await response.json();
        
        if (result.status === 'success') {
            document.getElementById('camera-feed').style.display = 'none';
            document.getElementById('openCamera').style.display = 'block';
            document.getElementById('closeCamera').style.display = 'none';
            
            const videoFeed = document.getElementById('video-feed');
            videoFeed.src = '';
        } else {
            throw new Error(result.message || 'Failed to stop camera');
        }
    } catch (error) {
        errorDiv.textContent = 'Failed to stop camera: ' + error.message;
        errorDiv.style.display = 'block';
    } finally {
        closeBtn.disabled = false;
        closeBtn.textContent = 'Close Camera';
    }
}