def evaluate_health(metrics, config):
    """
    Evaluates system metrics against JSON configured thresholds.
    Implements boundary classification logic to return state strings.
    """
    # 1. Edge Case Handling: If telemetry failed, state is UNKNOWN
    if "error" in metrics:
        return "UNKNOWN"

    usage = metrics["used_percent"]
    thresholds = config["thresholds"]

    # 2. Boundary Evaluation Logic
    if usage >= thresholds["critical"]:
        return "CRITICAL"
    elif usage >= thresholds["warning"]:
        return "WARNING"
    else:
        return "HEALTHY"