#!/usr/bin/env python3
"""
Custom HTTP server with slug-based routing for Quranic Studies
Routes /{lang}/juz{N} to juz-page.html template
"""
import http.server
import socketserver
import re
import os
from urllib.parse import unquote

PORT = 8080

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Parse the path
        path = unquote(self.path)
        
        # Remove query string and fragment for pattern matching
        path_without_query = path.split('?')[0].split('#')[0]
        
        # Pattern: /{lang}/juz{N} where lang is 2 letters and N is 1-2 digits
        juz_pattern = r'^/(en|ms)/juz(\d{1,2})/?$'
        match = re.match(juz_pattern, path_without_query)
        
        if match:
            # Serve juz-page.html for juz routes
            self.path = '/juz-page.html'
        
        # For root, serve index.html
        elif path_without_query == '/':
            self.path = '/index.html'
        
        # All other paths are served normally (static files)
        return super().do_GET()

if __name__ == '__main__':
    with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
        print(f"🌙 Quranic Studies server running at http://localhost:{PORT}")
        print(f"📖 Visit http://localhost:{PORT}/en/juz2 for Juz 2")
        print(f"Press Ctrl+C to stop")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n👋 Server stopped")
