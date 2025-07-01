[<img src="https://img.shields.io/badge/powered%20by-OpenCitations-%239931FC?labelColor=2D22DE" />](http://opencitations.net)
[![Run tests](https://github.com/opencitations/api/actions/workflows/run_tests.yml/badge.svg?branch=master)](https://github.com/opencitations/api/actions/workflows/run_tests.yml)
[![Coverage](https://raw.githubusercontent.com/arcangelo7/badges/main/opencitations-api-coverage-master.svg)](https://opencitations.github.io/api/coverage/)

# api
REST API specification for all the OpenCitations datasets

## Installation
Install dependencies using [uv](https://docs.astral.sh/uv/):
```bash
uv sync
```

## Testing

### Prerequisites
- Docker (for test database)

### Running Tests
1. Install development dependencies:
   ```bash
   uv sync --dev
   ```

2. Start the test database:
   ```bash
   ./test/start_test_db.sh  # Linux/macOS
   # or
   .\test\start_test_db.ps1  # Windows PowerShell
   ```

3. Run the test suite:
   ```bash
   uv run pytest
   ```

4. Stop the test database:
   ```bash
   ./test/stop_test_db.sh  # Linux/macOS
   # or
   .\test\stop_test_db.ps1  # Windows PowerShell
   ```