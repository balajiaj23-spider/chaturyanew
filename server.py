"""
Custom Development Server for Chathurya Student Developers Club Workshop Website
- Serves '/' directly to index.html (Homepage)
- Completely disables directory listings
- Blocks access to .git, dotfiles, and sensitive configuration files
- Serves static assets (HTML, CSS, JS, SVG, Images) cleanly with proper MIME types
"""

import os
import sys
import http.server
import socketserver
from urllib.parse import unquote

PORT = 8000
if len(sys.argv) > 1 and sys.argv[1].isdigit():
    PORT = int(sys.argv[1])

DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class SecureStaticHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_GET(self):
        # 1. Clean path
        url_path = unquote(self.path.split('?')[0].split('#')[0])
        
        # 2. Block hidden files (.git, .gitignore, etc)
        parts = [p for p in url_path.strip('/').split('/') if p]
        if any(p.startswith('.') for p in parts):
            self.send_error(403, "Access Forbidden: Hidden files and directories cannot be accessed.")
            return

        # 3. Handle root '/' -> serve index.html
        if url_path == '/' or url_path == '':
            self.path = '/index.html'
            return super().do_GET()

        # 4. Check local filesystem path
        local_path = self.translate_path(self.path)

        # 5. If it's a directory, check if index.html exists in it, else deny directory listing
        if os.path.isdir(local_path):
            index_file = os.path.join(local_path, 'index.html')
            if os.path.exists(index_file):
                self.path = self.path.rstrip('/') + '/index.html'
                return super().do_GET()
            else:
                self.send_error(403, "Access Forbidden: Directory listing is disabled.")
                return

        return super().do_GET()

    def list_directory(self, path):
        self.send_error(403, "Access Forbidden: Directory listing is disabled.")
        return None

if __name__ == '__main__':
    socketserver.TCPServer.allow_reuse_address = True
    
    with socketserver.TCPServer(("", PORT), SecureStaticHTTPRequestHandler) as httpd:
        print("================================================================")
        print("Server started successfully!")
        print(f"Homepage URL : http://localhost:{PORT}/")
        print(f"Serving Root : {DIRECTORY}")
        print("Directory listing disabled & hidden files protected.")
        print("================================================================")
        print("Press Ctrl+C to stop the server.")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")
            httpd.server_close()
