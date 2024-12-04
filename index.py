import discord
from discord.ext import commands
from discord.ui import Button, View

# إعداد البوت مع Intentات
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

# إنشاء البوت
bot = commands.Bot(command_prefix="!", intents=intents)

# معرف القناة المخصصة لإرسال تفاصيل الحذف
DELETE_CHANNEL_ID = 123456789012345678  # ضع هنا الـID الخاص بالقناة المخصصة للحذف

# أدوار التسليم
roles = ["BOSS", "OWNER", "FOUNDER", "MANAGER", "Developer"]

# إنشاء تذكرة جديدة
@bot.command()
async def ticket(ctx):
    """إنشاء تذكرة جديدة للمستخدم"""
    # تأكد من أن البوت لديه صلاحية لفتح قناة جديدة
    guild = ctx.guild
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        ctx.author: discord.PermissionOverwrite(read_messages=True)
    }

    # إنشاء القناة النصية
    ticket_channel = await guild.create_text_channel(f"ticket-{ctx.author.name}", overwrites=overwrites)

    # إنشاء الأزرار
    claim_button = Button(label="Claim", custom_id="claim_button", emoji="✅")
    delete_button = Button(label="حذف", custom_id="delete_button", emoji="🗑️")
    rules_button = Button(label="قواعد التذكرة", custom_id="rules_button", emoji="📜")

    # إضافة الأزرار إلى الـView
    view = View()
    view.add_item(claim_button)
    view.add_item(delete_button)
    view.add_item(rules_button)

    # إرسال رسالة داخل القناة الجديدة مع الأزرار
    await ticket_channel.send(f"مرحبًا {ctx.author.mention}, تم فتح تذكرتك بنجاح! كيف يمكنني مساعدتك؟", view=view)

    # إعلام المستخدم بأن التذكرة قد تم فتحها
    await ctx.send(f"تم فتح تذكرتك بنجاح في القناة {ticket_channel.mention}!")

# التعامل مع الأزرار
@bot.event
async def on_interaction(interaction):
    if interaction.type == discord.InteractionType.component:
        if interaction.custom_id == "claim_button":
            # اختيار شخص من الأدوار المحددة
            guild = interaction.guild
            role = None
            for r in roles:
                role = discord.utils.get(guild.roles, name=r)
                if role:
                    break

            if role:
                # اختيار الشخص المسئول عن التذكرة من هذا الدور
                member = discord.utils.get(guild.members, roles=[role])
                if member:
                    await interaction.response.send_message(f"تم تسليم التذكرة إلى {member.mention}.", ephemeral=True)
                    # إرسال رسالة للشخص الذي تم تسليمه التذكرة
                    await member.send(f"لقد تم تعيينك لتسليم تذكرة من {interaction.user.mention}.")
                else:
                    await interaction.response.send_message("لم يتم العثور على شخص مسؤول في هذا الدور.", ephemeral=True)
            else:
                await interaction.response.send_message("لم يتم العثور على أي من الأدوار المحددة.", ephemeral=True)

        elif interaction.custom_id == "delete_button":
            # طلب سبب الحذف من المستخدم
            await interaction.response.send_message("من فضلك، اكتب سبب حذف التذكرة.", ephemeral=True)
            
            def check(msg):
                return msg.author == interaction.user and isinstance(msg.channel, discord.TextChannel)

            reason_msg = await bot.wait_for("message", check=check)
            reason = reason_msg.content

            # إرسال سبب الحذف إلى القناة المخصصة
            delete_channel = bot.get_channel(DELETE_CHANNEL_ID)
            if delete_channel:
                await delete_channel.send(f"تم طلب حذف التذكرة من قبل {interaction.user.mention}.\nالسبب: {reason}")
            
            await interaction.followup.send("تم إرسال سبب الحذف إلى القناة المخصصة.", ephemeral=True)

        elif interaction.custom_id == "rules_button":
            # إرسال قواعد التذكرة
            rules = """
            **قواعد التذكرة:**
            1. يُمنع إرسال رسائل غير ذات صلة.
            2. يُمنع استخدام الألفاظ المسيئة.
            3. يُمنع إرسال الرسائل المتكررة أو غير المنطقية.
            4. يجب الالتزام بالهدوء عند التواصل مع فريق الدعم.
            """
            await interaction.response.send_message(rules, ephemeral=True)

# عند تشغيل البوت
@bot.event
async def on_ready():
    print(f'تم تسجيل الدخول كـ {bot.user}')

# تشغيل البوت باستخدام التوكن الخاص بك

bot.run('MTMxMDExNzE0ODYzMDMyMzIwMA.G5Ron0.lr6MFSPwK3RvS_kCzsQKxUpt-SfF7sipJdV0Tg')
