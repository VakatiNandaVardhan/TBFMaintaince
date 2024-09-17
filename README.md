
# Condition-based monitoring and maintenance system.

### Background

There are a large number of tunnel booster fans (TBF) of different capacity installed in tunnel area at underground metro stations. These IBFs have different maintenance schedules and frequency prescribed by OEM. The TBF's are not operated regularly but are tested during mock drills. The exercise of scheduled preventive maintenance of this equipment involves a large number of manpower and risk of working at height. The Condition-based maintenance in place of scheduled preventive maintenance would be very helpful in optimizing the maintenance and manpower cost involved. 
### Description: 
To optimize the maintenance and manpower cost there is a great need of developing a condition-based monitoring and maintenance system. The historical data pertaining to failures along with the symptoms, the permissible limits of different parameters. the previous maintenance records of TBF shall be fed into the Al based condition monitoring system. The Al based system shall analyze and compare this historical data with parameter obtained at the time of operation during the testing/mock drill to predict any maintenance requirement based on the condition of TBF and the system shall also alert in case of any deviation from specified values. Expected Solution: Condition-based monitoring and maintenance system which can use machine learning & behavioural analytics to predict any maintenance requirement based on the condition of a particular system.
###  Proposed solution
 • Sensor Data Collection: Sensors 
on TBFs capture operational data 
during drills, providing essential 
insights into fan condition.

 • Condition-Based Maintenance: 
The system shifts from scheduled 
maintenance to condition-based, 
ensuring maintenance is 
performed only when needed.

 • AI-Powered Alerts: The AI system 
sends alerts for deviations, 
optimizing maintenance and 
reducing manpower and 
operational risks.
### Addressing the problem

 • Efficient Data Collection: 
Sensors on TBFs gather precise 
operational data during drills, 
reducing the need for manual 
inspections.

 • Optimized Maintenance: 
Condition-based maintenance 
eliminates unnecessary routine 
checks, focusing on actual 
equipment needs.

 • Risk and Cost Reduction: The AI 
system alerts for deviations, 
minimizing manpower usage and 
safety risks, especially in high
risk environments.

### Uniqueness of the solution
 • Targeted Maintenance Approach: 
Shifting from scheduled to condition
based maintenance ensures 
resources are used only when 
necessary, reducing waste.

 • Real-Time AI Insights: The 
integration of AI provides predictive 
maintenance alerts, offering 
proactive solutions instead of 
reactive fixes.

 • Cost and Risk Efficiency: Minimizes 
operational costs and safety risks by 
optimizing manpower deployment 
and reducing high-risk 
manual inspections.


## prerequisites libraries
 Here is the single command to install all the required libraries:
for ML Part .

```bash
Copy code
pip install pandas matplotlib seaborn scikit-learn joblib
```
This will install:

pandas: For data manipulation.
matplotlib: For plotting graphs.
seaborn: For statistical graphics like heatmaps.
scikit-learn: For machine learning models and utilities.
joblib: For loading and saving models and scalers.






## Folder Contents





| File name | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `Train_KNN.py` | `python` | Trains a ML model and stores in **secret.py** |
|`secret.pkl` ||`pickle` ||Stores the Trained model and Scaling Factor| 


