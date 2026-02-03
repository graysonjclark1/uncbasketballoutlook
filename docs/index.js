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

function getOrdinalSuffix(day) {
  if (day >= 11 && day <= 13) return 'th';

  switch (day % 10) {
    case 1: return 'st';
    case 2: return 'nd';
    case 3: return 'rd';
    default: return 'th';
  }
}


function updateTime() {
            const today = new Date();
            const monthFormatter = new Intl.DateTimeFormat('en-US', { month: 'long' });
            const yearFormatter  = new Intl.DateTimeFormat('en-US', { year: 'numeric' });
            const day = today.getDate();
            const suffix = getOrdinalSuffix(day);
            const formattedDate =`${monthFormatter.format(today)} ${day}${suffix}, ${yearFormatter.format(today)}`;
            document.getElementById('title').textContent += formattedDate;
}

updateTime();