document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('plant-factors-form');
    const closeButton = document.getElementById('close-planting-ideas');

    form.addEventListener('submit', function (event) {
        event.preventDefault();

        const formData = new FormData(form);
        fetch('/recommend_by_criteria', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            console.log(data); // Handle data here (e.g., display suggestions)
            alert('Suggestions: ' + data.recommendations);
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });

    closeButton.addEventListener('click', function () {
        // Logic to close or hide the form
        document.getElementById('planting-ideas-page').style.display = 'none';
    });
});
