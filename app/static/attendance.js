(() =>{
const STREAM_URL = "http://localhost:8000/attendance/take_attendance";
const CAPTURE_INTERVAL = 300;

const elements = {
  startBtn: document.getElementById('start-btn'),
  stopBtn: document.getElementById('stop-btn'),
  statusEl: document.getElementById('status'),
  stage: document.getElementById('stage'),
  videoEl: document.getElementById('cam'),
  canvasEl: document.getElementById('overlay'),
  tbody: document.getElementById('att-body')
};

let mediaStream = null;
let captureInterval = null;
let isStreaming = false;
let attendanceList = [];

function updateStatus(message) {
  elements.statusEl.textContent = message;
}

function updateTable() {
  elements.tbody.innerHTML = '';
  attendanceList.forEach(record => {
    const row = document.createElement('tr');
    row.innerHTML = `<td>${record.first_name} ${record.last_name}</td><td>${record.date}</td><td>${record.status_type}</td>`;
    elements.tbody.appendChild(row);
  });
}

async function startCamera() {
  if (!navigator.mediaDevices?.getUserMedia) {
    updateStatus("Camera not supported.");
    return;
  }

  try {
    updateStatus("Requesting camera...");
    mediaStream = await navigator.mediaDevices.getUserMedia({ video: true });
    elements.videoEl.srcObject = mediaStream;
    elements.stage.style.display = 'block';

    elements.startBtn.disabled = true;
    elements.stopBtn.disabled = false;
    updateStatus("Camera started. Streaming...");
    isStreaming = true;

    elements.videoEl.onloadedmetadata = () => {
      elements.canvasEl.width = elements.videoEl.videoWidth;
      elements.canvasEl.height = elements.videoEl.videoHeight;
      startStreaming();
    };
  } catch (err) {
    console.error(err);
    updateStatus("Failed to access camera.");
  }
}

function stopCamera() {
  isStreaming = false;
  if (captureInterval) {
    clearInterval(captureInterval);
    captureInterval = null;
  }

  if (mediaStream) {
    mediaStream.getTracks().forEach(track => track.stop());
    mediaStream = null;
  }

  elements.videoEl.srcObject = null;
  elements.stage.style.display = 'none';

  elements.startBtn.disabled = false;
  elements.stopBtn.disabled = true;
  updateStatus("Camera stopped.");
}

async function sendFrame(blob) {
  const res = await fetch(STREAM_URL, {
    method: "POST",
    headers: { "Content-Type": "image/jpeg" },
    body: blob
  });

  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return await res.json();
}

function startStreaming() {
  const ctx = elements.canvasEl.getContext('2d');

  captureInterval = setInterval(async () => {
    if (!mediaStream || !isStreaming) return;

    ctx.drawImage(elements.videoEl, 0, 0, elements.canvasEl.width, elements.canvasEl.height);

    elements.canvasEl.toBlob(async (blob) => {
      if (!blob) return;
      try {
        const data = await sendFrame(blob);
        console.log("Response:", data);
        if (data.attendance && Object.keys(data.attendance).length > 0) {
          attendanceList.push(data.attendance);
          updateTable();
        }
      } catch (e) {
        console.error("Stream error:", e);
        updateStatus("Streaming error (check backend).");
      }
    }, 'image/jpeg', 0.8);
  }, CAPTURE_INTERVAL);
}

elements.startBtn.addEventListener('click', startCamera);
elements.stopBtn.addEventListener('click', stopCamera);


})();