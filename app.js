const BACKEND_URL = "https://ai-video-tutor-nkdp.onrender.com"; // Verified from your screenshot

async function createVideo() {
    const topic = document.getElementById('topic').value;
    const lang = document.getElementById('language').value;
    const status = document.getElementById('status');
    const videoArea = document.getElementById('video-area');

    if (!topic) return alert("Please enter a topic");

    status.classList.remove('hidden');
    status.innerHTML = "<p>Waking up server... This might take 60 seconds on Free Tier.</p>";
    videoArea.innerHTML = "";

    try {
        const response = await fetch(`${BACKEND_URL}/generate?topic=${encodeURIComponent(topic)}&lang=${lang}`);
        
        if (!response.ok) throw new Error(`Server status: ${response.status}`);

        const data = await response.json();
        
        // Screenshot error "reading '0'" fix: Data structure check
        if (!data.choices || !data.choices[0]) {
            throw new Error("Invalid response from AI provider");
        }

        const contentText = data.choices[0].message.content;
        const script = JSON.parse(contentText);

        status.classList.add('hidden');

        script.scenes.forEach((scene) => {
            const imgUrl = `https://image.pollinations.ai/prompt/${encodeURIComponent(scene.visual_prompt)}?width=1280&height=720&nologo=true`;
            videoArea.innerHTML += `
                <div class="bg-white p-4 rounded-xl shadow-md mb-6">
                    <img src="${imgUrl}" class="w-full rounded-lg mb-4">
                    <p class="text-slate-700 font-medium">${scene.narration_text}</p>
                </div>`;
        });

    } catch (error) {
        console.error("Error details:", error);
        status.innerHTML = `<p class="text-red-500 font-bold text-center">Error: ${error.message}<br>Please wait 1 minute and try again.</p>`;
    }
}
