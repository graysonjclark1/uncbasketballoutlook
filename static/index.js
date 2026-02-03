async function getResult() {
    try {
        const response = await fetch("result.json");
        if (!response.ok) {
            throw new Error(`Error! Status: ${response.status} `);
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.log(error);
    }

}

getResult().then(data =>  {
    console.log(data);
    const element = document.getElementById("container")
    element.style.fontSize = '108px';
    element.style.color = '#26b0deff';
    element.style.fontFamily = 'Arial';
    element.innerHTML = JSON.stringify(data.prediction, null, 2).replace(/['"]+/g, '');
})


function updateTime() {
            const today = new Date();
            document.getElementById('title').textContent += today.toDateString();
}

updateTime();