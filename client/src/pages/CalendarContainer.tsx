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