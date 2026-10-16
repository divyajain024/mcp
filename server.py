import os
import hashlib
from fastmcp import FastMCP
from fastmcp.server.dependencies import get_http_headers

# Initialize FastMCP server without the deprecated argument
mcp = FastMCP("Exam Challenge Server")

@mcp.tool()
def solve_challenge() -> str:
    """Solve the exam challenge by reading the X-Exam-Challenge header and hashing it with the registered email."""
    headers = get_http_headers(include_all=True)
    
    challenge = None
    for k, v in headers.items():
        if k.lower() == "x-exam-challenge":
            challenge = v
            break
            
    if not challenge:
        return "Error: X-Exam-Challenge header missing"
        
    normalized_email = "22f2000901@ds.study.iitm.ac.in".strip().lower()
    combined = f"{challenge}:{normalized_email}"
    full_hash = hashlib.sha256(combined.encode("utf-8")).hexdigest()
    
    return full_hash[:16]

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    mcp.run(transport="http", host="0.0.0.0", port=port)
