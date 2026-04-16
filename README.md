# Laravel Site Audit Tool

A lightweight Python-based auditing tool for authorized Laravel environment checks.
Built to help security teams and developers review web deployments at scale with concurrency, logging, and configurable request handling.

## Features

- Multi-target scanning from a domain list
- Concurrent requests using thread pools
- Request rate limiting
- Custom path checking
- Result logging to output files
- Simple and fast CLI workflow

## Use Cases

- Internal infrastructure review
- Staging and production validation
- Deployment verification
- Authorized security assessment

## Requirements

- Python 3.10+
- requests
- pymysql

## Installation

git clone https://github.com/AnggaTechI/laravel-scanner.git
cd laravel-scanner
pip install -r requirements.txt

## Usage

1. Put target domains into list.txt
2. Run the script:

python code.py

## Configuration

You can adjust the main settings inside the script:

- MAX_WORKERS
- MAX_REQUESTS_PER_SECOND
- REQUEST_TIMEOUT
- INPUT_FILE
- custom paths to audit

## Output

The tool stores findings in text-based result files for easier review and triage.

## Disclaimer

This project is intended only for authorized testing and internal auditing.
Do not use it against systems you do not own or do not have explicit permission to assess.

## Contributing

Pull requests, issue reports, and improvements are welcome.

## License

For educational and internal authorized use only.
