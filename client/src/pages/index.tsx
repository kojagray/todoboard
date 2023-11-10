import React, { useEffect, useState } from 'react';

function index() {
  let [lastWeeksTasks, updateLastWeeksTasks] = useState([]);

  useEffect(() => {
    fetch("http://localhost:8080/last_week")
    .then((response) => response.json())
    .then((data) => {
      // console.log(data);
      updateLastWeeksTasks(data['last_weeks_tasks']);
    });
  }, []);

  return (
    lastWeeksTasks.map((task) => 
      <li key={task['id']} className = "py-2">
        <p className = "content-center">{task['date']}</p>
        <p>{task['weekday']}</p>
        <p>{task['task_content']}</p>
      </li>
    )

  )
}

export default index
