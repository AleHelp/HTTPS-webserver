#!/usr/bin/env python3
import http.server
import socketserver
import ssl
import argparse
import os

def parse_arguments():
    parser = argparse.ArgumentParser(description='Simple web server over HTTPS.')
    parser.add_argument('-i', '--ip', type=str, default="0.0.0.0", help='Specify an IP address (default: 127.0.0.1)')
    parser.add_argument('-p', '--port', type=int, default=443, help='Select a port (default: 443)')
    parser.add_argument('-d', '--directory', type=str, default="./", help='Select a directory (default is the current directory where you start it)')
    parser.add_argument('-c', '--cert', type=str, help='Specify a certificate to use')
    parser.add_argument('-k', '--key', type=str, help='Specify a private key')
    parser.epilog = ('To generate a self-signed certificate and the corresponding private key, use the following command: openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365.')
    return parser.parse_args()

args = parse_arguments()
directory_to_serve = args.directory

if args.cert is None or not os.path.isfile(args.cert):
    print(f"[*] Invalid or missing certificate.")
    exit(1)

if args.key is None or not os.path.isfile(args.key):
    print(f"[*] Invalid or missing key.")
    exit(1)

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=directory_to_serve, **kwargs)

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.load_cert_chain(certfile=args.cert, keyfile=args.key)

with socketserver.TCPServer((args.ip, args.port), MyHandler) as httpd:
    httpd.socket = ssl_context.wrap_socket(httpd.socket, server_side=True)
    print(f"[*] Serving directory at https://{args.ip}:{args.port} from {args.directory}")
    httpd.serve_forever()