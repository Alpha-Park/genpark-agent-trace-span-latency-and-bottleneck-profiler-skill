"""Agent Trace Span Latency & Bottleneck Profiler.
100% Python Standard Library.
"""

class AgentTraceBottleneckProfiler:
    """Analyzes hierarchical OpenTelemetry-style agent execution spans to pinpoint latency bottlenecks and retry loops."""

    @staticmethod
    def profile_trace(spans: list, sla_ms: float = 2000.0) -> dict:
        total_duration = 0.0
        bottlenecks = []
        tool_call_counts = {}

        for sp in spans:
            name = sp.get("name", "unknown_span")
            dur = float(sp.get("duration_ms", 0.0))
            kind = sp.get("kind", "internal")
            total_duration += dur

            if kind == "tool_call":
                tool_call_counts[name] = tool_call_counts.get(name, 0) + 1

            if dur >= sla_ms * 0.4:
                bottlenecks.append({
                    "span": name,
                    "duration_ms": round(dur, 2),
                    "share_pct": 0.0
                })

        for b in bottlenecks:
            b["share_pct"] = round((b["duration_ms"] / max(1.0, total_duration)) * 100.0, 1)

        retry_loops = [k for k, v in tool_call_counts.items() if v >= 3]
        sla_breached = total_duration > sla_ms

        return {
            "total_duration_ms": round(total_duration, 2),
            "sla_breached": sla_breached,
            "bottlenecks": sorted(bottlenecks, key=lambda x: x["duration_ms"], reverse=True),
            "detected_retry_loops": retry_loops
        }
