import React, { useEffect, useState } from 'react';
import 'bootstrap/dist/css/bootstrap.css';

function LastWeekContainer() {
    let [lastWeeksTasks, updateLastWeeksTasks] = useState<any[]>([]);

    useEffect(() => {
        fetch("http://localhost:8080/last_weeks_tasks")
        .then((response) => response.json())
        .then((data) => {
            updateLastWeeksTasks( lastWeeksTasks => ({
                ...lastWeeksTasks, ...data
            }))
        });
        }, []);
          
    return (
        Object.keys(lastWeeksTasks).map((date) => 
            <div className="card">
                <div className="card-block">
                    <h3 className="card-title">{date}</h3>
                    {lastWeeksTasks[date as keyof typeof lastWeeksTasks].map((task: any) => 
                        <div className="card-text">{task.content}</div>
                    )}
                </div>
            </div>
        )
    )
}

export default LastWeekContainer;