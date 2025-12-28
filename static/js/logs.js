
const logArea = document.getElementById("logArea");

async function startLogStream() {
    const response = await fetch(`${API_BASE}/api/service-logs`);
    const reader = response.body.getReader();
    const decoder = new TextDecoder("utf-8");

    while (true) {
        const { value, done } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value, { stream: true });
        appendLog(chunk);
    }
}

function appendLog(text) {
    logArea.textContent += text;

    //oto scroll
    logArea.scrollTop = logArea.scrollHeight;

    //aşırı büyüme olmaması için otomatik silme
    const lines = logArea.textContent.split("\n");
    if (lines.length > 1000) {
        logArea.textContent = lines.slice(-600).join("\n");
    }
}

startLogStream();