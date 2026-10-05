"""MCP server for Natural Language SaaS Action Controller."""
import sys
import json
from client import NaturalLanguageSaaSController

def handle_request(req):
    method = req.get("method")
    if method == "tools/list":
        return {
            "tools": [{
                "name": "parse_saas_intent",
                "description": "Maps natural language commands to verified SaaS API endpoints",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "intent_str": {"type": "string"},
                        "entities": {"type": "object"}
                    },
                    "required": ["intent_str", "entities"]
                }
            }]
        }
    elif method == "tools/call":
        params = req.get("params", {})
        if params.get("name") == "parse_saas_intent":
            args = params.get("arguments", {})
            res = NaturalLanguageSaaSController.parse_intent(args.get("intent_str", ""), args.get("entities", {}))
            return {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
    return {"error": "Method not found"}

if __name__ == "__main__":
    for line in sys.stdin:
        if line.strip():
            print(json.dumps(handle_request(json.loads(line))))
            sys.stdout.flush()
