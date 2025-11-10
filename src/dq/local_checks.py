"""Data quality checks for local development."""

import pandas as pd
import json
from pathlib import Path
from typing import Dict, List, Any

def load_sample_data(file_path: str) -> pd.DataFrame:
    """Load sample telemetry data from JSONL file."""
    data = []
    with open(file_path, 'r') as f:
        for line in f:
            data.append(json.loads(line.strip()))
    return pd.DataFrame(data)

def run_dq_checks(df: pd.DataFrame) -> Dict[str, Any]:
    """Run data quality checks on telemetry data."""
    checks = {}

    # Completeness checks
    checks['total_rows'] = len(df)
    checks['null_rates'] = df.isnull().mean().to_dict()

    # Value range checks
    checks['speed_range'] = {
        'min': df['speed_kmh'].min(),
        'max': df['speed_kmh'].max(),
        'out_of_range': ((df['speed_kmh'] < 0) | (df['speed_kmh'] > 200)).sum()
    }

    checks['accel_range'] = {
        'x_range': {'min': df['accel_x_m_s2'].min(), 'max': df['accel_x_m_s2'].max()},
        'y_range': {'min': df['accel_y_m_s2'].min(), 'max': df['accel_y_m_s2'].max()}
    }

    # GPS accuracy checks
    checks['gps_accuracy'] = {
        'avg_accuracy': df['gps_accuracy_m'].mean(),
        'high_accuracy_count': (df['gps_accuracy_m'] < 10).sum()
    }

    # Event type distribution
    checks['event_distribution'] = df['event_type'].value_counts().to_dict()

    # Schema compliance (basic)
    required_fields = ['device_id', 'trip_id', 'ts', 'event_type', 'provider', 'location_precision']
    checks['schema_compliance'] = {
        'missing_required': [field for field in required_fields if field not in df.columns],
        'null_required': {field: df[field].isnull().sum() for field in required_fields if field in df.columns}
    }

    return checks

def generate_html_report(checks: Dict[str, Any], output_path: str):
    """Generate HTML report from DQ checks."""
    html = f"""
    <html>
    <head>
        <title>Data Quality Report</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            h1 {{ color: #333; }}
            h2 {{ color: #666; }}
            table {{ border-collapse: collapse; width: 100%; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #f2f2f2; }}
            .pass {{ color: green; }}
            .fail {{ color: red; }}
        </style>
    </head>
    <body>
        <h1>Data Quality Report</h1>
        <p>Generated on: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}</p>

        <h2>Summary</h2>
        <p>Total rows: {checks['total_rows']}</p>

        <h2>Null Rates</h2>
        <table>
            <tr><th>Field</th><th>Null Rate</th></tr>
            {"".join(f"<tr><td>{k}</td><td>{v:.2%}</td></tr>" for k, v in checks['null_rates'].items())}
        </table>

        <h2>Speed Range Check</h2>
        <p>Min: {checks['speed_range']['min']:.1f}, Max: {checks['speed_range']['max']:.1f}</p>
        <p class="{'fail' if checks['speed_range']['out_of_range'] > 0 else 'pass'}">
            Out of range (0-200 km/h): {checks['speed_range']['out_of_range']}
        </p>

        <h2>GPS Accuracy</h2>
        <p>Average accuracy: {checks['gps_accuracy']['avg_accuracy']:.1f}m</p>
        <p>High accuracy (<10m): {checks['gps_accuracy']['high_accuracy_count']}</p>

        <h2>Event Distribution</h2>
        <table>
            <tr><th>Event Type</th><th>Count</th></tr>
            {"".join(f"<tr><td>{k}</td><td>{v}</td></tr>" for k, v in checks['event_distribution'].items())}
        </table>

        <h2>Schema Compliance</h2>
        <p>Missing required fields: {checks['schema_compliance']['missing_required']}</p>
        <table>
            <tr><th>Field</th><th>Null Count</th></tr>
            {"".join(f"<tr><td>{k}</td><td>{v}</td></tr>" for k, v in checks['schema_compliance']['null_required'].items())}
        </table>
    </body>
    </html>
    """

    with open(output_path, 'w') as f:
        f.write(html)

if __name__ == "__main__":
    # Load sample data
    df = load_sample_data('data/samples/poc_telemetry.jsonl')

    # Run checks
    checks = run_dq_checks(df)

    # Generate report
    output_path = 'data/reports/dq_report.html'
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    generate_html_report(checks, output_path)

    print(f"Data quality report generated: {output_path}")
    print(f"Total rows: {checks['total_rows']}")
    print(f"Null rates: {checks['null_rates']}")
