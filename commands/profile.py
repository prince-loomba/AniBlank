import discord


async def profile(ctx):
    """Displays the profile information of the user."""
    users_collection = ctx.bot.db.users  # Access the 'users' collection
    user_id = ctx.author.id
    username = ctx.author.name

    # Retrieve user data from MongoDB
    user_data = users_collection.find_one({'user_id': user_id})

    if not user_data:
        await ctx.send(f"{username}, you need to register first!")
        return

    # Create an embed to display the user’s profile information
    embed = discord.Embed(title=f"{username}'s Profile", color=0x00ff00)
    embed.add_field(name="Name", value=user_data.get('username', 'N/A'))
    embed.add_field(name="About Me", value=user_data.get('about_me', 'N/A'))
    embed.add_field(name="Level", value=user_data.get('level', 1))
    embed.add_field(name="EXP", value=user_data.get('exp', 0))
    embed.add_field(name="Gold", value=user_data.get('gold', 0))
    embed.add_field(name="Stamina", value=user_data.get('stamina', 100))
    embed.add_field(name="Location", value=user_data.get('location', 1))
    embed.add_field(name="Floor", value=user_data.get('floor', 1))
    embed.add_field(name="Card Selected",
                    value=user_data.get('card_id', 'None'))
    embed.set_footer(text="Registered At " +
                     str(user_data.get('registration_timestamp', 'None')))

    await ctx.send(embed=embed)
