# Solana Transaction Monitor

A simple and beautiful way to monitor Solana transactions in real-time.

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the script:
```bash
python solana_monitor.py
```

The script will:
- Connect to Solana mainnet
- Display the most recent transactions in real-time
- Show transaction details including:
  - Timestamp
  - Transaction status
  - Transaction fee
  - Balance changes
- Update every 5 seconds

Press Ctrl+C to stop the monitoring.

## Features

- Real-time transaction monitoring
- Beautiful console output with Rich
- Clear and readable transaction information
- Automatic updates every 5 seconds