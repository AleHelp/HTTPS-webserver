# HTTPS-webserver
Python script to create a simple HTTPS web server.

### Installation:
```bash
sudo git clone https://github.com/AleHelp/HTTPS-webserver.git
cd HTTPS-webserver
sudo chmod +x https_server.py
sudo cp ./https_server /usr/bin
```

### Usage:

_Command to generate a self-signed certificate and the corresponding private key_
```bash
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
```
```bash
https_server.py -c <cert.pem> -k <key.pem> -i <ip address> -p <port> -d <directory to serve> #parameters -i, -p, and -d are not mandatory; default values can be used.
```
```bash
https_server.py --help #parameter to open help list
```
