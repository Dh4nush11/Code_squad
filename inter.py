@app.route('/submit-marks', methods=['POST'])
@login_required
def submit_marks():
    if current_user.role != 'teacher':  # Ensure only mentors can submit marks
        return jsonify({"error": "Unauthorized access"}), 403

    data = request.json
    try:
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()
        query = """
            INSERT INTO report_marks (report_id, marks, submitted_by, submission_date)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE marks = VALUES(marks), submission_date = VALUES(submission_date)
        """
        cursor.execute(query, (
            data['report_id'],
            data['marks'],
            current_user.id,
            datetime.now()
        ))
        db.commit()
        return jsonify({"message": "Marks submitted successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        db.close()
@app.route('/view-progress', methods=['GET'])
@login_required
def view_progress():
    if current_user.role != 'programmer':  # Ensure only coordinators can view progress
        return jsonify({"error": "Unauthorized access"}), 403

    try:
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor(dictionary=True)
        query = """
            SELECT ir.id, ir.intern_id, ir.report_type, ir.report_text, ir.submission_date,
                   rm.marks, rm.submission_date AS marks_submission_date
            FROM intern_reports ir
            LEFT JOIN report_marks rm ON ir.id = rm.report_id
        """
        cursor.execute(query)
        reports = cursor.fetchall()
        return jsonify(reports)
    finally:
        cursor.close()
        db.close()
@app.route('/interns', methods=['POST', 'GET', 'PUT', 'DELETE'])
@login_required
def manage_interns():
    if current_user.role != 'programmer':  # Ensure only coordinators can manage interns
        return jsonify({"error": "Unauthorized access"}), 403

    db = mysql.connector.connect(**db_config)
    cursor = db.cursor(dictionary=True)

    try:
        if request.method == 'POST':  # Create a new intern
            data = request.json
            cursor.execute("""
                INSERT INTO interns (name, email, contact_number, city, assigned_mentor)
                VALUES (%s, %s, %s, %s, %s)
            """, (data['name'], data['email'], data['contact_number'], data['city'], data['assigned_mentor']))
            db.commit()
            return jsonify({"message": "Intern added successfully"})

        elif request.method == 'GET':  # Read all interns
            cursor.execute("SELECT * FROM interns")
            interns = cursor.fetchall()
            return jsonify(interns)

        elif request.method == 'PUT':  # Update an intern record
            data = request.json
            cursor.execute("""
                UPDATE interns SET name = %s, email = %s, contact_number = %s, city = %s, assigned_mentor = %s
                WHERE id = %s
            """, (data['name'], data['email'], data['contact_number'], data['city'], data['assigned_mentor'], data['id']))
            db.commit()
            return jsonify({"message": "Intern updated successfully"})

        elif request.method == 'DELETE':  # Delete an intern
            data = request.json
            cursor.execute("DELETE FROM interns WHERE id = %s", (data['id'],))
            db.commit()
            return jsonify({"message": "Intern deleted successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        db.close()
@app.route('/submit-location', methods=['POST'])
@login_required
def submit_location():
    if current_user.role != 'teacher':  # Only mentors can submit location
        return jsonify({"error": "Unauthorized access"}), 403

    data = request.json
    try:
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO intern_locations (intern_id, latitude, longitude, timestamp)
            VALUES (%s, %s, %s, %s)
        """, (data['intern_id'], data['latitude'], data['longitude'], datetime.now()))
        db.commit()
        return jsonify({"message": "Location submitted successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        db.close()

