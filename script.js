base_url = "http://127.0.0.1:5000";

function getTask() {
    const url = "http://127.0.0.1:5000/recent";
    fetch(url)
    .then(response => response.json())  
    .then(json => {
        document.getElementById("ehp").innerHTML = JSON.stringify(json)
    })
}

function formatLastWeeksTasks(payloadJSON) {
    tasks = payloadJSON['last_weeks_tasks'];
    let thisWeeksTasksContainer = document.getElementById("this-weeks-tasks-container");
    for (let i = 0; i < tasks.length; i++) {
        let newTaskContainer = document.createElement("div");
        
        let newDate = document.createElement("div");
        let newWeekday = document.createElement("div");
        let newTaskContent = document.createElement("div");
        newDate.innerHTML = tasks[i]['date'];
        newWeekday.innerHTML = tasks[i]['weekday'];
        newTaskContent.innerHTML = tasks[i]['task_content'];

        newTaskContainer.appendChild(newDate);
        newTaskContainer.appendChild(newWeekday);
        newTaskContainer.appendChild(newTaskContent);

        thisWeeksTasksContainer.appendChild(newTaskContainer);
    }
}

function getLastWeeksTasks() {
    const url = base_url + "/last_week"
    console.log(url);
    console.log("getLastWeeksTasks hit?");
    fetch(url)
    .then(response => response.json())
    .then(json => {
        formatLastWeeksTasks(json)
    })
}