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
    uploadButton.addEventListener("click", () => uploadFile(file, listItem));

    listItem.appendChild(uploadButton);
    fileList.appendChild(listItem);
  });
}

// Upload file to the backend
function uploadFile(file, listItem) {
  const formData = new FormData();
  formData.append("file", file);

  fetch("/upload", {
    method: "POST",
    body: formData,
  })
    .then((response) => {
      if (response.ok) {
        return response.json(); // Assuming backend returns { message: "...", result: "...", fileName: "..." }
      } else {
        throw new Error("Upload failed");
      }
    })
    .then((data) => {
      alert(`${file.name} uploaded successfully!`);

      // Add a Churn button
      const churnButton = document.createElement("button");
      churnButton.textContent = "Churn";
      churnButton.addEventListener("click", () => churnFile(data.fileName));

      listItem.appendChild(churnButton);
    })
    .catch((error) => {
      console.error("Error:", error);
      alert(`Failed to upload ${file.name}`);
    });
}

// Send file for Churn processing
function churnFile(fileName) {
  fetch("/process-churn", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ file_name: fileName }),
  })
    .then((response) => {
      if (response.ok) {
        // Assuming backend returns churn result as plain text or HTML
        return response.text();
      } else {
        console.log({ ...response });
        throw new Error("Churn processing failed");
      }
    })
    .then((result) => {
      // Redirect to a new page or display result dynamically
      document.body.innerHTML = result;
    })
    .catch((error) => {
      console.error("Error:", error);
      alert("Failed to process Churn");
    });
}

document.getElementById("file-input").addEventListener("change", async () => {
  const fileInput = document.getElementById("file-input");
  const previewContainer = document.getElementById("preview-container");
  const dataPreview = document.getElementById("data-preview");
  const targetColumnSelect = document.getElementById("target-column");
  const processButton = document.getElementById("process-button");

  if (fileInput.files.length === 0) {
    alert("Please select a file.");
    return;
  }

  const formData = new FormData();
  formData.append("file", fileInput.files[0]);

  try {
    const response = await fetch("/preview-data", {
      method: "POST",
      body: formData,
    });

    if (response.ok) {
      const { headers, rows } = await response.json();

      // Populate the table preview
      let tableHtml = "<tr>";
      headers.forEach((header) => {
        tableHtml += `<th>${header}</th>`;
      });
      tableHtml += "</tr>";
      rows.forEach((row) => {
        tableHtml += "<tr>";
        headers.forEach((header) => {
          tableHtml += `<td>${row[header] || ""}</td>`;
        });
        tableHtml += "</tr>";
      });
      dataPreview.innerHTML = tableHtml;

      // Populate the target column dropdown
      targetColumnSelect.innerHTML = headers
        .map((header) => `<option value="${header}">${header}</option>`)
        .join("");

      previewContainer.style.display = "block";
      processButton.disabled = false;
    } else {
      const error = await response.json();
      alert("Error: " + error.error);
    }
  } catch (err) {
    console.error(err);
    alert("An error occurred while previewing the data.");
  }
});

// Get elements
const dataItems = document.querySelectorAll('.data-item');
const contentArea = document.getElementById('data-content');
const placeholder = document.querySelector('.placeholder');

// Data content for demonstration
const dataContent = {
    1: "This is the content of Data File 1. It contains detailed insights and analysis.",
    2: "This is the content of Data File 2. It includes user-uploaded data and metrics.",
    3: "This is the content of Data File 3. It summarizes key performance indicators."
};

// Add click event to each data item
dataItems.forEach(item => {
    item.addEventListener('click', () => {
        const dataId = item.getAttribute('data-id');
        displayContent(dataId);
    });
});

// Function to display content
function displayContent(dataId) {
    // Remove placeholder
    placeholder.style.display = "none";

    // Insert content
    contentArea.innerHTML = `
        <div class="content active">
            <h2>Data Content</h2>
            <p>${dataContent[dataId]}</p>
        </div>
    `;

    // Mobile-specific behavior
    if (window.innerWidth <= 768) {
        contentArea.classList.add('active');
        document.querySelector('.data-list').style.display = "none";
    }
}
