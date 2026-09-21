const form = document.getElementById('shorten-form');
const resultBox = document.getElementById('result');

form.addEventListener('submit', async (event) => {
    event.preventDefault();

    const urlInput = document.getElementById('url');
    const url = urlInput.value.trim();

    if (!url) {
        resultBox.textContent = 'Please enter a valid URL.';
        return;
    }

    try {
        const response = await fetch('/shorten', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url })
        });

        const data = await response.json();
        if (!response.ok) {
            resultBox.textContent = data.error || 'Something went wrong.';
            return;
        }

        const link = data.short_url;
        resultBox.innerHTML = `Your short URL: <a href="${link}" target="_blank" rel="noopener noreferrer">${link}</a>`;
        form.reset();
    } catch (error) {
        resultBox.textContent = 'Failed to create short URL.';
    }
});
