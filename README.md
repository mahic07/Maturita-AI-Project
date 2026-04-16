# Maturitní projekt: AI Asistentka Mahulina ✨

Tento projekt byl vytvořen jako maturitní práce v rámci předmětu eos. Jedná se o webovou aplikaci, která slouží jako interaktivní asistentka pro studenty připravující se na maturitu.

## 📄 Popis projektu
Mahulina je inteligentní chatovací bot, který využívá velký jazykový model (LLM) k odpovídání na dotazy uživatelů. Aplikace je navržena tak, aby si pamatovala historii konverzace pro každého uživatele zvlášť díky propojení s externí databází.

**Hlavní funkce:**
* Interaktivní chatovací rozhraní v češtině.
* Trvalé ukládání historie zpráv (zůstane i po obnovení stránky).
* Integrace s AI modelem přes OpenAI-kompatibilní API.
* Monitorování stavu systému přes API endpointy `/ping` a `/status`.

## 🛠 Použité technologie
[cite_start]Projekt je postaven na moderní kontejnerizované architektuře (Varianta A podle zadání)[cite: 8]:
* **Backend:** Python 3.11 s frameworkem **FastAPI**.
* [cite_start]**Databáze:** **PostgreSQL 15** (běží jako samostatný kontejner)[cite: 44].
* **Frontend:** HTML5, CSS3 (moderní tmavý design) a JavaScript (Fetch API).
* [cite_start]**Kontejnerizace:** **Docker** a **Docker Compose**[cite: 15, 42].
* [cite_start]**AI Model:** `gemma3:27b` poskytovaný školním serverem[cite: 46].

## 🏗 Architektura systému
[cite_start]V souladu se zadáním projekt využívá dva kontejnery, které spolu komunikují přes interní síť Dockeru[cite: 21, 23]:
1.  **maturita-app**: Obsahuje samotnou logiku aplikace, API a obsluhu frontendu.
2.  [cite_start]**db**: Oficiální obraz PostgreSQL pro ukládání dat[cite: 36].



## 🚀 Jak spustit projekt
[cite_start]Projekt je optimalizován pro nasazení na portálu **kurim.ithope.eu**[cite: 37].

1.  **Lokální spuštění:**
    ```powershell
    docker-compose up --build
    ```
    Aplikace bude dostupná na adrese `http://localhost:8081`.

2.  **Nasazení na server:**
    * [cite_start]Nahrát kód do veřejného GitHub repozitáře[cite: 20].
    * [cite_start]V dashboardu kurim.ithope.eu nastavit proměnné prostředí: `OPENAI_API_KEY`, `LM_STUDIO_URL` a `DATABASE_URL`[cite: 45].
    * [cite_start]Spustit nasazení (Deploy)[cite: 48].

## 📋 Splnění požadavků (Varianta A)
* Veřejné GitHub repo[cite: 20].
* Dva komunikující kontejnery (App + Postgres)[cite: 21, 23, 36].
* Reálné využití databáze (zápis i čtení historie)[cite: 24, 25, 47].
* Volání LLM modelu přes API[cite: 26, 27].
* Soubor `compose.yml` v kořenovém adresáři[cite: 42].

**Autor:** Mahi Chauhan IT4B
