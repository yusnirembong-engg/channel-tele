"""
TELEGRAM WELCOME BOT - BOLAPELANGI 2
Script untuk menyapa member baru yang join ke channel
Created for: @bolapelangi2_bot
"""

import logging
import asyncio
from datetime import datetime
from telegram import Update, ChatMember
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from telegram.constants import ParseMode

# ==================== KONFIGURASI ====================

# GANTI DENGAN TOKEN BOT KAMU!
BOT_TOKEN = "8793227199:AAEXajy3RDO7SpMSCloj13Z4ubX3DXNvN4M"

# GANTI DENGAN USERNAME CHANNEL KAMU!
CHANNEL_USERNAME = ""  # Ganti dengan username channel kamu

# ID CHANNEL (opsional, bisa pakai username atau ID)
CHANNEL_ID = -1003573191693  # Ganti dengan ID channel kamu (angka negatif)

# PESAN WELCOME
WELCOME_MESSAGE = """
🎉 *SELAMAT DATANG DI BOLAPELANGI 2 COMMUNITY!* 🎉

Halo {mention}!

Terima kasih sudah bergabung dengan channel resmi kami. 
Jangan lupa untuk:

✅ Follow semua channel official kami:
   • Bot: @bolapelangi2_bot
   • Channel WA: https://bopel2.vip/Channel-Whatsapp
   • Channel TG: https://bopel2.vip/Channel-Telegram

✅ Baca aturan & promo terbaru:
   • Cashback 100% Mix Parlay
   • Bonus harian Rp 300.000

🔥 *GasPoll terus parlaynya Bosku!* 🔥
"""

# ==================== KONFIGURASI LOGGING ====================

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ==================== FUNGSI UTAMA ====================

async def welcome_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Fungsi untuk menyapa member baru yang bergabung ke channel
    """
    
    # Cek apakah ini message dari channel
    if not update.chat_post or not update.effective_chat:
        return
    
    chat = update.effective_chat
    message = update.chat_post
    
    # Cek apakah ini di channel yang kita targetkan
    if chat.username != CHANNEL_USERNAME.replace('@', '') and chat.id != CHANNEL_ID:
        return
    
    # Cek apakah ada member baru
    if not message.new_chat_members:
        return
    
    # Loop untuk setiap member baru
    for new_member in message.new_chat_members:
        # Jangan sapa bot sendiri
        if new_member.is_bot:
            continue
        
        # Dapatkan informasi member
        user_id = new_member.id
        first_name = new_member.first_name or "Member"
        username = f"@{new_member.username}" if new_member.username else first_name
        
        # Buat mention (bisa pakai markdown atau teks biasa)
        mention_markdown = f"[{first_name}](tg://user?id={user_id})"
        mention_text = f"@{new_member.username}" if new_member.username else first_name
        
        # Kirim pesan welcome ke channel (sebagai pengumuman)
        welcome_text = f"""
🎉 *SELAMAT DATANG* 🎉

Halo {mention_markdown}!
Selamat bergabung di *BOLAPELANGI 2 Official Channel*!

