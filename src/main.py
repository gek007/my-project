import re

from fastapi import FastAPI
import uvicorn

# Create FastAPI app at module level for uvicorn reload to work
app = FastAPI()

@app.get("/")
async def read_root():
    return "Hello Kostya4"

def main():
    host = "0.0.0.0"
    port = 8000
    uvicorn.run(app, host=host, port=port)

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