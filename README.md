# Steam Deck Refurbished Stock Checker

## Description

This project provides a dockerized script to monitor the availability of refurbished Steam Deck units on the official store page and send notifications to a specified Discord channel when stock is detected. The script uses Selenium for web scraping and Discord webhooks for notifications.

## Setup

1. Get `docker-compose.yml` from main branch

2. Edit the `docker-compose.yaml` file and set your Discord webhook URL

3. Start the container:
   ```sh
   docker compose up -d
   ```

## Configuration

Configure the script by editing the environment variables in the provided `docker-compose.yaml` file:

| Variable | Default | Description |
|----------|---------|-------------|
| `DISCORD_WEBHOOK_URL` | *Required* | Your Discord webhook URL for notifications |
| `CRON_SCHEDULE` | `*/5 * * * *` | Cron schedule (every 5 minutes by default) |
| `PRODUCT_TITLES` | OLED models | Comma-separated list of Steam Deck models to monitor |
| `DEBUG` | `false` | Set to `true` to always send notifications (for testing) |

### Available Steam Deck Models

- `Steam Deck 512GB OLED - Valve Certified Refurbished`
- `Steam Deck 1TB OLED - Valve Certified Refurbished` 
- `Steam Deck 64 GB LCD - Valve Certified Refurbished`
- `Steam Deck 256 GB LCD - Valve Certified Refurbished`
- `Steam Deck 512 GB LCD - Valve Certified Refurbished`

## Docker Commands

```sh
# Start the container
docker compose up --build -d

# Stop the container
docker compose down

# View logs
docker compose logs -f sd-notifier

# Check application logs
docker exec -it sd-notifier cat /app/checker.log
```

## Discord Webhook Setup

1. In Discord, go to Server Settings → Integrations → Webhooks
2. Click "New Webhook" or "Create Webhook"
3. Choose the channel where you want notifications
4. Copy the webhook URL
5. Use this URL in your `docker-compose.yaml`

## Disclaimer

This script is provided "as is" for personal use. Be aware of website scraping policies and use responsibly.