Jangan lupa follow:
• Bot: @bolapelangi2_bot
• WA: [Klik Disini](https://bopel2.vip/Channel-Whatsapp)
• TG: [Klik Disini](https://bopel2.vip/Channel-Telegram)

🔥 *GasPoll!* 🔥
        """
        
        try:
            await message.reply_text(
                text=welcome_text,
                parse_mode=ParseMode.MARKDOWN,
                disable_web_page_preview=True
            )
            logger.info(f"Welcome message sent to {first_name} (ID: {user_id})")
        except Exception as e:
            logger.error(f"Failed to send welcome message: {e}")
        
        # OPSIONAL: Kirim pesan private ke member baru
        try:
            private_message = f"""
Halo {first_name}!

Terima kasih sudah bergabung dengan *BOLAPELANGI 2*! 🎉

Kami punya PROMO SPESIAL untuk member baru:
⚽ *CASHBACK 100% MIX PARLAY*
• Modal Rp 10.000
• 5 tim TODAY
• Odds 1.80
• Max bonus Rp 300.000

📱 *Link Penting:*
• Klaim Bonus: https://bopel2.link/wa
• Prediksi Jitu: https://bopel2.vip/ChannelWA-Jadwal-Prediksi

GasPoll terus Bosku! 🚀
            """
            
            await context.bot.send_message(
                chat_id=user_id,
                text=private_message,
                parse_mode=ParseMode.MARKDOWN
            )
            logger.info(f"Private message sent to {first_name} (ID: {user_id})")
        except Exception as e:
            logger.error(f"Failed to send private message to {user_id}: {e}")
            # Bot mungkin tidak bisa memulai chat dengan user jika user belum pernah chat dengan bot


async def track_member_join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Fungsi alternatif untuk track member join via chat member update
    """
    if not update.my_chat_member:
        return
    
    # Cek jika ada member baru di channel
    if update.my_chat_member.new_chat_member.status == ChatMember.MEMBER:
        chat = update.effective_chat
        user = update.my_chat_member.from_user
        
        logger.info(f"New member detected via chat member: {user.first_name} in {chat.title}")
        
        # Kirim welcome message jika diperlukan
        # (ini lebih kompleks dan membutuhkan setup webhook)


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle errors"""
    logger.error(f"Update {update} caused error {context.error}")


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    user = update.effective_user
    welcome_text = f"""
Halo {user.first_name}! 👋

Selamat datang di *BOLAPELANGI 2 Bot*!

🤖 *Apa yang bisa saya bantu?*
• Saya akan menyapa member baru di channel
• Info promo terbaru
• Cara klaim bonus

📌 *Link Penting:*
• Channel: @bolapelangi2_channel
• Klaim Bonus: https://bopel2.link/wa
• Prediksi: https://bopel2.vip/ChannelWA-Jadwal-Prediksi

🔥 *GasPoll!* 🔥
    """
    
    await update.message.reply_text(
        text=welcome_text,
        parse_mode=ParseMode.MARKDOWN
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    help_text = """
📚 *BANTUAN BOT BOLAPELANGI 2*

*Fitur Bot:*
• /start - Mulai bot
• /help - Bantuan ini
• /promo - Info promo terbaru
• /aturan - Syarat & ketentuan
• /kontak - Kontak official

*Untuk Admin:*
Bot akan otomatis menyapa member baru yang join ke channel @bolapelangi2_channel

*Kendala Teknis?*
Hubungi WA Official: https://bopel2.link/wa
    """
    
    await update.message.reply_text(
        text=help_text,
        parse_mode=ParseMode.MARKDOWN
    )


async def promo_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /promo command"""
    promo_text = """
🎁 *PROMO SPESIAL BOLAPELANGI 2* 🎁

⚽ *CASHBACK 100% MIX PARLAY*
• Minimal Bet: Rp 10.000
• Minimal 5 tim (TODAY)
• Odds Minimal 1.80
• 1 tim Lose, sisanya Win Full
• Max Bonus: Rp 300.000/hari

📌 *Syarat:*
• Follow semua channel official
• Add Telegram Bot: @bolapelangi2_bot
• Klaim via WA: https://bopel2.link/wa

🚀 *GasPoll!*
    """
    
    await update.message.reply_text(
        text=promo_text,
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True
    )


async def aturan_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /aturan command"""
    aturan_text = """
📋 *SYARAT & KETENTUAN*

1. Bonus hanya bisa diklaim *1x sehari*
2. Maksimal bonus *Rp 300.000/hari*
3. Tidak boleh ada *kesamaan IP*
4. Tidak boleh *safety bet* atau kecurangan
5. Keputusan admin *mutlak*

⚠️ Jika ketahuan curang, bonus *HANGUS*!

✅ *Cara Klaim:*
• Gabung semua channel official
• Add bot @bolapelangi2_bot
• Kirim bukti ke WA: https://bopel2.link/wa
    """
    
    await update.message.reply_text(
        text=aturan_text,
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True
    )


async def kontak_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /kontak command"""
    kontak_text = """
📞 *KONTAK OFFICIAL BOLAPELANGI 2*

🟢 *WA Official (Klaim Bonus):*
https://bopel2.link/wa

📢 *Channel WhatsApp:*
https://bopel2.vip/Channel-Whatsapp

📢 *Channel Telegram:*
https://bopel2.vip/Channel-Telegram

🤖 *Bot Telegram:*
@bolapelangi2_bot

📈 *Prediksi & Jadwal:*
https://bopel2.vip/ChannelWA-Jadwal-Prediksi

🔥 *Follow semua biar gak ketinggalan info!*
    """
    
    await update.message.reply_text(
        text=kontak_text,
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True
    )


# ==================== MAIN FUNCTION ====================

def main():
    """Main function to run the bot"""
    
    # Buat aplikasi
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Tambahkan command handlers
    application.add_handler(MessageHandler(filters.COMMAND & filters.Regex('^/start$'), start_command))
    application.add_handler(MessageHandler(filters.COMMAND & filters.Regex('^/help$'), help_command))
    application.add_handler(MessageHandler(filters.COMMAND & filters.Regex('^/promo$'), promo_command))
    application.add_handler(MessageHandler(filters.COMMAND & filters.Regex('^/aturan$'), aturan_command))
    application.add_handler(MessageHandler(filters.COMMAND & filters.Regex('^/kontak$'), kontak_command))
    
    # Handler untuk welcome message (via channel post)
    application.add_handler(MessageHandler(filters.Chat(chat_id=CHANNEL_ID) & filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_new_member))
    
    # Handler untuk track member join (alternatif)
    application.add_handler(MessageHandler(filters.StatusUpdate.MY_CHAT_MEMBER, track_member_join))
    
    # Error handler
    application.add_error_handler(error_handler)
    
    # Start bot
    print("🤖 Bot BOLAPELANGI 2 is running...")
    print(f"📢 Monitoring channel: {CHANNEL_USERNAME}")
    print("Press Ctrl+C to stop")
    
    # Run bot dengan polling
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
