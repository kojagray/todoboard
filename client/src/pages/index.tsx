import React, { useEffect, useState } from 'react';
import 'bootstrap/dist/css/bootstrap.css';
import lastWeek from "../styles/lastWeek.module.css"
import LastWeekContainer from './LastWeekContainer';

function dayCard(cardHeader: String, cardContents: String[]) {
  return (
    <div className="card">
      <div className="card-block">
        <h3 className="card-title">{cardHeader}</h3>
        {
          cardContents.map((content) => (
            <p>{content}</p>)
          )}
      </div>
    </div>
  )
}

function index() {

  // useEffect(() => {
  //   fetch("http://localhost:5000/last_weeks_tasks")
  //   .then((response) => response.json())
  //   .then((data) => {
  //       console.log(data);
  //   });
  //   }, []);

  return (
    <>
      <div className={lastWeek.row}>
        {LastWeekContainer()}
      </div>
      <button>
        Update Tasks
      </button>
    </>
  );
}

export default index;
