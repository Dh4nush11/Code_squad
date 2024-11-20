-- Table for storing marks assigned by mentors
CREATE TABLE report_marks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    report_id INT NOT NULL,
    marks INT CHECK(marks BETWEEN 0 AND 100),
    submitted_by INT NOT NULL, -- Mentor ID
    submission_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (report_id) REFERENCES intern_reports(id),
    FOREIGN KEY (submitted_by) REFERENCES users(id)
);

-- Table for intern records
CREATE TABLE interns (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    contact_number VARCHAR(15),
    city VARCHAR(50),
    assigned_mentor INT,
    FOREIGN KEY (assigned_mentor) REFERENCES users(id)
);

-- Table for storing locations of interns
CREATE TABLE intern_locations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    intern_id INT NOT NULL,
    latitude DECIMAL(10, 8) NOT NULL,
    longitude DECIMAL(11, 8) NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (intern_id) REFERENCES interns(id)
);
