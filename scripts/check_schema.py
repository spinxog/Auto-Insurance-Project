#!/usr/bin/env python3
"""Schema validation script using fastavro."""

import json
import sys
import fastavro
from pathlib import Path

def validate_jsonl_with_avro(jsonl_file: str, avro_schema_file: str) -> bool:
    """Validate JSONL file against Avro schema."""
    try:
        # Load Avro schema
        with open(avro_schema_file, 'r') as f:
            schema = json.load(f)

        # Read and validate each line
        with open(jsonl_file, 'r') as f:
            for i, line in enumerate(f, 1):
                try:
                    record = json.loads(line.strip())
                    # Validate against schema (fastavro will raise exception if invalid)
                    fastavro.validate(record, schema)
                except (json.JSONDecodeError, fastavro.ValidationError) as e:
                    print(f"Record {i}: {e}")
                    return False

        print(f"All {i} records valid")
        return True

    except FileNotFoundError as e:
        print(f"File not found: {e}")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python check_schema.py <jsonl_file> <avro_schema_file>")
        sys.exit(1)

    jsonl_file = sys.argv[1]
    avro_file = sys.argv[2]

    if validate_jsonl_with_avro(jsonl_file, avro_file):
        print("Schema validation PASSED")
        sys.exit(0)
    else:
        print("Schema validation FAILED")
        sys.exit(1)
