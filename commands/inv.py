import discord
import math


async def inv(ctx):
    """Displays the user's inventory of cards, with optional filters and pagination."""
    user_id = ctx.author.id
    message_content = ctx.message.content.split()

    # Initialize filters and pagination variables
    rarity_arg = None
    name_arg = None
    page = 1

    # Process command arguments
    i = 0
    while i < len(message_content):
        arg = message_content[i]

        if arg in ['-p', '-page']:
            try:
                page = int(message_content[i + 1])
                i += 1
            except (IndexError, ValueError):
                await ctx.send(
                    "Please provide a valid page number after '-p' or '-page'."
                )
                return
        elif arg in ['-r', '-rarity']:
            try:
                rarity_arg = message_content[i + 1].lower()
                i += 1
            except IndexError:
                await ctx.send(
                    "Please specify a rarity after '-r' or '-rarity'.")
                return
        elif arg in ['-n', '-name']:
            try:
                name_arg = ' '.join(message_content[i + 1:]).lower()
                break  # Stop after the name argument as it might be the last argument
            except IndexError:
                await ctx.send("Please specify a name after '-n' or '-name'.")
                return
        i += 1

    # Access the 'users' collection for inventory and the 'cards' collection for card details
    users_collection = ctx.bot.db.users
    cards_collection = ctx.bot.db.cards

    # Find user's inventory
    inventory = users_collection.find_one({'user_id': user_id})

    if not inventory or not inventory.get('cards'):
        await ctx.send(
            f"{ctx.author.name}, you don't have any cards in your inventory.")
        return

    # Pagination setup
    cards_per_page = 10
    total_cards = len(inventory['cards'])
    total_pages = math.ceil(total_cards / cards_per_page)

    if page < 1 or page > total_pages:
        await ctx.send(
            f"Invalid page number. Please enter a number between 1 and {total_pages}."
        )
        return

    # Calculate the range of cards to show
    start_index = (page - 1) * cards_per_page
    end_index = min(start_index + cards_per_page, total_cards)
    user_cards = inventory['cards'][start_index:end_index]

    # Apply filters
    exact_match = None
    filter_query = {}

    if name_arg:
        # Check for exact match first
        exact_match = cards_collection.find_one(
            {'name': {
                '$regex': f'^{name_arg}$',
                '$options': 'i'
            }})

    if exact_match:
        # If exact match found, get its details
        filtered_cards = [
            card_entry for card_entry in user_cards
            if card_entry['card_id'] == exact_match['card_id']
        ]
    else:
        # If no exact match found, apply filters
        if rarity_arg:
            if rarity_arg in ['c', 'common']:
                filter_query['rarity'] = 'Common'
            elif rarity_arg in ['r', 'rare']:
                filter_query['rarity'] = 'Rare'
            elif rarity_arg in ['sr', 'super rare']:
                filter_query['rarity'] = 'Super Rare'
            elif rarity_arg in ['ur', 'ultra rare']:
                filter_query['rarity'] = 'Ultra Rare'

        # Filter the cards in user's inventory based on the filter options
        filtered_cards = []
        for card_entry in user_cards:
            card = cards_collection.find_one({
                'card_id': card_entry['card_id'],
                **filter_query
            })
            if card:
                filtered_cards.append(card_entry)

    if not filtered_cards:
        await ctx.send(f"No cards found matching your filters.")
        return

    # Create an embed to display the inventory
    embed = discord.Embed(
        title=f"{ctx.author.name}'s Inventory (Page {page}/{total_pages})",
        color=0x00ff00)

    for card_entry in filtered_cards:
        card = cards_collection.find_one({'card_id': card_entry['card_id']})
        if card:
            embed.add_field(name=f"ID {card_entry['global_id']}. ",
                            value=f"{card['name']} ({card_entry['rarity']})",
                            inline=True)

    # Set footer and send the embed
    embed.set_footer(text=f"Page {page}/{total_pages} | Calculated by Shiro")
    await ctx.send(embed=embed)
