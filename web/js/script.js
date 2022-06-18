function getDataFromLed(id) {
    const btn = document.getElementById(id);
    if (btn.className === 'button') {
        sendCommandToServer(id)
    }
}


function sendCommandToServer(command) {
    fetch("http://127.0.0.1:5000/result", {
        method: 'POST',
        mode: 'cors',
        cache: 'no-cache',
        credentials: 'same-origin',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(command)
    }).then(function (response) {
        if (response.status !== 200) {
            console.log('Error');
        } else console.log(response)
    })

}

