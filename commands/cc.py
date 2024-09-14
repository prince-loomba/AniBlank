import discord
from pymongo import DESCENDING


async def cc(ctx):
    """Creates a new card for the game interactively. Only available to certain users."""

    # Check if the user is allowed to use this command
    if ctx.author.id not in ctx.bot.admins:
        await ctx.send("You don't have permission to use this command.")
        return

    # Ask the user for card details
    await ctx.send(
        "Please provide the card details one by one. Type `cancel` to abort at any time."
    )

    # Define a dictionary to hold card details
    card_details = {
        'location': None,
        'name': None,
        'quote': None,
        'image': None,
        'hp': None,
        'atk': None,
        'def': None,
        'spd': None,
        'talent': None,
        'description': None
    }

    # Define a list of prompts and corresponding keys
    prompts = [
        ("Location (e.g., 1):", 'location'), ("Name (e.g., Sora):", 'name'),
        ("Quote (e.g., 'Life is not a game of luck. If you wanna win, work hard'):",
         'quote'),
        ("Image URL (e.g., http://example.com/image.jpg):", 'image'),
        ("HP (e.g., 70):", 'hp'), ("Attack (e.g., 90):", 'atk'),
        ("Defense (e.g., 90):", 'def'), ("Speed (e.g., 100):", 'spd'),
        ("Talent (e.g., Brilliant Tactics):", 'talent'),
        ("Talent Description (e.g., Reduces enemy defense by 10% and increases our attack by 10%):",
         'description')
    ]

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    # Iterate through the prompts to get user input
    for prompt, key in prompts:
        await ctx.send(prompt)

        try:
            msg = await ctx.bot.wait_for('message', timeout=60.0, check=check)
            if msg.content.lower() == 'cancel':
                await ctx.send("Card creation cancelled.")
                return

            # Validate and store input
            if key in ['hp', 'atk', 'def', 'spd', 'location']:
                card_details[key] = int(msg.content)
            else:
                card_details[key] = msg.content

        except ValueError:
            await ctx.send("Invalid input. Please enter a valid number.")
            return
        except Exception as e:
            await ctx.send(f"An error occurred: {e}")
            return

    # Check if a card with the same name already exists in the same location
    cards_collection = ctx.bot.db.cards
    existing_card = cards_collection.find_one({
        "name":
        card_details['name'],
        "location":
        card_details['location']
    })
    if existing_card:
        await ctx.send(
            f"A card with the name '{card_details['name']}' already exists in location {card_details['location']}."
        )
        return

    # Get the highest card_id and floor in the given location
    highest_card = cards_collection.find_one(
        {"location": card_details['location']}, sort=[("card_id", DESCENDING)])
    card_id = highest_card["card_id"] + 1 if highest_card else 1

    highest_floor = cards_collection.find_one(
        {"location": card_details['location']}, sort=[("floor", DESCENDING)])
    floor = highest_floor["floor"] + 1 if highest_floor else 1

    # Create the new card object
    new_card = {
        "location": card_details['location'],
        "floor": floor,
        "name": card_details['name'],
        "quote": card_details['quote'],
        "image": card_details['image'],
        "hp": card_details['hp'],
        "atk": card_details['atk'],
        "def": card_details['def'],
        "spd": card_details['spd'],
        "talent": card_details['talent'],
        "talent_description": card_details['description'],
        "card_id": card_id
    }

    # Insert the new card into the collection
    cards_collection.insert_one(new_card)

    # Create an embed to display the card details
    embed = discord.Embed(title=f"Card Created: {card_details['name']}",
                          color=0x00ff00)
    embed.set_thumbnail(url=card_details['image'])
    embed.add_field(name="Location",
                    value=card_details['location'],
                    inline=True)
    embed.add_field(name="Floor", value=floor, inline=True)
    embed.add_field(name="HP", value=card_details['hp'], inline=True)
    embed.add_field(name="Attack", value=card_details['atk'], inline=True)
    embed.add_field(name="Defense", value=card_details['def'], inline=True)
    embed.add_field(name="Speed", value=card_details['spd'], inline=True)
    embed.add_field(name="Talent", value=card_details['talent'], inline=True)
    embed.add_field(name="Talent Description",
                    value=card_details['description'],
                    inline=True)
    embed.add_field(name="Quote", value=card_details['quote'], inline=False)
    embed.add_field(name="Card ID", value=card_id, inline=True)

    embed.set_footer(text="Calculated by Shiro")  # Footer for consistency

    # Send the embed
    await ctx.send(embed=embed)
