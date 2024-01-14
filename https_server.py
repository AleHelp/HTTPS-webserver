#!/usr/bin/env python3

from http.server import SimpleHTTPRequestHandler, HTTPServer
import socketserver
import ssl
import argparse
import os
import socket
import psutil
import sys

class MyHTTPServer(socketserver.TCPServer):
    def server_bind(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        super().server_bind()

def serve_http(args):
    print(f"[+] Serving over HTTP at http://{args.ip}:{args.port} from {args.directory}")
    os.chdir(args.directory)
    server_class = HTTPServer
    server_address = (args.ip, args.port)
    with server_class(server_address, SimpleHTTPRequestHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n[!] Server stopped by user.")

def serve_https(args):
    if not os.path.isfile(args.cert) or not os.path.isfile(args.key):
        print("[-] Invalid or missing certificate or key.")
        exit(1)

    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain(certfile=args.cert, keyfile=args.key)

    os.chdir(args.directory)
    print(f"[+] Serving over HTTPS at https://{args.ip}:{args.port} from {args.directory}")
    httpd = MyHTTPServer((args.ip, args.port), SimpleHTTPRequestHandler)
    httpd.socket = ssl_context.wrap_socket(httpd.socket, server_side=True)
    with httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n[!] Server stopped by user.")

def list_interfaces():
    interfaces = psutil.net_if_addrs()
    print(f"[+] Listing network interfaces:\n")
    for interface_name, addresses in interfaces.items():
        print(f"Interface: {interface_name}")
        for address in addresses:
            if address.family == socket.AF_INET:
                print(f"address: {address.address}\n")

def main():
    parser = argparse.ArgumentParser(description='Simple web server over HTTPS and also in HTTP.')
    parser.add_argument('-l', '--list', action='store_true', help='List all network interfaces')
    parser.add_argument('-i', '--ip', type=str, default="0.0.0.0", help='Specify an IP address (default: 0.0.0.0)')
    parser.add_argument('-p', '--port', type=int, default=443, help='Select a port (default: 443 for HTTPS, 80 for HTTP)')
    parser.add_argument('-d', '--directory', type=str, default="./", help='Select a directory (default is the current directory where you start it)')
    parser.add_argument('-c', '--cert', type=str, help='Specify a certificate')
    parser.add_argument('-k', '--key', type=str, help='Specify a private key')
    parser.add_argument('--no-https', action='store_true', help='Serve over HTTP')
    parser.epilog = ('To generate a self-signed certificate and the corresponding private key, use the following command: openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365.')
    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        exit(0)

    if args.list:
        if any([args.cert, args.key, args.no_https]):
            list_interfaces()
        else:
            list_interfaces()
            exit(0) 
            
    if args.no_https:
        if any([args.cert, args.key]):
            print("[-] Cannot use Certificate and private key in HTTP")
            exit(1)
        if args.port == 443:
            args.port = 80
        serve_http(args)
    else:
        serve_https(args)

if __name__ == "__main__":
    main()
