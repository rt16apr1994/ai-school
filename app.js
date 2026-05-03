const BACKEND_URL = "https://your-app-name.onrender.com";

async function createVideo() {
    const topic = document.getElementById('topic').value;
    const lang = document.getElementById('language').value;
    
    // 1. Get Script from your Backend
    const response = await fetch(`${BACKEND_URL}/generate?topic=${topic}&lang=${lang}`);
    const data = await response.json();
    const script = JSON.parse(data.choices[0].message.content);

    // 2. Map scenes to Free Image Generator (Pollinations.ai)
    const videoContainer = document.getElementById('video-area');
    videoContainer.innerHTML = ''; 

    script.scenes.forEach((scene, index) => {
        const imgUrl = `https://image.pollinations.ai/prompt/${encodeURIComponent(scene.visual_prompt)}?width=1280&height=720&nologo=true`;
        
        videoContainer.innerHTML += `
            <div class="scene-box mb-4">
                <img src="${imgUrl}" class="rounded shadow-lg w-full">
                <p class="mt-2 italic">"${scene.narration_text}"</p>
            </div>
        `;
    });
}
