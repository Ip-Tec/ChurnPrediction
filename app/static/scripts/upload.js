const dropArea = document.getElementById("drop-area");
const fileInput = document.getElementById("file-input");
const fileList = document.getElementById("file-list");
const browseButton = document.getElementById("browse-button");

// Highlight the drag area when files are dragged over
dropArea.addEventListener("dragover", (e) => {
  e.preventDefault();
  dropArea.style.backgroundColor = "#f0f8ff";
});

// Remove highlight when drag leaves
dropArea.addEventListener("dragleave", () => {
  dropArea.style.backgroundColor = "#fff";
});

// Handle file drop
dropArea.addEventListener("drop", (e) => {
  e.preventDefault();
  dropArea.style.backgroundColor = "#fff";
  handleFiles(e.dataTransfer.files);
});

// Open file dialog when the browse button is clicked
browseButton.addEventListener("click", () => fileInput.click());

// Handle file selection through the file input
fileInput.addEventListener("change", () => handleFiles(fileInput.files));

// Handle the files
function handleFiles(files) {
  Array.from(files).forEach((file) => {
    const listItem = document.createElement("li");
    listItem.textContent = `${file.name} (${(file.size / 1024).toFixed(2)} KB)`;

    const uploadButton = document.createElement("button");
    uploadButton.textContent = "Upload";
    uploadButton.addEventListener("click", () => uploadFile(file));

    listItem.appendChild(uploadButton);
    fileList.appendChild(listItem);
  });
}

// Upload file to the backend
function uploadFile(file) {
  const formData = new FormData();
  formData.append("file", file);

  fetch("/upload", {
    method: "POST",
    body: formData,
  })
    .then((response) => {
      if (response.ok) {
        alert(`${file.name} uploaded successfully!`);
      } else {
        alert(`Failed to upload ${file.name}`);
      }
    })
    .catch((error) => console.error("Error:", error));
}
