import os

def parse_meminfo(file_path='/proc/meminfo'):
    """
    Reads Linux /proc/meminfo directly to calculate memory utilization.
    Safely falls back if executed on non-Linux environments (like Windows/macOS host).
    """
    # 1. Fallback check for local development inside Windows/Mac PyCharm
    if not os.path.exists(file_path):
        return {
            "total_mb": 16000.0,
            "used_mb": 8000.0,
            "used_percent": 50.0
        }

    # 2. Parse the real Linux /proc/meminfo file
    mem_data = {}
    with open(file_path, 'r') as f:
        for line in f:
            fields = line.split()
            if not fields:
                continue
            # Remove the colon from keys like 'MemTotal:' -> 'MemTotal'
            key = fields[0].strip(':')
            val = int(fields[1])
            mem_data[key] = val

    # 3. Extract core metrics
    total = mem_data.get('MemTotal', 0)
    available = mem_data.get('MemAvailable', 0)

    if total == 0:
        return {"error": "MemTotal read as zero or unavailable"}

    # 4. Calculate mathematical telemetry
    used = total - available
    used_percent = (used / total) * 100

    # 5. Return a clean, structured dictionary
    return {
        "total_mb": round(total / 1024, 2),
        "used_mb": round(used / 1024, 2),
        "used_percent": round(used_percent, 2)
    }