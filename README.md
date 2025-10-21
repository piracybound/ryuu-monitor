## Ryuu Monitor
A Discord self-bot that monitors Ryuu's update and upload channels and relays them to webhooks with Steam API integration.

> [!WARNING]
> As a self-bot, this runs on your personal Discord account via a user token and is against Discord's ToS.

- Monitors channels for messages
- Fetches game information from Steam API
- Tracks processed messages to avoid duplicates
- Automatically processes backlog on startup

### prerequisites
- Python 3.8 or higher
- Discord Token
- Discord Webhook URLs (for output channels)
- Steam API key (optional, but recommended for better data)

### config
Create a `.env` file with the following variables:
```env
# Your Discord user token (REQUIRED)
DISCORD_TOKEN=your_user_token_here

# Channel IDs to monitor (REQUIRED)
UPDATE_CHANNEL_ID=1234567890123456789
UPLOAD_CHANNEL_ID=9876543210987654321

# Webhook URLs for forwarding messages (REQUIRED)
UPDATE_WEBHOOK_URL=https://discord.com/api/webhooks/...
UPLOAD_WEBHOOK_URL=https://discord.com/api/webhooks/...

# Steam API key (OPTIONAL - enhances game information)
STEAM_API_KEY=your_steam_api_key_here

# File to store last processed message IDs (OPTIONAL)
PROCESSED_FILE=last_processed.json
```

#### obtain your token
> [!WARNING]
> Never share your Discord token with anyone.
1. Open Discord in your web browser
2. Press `F12` to open Developer Tools
3. Go to the `Console` tab
4. Type this and press Enter:
   ```javascript
   (webpackChunkdiscord_app.push([[''],{},e=>{m=[];for(let c in e.c)m.push(e.c[c])}]),m).find(m=>m?.exports?.default?.getToken!==void 0).exports.default.getToken()
   ```
5. Copy the token (without quotes)

#### obtain channel ids
1. Enable Developer Mode in Discord (User Settings > Advanced > Developer Mode)
2. Right-click on the channel you want to monitor
3. Click "Copy ID"

#### create webhook
1. Go to the channel where you want to receive notifications
2. Click the gear icon (Edit Channel)
3. Go to Integrations > Webhooks
4. Click "New Webhook"
5. Copy the webhook URL

#### obtain Steam API key
1. Visit [Steam Web API Key](https://steamcommunity.com/dev/apikey)
2. Sign in with your Steam account
3. Register a new API key
4. Copy the key to your `.env` file

### usage
Run the bot:
```bash
python monitor.py
```

You should see:
```
🤖 Bot is running!
```

### license
This project is technically unlicensed, but do what the fuck you want with it.