# 🌸 Maturitní AI Asistentka Mahulina

Tento projekt je interaktivní webová aplikace postavená na frameworku **FastAPI**. Slouží jako inteligentní pomocník pro studenty připravující se na maturitu, využívající model **Gemma 3**.

## 🛠 Jak projekt funguje (Architektura)

Celá aplikace funguje jako řetězec tří hlavních částí:

1.  **Frontend (To, co vidíš):** HTML, CSS a JavaScript v tvém prohlížeči. JavaScript sbírá tvoje otázky a posílá je "za oponu" na tvůj server.
2.  **Backend (Mozeček - api.py):** Běží v Dockeru. Přijímá otázky z prohlížeče, přidá k nim instrukce (System Prompt - jak se má Mahulina chovat) a přepošle je s tvým klíčem na velký AI server.
3.  **AI Server (Školní mozek):** Zpracuje text pomocí modelu `gemma3:27b` a pošle odpověď zpět tvému backendu, který ji doručí až k tobě do chatu.

## 🚀 Spuštění přes PowerShell

Pokud vyvíjíš lokálně na Windows, otevři **PowerShell** ve složce projektu a použij tyto příkazy:

1.  **Sestavení a spuštění:**
    ```powershell
    docker-compose up --build
    ```
    *Tento příkaz vezme tvůj Dockerfile, stáhne Python, nainstaluje knihovny z requirements.txt a spustí aplikaci na portu 8081.*

2.  **Zastavení aplikace:**
    Stiskni `Ctrl + C` nebo v novém okně napiš:
    ```powershell
    docker-compose down
    ```

## 📂 Struktura souborů

- `api.py` — **Srdce aplikace.** Obsahuje API routy (endpointy) pro chat, status a čas.
- `templates/index.html` — **Kostra webu.** Definice toho, kde je chatovací okno a tlačítka.
- `static/css/style.css` — **Vzhled.** Pink-Purple barvy, animace z js a moderní design.
- `static/js/app.js` — **Logika webu.** Zpracovává kliknutí na tlačítka a vypisuje odpovědi z AI.
- `Dockerfile` — **Recept na kontejner.** Říká Dockeru, jak připravit prostředí pro Python.
- `docker-compose.yml` — **Správce spuštění.** Nastavuje porty a propojuje tvůj kód s AI serverem pomocí klíčů.

## ⚙️ Technologie
Aplikace je tak, aby byla flexibilní a mohla běžet v různých prostředích tak ve škole a doma:

- **na kurim.ithope.eu:** - Využívá výkonný model **Gemma 3 (27B)**.
  - Připojení probíhá přes školní API gateway s autorizací pomocí tokenu.
  
- **Lokální na muj pc (PowerShell / localhost):** - Optimalizováno pro běh na běžném hardwaru s modelem **Llama 3.2 1B** (přes LM Studio).
  - Backend automaticky komunikuje s lokálním endpointem, pokud není nastaven jiný.

- **Jazyk a Framework:** Python 3.9+ a FastAPI.
- **Kontejnerizace:** Docker – zajišťuje, že se aplikace chová stejně na Windows (PowerShell) i na Linuxovém serveru.
