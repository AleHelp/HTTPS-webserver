#!/usr/bin/env python3

from http.server import SimpleHTTPRequestHandler, HTTPServer
import socketserver
import ssl
import argparse
import os
import socket

def parse_arguments():
    parser = argparse.ArgumentParser(description='Simple web server over HTTPS.')
    parser.add_argument('-i', '--ip', type=str, default="0.0.0.0", help='Specify an IP address (default: 0.0.0.0)')
    parser.add_argument('-p', '--port', type=int, default=443, help='Select a port (default: 443)')
    parser.add_argument('-d', '--directory', type=str, default="./", help='Select a directory (default is the current directory where you start it)')
    parser.add_argument('-c', '--cert', type=str, help='Specify a certificate to use')
    parser.add_argument('-k', '--key', type=str, help='Specify a private key')
    parser.add_argument('--no-https', action='store_true', help='Serve over HTTP.')
    parser.epilog = ('To generate a self-signed certificate and the corresponding private key, use the following command: openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365.')
    return parser.parse_args()

def serve_http(args):
    print(f"[+] Serving directory at http://{args.ip}:{args.port} from {args.directory}")
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

    print(f"[+] Serving directory at https://{args.ip}:{args.port} from {args.directory}")
    httpd = socketserver.TCPServer((args.ip, args.port), SimpleHTTPRequestHandler)
    httpd.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    with httpd:
        httpd.socket = ssl_context.wrap_socket(httpd.socket, server_side=True)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n[!] Server stopped by user.")

def main():
    args = parse_arguments()

    if args.no_https:
        if any([args.cert, args.key]):
            print("[-] Cannot use Certificate and private key in HTTP")
            exit(1)
        else:
            serve_http(args)
    else:
        serve_https(args)

if __name__ == "__main__":
    main()
