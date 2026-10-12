"""Example usage for Agent Trace Span Latency & Bottleneck Profiler."""
from client import AgentTraceBottleneckProfiler

if __name__ == "__main__":
    spans = [
        {"name": "planner_step", "duration_ms": 350, "kind": "llm"},
        {"name": "sql_fetch", "duration_ms": 1400, "kind": "tool_call"},
        {"name": "sql_fetch", "duration_ms": 400, "kind": "tool_call"},
        {"name": "sql_fetch", "duration_ms": 450, "kind": "tool_call"}
    ]
    report = AgentTraceBottleneckProfiler.profile_trace(spans, sla_ms=2000.0)
    print("SLA Breached:", report["sla_breached"])
    print("Retry Loops:", report["detected_retry_loops"])
