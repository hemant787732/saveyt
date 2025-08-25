const form = document.getElementById('download-form');
const progressContainer = document.getElementById('progress-container');
const progressBar = document.getElementById('progress-bar');
const downloadLink = document.getElementById('download-link');
const errorMsg = document.getElementById('error-msg');

form.addEventListener('submit', function(e){
    e.preventDefault();

    const formData = new FormData(form);
    fetch("/", {method: "POST", body: formData})
    .then(response => response.text())
    .then(html => {
        const parser = new DOMParser();
        const doc = parser.parseFromString(html, 'text/html');
        const downloadId = doc.querySelector("#progress-bar") ? doc.querySelector("#progress-bar").dataset.id : null;
        const newDownloadId = doc.querySelector("[data-download-id]")?.getAttribute("data-download-id");
        startProgress(newDownloadId);
    });
});

function startProgress(downloadId){
    if(!downloadId) return;
    progressContainer.style.display = "block";
    const interval = setInterval(() => {
        fetch(`/progress/${downloadId}`)
        .then(res => res.json())
        .then(data => {
            progressBar.style.width = data.progress;
            progressBar.textContent = data.progress;
            if(data.progress === "100%" || data.progress === "error"){
                clearInterval(interval);
                if(data.progress === "100%"){
                    downloadLink.innerHTML = `<a href="/downloads/${downloadId}">Click here to save your file</a>`;
                } else {
                    errorMsg.textContent = "Download failed!";
                }
            }
        });
    }, 1000);
}
