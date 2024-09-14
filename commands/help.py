import discord


async def help_command(ctx):
    """Displays an embed with a list of all commands and their details."""
    # Create an embed object
    embed = discord.Embed(title="Help",
                          description="List of available commands:",
                          color=0x00ff00)

    # Loop through the command metadata to add fields to the embed
    for _, info in ctx.bot.command_metadata.items():
        embed.add_field(
            name=info['name'],
            value=
            f"**Description:** {info['description']}\n**Usage:** {info['usage']}",
            inline=False)

    # Send the embed message
    await ctx.send(embed=embed)
