import subprocess
import sys
import json
import time

# 1. Start the MCP server as a subprocess (if not already running)
#    This assumes weather_server.py is in the same directory and is executable.
proc = subprocess.Popen(
    [sys.executable, "weather_server.py"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,  # Use text mode for easier string handling
    bufsize=1   # Line-buffered
)

def send_request(request):
    """
    Sends a JSON-RPC request to the MCP server and returns the parsed response.
    """
    # Convert the request dictionary to a JSON string and send it to the server
    req_str = json.dumps(request)
    proc.stdin.write(req_str + "\n")
    proc.stdin.flush()
    # Read the response line from the server
    while True:
        line = proc.stdout.readline()
        if not line:
            continue
        try:
            response = json.loads(line)
            return response
        except json.JSONDecodeError:
            continue

# 2. Send the initialization request
init_request = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {
        "protocolVersion": "2024-11-05",
        "capabilities": {
            "roots": {"listChanged": True},
            "sampling": {}
        },
        "clientInfo": {"name": "test-client", "version": "1.0.0"}
    }
}
print("Sending initialize request...")
print(send_request(init_request))

# 3. Confirm initialization (no response expected)
initialized_notification = {
    "jsonrpc": "2.0",
    "method": "notifications/initialized"
}
# Notifications do not expect a response, but we send it anyway
proc.stdin.write(json.dumps(initialized_notification) + "\n")
proc.stdin.flush()
time.sleep(0.1)  # Give the server a moment

# 4. Request the list of available tools
list_tools_request = {
    "jsonrpc": "2.0",
    "id": 2,
    "method": "tools/list"
}
print("Requesting list of tools...")
print(send_request(list_tools_request))

# 5. Call the get_weather tool for Berlin
call_weather = {
    "jsonrpc": "2.0",
    "id": 3,
    "method": "tools/call",
    "params": {
        "name": "get_weather",
        "arguments": {"city": "berlin"}
    }
}
print("get_weather response:")
print(send_request(call_weather))

# 6. (Optional) Clean up: terminate