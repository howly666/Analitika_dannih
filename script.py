import psycopg2
import time
from datetime import datetime
import random
from dotenv import load_dotenv
import os

load_dotenv()

dbConfig = {
    "dbname": os.getenv("dbName"),
    "user": os.getenv("dbUser"),
    "password": os.getenv("dbPassword"),
    "host": os.getenv("dbHost"),
    "port": os.getenv("dbPort"),
}

class FitnessTrackerSimulator:
    ACTIVITY_TYPES = ["resting", "walking", "running", "cycling"]

    def __init__(self):
        self.currentSteps = 0
        self.currentCalories = 0
        self.currentHeartRate = 65  
        self.currentActivity = "resting"

    def updateActivity(self):
        if random.random() < 0.1: 
            self.currentActivity = random.choice(self.ACTIVITY_TYPES)

        if self.currentActivity == "resting":
            stepsIncrement = random.randint(0, 2)
            calorieBurn = random.uniform(0.0, 0.5)
            heartRateChange = random.uniform(-1, 1)
            baseHeartRate = 60
        elif self.currentActivity == "walking":
            stepsIncrement = random.randint(50, 100)
            calorieBurn = random.uniform(0.3, 0.8)
            heartRateChange = random.uniform(0, 3)
            baseHeartRate = 75
        elif self.currentActivity == "running":
            stepsIncrement = random.randint(120, 200)
            calorieBurn = random.uniform(0.8, 1.5)
            heartRateChange = random.uniform(2, 6)
            baseHeartRate = 110
        elif self.currentActivity == "cycling":
            stepsIncrement = random.randint(0, 10) 
            calorieBurn = random.uniform(0.7, 1.3)
            heartRateChange = random.uniform(1, 5)
            baseHeartRate = 100

        self.currentSteps += stepsIncrement
        self.currentCalories += calorieBurn

        self.currentHeartRate = baseHeartRate + heartRateChange
        self.currentHeartRate = max(50, min(180, self.currentHeartRate))  

        return {
            "calories": round(self.currentCalories, 2),
            "steps": self.currentSteps,
            "heartRate": int(self.currentHeartRate),
            "activityType": self.currentActivity,
        }


def insertFitnessDataToDb(data):
    try:
        conn = psycopg2.connect(**dbConfig)
        cur = conn.cursor()

        insertQuery = """
        INSERT INTO fitness_tracker_data 
        (timestamp, calories, steps, heart_rate, activity_type)
        VALUES (%s, %s, %s, %s, %s);
        """
        cur.execute(
            insertQuery,
            (
                datetime.now(),
                data["calories"],
                data["steps"],
                data["heartRate"],
                data["activityType"],
            ),
        )

        conn.commit()
        print(
            f"Запись добавлена: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}, "
            f"Калории={data['calories']}, Шаги={data['steps']}, "
            f"Пульс={data['heartRate']} BPM, Активность={data['activityType']}"
        )

    except psycopg2.Error as e:
        print(f"Ошибка при работе с БД: {e}")
    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()


def main():
    simulator = FitnessTrackerSimulator()
    print("Фитнес-трекер запущен. Отправка данных каждую секунду...")
    while True:
        fitnessData = simulator.updateActivity()
        insertFitnessDataToDb(fitnessData)
        time.sleep(1)


if __name__ == "__main__":
    main()