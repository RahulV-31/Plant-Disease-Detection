document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const dropzone = document.getElementById('dropzone');
    const fileInput = document.getElementById('file-input');
    const browseBtn = document.getElementById('browse-btn');
    const uploadArea = document.getElementById('upload-area');
    const previewArea = document.getElementById('preview-area');
    const loadingArea = document.getElementById('loading-area');
    const resultCard = document.getElementById('result-card');
    const previewImage = document.getElementById('preview-image');
    const resultImage = document.getElementById('result-image');
    const filename = document.getElementById('filename');
    const removeBtn = document.getElementById('remove-btn');
    const analyzeBtn = document.getElementById('analyze-btn');
    const analyzeAnotherBtn = document.getElementById('analyze-another-btn');
    
    // Result elements
    const resultBadge = document.getElementById('result-badge');
    const resultClass = document.getElementById('result-class');
    const confidenceProgress = document.getElementById('confidence-progress');
    const confidenceValue = document.getElementById('confidence-value');
    const recommendationText = document.getElementById('recommendation-text');
    
    // File handling variables
    let selectedFile = null;
    
    // Event listeners
    if (browseBtn) browseBtn.addEventListener('click', () => fileInput.click());
    if (dropzone) {
        dropzone.addEventListener('click', () => fileInput.click());
        
        // Drag and drop events
        dropzone.addEventListener('dragover', (e) => {
            e.preventDefault();
            dropzone.classList.add('drag-over');
        });
        
        dropzone.addEventListener('dragleave', () => {
            dropzone.classList.remove('drag-over');
        });
        
        dropzone.addEventListener('drop', (e) => {
            e.preventDefault();
            dropzone.classList.remove('drag-over');
            
            if (e.dataTransfer.files.length) {
                handleFileSelection(e.dataTransfer.files[0]);
            }
        });
    }
    
    // File input change event
    if (fileInput) {
        fileInput.addEventListener('change', () => {
            if (fileInput.files.length) {
                handleFileSelection(fileInput.files[0]);
            }
        });
    }
    
    // Remove button click
    if (removeBtn) {
        removeBtn.addEventListener('click', resetUpload);
    }
    
    // Analyze button click
    if (analyzeBtn) {
        analyzeBtn.addEventListener('click', analyzeImage);
    }
    
    // Analyze another button click
    if (analyzeAnotherBtn) {
        analyzeAnotherBtn.addEventListener('click', resetUpload);
    }
    
    // Functions
    function handleFileSelection(file) {
        // Check if file is an image
        if (!file.type.match('image.*')) {
            alert('Please select an image file (JPEG, PNG)');
            return;
        }
        
        selectedFile = file;
        
        // Update UI
        uploadArea.style.display = 'none';
        previewArea.style.display = 'block';
        
        // Display file name
        if (filename) filename.textContent = file.name;
        
        // Preview image
        const reader = new FileReader();
        reader.onload = (e) => {
            previewImage.src = e.target.result;
        };
        reader.readAsDataURL(file);
    }
    
    function resetUpload() {
        // Reset file input
        if (fileInput) fileInput.value = '';
        selectedFile = null;
        
        // Reset UI
        uploadArea.style.display = 'block';
        previewArea.style.display = 'none';
        loadingArea.style.display = 'none';
        resultCard.style.display = 'none';
    }
    
    function analyzeImage() {
        if (!selectedFile) {
            alert('Please select an image first');
            return;
        }
        
        // Show loading state
        previewArea.style.display = 'none';
        loadingArea.style.display = 'block';
        
        // Create form data
        const formData = new FormData();
        formData.append('file', selectedFile);
        
        // Send request to server
        fetch('/predict', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
                resetUpload();
                return;
            }
            
            // Display results
            displayResults(data);
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while analyzing the image');
            resetUpload();
        });
    }
    
    function displayResults(data) {
        // Hide loading
        loadingArea.style.display = 'none';
        
        // Show result card
        resultCard.style.display = 'block';
        
        // Set result image
        resultImage.src = '/' + data.filepath;
        
        // Update disease class
        resultClass.textContent = data.class;
        
        // Update confidence
        const confidence = data.confidence.toFixed(1);
        confidenceProgress.style.width = confidence + '%';
        confidenceValue.textContent = confidence + '%';
        
        // Update recommendation
        recommendationText.textContent = data.recommendation;
        
        // Update badge status
        if (data.class.toLowerCase().includes('healthy')) {
            resultBadge.textContent = 'Healthy';
            resultBadge.className = 'badge healthy';
        } else {
            resultBadge.textContent = 'Disease Detected';
            resultBadge.className = 'badge diseased';
        }
        
        // Smooth scroll to results
        resultCard.scrollIntoView({ behavior: 'smooth' });
    }
    
    // Initialize tooltips if Bootstrap 5 is used
    if (typeof bootstrap !== 'undefined' && bootstrap.Tooltip) {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
});