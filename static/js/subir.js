const dropArea = document.getElementById('drop-area');
const fileInput = document.getElementById('fileElem');
const fileName = document.getElementById('fileName');

dropArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropArea.classList.add('dragover');
});

dropArea.addEventListener('dragleave', () => {
    dropArea.classList.remove('dragover');
});

dropArea.addEventListener('drop', (e) => {
    e.preventDefault();
    dropArea.classList.remove('dragover');

    const files = e.dataTransfer.files;
    if (files.length > 0) {
        fileInput.files = files;
        fileName.textContent = "Archivo: " + files[0].name;
    }
});

fileInput.addEventListener('change', () => {
    if (fileInput.files.length > 0) {
        fileName.textContent = "Archivo: " + fileInput.files[0].name;
    }
});