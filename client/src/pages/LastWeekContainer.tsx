import React, { useEffect, useState } from 'react';
import 'bootstrap/dist/css/bootstrap.css';

function getDayOfWeek(date: string) {
    const dayOfWeek = new Date(date + " 00:00:00").getDay();
    const weekday = isNaN(dayOfWeek) ? null :
        ['Sun', 'Mon', 'Tues', 'Wed', 'Thurs', 'Fri', 'Sat'][dayOfWeek];

    return `${date} (${weekday})`
}

function LastWeekContainer() {
    let [lastWeeksTasks, updateLastWeeksTasks] = useState<any[]>([]);

    useEffect(() => {
        fetch("http://localhost:8080/last_weeks_tasks")
            .then((response) => response.json())
            .then((data) => {
                updateLastWeeksTasks(lastWeeksTasks => ({
                    ...lastWeeksTasks, ...data
                }))
            });
    }, []);

    return (
        Object.keys(lastWeeksTasks).map((date) =>
            <div className="card">
                <div className="card-block">
                    <h3 className="card-title">{getDayOfWeek(date)}</h3>
                    {lastWeeksTasks[date as keyof typeof lastWeeksTasks].map((task: any) =>
                        <li style={{backgroundColor : task.color}}>{task.content}</li>
                    )}
                </div>
            </div>
        )
    )
}

export default LastWeekContainer;