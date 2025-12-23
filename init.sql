CREATE TABLE fitness_tracker_data (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL,
    calories NUMERIC(8,2) NOT NULL,
    steps INTEGER NOT NULL,
    heart_rate INTEGER NOT NULL,
    activity_type VARCHAR(20) NOT NULL
);