import discord
from discord.ext import commands
from discord import app_commands

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
created = {}

@bot.event
async def on_ready():
    print(f"✅ Бот {bot.user} запущен!")
    await bot.tree.sync()  # синхронизация слеш-команд

# ===== КОМАНДА /setup =====
@bot.tree.command(name="setup", description="Отправить панель управления голосовым каналом")
async def setup(interaction: discord.Interaction):
    embed = discord.Embed(
        title="Управление голосовым каналом",
        description=(
            "- Зайди в `[Создать]` — комната твоя.\n"
            "- Управляй кнопками — только для владельца.\n\n"
            "**Настройки**\n"
            "- Закрыть\n- Открыть\n- Название\n- Лимит\n- Передать\n\n"
            "**Участники**\n"
            "- Доступ\n- Кик\n- Бан\n- Мут\n- Размут"
        ),
        color=0x2b2d31
    )
    embed.set_author(name="FUN BOT")
    embed.set_footer(text="FUN · Voice Control")
    await interaction.response.send_message(embed=embed)

# ===== СОЗДАНИЕ КОМНАТЫ =====
@bot.event
async def on_voice_state_update(member, before, after):
    if after.channel and after.channel.name == "Создать":
        guild = after.channel.guild
        new_channel = await guild.create_voice_channel(
            name=member.name,
            category=after.channel.category
        )
        await member.move_to(new_channel)
        created[new_channel.id] = member.id

        setup_channel = discord.utils.get(guild.text_channels, name="настройка")
        if setup_channel:
            embed = discord.Embed(
                title="Управление голосовым каналом",
                description=(
                    "- Зайди в `[Создать]` — комната твоя.\n"
                    "- Управляй кнопками — только для владельца.\n\n"
                    "**Настройки**\n"
                    "- Закрыть\n- Открыть\n- Название\n- Лимит\n- Передать\n\n"
                    "**Участники**\n"
                    "- Доступ\n- Кик\n- Бан\n- Мут\n- Размут"
                ),
                color=0x2b2d31
            )
            embed.set_author(name="FUN BOT")
            embed.set_footer(text="FUN · Voice Control")
            await setup_channel.send(embed=embed)

    if before.channel and before.channel.id in created:
        if len(before.channel.members) == 0:
            await before.channel.delete()
            del created[before.channel.id]

bot.run("MTUyNTQwNDMyNDcyODAxNzAwNg.GgGgR2.ozKP7LWr6ckrNI38qbsHQ9_wRCicQwmt6qZXvA")