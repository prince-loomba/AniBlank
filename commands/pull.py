import random
from utils.next_card_id import get_next_card_id
import discord


async def pull(ctx):
    """Generates a random card for the user and adds it to their inventory, displaying card info in an embed."""
    user_id = ctx.author.id

    # Access the 'cards' and 'users' collections
    cards_collection = ctx.bot.db.cards
    users_collection = ctx.bot.db.users

    # Get next global card ID
    card_id = get_next_card_id(ctx.bot.db)

    # Define rarity probabilities
    rarities = ['Common', 'Rare', 'Super Rare', 'Ultra Rare']
    probabilities = [0.90, 0.08, 0.019, 0.001]

    # Select a rarity based on probabilities
    rarity = random.choices(rarities, probabilities)[0]

    # Fetch a random card from the cards collection
    card = random.choice(list(cards_collection.find()))

    # Find user's inventory in the 'users' collection
    inventory = users_collection.find_one({'user_id': user_id})

    if inventory:
        # Add card to existing inventory
        update_result = users_collection.update_one({'user_id': user_id}, {
            '$addToSet': {
                'cards': {
                    'global_id': card_id,
                    'card_id': card['card_id'],
                    'rarity': rarity
                }
            }
        })
    else:
        # User is not registered
        await ctx.send(f"{ctx.author.name}, you need to register first!")
        return

    if update_result.modified_count > 0:
        # Create an embed to display the card details
        embed = discord.Embed(
            title=f"🎴 You pulled a {rarity} card: {card['name']}!",
            description=
            f"**Talent:** {card['talent_description']}\n**HP:** {card['hp']} | **ATK:** {card['atk']} | **DEF:** {card['def']} | **SPD:** {card['spd']}",
            color=discord.Color.blue())

        # Add card-specific details like quote and talent description
        embed.add_field(name="Quote",
                        value=card.get('quote', 'No quote available'),
                        inline=False)

        # Add the card image (if available)
        if card.get('image'):
            embed.set_thumbnail(url=card['image'])

        # Footer with card information
        embed.set_footer(
            text=f"Card ID: {card['card_id']} | Global ID: {card_id}")

        # Send the embed message
        await ctx.send(embed=embed)
    else:
        await ctx.send("Failed to add the card to your inventory.")
