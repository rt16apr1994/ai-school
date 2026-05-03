const BACKEND_URL = "https://ai-video-tutor-nkdp.onrender.com"; // Verified from your screenshot

async function createVideo() {
    const topic = document.getElementById('topic').value;
    const lang = document.getElementById('language').value;
    const status = document.getElementById('status');
    const videoArea = document.getElementById('video-area');

    if (!topic) return alert("Please enter a topic");

    status.classList.remove('hidden');
    videoArea.innerHTML = "";

    try {
        const response = await fetch(`${BACKEND_URL}/generate?topic=${encodeURIComponent(topic)}&lang=${lang}`);
        
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

        const data = await response.json();
        console.log("Response Data:", data); // Debugging ke liye data print karein

        // Error fix: Check karein ki choices exist karta hai ya nahi
        if (!data.choices || data.choices.length === 0) {
            throw new Error("AI provider se koi choices nahi mili. Please check OpenRouter quota.");
        }

        let contentText = data.choices[0].message.content;

        // Kabhi-kabhi AI JSON ke sath markdown (```json ...) bhej deta hai, ise saaf karein
        contentText = contentText.replace(/```json/g, "").replace(/```/g, "").trim();
        
        const script = JSON.parse(contentText);

        status.classList.add('hidden');

        script.scenes.forEach((scene) => {
            const imgUrl = `[https://image.pollinations.ai/prompt/$](https://image.pollinations.ai/prompt/$){encodeURIComponent(scene.visual_prompt)}?width=1280&height=720&nologo=true`;
            videoArea.innerHTML += `
                <div class="bg-white p-4 rounded-xl shadow-md mb-6 border border-slate-200">
                    <img src="${imgUrl}" class="w-full rounded-lg mb-4" alt="Scene Image">
                    <p class="text-slate-700 font-medium">${scene.narration_text}</p>
                </div>`;
        });

    } catch (error) {
        console.error("Detailed Error:", error);
        status.innerHTML = `<p class="text-red-500 font-bold">Error: ${error.message}</p>`;
    }
}
