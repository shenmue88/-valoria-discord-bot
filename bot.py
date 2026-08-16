
import os
import discord
from discord.ext import commands

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

RULES_CHANNEL_NAME = "regles"
SERVER_CHANNEL_NAME = "serveur"
WELCOME_CHANNEL_NAME = "bienvenue"

@bot.event
async def on_ready():
    print(f"✅ Valoria connecté en tant que {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"✅ {len(synced)} commande(s) slash synchronisée(s)")
    except Exception as e:
        print(f"Erreur sync commandes : {e}")

@bot.event
async def on_member_join(member: discord.Member):
    guild = member.guild

    rules_channel = discord.utils.get(
        guild.text_channels,
        name=RULES_CHANNEL_NAME
    )

    server_channel = discord.utils.get(
        guild.text_channels,
        name=SERVER_CHANNEL_NAME
    )

    welcome_channel = discord.utils.get(
        guild.text_channels,
        name=WELCOME_CHANNEL_NAME
    )

    rules_mention = (
        rules_channel.mention
        if rules_channel
        else "#regles"
    )

    server_mention = (
        server_channel.mention
        if server_channel
        else "#serveur"
    )

    embed = discord.Embed(
        title="🏰 Bienvenue sur Valoria !",
        description=(
            f"Bienvenue {member.mention} !\n\n"
            f"📜 Commence par lire {rules_mention}.\n"
            f"🎮 Ensuite, va dans {server_mention} "
            "pour retrouver les informations du serveur Minecraft.\n\n"
            "Bonne aventure sur Valoria ⚔️"
        ),
        color=0xF39C12
    )

    embed.set_footer(
        text="Valoria • Serveur Minecraft"
    )

    if welcome_channel:
        await welcome_channel.send(embed=embed)

    elif guild.system_channel:
        await guild.system_channel.send(embed=embed)

    try:
        await member.send(
            f"🏰 Bienvenue sur **{guild.name}** !\n\n"
            f"📜 Lis d'abord {rules_mention}.\n"
            f"🎮 Puis consulte {server_mention} "
            "pour rejoindre le serveur Minecraft."
        )
    except discord.Forbidden:
        pass

@bot.event
async def on_member_remove(member: discord.Member):
    guild = member.guild

    welcome_channel = discord.utils.get(
        guild.text_channels,
        name=WELCOME_CHANNEL_NAME
    )

    target = welcome_channel or guild.system_channel

    if target:
        await target.send(
            f"👋 **{member.display_name}** a quitté Valoria."
        )

@bot.command()
async def ping(ctx):
    await ctx.send("🏰 Valoria est en ligne !")

@bot.command()
@commands.has_permissions(administrator=True)
async def config(ctx):
    await ctx.send(
        "✅ Configuration Valoria active.\n"
        f"Salon règles : `#{RULES_CHANNEL_NAME}`\n"
        f"Salon serveur : `#{SERVER_CHANNEL_NAME}`\n"
        f"Salon bienvenue : `#{WELCOME_CHANNEL_NAME}`"
    )

@bot.tree.command(
    name="valoria",
    description="Vérifie que le bot Valoria fonctionne"
)
async def valoria(interaction: discord.Interaction):
    await interaction.response.send_message(
        "🏰 Valoria est opérationnel !",
        ephemeral=True
    )

if not TOKEN:
    raise RuntimeError(
        "La variable DISCORD_TOKEN est absente."
    )

bot.run(TOKEN)
