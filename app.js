const BACKEND_URL = "https://ai-video-tutor-nkdp.onrender.com";

async function createVideo() {
    const topic = document.getElementById('topic').value;
    const lang = document.getElementById('language').value;
    const status = document.getElementById('status');
    const videoArea = document.getElementById('video-area');

    if(!topic) return alert("Please enter a topic");

    status.classList.remove('hidden');
    videoArea.innerHTML = "";

    try {
        const response = await fetch(`${BACKEND_URL}/generate?topic=${encodeURIComponent(topic)}&lang=${lang}`);
        const data = await response.json();

        if (data.error || !data.choices) {
            throw new Error(data.details || "AI Error: Check Quota/Model");
        }

        const content = JSON.parse(data.choices[0].message.content);
        status.classList.add('hidden');

        content.scenes.forEach(scene => {
            const imgUrl = `https://image.pollinations.ai/prompt/${encodeURIComponent(scene.visual_prompt)}?width=800&height=450&nologo=true`;
            videoArea.innerHTML += `
                <div class="mb-8 border-b pb-4">
                    <img src="${imgUrl}" class="w-full rounded shadow-lg mb-2">
                    <p class="text-gray-800 italic text-lg">"${scene.narration_text}"</p>
                </div>
            `;
        });
    } catch (err) {
        status.innerHTML = `<span class="text-red-500">Error: ${err.message}</span>`;
        console.error(err);
    }
}
