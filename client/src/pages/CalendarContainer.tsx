import React from 'react';
import Calendar from 'react-github-contribution-calendar';

function getCurrentDate() {
  let t = new Date();
  let dateString = `${t.getFullYear()}-${t.getMonth()}-${t.getDate()}`
  
  return dateString;
}

function CalendarContainer() {
    var values = {
        '2023-06-23': 1,
        '2023-06-26': 2,
        '2023-06-27': 3,
        '2023-06-28': 4,
        '2023-06-29': 4
      };
    var until = getCurrentDate();
    var panelAttributes = { 'rx': 0, 'ry': 0 };
    var weekLabelAttributes = {
    'rotate': 0
    };
    var monthLabelAttributes = {
    'style': {
        'text-decoration': 'underline',
        'font-size': 10,
        'alignment-baseline': 'central',
        'fill': '#000000'
    }
    };
  getCurrentDate();
  return (
    <Calendar 
      values={values} 
      until={until}     
      panelAttributes={panelAttributes}
      weekLabelAttributes={weekLabelAttributes}
      monthLabelAttributes={monthLabelAttributes}
    />
  )
}

export default CalendarContainer
