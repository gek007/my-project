import re
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


def main():
    """Start a simple HTTP server that responds to GET / with 'Hello Kostya'.

    The server only starts when this module is executed as a script so importing
    `src.main` in tests doesn't start the server.
    """
    host = "0.0.0.0"
    port = 8000

    class HelloHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path == "/":
                body = "Hello Kostya".encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "text/plain; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
            else:
                self.send_response(404)
                self.send_header("Content-Type", "text/plain; charset=utf-8")
                self.end_headers()
                self.wfile.write(b"Not Found")

        # silence logging to keep output clean during tests/runs
        def log_message(self, format, *args):
            return

    server = ThreadingHTTPServer((host, port), HelloHandler)
    print(f"Starting HTTP server at http://{host}:{port} (GET / returns 'Hello Kostya')")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


def is_valid_email(email):
    """
    Optimized email validation function.
    Reduces redundant string operations while maintaining original logic.
    """
    # Combined early checks to reduce function calls
    if not email or "@" not in email:
        return False
    
    # Single split operation instead of multiple checks
    parts = email.split("@", 1)
    if len(parts) != 2:
        return False
    
    local_part, domain = parts
    
    # Combined checks using short-circuit evaluation
    if (not local_part or 
        not domain or 
        "." not in domain or
        domain.startswith(".") or 
        domain.endswith(".") or
        ".." in domain):
        return False
    
    return True


# write function that checks if the email is from a specific domain
def is_email_from_domain(email, domain):
    """
    Check if the email is from a specific domain.
    """
    # Validate email format
    if not is_valid_email(email):
        return False

    # Extract the domain from the email
    email_domain = email.split("@")[-1]
    return email_domain == domain

if __name__ == "__main__":
    main()