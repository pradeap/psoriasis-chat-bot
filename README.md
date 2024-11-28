Prerequisites
Ensure you have the following installed:
  Git and 
  Docker

  
Installation
  1. Clone the Repository
    Clone this repository to your local machine:
    Copy code
    git clone [https://github.com/pradeap/psoriasis-chat-bot)](https://github.com/pradeap/psoriasis-chat-bot.git)
    cd psoriasis-chat-bot
  2. Install Docker
    Follow the official Docker installation guide for your operating system.
    Verify Docker installation:
    bash
    Copy code
    docker --version

Setup
1. Build the Docker Image
  docker build -t psoriasis-chat-bot .

2. Run the Docker Container
   docker run -p 8080:8080 --name psoriasis-chat-container psoriasis-chat-bot

Usage
  Access the chatbot through your web browser at:
   http://localhost:8080

Stopping the Container

  To stop the container:
  
    docker stop psoriasis-chat-container
Removing the Container

  To remove the stopped container:
  
    docker rm psoriasis-chat-container
    
Removing the Image

  To delete the image:
  
    docker rmi psoriasis-chat-bot
    
