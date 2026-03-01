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
        
        # Pattern: /{lang}/juz{N} (e.g. /en/juz2, /ms/juz14)
        juz_pattern = r'^/(en|ms)/juz(\d{1,2})(?:\.html)?/?$'
        match = re.match(juz_pattern, path_without_query)

        # Pattern: /juz{N}.html (old static file links)
        bare_juz_pattern = r'^/juz(\d{1,2})\.html$'
        bare_match = re.match(bare_juz_pattern, path_without_query)

        if match:
            # Serve juz-page.html for juz routes
            self.path = '/juz-page.html'

        elif bare_match:
            # Redirect to clean slug URL
            self.send_response(302)
            self.send_header('Location', '/en/juz' + bare_match.group(1))
            self.end_headers()
            return

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
