async def edit(ctx):
    """Updates the 'about me' field for the user based on the message content."""
    users_collection = ctx.bot.db.users  # Access the 'users' collection
    user_id = ctx.author.id
    username = ctx.author.name

    # Extract the 'about me' content from the message after the command
    about_me = ctx.message.content[len(ctx.prefix) + len(ctx.command.name) +
                                   1:].strip()

    if not about_me:
        await ctx.send("Please provide an 'about me' description.")
        return

    # Find the user and update the 'about me' field
    result = users_collection.update_one({'user_id': user_id},
                                         {'$set': {
                                             'about_me': about_me
                                         }})

    if result.matched_count == 0:
        await ctx.send(f"{username}, you need to register first!")
    else:
        await ctx.send(f"{username}, your 'about me' has been updated!")
