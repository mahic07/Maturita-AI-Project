const chat = document.getElementById("chat");
const chatForm = document.getElementById("chatForm");
const promptInput = document.getElementById("promptInput");
const pingBtn = document.getElementById("pingBtn");
const statusBtn = document.getElementById("statusBtn");
const statusBox = document.getElementById("statusBox");
const toast = document.getElementById("toast");
const sidebarTime = document.getElementById("sidebarTime");


let sessionId = localStorage.getItem("chatSessionId") || generateSessionId();
localStorage.setItem("chatSessionId", sessionId);

function generateSessionId() {
    return "session_" + Date.now() + "_" + Math.random().toString(36).substr(2, 9);
}

function escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
}

function addMessage(role, content, isHtml = false) {
    const article = document.createElement("article");

    article.className = `message ${role} glass-panel`; 

    const inner = document.createElement("div");
    inner.className = "message-content";
    inner[isHtml ? "innerHTML" : "textContent"] = content;

    article.appendChild(inner);
    chat.appendChild(article);
    
    article.scrollIntoView({ behavior: "smooth", block: "end" });
    return article;
}

async function loadHistory() {
    try {
        const res = await fetch(`/api/history/${sessionId}`);
        if (res.ok) {
            const data = await res.json();
            if (data.messages && data.messages.length > 0) {

                chat.innerHTML = ""; 
                data.messages.forEach(msg => {
                    addMessage(msg.sender === "user" ? "user" : "assistant", msg.content);
                });
            }
        }
    } catch (err) {
        console.error("Historii se nepodařilo načíst:", err);
    }
}

function showToast(message) {
    toast.textContent = message;
    toast.classList.remove("hidden");
    clearTimeout(showToast._timer);
    showToast._timer = setTimeout(() => toast.classList.add("hidden"), 2600);
}

async function loadPing() {
    try {
        const res = await fetch("/api/ping");
        const data = await res.json();
        showToast(`✅ ${data.message}`);
    } catch {
        showToast("Server neodpovídá (Ping selhal).");
    }
}

async function loadStatus() {
    try {
        const res = await fetch("/api/status");
        const data = await res.json();
        statusBox.innerHTML = `
            <b>Autor:</b> ${escapeHtml(data.author)}<br>
            <b>Status:</b> ${escapeHtml(data.status)}<br>
            <b>Čas:</b> ${escapeHtml(data.time)}
        `;
        statusBox.classList.remove("hidden");
        sidebarTime.textContent = data.time;
    } catch {
        showToast("Status se nepodařilo aktualizovat.");
    }
}


pingBtn.addEventListener("click", loadPing);
statusBtn.addEventListener("click", loadStatus);

chatForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const prompt = promptInput.value.trim();
    if (!prompt) return;

    addMessage("user", prompt);
    promptInput.value = "";
    promptInput.focus();

    const typing = addMessage("assistant", "Přemýšlím, počkej chvilku...");
    const contentDiv = typing.querySelector(".message-content");
    contentDiv.classList.add("typing");

    try {
        const res = await fetch("/api/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ 
                prompt: prompt,
                session_id: sessionId 
            })
        });
        
        const data = await res.json();
        contentDiv.classList.remove("typing");

        if (res.ok && data.answer) {
            contentDiv.textContent = data.answer;
        } else {
            contentDiv.textContent = data.fallback || "Omlouvám se, něco se pokazilo.";
            showToast(data.error || "Chyba komunikace.");
        }
    } catch (error) {
        contentDiv.classList.remove("typing");
        contentDiv.textContent = "Server je momentálně nedostupný. Zkontroluj Docker!";
        showToast("Chyba sítě.");
    }
});

// --- SPUŠTĚNÍ PŘI STARTU ---
// Nejdřív načteme historii a pak status
loadHistory();
loadStatus();
