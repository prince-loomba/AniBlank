import datetime


async def register(ctx):
    """Let the game begin."""
    users_collection = ctx.bot.db.users  # Access the 'users' collection
    user_id = ctx.author.id
    username = ctx.author.name

    # Check if the user is already registered
    user_data = users_collection.find_one({'user_id': user_id})

    if user_data:
        await ctx.send(f"{username}, you are already registered!")
        return

    # Insert user data into MongoDB with default fields
    new_user = {
        'user_id': user_id,
        'username': username,
        'registration_timestamp': datetime.datetime.now(),
        'about_me': '',
        'level': 1,
        'exp': 0,
        'gold': 0,
        'stamina': 100,
        'location': 1,
        'floor': 1,
        'card_id': 0
    }
    users_collection.insert_one(new_user)

    await ctx.send(f"{username}, you have been registered successfully! 🎉")
