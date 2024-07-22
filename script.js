document.getElementById('fetchNumbers').addEventListener('click', () => {
    const numberType = document.getElementById('numberType').value;
    
    fetch(`http://localhost:9876/numbers/${numberType}`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`Network response was not ok: ${response.statusText}`);
            }
            return response.json();
        })
        .then(data => {
            document.getElementById('windowPrevState').innerText = JSON.stringify(data.windowPrevState);
            document.getElementById('windowCurrState').innerText = JSON.stringify(data.windowCurrState);
            document.getElementById('fetchedNumbers').innerText = JSON.stringify(data.numbers);
            document.getElementById('average').innerText = data.avg.toFixed(2);
        })
        .catch(error => {
            console.error('Error fetching numbers:', error);
            alert('Failed to fetch numbers. Please try again later.');
        });
});
