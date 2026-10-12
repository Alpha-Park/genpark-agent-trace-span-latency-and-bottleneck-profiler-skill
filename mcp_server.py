"""MCP server for Agent Trace Span Latency & Bottleneck Profiler."""
import sys
import json
from client import AgentTraceBottleneckProfiler

def handle_request(req):
    method = req.get("method")
    if method == "tools/list":
        return {
            "tools": [{
                "name": "profile_agent_trace",
                "description": "Profiles agent trace spans to identify latency bottlenecks and retry loops",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "spans": {"type": "array"},
                        "sla_ms": {"type": "number"}
                    },
                    "required": ["spans"]
                }
            }]
        }
    elif method == "tools/call":
        params = req.get("params", {})
        if params.get("name") == "profile_agent_trace":
            args = params.get("arguments", {})
            res = AgentTraceBottleneckProfiler.profile_trace(
                args.get("spans", []),
                args.get("sla_ms", 2000.0)
            )
            return {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
    return {"error": "Method not found"}

if __name__ == "__main__":
    for line in sys.stdin:
        if line.strip():
            print(json.dumps(handle_request(json.loads(line))))
            sys.stdout.flush()
