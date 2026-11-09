# anti-furto-per-ubuntu
sistema di protezione pc, tramite avviso di bot su telegram con opzione di blocco pc e posizione pc


1. Preparazione delle Credenziali

Prima di toccare il terminale sul PC, assicurati di avere a disposizione queste tre chiavi:

* *Token del Bot:* Generato creando un nuovo bot tramite `BotFather` su Telegram.
* *Chat ID Personale:* Ottenuto inviando un messaggio al bot `userinfobot` su Telegram.
* *API Key di Google:* Creata dalla Google Cloud Console (assicurandoti di aver abilitato la libreria "Geolocation API").

2. Creazione dell'Ambiente e dello Script

Sul nuovo PC, apri il terminale e prepara l'ambiente virtuale isolato:

```
sudo apt update && sudo apt install python3-venv
mkdir ~/security_bot && cd ~/security_bot
python3 -m venv venv
source venv/bin/activate
pip install pyTelegramBotAPI requests

```

Crea il file principale (es. `nano security_bot.py`) e incolla il codice unificato. Sostituisci i campi `TOKEN`, `MY_CHAT_ID` e `GOOGLE_API_KEY`:


3. Configurazione del Servizio Systemd (Avvio Automatico)

Esci dall'ambiente virtuale digitando `deactivate`. Crea il file del demone che farà girare lo script in background:

```
sudo nano /etc/systemd/system/securitybot.service

```

Incolla questa configurazione, prestando molta attenzione a **sostituire `TUO_UTENTE**` (tutte e 4 le volte) con il vero nome utente di Linux di quel computer:


Salva il file, ricarica i demoni di sistema e abilita l'avvio automatico:

```
sudo systemctl daemon-reload
sudo systemctl enable --now securitybot.service

```

4. Creazione dell'Account Esca (Honeypot)

Crea l'utente "trappola" per attirare il ladro, assicurandoti che possa accedere senza password e connettersi al Wi-Fi in totale autonomia:

```
# Crea l'utente ignorando i campi anagrafici
sudo adduser --disabled-password --gecos "" ospite

# Svuota definitivamente la password per sbloccare l'utente nella schermata di login
sudo passwd -d ospite

# Crea il gruppo per il login senza password (se non esiste)
sudo groupadd -f nopasswdlogin

# Assegna i permessi di login diretto e di gestione delle schede di rete (Wi-Fi)
sudo usermod -aG nopasswdlogin,netdev ospite

# Nasconde il tutorial di benvenuto di GNOME per l'ospite
sudo su - ospite -c "mkdir -p ~/.config && echo 'yes' > ~/.config/gnome-initial-setup-done"

```

5. Sigillo della Cartella Personale

Dal tuo utente principale (non come ospite e non come root), chiudi a chiave la tua cartella `Home` in modo che il ladro non possa esplorarla a sistema avviato:

```
chmod 700 ~

```

Per verificare la corretta esecuzione del sistema, riavvia il PC, entra nell'account `ospite` cliccandoci sopra e connettiti a una nuova rete Wi-Fi: se entro pochi secondi ricevi la notifica Telegram sul telefono, l'installazione è un successo.
