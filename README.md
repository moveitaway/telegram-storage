# Telegram Storage

## How to use

1. Create `.env.docker` in project root
 ```
TELEGRAM_BOT_TOKEN=<your-telegram-token>
TELEGRAM_API_ID=<api-id>
TELEGRAM_API_HASH=<api-hash>
TELEGRAM_LOCAL=1
TELEGRAM_LOCAL_API=http://telegram-bot-api:8081
PUBLIC_URL_PREFIX=https://your-domain.tld/
UPLOAD_DIRECTORY=uploads
```
You can retrieve `<api-id>` and `<api-hash>` [here](https://core.telegram.org/api/obtaining_api_id).

2. Run docker-compose up -d
3. Configure your webserver (nginx) to serve `UPLOAD_DIRECTORY` directory
4. Enjoy