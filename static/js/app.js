let uploadedImages = [];

const dropZone = document.getElementById('dropZone');
const fileInput = document.getElementById('fileInput');
const imageGallery = document.getElementById('imageGallery');
const clearImageBtn = document.getElementById('clearImage');
const chatMessages = document.getElementById('chatMessages');
const promptInput = document.getElementById('promptInput');
const sendBtn = document.getElementById('sendBtn');
const loading = document.getElementById('loading');
const lightbox = document.getElementById('lightbox');
const lightboxImage = document.getElementById('lightboxImage');
const lightboxClose = document.getElementById('lightboxClose');

// File upload handlers
dropZone.addEventListener('click', () => fileInput.click());

dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.classList.add('drag-over');
});

dropZone.addEventListener('dragleave', () => {
    dropZone.classList.remove('drag-over');
});

dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('drag-over');
    const files = Array.from(e.dataTransfer.files).filter(f => f.type.startsWith('image/'));
    if (files.length > 0) {
        uploadMultipleImages(files);
    }
});

fileInput.addEventListener('change', (e) => {
    const files = Array.from(e.target.files);
    if (files.length > 0) {
        uploadMultipleImages(files);
    }
});

clearImageBtn.addEventListener('click', () => {
    uploadedImages = [];
    updateImagePreview();
    fileInput.value = '';
});

async function uploadMultipleImages(files) {
    for (const file of files) {
        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (data.success) {
                uploadedImages.push({
                    filename: data.filename,
                    url: data.url
                });
            } else {
                addMessage('Error uploading image: ' + data.error, 'error');
            }
        } catch (error) {
            addMessage('Error uploading image: ' + error.message, 'error');
        }
    }

    updateImagePreview();
    const count = uploadedImages.length;
    const msg = count === 1
        ? 'Image uploaded! Ask me anything about it.'
        : `${count} images uploaded! I can compare and analyze them together.`;
    addMessage(msg, 'assistant');
}

function updateImagePreview() {
    imageGallery.innerHTML = '';

    if (uploadedImages.length === 0) {
        clearImageBtn.style.display = 'none';
    } else {
        clearImageBtn.style.display = 'block';
        clearImageBtn.textContent = uploadedImages.length === 1
            ? 'Clear Image'
            : `Clear All Images (${uploadedImages.length})`;

        // Create gallery items
        uploadedImages.forEach((img, index) => {
            const galleryItem = document.createElement('div');
            galleryItem.className = 'gallery-item';

            const imgElement = document.createElement('img');
            imgElement.src = img.url;
            imgElement.alt = img.filename;

            // Click to view full size
            imgElement.addEventListener('click', () => {
                showLightbox(img.url);
            });

            const removeBtn = document.createElement('button');
            removeBtn.className = 'gallery-item-remove';
            removeBtn.innerHTML = '×';
            removeBtn.onclick = (e) => {
                e.stopPropagation();
                removeImage(index);
            };

            galleryItem.appendChild(imgElement);
            galleryItem.appendChild(removeBtn);
            imageGallery.appendChild(galleryItem);
        });
    }
}

function removeImage(index) {
    uploadedImages.splice(index, 1);
    updateImagePreview();
    if (uploadedImages.length === 0) {
        addMessage('All images cleared.', 'assistant');
    } else {
        addMessage(`Image removed. ${uploadedImages.length} image(s) remaining.`, 'assistant');
    }
}

function showLightbox(imageUrl) {
    lightboxImage.src = imageUrl;
    lightbox.classList.add('show');
}

function closeLightbox() {
    lightbox.classList.remove('show');
}

// Lightbox event listeners
lightboxClose.addEventListener('click', closeLightbox);
lightbox.addEventListener('click', (e) => {
    if (e.target === lightbox) {
        closeLightbox();
    }
});

// Close lightbox with Escape key
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && lightbox.classList.contains('show')) {
        closeLightbox();
    }
});

// Chat handlers
sendBtn.addEventListener('click', sendMessage);
promptInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

async function sendMessage() {
    const prompt = promptInput.value.trim();

    if (!prompt) {
        return;
    }

    addMessage(prompt, 'user');
    promptInput.value = '';

    loading.classList.add('show');
    sendBtn.disabled = true;

    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                prompt: prompt,
                image_paths: uploadedImages.map(img => img.filename)
            })
        });

        const data = await response.json();

        if (data.success) {
            addMessage(data.response, 'assistant');
        } else {
            addMessage('Error: ' + data.error, 'error');
        }
    } catch (error) {
        addMessage('Error: ' + error.message, 'error');
    } finally {
        loading.classList.remove('show');
        sendBtn.disabled = false;
    }
}

function addMessage(text, type) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;
    messageDiv.textContent = text;
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

