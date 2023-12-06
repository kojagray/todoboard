import React, { useEffect, useState } from 'react';
import lastWeek from "../styles/lastWeek.module.css"

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
            <div className={lastWeek.dayCard}>
                <div className={lastWeek.dateHeader}>
                    {getDayOfWeek(date)}
                </div>
                {lastWeeksTasks[date as keyof typeof lastWeeksTasks].map((task: any) =>
                    <div style={{backgroundColor : task.color}} className={lastWeek.taskContent}>
                        {task.content}
                    </div>
                )}
            </div>
        )
    )
}

export default LastWeekContainer;