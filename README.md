# SCC2019

## List of services
### UserManager
*A simple User Manager that supports Login, Register, and basic User management tasks written in Typescript*
### Client
*A vuejs web client to access the features of the app*
### FileService
*A python Server handling all file related requests*
### Redirector
*A nginx Server that redirects incoming requests to the correct service*


## Run full application 
Run the docker-compose.yml file to start all services and containers. If started on a local machine you need to edit *services/Redirector/nginx.conf* to use the localhost domain name and add the correct https certificates.