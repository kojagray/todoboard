import React, { useEffect, useState } from 'react';
import 'bootstrap/dist/css/bootstrap.css';
import lastWeek from "../styles/lastWeek.module.css"
import LastWeekContainer from './LastWeekContainer';
import CalendarContainer from './CalendarContainer';

function updateTasks() {
  fetch("http://localhost:8080/update_tasks")
  .then((response) => {
    console.log(response.json())
    window.location.reload();
  })
}

function index() {
  return (
    <>
      <div className={lastWeek.row}>
        {LastWeekContainer()}
      </div>
      <button type="button" className="btn btn-primary btn-med" onClick={updateTasks}>
        Update Tasks
      </button>
      <CalendarContainer />
    </>
  );
}

export default index;
