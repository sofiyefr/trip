document.addEventListener("DOMContentLoaded", () => {
    const contentDiv = document.getElementById("content");

    // Fetch data from the backend
    fetch("http://127.0.0.1:5000/api/example")
        .then(response => response.json())
        .then(data => {
            contentDiv.innerHTML = `<p>${data.message}</p>`;
        })
        .catch(error => {
            console.error("Error fetching data:", error);
            contentDiv.innerHTML = `<p>Failed to load data from the server.</p>`;
        });
});