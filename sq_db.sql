CREATE TABLE IF NOT EXISTS registration_of_employees (
    id integer PRIMARY KEY AUTOINCREMENT,
    userCode TEXT NOT NULL,
    usbCode TEXT NOT NULL,
    timeIn integer NOT NULL  DEFAULT (0),
    timeOut integer NOT NULL  DEFAULT (0),
    unloaded integer NOT NULL DEFAULT (0)
);