import telebot
import os
import requests
import subprocess
import time

TOKEN = 'INSERISCI_TOKEN'
MY_CHAT_ID = 123456789  # Inserisci il tuo Chat ID numerico senza virgolette
GOOGLE_API_KEY = "INSERISCI_API_KEY"

bot = telebot.TeleBot(TOKEN)

def check_auth(message):
    return message.chat.id == MY_CHAT_ID

@bot.message_handler(commands=['lock'])
def lock_pc(message):
    if not check_auth(message): return
    os.system("loginctl lock-sessions")
    bot.reply_to(message, "🔒 Tutte le sessioni bloccate con successo.")

@bot.message_handler(commands=['locate'])
def locate_pc_precise(message):
    if not check_auth(message): return
    bot.reply_to(message, "📡 Scansione reti Wi-Fi e triangolazione in corso...")
    try:
        # Scansiona le reti Wi-Fi vicine per la triangolazione
        result = subprocess.run(['nmcli', '-t', '-f', 'BSSID', 'dev', 'wifi', 'list'], capture_output=True, text=True)
        mac_addresses = result.stdout.replace('\\', '').strip().split('\n')
        wifi_aps = [{"macAddress": mac} for mac in mac_addresses if len(mac) == 17]
        
        if not wifi_aps:
            bot.reply_to(message, "⚠️ Nessuna rete Wi-Fi rilevata.")
            return

        # Invia i dati a Google
        payload = {"wifiAccessPoints": wifi_aps}
        res = requests.post(f"https://www.googleapis.com/geolocation/v1/geolocate?key={GOOGLE_API_KEY}", json=payload).json()
        
        if 'location' in res:
            lat, lng = res['location']['lat'], res['location']['lng']
            bot.reply_to(message, f"📍 **Posizione (Scarto: ~{res.get('accuracy', 'N/D')} m)**\n🗺️ https://www.google.com/maps/search/?api=1&query={lat},{lng}")
        else:
            bot.reply_to(message, f"❌ Errore API: {res.get('error', {}).get('message', 'Sconosciuto')}")
    except Exception as e:
        bot.reply_to(message, f"❌ Errore di sistema: {e}")

if __name__ == '__main__':
    # Attende l'aggancio del Wi-Fi all'avvio
    time.sleep(15) 
    try:
        bot.send_message(MY_CHAT_ID, "🚨 ALLARME: Il PC è stato acceso ed è online! Usa /locate per rintracciarlo e /lock per bloccarlo.")
    except:
        pass # Ignora se non c'è ancora rete
    
    bot.infinity_polling()
