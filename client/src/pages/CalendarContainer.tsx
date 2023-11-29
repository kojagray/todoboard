import React, { useEffect, useState } from 'react';
import Calendar from 'react-github-contribution-calendar';


function getCurrentDate() {
  let t = new Date();
  let dateString = `${t.getFullYear()}-${t.getMonth()}-${t.getDate()}`

  return dateString;
}




function CalendarContainer() {
  let [allTasksCounter, updateAllTasksCounter] = useState<any[]>([]);

  useEffect(() => {
    fetch("http://localhost:8080/all_tasks_date_counter")
      .then((response) => response.json())
      .then((data) => {
        updateAllTasksCounter(allTasksCounter => ({
          ...allTasksCounter, ...data
        }))
      });
  }, []);
  let until = getCurrentDate();
  let panelAttributes = { 'rx': 0, 'ry': 0 };
  let weekLabelAttributes = {
    'rotate': 0
  };
  let monthLabelAttributes = {
    'style': {
      'text-decoration': 'underline',
      'font-size': 10,
      'alignment-baseline': 'central',
      'fill': '#000000'
    }
  };
  return (
    <Calendar
      values={allTasksCounter}
      until={until}
      panelAttributes={panelAttributes}
      weekLabelAttributes={weekLabelAttributes}
      monthLabelAttributes={monthLabelAttributes}
    />
  )
}

export default CalendarContainer
