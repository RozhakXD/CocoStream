const form = document.getElementById('convertForm');
const linkInput = document.getElementById('linkInput');
const notification = document.getElementById('notification');
const convertedLinksContainer = document.getElementById('convertedLinks');

function showNotification(message, type = 'success') {
    notification.textContent = message;
    notification.className = `notification show ${
        type === 'success' ? 'bg-green-500 text-white' : 'bg-red-500 text-white'
    }`;
    setTimeout(() => {
        notification.className = 'notification hidden';
    }, 3000);
}

form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const video_urls = linkInput.value.trim();

    if (!video_urls) {
        showNotification('Please enter a valid link!', 'error');
        return;
    }

    try {
        const response = await fetch('/' , {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(
                {
                    video_urls
                }
            ),
        });
        const results = await response.json();
        if (results.success) {
            showNotification(results.message, 'success');
            convertedLinksContainer.innerHTML = results.download_links.map(link => `
                <div class="card bg-white dark:bg-gray-800 p-6 rounded-lg shadow-md">
                    <h4 class="text-xl font-semibold mb-2 text-blue-600 truncate">${link.server_filename}</h4>
                    <p class="text-sm text-gray-600 dark:text-gray-400 mb-4">Size: ${link.size.toFixed(2)} MB</p>
                    <a 
                href="${link.direct_link}" 
                target="_blank"
                rel="noopener noreferrer"
                class="bg-blue-500 text-white px-4 py-2 rounded-lg text-sm font-semibold hover:bg-blue-600 focus:ring-2 focus:ring-blue-400 inline-block">
                Download
                    </a>
                </div>
            `).join('');
        } else {
            showNotification(results.message, 'error');
        }
    } catch (error) {
        console.log(error);
        showNotification('Something went wrong!', 'error');
    }
});