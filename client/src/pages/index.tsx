import React, { useEffect, useState } from 'react';
import 'bootstrap/dist/css/bootstrap.css';
import lastWeek from "../styles/lastWeek.module.css"
import LastWeekContainer from './LastWeekContainer';

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
      <button onClick={updateTasks}>
        Update Tasks
      </button>
    </>
  );
}

export default index;
