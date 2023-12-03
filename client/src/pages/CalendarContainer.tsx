import React, { useEffect, useState } from 'react';
import Calendar from 'react-github-contribution-calendar';

type TaskCounter = Record<string, ProjectData>;

type ProjectData = {
  project_name: string;
  counter: Record<string, number>;
};

function generateCalendar(projectData: ProjectData) {
  const until = getCurrentDate();
  const panelAttributes = { rx: 0, ry: 0 };
  const weekLabelAttributes = {
    rotate: 0,
  };
  const monthLabelAttributes = {
    style: {
      textDecoration: 'underline',
      fontSize: 10,
      alignmentBaseline: 'central',
      fill: '#000000',
    },
  };

  return (
    <div>
      <h1>{projectData.project_name}</h1>
      <Calendar
        values={projectData.counter}
        until={until}
        panelAttributes={panelAttributes}
        weekLabelAttributes={weekLabelAttributes}
        monthLabelAttributes={monthLabelAttributes}
      />
    </div>
  );
}

function colorSpacer(hex : string, spacer=15){
  const rgb = hex.slice(1)
  const r = rgb.slice(0,2)
  const g = rgb.slice(2,4)
  const b = rgb.slice(4,6)

  const rval = parseInt(r, 16)
  const gval = parseInt(g, 16)
  const bval = parseInt(b, 16)

  let panelColors = []
  for (let i = -2; i <= 2; i++){
    let currR = leftPadWithZeros(boundColor(rval + i*spacer).toString(16))
    let currG = leftPadWithZeros(boundColor(gval + i*spacer).toString(16))
    let currB = leftPadWithZeros(boundColor(bval + i*spacer).toString(16))

    let panelColor = "#" + currR + currG + currB
    panelColor = panelColor.toUpperCase()
    panelColors.push(panelColor)
  }

  return panelColors
}

function boundColor(colorInt : number){
  return Math.max(0, Math.min(colorInt, 255))
}

function leftPadWithZeros(hex : string){
  if (hex.length < 2){
    hex = "0" + hex
  }

  return hex
}
function getCurrentDate() {
  const t = new Date();
  const dateString = `${t.getFullYear()}-${t.getMonth() + 1}-${t.getDate()}`;

  return dateString;
}

function processProjects(allTasksCounter: TaskCounter) {
  const taskArray: JSX.Element[] = [];
  for (const [pid, data] of Object.entries(allTasksCounter)) {
    const pd: ProjectData = data as ProjectData;
    taskArray.push(generateCalendar(pd));
  }

  return taskArray;
}

function CalendarContainer() {
  const [allTasksCounter, updateAllTasksCounter] = useState<TaskCounter>({});

  useEffect(() => {
    fetch('http://localhost:8080/per_project_date_counter')
      .then((response) => response.json())
      .then((data: TaskCounter) => {
        updateAllTasksCounter((prevData) => ({ ...prevData, ...data }));
      });
  }, []);

  const calendars = processProjects(allTasksCounter);

  return <>{calendars}</>;
}

export default CalendarContainer;