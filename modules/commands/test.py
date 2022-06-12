from typing import Union

import discord
from discord import app_commands
from discord.ext import commands

from bot import Bot

key_perms = ["kick_members", "ban_members", "administrator", "manage_channels", "manage_server", "manage_messages",
             "mention_everyone", "manage_nicknames", "manage_roles", "manage_webhooks", "manage_emojis"]

voice_perms = ["connect", "deafen_members", "move_members", "mute_members", "priority_speaker", "speak", "stream",
               "use_voice_activation", "use_embedded_activities"]


class Testing(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    user = app_commands.Group(name="user", description="Various information about a user",
                              guild_ids=[553953983409029148])

    @staticmethod
    def get_member_status(member):
        status = f"{str(member.status).capitalize()}\n\n"
        if not member.activity:
            pass
        elif member.activity.type == discord.ActivityType.playing:
            activity = member.activity.to_dict()
            status += f"Playing **{member.activity.name}**"
            if "details" in activity:
                status += f"\n{activity['details']}"
            if "state" in activity:
                status += f"\n{activity['state']}"
        elif member.activity.type == discord.ActivityType.watching:
            status += f"Watching {member.activity.name}"
        elif member.activity.type == discord.ActivityType.listening:
            status += f"Listening to {member.activity.title}\n" \
                      f"By {', '.join([x for x in member.activity.artists])}\n" \
                      f"On {member.activity.name}"
        elif member.activity.type == discord.ActivityType.streaming:
            status += f"Streaming **[{member.activity.name}]({member.activity.url})**"
        else:
            status += str(member.activity)
        return status

    @user.command(name="info")
    async def user_info(self, interaction: discord.Interaction, user: discord.Member = None):
        user = user or interaction.user
        em = discord.Embed(color=user.color)
        em.set_thumbnail(url=user.avatar.url)
        em.set_author(
            name=f"{'BOT: ' if user.bot else ''}"
                 f"{' ~ '.join((str(user), user.nick)) if user.nick else str(user)}"
        )
        em.add_field(name="Status:", value=self.get_member_status(user), inline=False)
        vc = "Not connected"
        if user.voice:
            other_people = len(user.voice.channel.members) - 1
            vc = f"In {user.voice.channel.mention}"
            vc += f" with {other_people} others" if other_people else " alone"
        em.add_field(name='Voice:', value=vc, inline=False)
        em.add_field(
            name=f"Roles [{len(user.roles) - 1}]:",
            value=" ".join([x.mention for x in user.roles if x is not interaction.guild.default_role][::-1]) or "None"
            if len(user.roles) <= 41 else "Too many to display",
            inline=False
        )
        em.add_field(
            name="Key Permissions:",
            value=", ".join(
                sorted([str(x).replace("_", " ").title()
                        for x in
                        [x[0] for x in iter(interaction.channel.permissions_for(user)) if x[1]] if x in key_perms])
            ) or "None",
            inline=False
        )
        em.add_field(
            name="Account created:", value=str(user.created_at), inline=False
        )
        em.add_field(
            name="Joined this server on:", value=str(user.created_at), inline=False
        )
        em.set_footer(
            text=f"Member #{len([x for x in interaction.guild.members if x.joined_at < user.joined_at]) + 1} • ID: {user.id}"
        )
        await interaction.response.send_message(embed=em)

    @user.command(name="permissions", description="Check a users permissions for a given Text/Voice channel")
    async def user_permissions(self, interaction: discord.Interaction, user: discord.Member = None, *,
                               channel: Union[discord.TextChannel, discord.VoiceChannel] = None):
        user = user or interaction.user
        channel = channel or interaction.channel
        perms = channel.permissions_for(user)
        perms_list = []
        if isinstance(channel, discord.TextChannel):
            for perm in perms:
                if perm[0] not in voice_perms:
                    perm_name = perm[0].replace('_', ' ').title()
                    perms_list.append(f"+\t{perm_name}" if perm[1] else f"-\t{perm_name}")
        elif isinstance(channel, discord.VoiceChannel):
            for perm in perms:
                if perm[0] in voice_perms:
                    perm_name = perm[0].replace('_', ' ').title()
                    perms_list.append(f"+\t{perm_name}" if perm[1] else f"-\t{perm_name}")
        end = "\n".join(sorted(perms_list))
        desc = f"```diff\n{end}\n```"
        em = discord.Embed(color=user.color, description=desc)
        em.set_author(name=f"{user.name}'s permissions in {channel}:")
        await interaction.response.send_message(embed=em)


async def setup(bot):
    await bot.add_cog(Testing(bot))
