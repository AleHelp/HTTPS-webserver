# HTTPS-webserver
Python script to create a simple HTTPS web server.

### Installation:
```bash
sudo git clone https://github.com/AleHelp/HTTPS-webserver.git
cd HTTPS-webserver
chmod +x https_server 
sudo cp ./https_server /usr/bin
```

### Usage:
```bash
https_server -c <cert.pem> -k <key.pem> -i <ip address> -p <port> -d <directory to server> #The parameters -i, -p, and -d are not mandatory; default values can be used.
```
```bash
https_server --help #parameter to open help list
```
