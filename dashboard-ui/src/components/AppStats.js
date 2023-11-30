import React, { useEffect, useState } from 'react'
import '../App.css';

export default function AppStats() {
    const [isLoaded, setIsLoaded] = useState(false);
    const [stats, setStats] = useState({});
    const [error, setError] = useState(null)

	const getStats = () => {
	
        fetch(`http://ec2-52-10-1-233.us-west-2.compute.amazonaws.com/processing/stats`)
            .then(res => res.json())
            .then((result)=>{
				console.log("Received Stats")
                setStats(result);
                setIsLoaded(true);
            },(error) =>{
                setError(error)
                setIsLoaded(true);
            })
    }
    useEffect(() => {
		const interval = setInterval(() => getStats(), 2000); // Update every 2 seconds
		return() => clearInterval(interval);
    }, [getStats]);

    if (error){
        return (<div className={"error"}>Error found when fetching from API</div>)
    } else if (isLoaded === false){
        return(<div>Loading...</div>)
    } else if (isLoaded === true){
        return(
            <div>
                <h1>Latest Stats</h1>
                <table className={"StatsTable"}>
					<tbody>
						<tr>
							<th>User Weight</th>
							<th>Meal Calories</th>
						</tr>
						<tr>
							<td># UW: {stats['total_meal_calorie_entries']}</td>
							<td># MC: {stats['total_user_weight_entries']}</td>
						</tr>
						<tr>
							<td colspan="2">Highest Meal Calories Recorded: {stats['highest_meal_calorie']}</td>
						</tr>
						<tr>
							<td colspan="2">Lowest User Weight Recorded In Lbs: {stats['lowest_user_weight']}</td>
						</tr>
					</tbody>
                </table>
                <h3>Last Updated: {stats['last_updated_stats']}</h3>

            </div>
        )
    }
}
