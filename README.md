# Group Kahoot

## Installation
You can run this through docker or manually:

### Docker Run
1. Install [docker](https://www.docker.com/).
2. Clone the repo
3. Run `docker compose up --build` in the root folder
4. Go to `http://localhost`

### Manual Run (Recommended for active development)
#### Frontend
1. Install [node.js](https://nodejs.com)
3. open terminal in root
4. `cd client`
5. `npm install`
6. `npm run dev`
#### Backend
#### First cd to server directory
Should be something like
`cd <path to server>/server`  
#### Build the image
`docker build -t kahoot-server .`  

#### Run the container
`docker run -p 8080:8080 kahoot-server`  

#### When you make changes  
1. Stop the container  
2, Run `docker run -p 8080:8080 kahoot-server`  
This will hot reload the code  

## Contributing
- Make sure you only push working code to main  
