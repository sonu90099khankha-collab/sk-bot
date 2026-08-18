from pyrogram import Client, filters
import asyncio

# टेलीग्राम API डिटेल्स और बॉट टोकन
API_ID = 2040  # Pyrogram की डमी डिफॉल्ट आईडी
API_HASH = "b18441a1ff607e10a989891a5462e627"
BOT_TOKEN = "8936926889:AAG6hOg66zUleGTgn50qx4CrdPdfnnXvowQ"

app = Client(
    "sk_ultimate_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

BAD_WORDS = ["गाली1", "गाली2", "badword1"]

@app.on_message(filters.all)
async def ultimate_bot_engine(client, message):
    if not message.text:
        if message.photo or message.video or message.document:
            await message.delete()
            await message.reply_text("🚫 इस ग्रुप में फोटो/वीडियो भेजना सख्त मना है!", quote=True)
        return

    text = message.text.lower()

    # 1. म्यूजिक कमांड
    if text.startswith("/play") or "गाना" in text or "song" in text:
        await message.reply_text(
            "🎶 **म्यूजिक मोड:** भाई, वॉइस चैट ऑन कर लो! "
            "गाना बजाने के लिए बॉट तैयार है।"
        )
        return

    # 2. लिंक ब्लॉक
    if "http" in text or "t.me/" in text or "www." in text:
        if "t.me/SK_Chatting_Club" not in text:
            await message.delete()
            return

    # 3. गाली ब्लॉक
    for word in BAD_WORDS:
        if word in text:
            await message.delete()
            warn = await message.reply_text(f"⚠️ {message.from_user.mention}, गंदी भाषा का प्रयोग मत करो भाई!")
            await asyncio.sleep(5)
            await warn.delete()
            return

    # 4. ओनर असिस्टेंट
    if any(word in text for word in ["owner", "oaner", "creator", "ओनर", "मालिक", "बॉस"]):
        await message.reply_text(
            "🤖 **सुने भाई!** अभी हमारे दोनों ओनर (**@SK_KING_CHILL** और **@S_K_KI_NG**) ऑफलाइन हैं। 📴\n\n"
            "बता तू क्या बात है? अपना मैसेज छोड़ जा, ओनर आते ही देख लेंगे! 😎\n\n"
            "🔗 **ग्रुप:** https://t.me/SK_Chatting_Club"
        )
        return

    # 5. AI चैट
    if text.startswith("/ai"):
        query = message.text.replace("/ai", "").strip()
        if query:
            await message.reply_text(f"🤖 **AI जवाब:** भाई, तूने '{query}' पूछा है। ओनर के आने पर पूरा जवाब मिलेगा!")
            return

    # 6. Start कमांड
    if text.startswith("/start"):
        await message.reply_text(
            "🔥 राम-राम भाई! मैं **@SK_Chatting_Club** का अल्टीमेट ऑल-इन-वन बॉट हूँ!\n\n"
            "👑 **ओनर:**\n👉 @SK_KING_CHILL\n👉 @S_K_KI_NG"
        )

print("🚀 बॉट अब बिना किसी एरर के चालू हो रहा है...")
app.run()
