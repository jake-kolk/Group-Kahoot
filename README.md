If you want to run this, install docker, clone the repo, open a terminal in the root, and run these commands:  
`docker build -t kahoot-server .`  
Once that runs, enter  
`docker run -it --rm -p 8080:8080  kahoot-server`  
You should see Server running on :8080 if it is sucsessful  
Now open the client.html file in a browser to test  
