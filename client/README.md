## Installation

Run without docker. This is best for development as the site will update live without needing to restart the webserver.
1. Install [node.js](https://nodejs.org/)
2. clone repository
3. `cd ./client`
5. `npm install`
6. `npm run dev`

Alternatively, you can use docker
1. `docker build -t kahoot-client .`
2. `docker run --rm -p 80:80 kahoot-client`
You can change the first port number 80 to whatever port you want