BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "goal_planner" (
	"goal"	TEXT NOT NULL UNIQUE,
	"due_date"	TEXT NOT NULL UNIQUE,
	"description"	TEXT UNIQUE,
	"goal_id"	INTEGER,
	"user_id"	INTEGER NOT NULL UNIQUE,
	PRIMARY KEY("goal_id" AUTOINCREMENT),
	FOREIGN KEY("user_id") REFERENCES "users"("id")
);
CREATE TABLE IF NOT EXISTS "habit_builder" (
	"habit_id"	INTEGER,
	"description"	TEXT NOT NULL UNIQUE,
	"habit_name"	TEXT NOT NULL UNIQUE,
	"user_id"	INTEGER NOT NULL UNIQUE,
	PRIMARY KEY("habit_id" AUTOINCREMENT),
	FOREIGN KEY("user_id") REFERENCES "users"("id")
);
CREATE TABLE IF NOT EXISTS "pomodoro_timer" (
	"task_id"	INTEGER,
	"task"	TEXT NOT NULL UNIQUE,
	"start_time"	TEXT NOT NULL,
	"end_time"	TEXT NOT NULL,
	"duration"	INTEGER NOT NULL,
	"completed"	INTEGER NOT NULL DEFAULT 1,
	PRIMARY KEY("task_id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "users" (
	"id"	INTEGER,
	"username"	INTEGER NOT NULL UNIQUE,
	"email"	TEXT UNIQUE,
	"password"	TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
INSERT INTO "users" VALUES (1,'safwan ','ilovearif@yahoo.com','123abc');
COMMIT;
