import os
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True  # Enable message content intent
bot = commands.Bot(command_prefix='!', intents=intents)

GUILD_ID = YOUR_GUILD_ID  # Ersetze durch deine Server-ID
CATEGORY_ID = YOUR_CATEGORY_ID  # Ersetze durch die Kategorie-ID, in der Tickets erstellt werden sollen
TICKET_ROLE_NAME = 'Support'  # Ersetze durch den Namen der Rolle, die Tickets erstellen darf
ADMIN_ROLE_NAME = 'Admin'  # Ersetze durch den Namen der Administratorrolle

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("Ticket System"))
    print(f'Logged in als {bot.user}')

@bot.command()
@commands.has_role(TICKET_ROLE_NAME)
async def ticket(ctx, *, reason=None):
    guild = bot.get_guild(GUILD_ID)
    category = discord.utils.get(guild.categories, id=CATEGORY_ID)
    
    # Erstelle einen neuen Textkanal
    channel = await guild.create_text_channel(f'ticket-{ctx.author.name}', category=category)
    
    # Setze Berechtigungen so, dass nur der Benutzer und Admins den Kanal sehen können
    await channel.set_permissions(ctx.guild.default_role, read_messages=False)
    await channel.set_permissions(ctx.author, read_messages=True, send_messages=True)
    await channel.set_permissions(ctx.guild.me, read_messages=True, send_messages=True)

    # Benachrichtige alle Administratoren
    admin_role = discord.utils.get(ctx.guild.roles, name=ADMIN_ROLE_NAME)
    if admin_role:
        admin_members = [member.mention for member in admin_role.members]
        await channel.send(f'Admins: {", ".join(admin_members)}, ein neues Ticket wurde erstellt von {ctx.author.mention}.\nGrund: {reason}')

    # Begrüßungsnachricht im Ticketkanal senden
    await channel.send(f'Danke, dass du ein Ticket erstellt hast, {ctx.author.mention}. Ein Mitglied des Support-Teams wird sich bald um dich kümmern.\nGrund: {reason}')

    await ctx.send(f'{ctx.author.mention}, dein Ticket wurde erstellt: {channel.mention}')

@bot.command()
@commands.has_role(ADMIN_ROLE_NAME)
async def close(ctx):
    if ctx.channel.category.id == CATEGORY_ID:
        await ctx.channel.delete()

# Ersetze 'YOUR_BOT_TOKEN' durch den Token deines Bots
bot.run('YOUR_BOT_TOKEN')
