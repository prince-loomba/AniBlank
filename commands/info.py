import discord


async def info(ctx):
    """Displays information about a card based on its name."""
    card_name = ctx.message.content[len('bk info '):].strip(
    )  # Extract the card name from the message content

    # Access the 'cards' collection
    cards_collection = ctx.bot.db.cards

    # Search for an exact match
    card = cards_collection.find_one({'name': card_name})

    if not card:
        # If no exact match, search for the best match using regex
        card = cards_collection.find_one(
            {'name': {
                '$regex': card_name,
                '$options': 'i'
            }})

    if card:
        # Create an embed with the card details
        embed = discord.Embed(title=card['name'],
                              description="",
                              color=0x00ff00)
        embed.add_field(name=card['talent'], value=card['talent_description'])
        embed.add_field(name='HP', value=card['hp'])
        embed.add_field(name='Attack', value=card['atk'])
        embed.add_field(name='Defense', value=card['def'])
        embed.add_field(name='Speed', value=card['spd'])
        embed.set_footer(text=card['quote'])
        embed.set_image(url=card['image'])

        await ctx.send(embed=embed)
    else:
        await ctx.send("Card not found.")
