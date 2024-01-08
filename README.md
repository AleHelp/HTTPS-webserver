# HTTPS-webserver
_Python script to create a simple HTTPS web server is also possible to use it in HTTP._

### Installation:
```bash
git clone https://github.com/AleHelp/HTTPS-webserver.git
cd HTTPS-webserver
pip3 install -r requirements.txt
chmod +x https_server.py
sudo cp ./https_server.py /usr/bin
```
### Usage:
```
-h, --help            show this help message and exit
-l, --list            List all network interfaces
-i IP, --ip IP        Specify an IP address (default: 0.0.0.0)
-p PORT, --port PORT  Select a port (default: 443 for HTTPS, 80 for HTTP)
-d DIRECTORY, --directory DIRECTORY
                      Select a directory (default is the current directory where you start it)
-c CERT, --cert CERT  Specify a certificate
-k KEY, --key KEY     Specify a private key
--no-https            Serve over HTTP
```
_Command to generate a self-signed certificate and the corresponding private key_
```bash
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
```
_Command to use it in HTTPS_
```bash
https_server.py -c <cert.pem> -k <key.pem> -i <ip address> -p <port> -d <directory to serve> #parameters -i, -p, and -d are not mandatory; default values can be used.
```
_Command to use it in HTTP_
```bash
https_server.py --no-https -i <ip address> -p <port> -d <directory to serve> #parameters -i, -p, and -d are not mandatory; default values can be used.
```
_Command to list network interfaces_
```bash
https_server.py -l
```
