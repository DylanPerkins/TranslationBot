# Polyglot

Polyglot is a multilingual translation Discord bot built using Python and the discord.http library. It utilizes the DeepL API for high-quality and efficient translations.

## What you will need

- Python 3.11 or higher
- A DeepL API key (you can get one from [DeepL's website](https://www.deepl.com/pro-api))
- A Discord bot token (you can create a bot and get a token from the [Discord Developer Portal](https://discord.com/developers/applications))

### Local Development Environment

- NGROK to expose your local server to the internet for testing HTTP webhooks

### Production Environment

- A VPS or server to host the bot (e.g., OVH, AWS, DigitalOcean, etc.)
- Nodejs and NPM to install PM2 for process management
- A web server like Nginx to handle incoming requests to your bot
- A non-self-signed SSL certificate for secure communication (Required by Discord for webhooks)

## Setup Instructions for Local Development

1. **Clone the Repository**: Start by cloning the repository to your local machine.

   ```bash
   git clone <repository-url>
   cd TranslationBot
   ```

2. **Create a Virtual Environment**: It's recommended to use a virtual environment to manage dependencies.

   ```bash
   python -m venv Polyglot
   source Polyglot/bin/activate  # On Windows use `Polyglot\Scripts\activate`
   ```

3. **Install Dependencies**: Install the required Python packages.

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**: Copy and rename the `.env.example` file in the root directory to `.env` and fill in all of the required values.

5. **Run the Bot**: You can run the bot locally for testing.

   ```bash
   python index.py
   ```

6. **Set Up Webhooks**: If you plan to use webhooks, set up NGROK to expose your local server.

   ```bash
   ngrok http 8080
   ```

   NGROK will provide you with a public URL that you will need to input into the Interactions Endpoint URL field in your Discord application settings through the Discord Developer Portal. Make sure the bot is running before trying to "save" the changes in the Discord Developer Portal.

7. **Invite the Bot to Your Server**: Use the OAuth2 URL Generator in the Discord Developer Portal to generate an invite link for your bot with the necessary permissions and invite it to your server.

8. **That's it!**: Your bot should now be up and running. You can test it by running the `/bot info` command in your Discord server.

## Setup Instructions for Production

You will need to follow the steps from the Local Development section, excluding the usage of NGROK in step 6. Instead, you will need to set up a web server like NGINX on your PC or on a VPS to handle incoming requests to your bot. You will also need a non-self-signed SSL certificate, as Discord requires this for an interations endpoint.

***Note**: This section will be detailed with what I did to set up my bot on a VPS and is not the only way to do it.*

1. **Purchase a VPS or server**: You can purchase this from a provider of your choice (e.g., OVH, AWS, DigitalOcean, etc.), or you can host it on your own PC.

2. **Purchase a domain name**: If you don't already have one, you can purchase a domain name from a provider of your choice (e.g., Namecheap, GoDaddy, etc.). This is a requirement, from what I understand.

3. **Setup Cloudflare Tunneling**: This will expose your local server to the internet securely. This will also provide you with a signed SSL certificate, which we need.

4. **Install Nodejs and NPM**: We need to install Nodejs and NPM to use PM2 for process management. If you do not want to use PM2, you can skip this step and step 5.

5. **Setup PM2**: Copy and rename the `pm2.example.json` file in the root directory to `pm2.json` and fill in all of the required values.

6. **Setup NGINX**: Copy and rename the `.example.conf` file in the root directory to `{app_name}.conf` (ex.: `polyglot.conf`) and fill in all of the required values. You may need to adjust the file path for this. I had to move it to `/etc/nginx/sites-available/` and create a symbolic link to it in `/etc/nginx/sites-enabled/` and delete the default file in `/etc/nginx/conf.d/` to get it to work.

7. **Start the bot with PM2**: You can start the bot with PM2 using the following command:

   ```bash
   pm2 start pm2.json
   ```

8. **Set up Webhooks**: Input your domain name in the Interactions Endpoint URL field in your Discord application settings through the Discord Developer Portal. Make sure the bot is running before trying to "save" the changes in the Discord Developer Portal.

***Note**: See Local Development step 6 for instructions on setting up webhooks.*

9. **Invite the Bot to Your Server**: Use the OAuth2 URL Generator in the Discord Developer Portal to generate an invite link for your bot with the necessary permissions and invite it to your server.

10. **That's it!**: Your bot should now be up and running. You can test it by running the `/bot info` command in your Discord server.

## Contributing

Feel free to fork the repository and submit pull requests. Please ensure that your code works and is well-documented and tested before submitting a pull request.

## Thanks

- Thanks to [DeepL](https://www.deepl.com/pro-api) for providing a powerful translation API.
- Thanks to [discord.http](https://discordhttp.alexflipnote.dev/) for creating a interactions library for Discord using python that is easy to use and understand.
