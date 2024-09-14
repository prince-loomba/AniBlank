import os
import importlib
from discord import Intents
from discord.ext import commands
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from decorators import log_command_execution
from keep_alive import keep_alive

# Load environment variables
load_dotenv()
TOKEN = os.environ['TOKEN']
URI = os.getenv('URI')

# MongoDB connection setup
client = MongoClient(URI)
db = client.game

# Intents and Bot setup
intents = Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='bk ', intents=intents)

# Store command metadata
command_metadata = {}

# Attach db to the bot instance
bot.db = db
bot.admins = os.getenv('ADMINS').split(',')


def load_commands():
  for filename in os.listdir('./commands'):
    if filename.endswith('.py') and filename != '__init__.py':
      command_name = filename[:-3]  # Remove .py extension
      try:
        # Dynamically import the command module
        module = importlib.import_module(f'commands.{command_name}')

        # Register each command function
        for attr_name in dir(module):
          attr = getattr(module, attr_name)

          # Check if the attribute is a callable function
          if callable(attr):
            # Wrap the command function with logging decorator
            decorated_command = log_command_execution(db)(attr)

            # Register the command
            bot.add_command(
                commands.Command(decorated_command,
                                 name=attr.__name__,
                                 help=attr.__doc__,
                                 usage='bk ' + attr.__name__))

            # Store metadata
            command_metadata[attr.__name__] = {
                'name': attr.__name__,
                'description': attr.__doc__,
                'usage': 'bk ' + attr.__name__,
            }

        print(f'Loaded command: {command_name}')
      except Exception as e:
        print(f'Failed to load command {command_name}: {e}')


@bot.event
async def on_ready():
  print(f'Logged in as {bot.user}')
  print("Available commands:")
  for _, info in command_metadata.items():
    print(f"Command: {info['name']}")


@bot.event
async def on_command_error(ctx, error):
  """Handle errors during command execution."""
  error_message = f"An error occurred: {str(error)}"
  print(error_message)
  await ctx.send(error_message)


# Load commands and start the bot
load_commands()
keep_alive()

bot.run(TOKEN)
