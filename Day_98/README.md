# Daily News Digest

Automated German news aggregation with email delivery.

## Features

- RSS feed integration from German news sources
- HTML email generation and delivery
- Automated daily scheduling
- Smart filtering and deduplication

## Sources

- SPIEGEL Online
- ZEIT Online  
- Handelsblatt
- WELT
- FAZ
- Süddeutsche
- FOCUS Online

## Setup

### Installation
```bash
pip install -r requirements.txt
```

### Configuration
Copy `.env.example` to `.env` and update with your credentials:
```bash
cp .env.example .env
```

Edit `.env` with your Gmail credentials and preferences.

## Usage

```bash
# Run once
python news_digest.py

# Run scheduled daily
python news_digest.py --schedule
```
