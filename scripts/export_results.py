from __future__ import annotations
import argparse
from pathlib import Path

from backend.analytics.hub_analysis import busiest_hubs, hub_load_and_delay
from backend.analytics.dashboard_queries import busiest_routes, delay_risk_overview


def main() -> int:
    parser = argparse.ArgumentParser(description="Export analytics to CSV")
    parser.add_argument("--out", type=Path, default=Path("exports"), help="Output directory")
    args = parser.parse_args()

    args.out.mkdir(parents=True, exist_ok=True)

    busiest_hubs().to_csv(args.out / "busiest_hubs.csv", index=False)
    hub_load_and_delay().to_csv(args.out / "hub_load_delay.csv", index=False)
    busiest_routes().to_csv(args.out / "busiest_routes.csv", index=False)
    delay_risk_overview().to_csv(args.out / "delay_risk_overview.csv", index=False)

    print(f"Exports written to {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
