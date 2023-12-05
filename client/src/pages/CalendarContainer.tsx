import React, { useEffect, useState } from 'react';
import Calendar from 'react-github-contribution-calendar';

type TaskCounter = Record<string, ProjectData>;

type ProjectData = {
  project_name: string;
  project_color: string;
  counter: Record<string, number>;
};

function generateCalendar(projectData: ProjectData) {
  const until = getCurrentDate();
  const panelAttributes = { rx: 6, ry: 6 };
  const weekLabelAttributes = {
    rotate: 0,
  };
  const monthLabelAttributes = {
    style: {
      fontSize: 11,
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
        panelColors={generatePanelColors(projectData.project_color)}
        weekLabelAttributes={weekLabelAttributes}
        monthLabelAttributes={monthLabelAttributes}
      />
    </div>
  );
}

function generatePanelColors(hex : string){
  const cendpt = 242 // grey #EEEEEE is 238, 238, 238
  
  const rgb = hex.slice(1)
  const r = rgb.slice(0,2)
  const g = rgb.slice(2,4)
  const b = rgb.slice(4,6)

  const rval = parseInt(r, 16)
  const gval = parseInt(g, 16)
  const bval = parseInt(b, 16)

  const newR = interpColor(rval, cendpt)
  const newG = interpColor(gval, cendpt)
  const newB = interpColor(bval, cendpt)

  // generate colors from #EEEEEE to $hex 
  let panelColors = []
  for (let i = 0; i < 5; i++) {
    let rhex = leftPadWithZeros(boundColor(newR[i]).toString(16))
    let ghex = leftPadWithZeros(boundColor(newG[i]).toString(16))
    let bhex = leftPadWithZeros(boundColor(newB[i]).toString(16)) 
    let panelColor = "#" + rhex + ghex + bhex
    panelColors.unshift(panelColor)
  }

  return panelColors
}

function interpColor(colInt : number, cendpt = 238) {
  let cslice = (cendpt - colInt) / 5
  let newCol = []
  if (colInt < cendpt) {
    for (let i = 1; i <= 5; i++) {
      newCol.push(Math.floor(colInt + i*cslice))
    }
  } else {
    for (let i = 1; i <= 5; i++){
      newCol.push(Math.floor(colInt - i*cslice))
    }
  }
  
  return newCol
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