document.addEventListener('DOMContentLoaded', function () {
    const uploadZone = document.getElementById('upload-zone');
    const fileInput = document.getElementById('file-input');
    const uploadContent = document.getElementById('upload-content');
    const previewContent = document.getElementById('preview-content');
    const previewImage = document.getElementById('preview-image');
    const previewFilename = document.getElementById('preview-filename');
    const clearBtn = document.getElementById('clear-btn');
    const analyzeBtn = document.getElementById('analyze-btn');
    const uploadError = document.getElementById('upload-error');
    const uploadForm = document.getElementById('upload-form');

    const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10MB
    const ALLOWED_TYPES = ['image/jpeg', 'image/jpg', 'image/png'];

    // Open file picker when clicking the upload zone
    uploadZone.addEventListener('click', function (e) {
        if (e.target !== clearBtn) {
            fileInput.click();
        }
    });

    // Handle drag and drop
    uploadZone.addEventListener('dragover', function (e) {
        e.preventDefault();
        uploadZone.classList.add('dragover');
    });

    uploadZone.addEventListener('dragleave', function () {
        uploadZone.classList.remove('dragover');
    });

    uploadZone.addEventListener('drop', function (e) {
        e.preventDefault();
        uploadZone.classList.remove('dragover');

        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFile(files[0]);
        }
    });

    // Handle file selection via input
    fileInput.addEventListener('change', function () {
        if (fileInput.files.length > 0) {
            handleFile(fileInput.files[0]);
        }
    });

    // Clear selection
    clearBtn.addEventListener('click', function (e) {
        e.stopPropagation();
        resetUpload();
    });

    // Form submission
    uploadForm.addEventListener('submit', function (e) {
        if (!fileInput.files.length) {
            e.preventDefault();
            showError('Please select an image to upload.');
            return;
        }

        // Show loading state
        analyzeBtn.disabled = true;
        analyzeBtn.querySelector('.btn-text').classList.add('hidden');
        analyzeBtn.querySelector('.btn-loading').classList.remove('hidden');
    });

    function handleFile(file) {
        hideError();

        // Validate file type
        if (!ALLOWED_TYPES.includes(file.type)) {
            showError('Please upload a valid image file (JPG or PNG).');
            return;
        }

        // Validate file size
        if (file.size > MAX_FILE_SIZE) {
            showError('File is too large. Maximum size is 10MB.');
            return;
        }

        // Update file input (for drag and drop case)
        const dataTransfer = new DataTransfer();
        dataTransfer.items.add(file);
        fileInput.files = dataTransfer.files;

        // Show preview
        const reader = new FileReader();
        reader.onload = function (e) {
            previewImage.src = e.target.result;
            previewFilename.textContent = file.name;
            uploadContent.classList.add('hidden');
            previewContent.classList.remove('hidden');
            analyzeBtn.disabled = false;
        };
        reader.readAsDataURL(file);
    }

    function resetUpload() {
        fileInput.value = '';
        previewImage.src = '';
        previewFilename.textContent = '';
        uploadContent.classList.remove('hidden');
        previewContent.classList.add('hidden');
        analyzeBtn.disabled = true;
        hideError();
    }

    function showError(message) {
        uploadError.textContent = message;
        uploadError.classList.remove('hidden');
    }

    function hideError() {
        uploadError.classList.add('hidden');
    }
});
