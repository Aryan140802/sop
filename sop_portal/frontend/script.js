// Global variable for all SOPs
let allSOPs = [];

// Fetch all SOPs on page load
async function fetchSOPs() {
  try {
    const res = await fetch("http://localhost:8000/api/sops/");
    const data = await res.json();
    allSOPs = data;
    filterAndRenderSOPs();
    loadPinned();
  } catch (error) {
    console.error("Failed to fetch SOPs:", error);
  }
}

// Render SOP list from given array
function renderSOPList(sops) {
  const sopList = document.getElementById("sopList");
  if (!sopList) return; // safety check

  sopList.innerHTML = "";

  sops.forEach(sop => {
    const li = document.createElement("li");
    li.className = "sop-item";

    const icon = document.createElement("span");
    icon.className = "sop-icon";
    icon.textContent = "📝";

    const title = document.createElement("span");
    title.className = "sop-title";
    title.textContent = sop.title;

    const pinBtn = document.createElement("button");
    pinBtn.textContent = "📌";
    pinBtn.title = "Pin this SOP";
    pinBtn.className = "pin-btn";
    pinBtn.onclick = (e) => {
      e.stopPropagation();
      togglePin(sop.id, sop.title);
    };

    const contentWrapper = document.createElement("div");
    contentWrapper.className = "sop-content";
    contentWrapper.appendChild(icon);
    contentWrapper.appendChild(title);

    li.appendChild(contentWrapper);
    li.appendChild(pinBtn);

    li.addEventListener("click", () => openModal(sop));

    sopList.appendChild(li);
  });
}

// Filter SOPs based on team dropdown and search input, then render
function filterAndRenderSOPs() {
  const teamFilterElem = document.getElementById("teamFilter");
  const searchElem = document.getElementById("search");

  const teamFilter = teamFilterElem ? teamFilterElem.value.trim().toLowerCase() : "";
  const searchTerm = searchElem ? searchElem.value.trim().toLowerCase() : "";

  let filtered = allSOPs;

  if (teamFilter) {
    filtered = filtered.filter(sop => sop.team.toLowerCase() === teamFilter);
  }

  if (searchTerm) {
    filtered = filtered.filter(sop => sop.title.toLowerCase().includes(searchTerm));
  }

  renderSOPList(filtered);
}

// Modal open function with line numbers
function openModal(sop) {
  const content = sop.sop_text || sop.content || "";
  const lines = content.split(/\r\n|\r|\n/);

  const modalTitle = document.getElementById("modalTitle");
  if (modalTitle) modalTitle.textContent = `${sop.title} (${lines.length} lines)`;

  const contentContainer = document.getElementById("modalContent");
  if (!contentContainer) return;
  contentContainer.innerHTML = ''; // Clear previous content

  lines.forEach((line, idx) => {
    const lineElement = document.createElement("div");
    lineElement.style.display = "flex";

    const lineNumber = document.createElement("span");
    lineNumber.style.width = "30px";
    lineNumber.style.color = "#999";
    lineNumber.style.textAlign = "right";
    lineNumber.style.marginRight = "10px";
    lineNumber.textContent = idx + 1;

    const lineText = document.createElement("span");
    lineText.textContent = line;

    lineElement.appendChild(lineNumber);
    lineElement.appendChild(lineText);

    contentContainer.appendChild(lineElement);
  });

  const modal = document.getElementById("sopModal");
  if (modal) modal.style.display = "flex";
}

// Pin/unpin toggle function
function togglePin(id, title) {
  let pinned = JSON.parse(localStorage.getItem('pinned') || '[]');
  const index = pinned.findIndex(p => p.id === id);
  if (index !== -1) {
    pinned.splice(index, 1);
  } else {
    pinned.push({ id, title });
  }
  localStorage.setItem('pinned', JSON.stringify(pinned));
  loadPinned();
}

// Load pinned SOPs list
function loadPinned() {
  const pinned = JSON.parse(localStorage.getItem('pinned') || '[]');
  const pinList = document.getElementById('pinnedList');
  if (!pinList) return;

  pinList.innerHTML = '';

  pinned.forEach(pin => {
    const li = document.createElement('li');
    li.className = 'pinned-item';

    const label = document.createElement('span');
    label.textContent = `📌 ${pin.title}`;
    label.style.flexGrow = 1;

    const removeBtn = document.createElement('button');
    removeBtn.textContent = "❌";
    removeBtn.title = "Remove Pin";
    removeBtn.className = "remove-pin";
    removeBtn.onclick = (e) => {
      e.stopPropagation();
      togglePin(pin.id, pin.title);
    };

    const match = allSOPs.find(s => s.id === pin.id);
    if (match) {
      li.style.cursor = "pointer";
      li.addEventListener("click", () => openModal(match));
    }

    li.appendChild(label);
    li.appendChild(removeBtn);
    pinList.appendChild(li);
  });

  updatePinnedSectionVisibility();
}

// Show/hide pinned section based on pins count
function updatePinnedSectionVisibility() {
  const pinnedSection = document.getElementById('pinnedSection');
  const pinnedList = document.getElementById('pinnedList');
  if (!pinnedSection || !pinnedList) return;

  pinnedSection.style.display = pinnedList.children.length > 0 ? 'block' : 'none';
}

// Close modal
function closeModal() {
  const modal = document.getElementById("sopModal");
  if (modal) modal.style.display = "none";
}

// Copy SOP to clipboard
function copyToClipboard() {
  const contentContainer = document.getElementById("modalContent");
  if (!contentContainer) return;

  const content = contentContainer.textContent;
  navigator.clipboard.writeText(content)
    .then(() => alert("SOP copied to clipboard!"))
    .catch(() => alert("Failed to copy!"));
}

// Attach all event listeners after DOM content loaded
document.addEventListener("DOMContentLoaded", () => {
  // Fetch SOPs and load pinned
  fetchSOPs();

  // Upload form listener
  const uploadForm = document.getElementById("uploadForm");
  if (uploadForm) {
    uploadForm.addEventListener("submit", async function (e) {
      e.preventDefault();

      const title = document.getElementById("title").value;
      const team = document.getElementById("team").value;
      const sop_text = document.getElementById("sop_text").value;

      try {
        const res = await fetch("http://localhost:8000/api/sops/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ title, team, sop_text }),
        });

        if (res.ok) {
          alert("SOP uploaded successfully!");
          window.location.href = "index.html"; // Redirect after success
        } else {
          const errData = await res.json();
          alert("Upload failed: " + JSON.stringify(errData));
        }
      } catch (err) {
        alert("Error uploading SOP: " + err.message);
      }
    });
  }

  // Filter team dropdown listener
  const teamFilter = document.getElementById("teamFilter");
  if (teamFilter) teamFilter.addEventListener("change", filterAndRenderSOPs);

  // Search input listener
  const searchInput = document.getElementById("search");
  if (searchInput) searchInput.addEventListener("input", filterAndRenderSOPs);

  // Modal close button listener
  const closeModalBtn = document.getElementById("closeModal");
  if (closeModalBtn) closeModalBtn.addEventListener("click", closeModal);

  // Copy to clipboard button listener
  const copyBtn = document.getElementById("copyBtn");
  if (copyBtn) copyBtn.addEventListener("click", copyToClipboard);
});
