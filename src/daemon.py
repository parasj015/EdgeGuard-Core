import time
import json
import os
from telemetry import parse_meminfo
from evaluator import evaluate_health


def load_config():
    """Safely resolves the path to config.json and loads the threshold rules."""
    # 1. Dynamically find the absolute path of the current file
    base_dir = os.path.dirname(os.path.abspath(__file__))  # points to EdgeGuard/src
    root_dir = os.path.dirname(base_dir)  # points to EdgeGuard/

    # 2. Explicitly define config_path relative to the project root folder
    config_path = os.path.join(root_dir, 'config', 'config.json')

    # 3. Check if the file exists before reading to avoid crashes
    if not os.path.exists(config_path):
        # Fallback default rules if the file is missing
        return {
            "check_interval_seconds": 5,
            "thresholds": {"warning": 75.0, "critical": 90.0}
        }

    # 4. Open and parse the JSON file safely
    with open(config_path, 'r') as f:
        return json.load(f)

def main():
    config = load_config()
    log_path = config["log_file_path"]

    print("[*] EdgeGuard Engine successfully running. Press Ctrl+C to terminate.")

    # Main infinite daemon execution loop
    while True:
        try:
            # 1. Gather system telemetry metrics
            metrics = parse_meminfo()

            # 2. Evaluate system state against thresholds
            status = evaluate_health(metrics, config)

            # 3. Serialize data into a structured JSON log entry
            report = {
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "metrics": metrics,
                "status": status
            }

            # 4. Attempt writing to production system log path
            try:
                with open(log_path, 'a') as log_file:
                    log_file.write(json.dumps(report) + '\n')
            except (PermissionError, FileNotFoundError):
                # Fallback to local project directory if running without administrative rights on host
                fallback_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'edgeguard_local.log')
                with open(fallback_path, 'a') as log_file:
                    log_file.write(json.dumps(report) + '\n')

            # 5. Sleep for the configured interval duration
            time.sleep(config["check_interval_seconds"])

        except KeyboardInterrupt:
            print("\n[-] EdgeGuard Daemon shutting down gracefully. Goodbye.")
            break


if __name__ == "__main__":
    main()