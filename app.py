from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

students = []


def get_dashboard_data():
    total_students = len(students)
    active_students = sum(1 for s in students if str(s.get('status', 'Active')).lower() == 'active')
    inactive_students = sum(1 for s in students if str(s.get('status', 'Active')).lower() == 'inactive')
    graduated_students = sum(1 for s in students if str(s.get('status', 'Active')).lower() == 'graduated')
    suspended_students = sum(1 for s in students if str(s.get('status', 'Active')).lower() == 'suspended')

    male_students = sum(1 for s in students if str(s.get('gender', '')).lower() == 'male')
    female_students = sum(1 for s in students if str(s.get('gender', '')).lower() == 'female')

    courses = {}
    for student in students:
        course = student.get('course', 'Unspecified').strip()
        if course:
            courses[course] = courses.get(course, 0) + 1

    top_courses = sorted(courses.items(), key=lambda item: item[1], reverse=True)[:5]
    recent_students = students[-5:][::-1]

    return {
        'total_students': total_students,
        'active_students': active_students,
        'inactive_students': inactive_students,
        'graduated_students': graduated_students,
        'suspended_students': suspended_students,
        'male_students': male_students,
        'female_students': female_students,
        'top_courses': top_courses,
        'recent_students': recent_students,
    }


@app.route('/dashboard')
def dashboard():
    stats = get_dashboard_data()

    return render_template_string('''
    <!doctype html>
    <html>
    <head>
        <title>Admin Dashboard</title>
        <style>
            :root {
                --bg: #f3f7fb;
                --panel: #ffffff;
                --primary: #1d4ed8;
                --primary-soft: #dbeafe;
                --text: #10223b;
                --muted: #62748b;
                --success: #10b981;
                --warning: #f59e0b;
                --danger: #ef4444;
                --border: #e2e8f0;
                --shadow: 0 14px 35px rgba(15, 23, 42, 0.08);
            }
            * { box-sizing: border-box; }
            body {
                margin: 0;
                font-family: Arial, sans-serif;
                background: linear-gradient(135deg, #eff6ff, #f8fafc 45%, #eef2ff);
                color: var(--text);
            }
            .topbar {
                background: #0f172a;
                color: #fff;
                padding: 18px 40px;
                display: flex;
                align-items: center;
                justify-content: space-between;
                box-shadow: 0 6px 24px rgba(15, 23, 42, 0.12);
            }
            .brand {
                font-size: 1.5rem;
                font-weight: 700;
                letter-spacing: 0.5px;
            }
            .nav-links {
                display: flex;
                gap: 12px;
                align-items: center;
            }
            .nav-links a {
                color: #dfe8f5;
                text-decoration: none;
                padding: 8px 14px;
                border-radius: 8px;
                transition: 0.2s ease;
            }
            .nav-links a:hover {
                background: rgba(255,255,255,0.08);
            }
            .container {
                max-width: 1280px;
                margin: 30px auto;
                padding: 0 20px 40px;
            }
            .hero {
                background: linear-gradient(120deg, #1d4ed8, #0f172a);
                color: white;
                padding: 32px 28px;
                border-radius: 20px;
                margin-bottom: 25px;
                box-shadow: var(--shadow);
            }
            .hero h1 {
                margin: 0 0 10px;
                font-size: 2.2rem;
            }
            .hero p {
                margin: 0;
                color: rgba(255,255,255,0.8);
                font-size: 1rem;
            }
            .stats-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 18px;
                margin-bottom: 30px;
            }
            .stat-card {
                background: var(--panel);
                border: 1px solid var(--border);
                border-radius: 16px;
                padding: 22px 20px;
                box-shadow: var(--shadow);
            }
            .stat-label {
                color: var(--muted);
                font-size: 0.9rem;
                margin-bottom: 8px;
                text-transform: uppercase;
                letter-spacing: 0.06em;
            }
            .stat-value {
                font-size: 2rem;
                font-weight: 700;
                margin: 0;
            }
            .stat-value.success { color: var(--success); }
            .stat-value.warning { color: var(--warning); }
            .stat-value.primary { color: var(--primary); }
            .stat-value.danger { color: var(--danger); }
            .layout {
                display: grid;
                grid-template-columns: 1.2fr 0.8fr;
                gap: 22px;
            }
            .panel {
                background: var(--panel);
                border: 1px solid var(--border);
                border-radius: 18px;
                padding: 22px;
                box-shadow: var(--shadow);
            }
            .panel h2 {
                margin: 0 0 18px;
                font-size: 1.2rem;
            }
            .list {
                list-style: none;
                padding: 0;
                margin: 0;
            }
            .list li {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 14px 0;
                border-bottom: 1px solid var(--border);
            }
            .list li:last-child { border-bottom: none; }
            .badge {
                display: inline-block;
                padding: 6px 10px;
                border-radius: 999px;
                font-size: 0.78rem;
                font-weight: 700;
                background: var(--primary-soft);
                color: var(--primary);
            }
            table {
                width: 100%;
                border-collapse: collapse;
                margin-top: 8px;
            }
            th, td {
                text-align: left;
                padding: 12px 8px;
                border-bottom: 1px solid var(--border);
            }
            th {
                color: var(--muted);
                font-size: 0.8rem;
                text-transform: uppercase;
                letter-spacing: 0.05em;
            }
            .status-pill {
                display: inline-block;
                padding: 5px 10px;
                border-radius: 999px;
                font-size: 0.72rem;
                font-weight: 700;
                background: #ecfeff;
                color: #0f766e;
            }
            .status-pill.inactive { background: #fef3c7; color: #b45309; }
            .status-pill.graduated { background: #e0e7ff; color: #3730a3; }
            .status-pill.suspended { background: #fee2e2; color: #b91c1c; }
            .button {
                display: inline-block;
                padding: 10px 16px;
                background: var(--primary);
                color: #fff;
                border-radius: 10px;
                text-decoration: none;
                margin-top: 14px;
                font-weight: 600;
            }
            @media (max-width: 820px) {
                .layout { grid-template-columns: 1fr; }
                .topbar { padding: 16px 18px; flex-direction: column; gap: 12px; }
                .nav-links { flex-wrap: wrap; justify-content: center; }
            }
        </style>
    </head>
    <body>
        <div class="topbar">
            <div class="brand">StudentHub Admin</div>
            <div class="nav-links">
                <a href="{{ url_for('dashboard') }}">Dashboard</a>
                <a href="{{ url_for('home') }}">Student Management</a>
            </div>
        </div>

        <div class="container">
            <div class="hero">
                <h1>Student Administration Dashboard</h1>
                <p>Track registrations, monitor status, and manage your student records in one place.</p>
            </div>

            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-label">Total Students</div>
                    <p class="stat-value primary">{{ total_students }}</p>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Active</div>
                    <p class="stat-value success">{{ active_students }}</p>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Inactive</div>
                    <p class="stat-value warning">{{ inactive_students }}</p>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Graduated</div>
                    <p class="stat-value primary">{{ graduated_students }}</p>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Suspended</div>
                    <p class="stat-value danger">{{ suspended_students }}</p>
                </div>
            </div>

            <div class="layout">
                <div class="panel">
                    <h2>Recent Student Records</h2>
                    <table>
                        <thead>
                            <tr>
                                <th>Name</th>
                                <th>ID</th>
                                <th>Course</th>
                                <th>Status</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for student in recent_students %}
                            <tr>
                                <td>{{ student.name }}</td>
                                <td>{{ student.student_id }}</td>
                                <td>{{ student.course }}</td>
                                <td>
                                    <span class="status-pill {% if student.status|lower == 'inactive' %}inactive{% elif student.status|lower == 'graduated' %}graduated{% elif student.status|lower == 'suspended' %}suspended{% endif %}">
                                        {{ student.status }}
                                    </span>
                                </td>
                            </tr>
                            {% else %}
                            <tr>
                                <td colspan="4">No students registered yet.</td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                    <a class="button" href="{{ url_for('home') }}">Manage Students</a>
                </div>

                <div class="panel">
                    <h2>Enrollment Overview</h2>
                    <ul class="list">
                        <li><span>Male Students</span><span class="badge">{{ male_students }}</span></li>
                        <li><span>Female Students</span><span class="badge">{{ female_students }}</span></li>
                        <li><span>Active</span><span class="badge">{{ active_students }}</span></li>
                        <li><span>Inactive</span><span class="badge">{{ inactive_students }}</span></li>
                    </ul>

                    <h2 style="margin-top: 24px;">Top Courses</h2>
                    <ul class="list">
                        {% for course, count in top_courses %}
                        <li><span>{{ course }}</span><span class="badge">{{ count }}</span></li>
                        {% else %}
                        <li><span>No course data yet</span><span class="badge">0</span></li>
                        {% endfor %}
                    </ul>
                </div>
            </div>
        </div>
    </body>
    </html>
    ''', **stats)


@app.route('/', methods=['GET', 'POST'])
def home():
    search = request.args.get('search', '').strip().lower()

    if request.method == 'POST':
        student = {
            'id': len(students) + 1,
            'name': request.form.get('name', ''),
            'student_id': request.form.get('student_id', ''),
            'email': request.form.get('email', ''),
            'phone': request.form.get('phone', ''),
            'course': request.form.get('course', ''),
            'department': request.form.get('department', ''),
            'year': request.form.get('year', ''),
            'semester': request.form.get('semester', ''),
            'dob': request.form.get('dob', ''),
            'gender': request.form.get('gender', ''),
            'nationality': request.form.get('nationality', ''),
            'religion': request.form.get('religion', ''),
            'address': request.form.get('address', ''),
            'guardian_name': request.form.get('guardian_name', ''),
            'guardian_phone': request.form.get('guardian_phone', ''),
            'emergency_contact': request.form.get('emergency_contact', ''),
            'cgpa': request.form.get('cgpa', ''),
            'status': request.form.get('status', 'Active'),
            'admission_date': request.form.get('admission_date', '')
        }
        students.append(student)
        return redirect(url_for('home'))

    filtered_students = []
    if search:
        for student in students:
            text = ' '.join([
                student.get('name', ''),
                student.get('student_id', ''),
                student.get('email', ''),
                student.get('course', ''),
                student.get('department', '')
            ]).lower()
            if search in text:
                filtered_students.append(student)
    else:
        filtered_students = students

    return render_template_string('''
    <!doctype html>
    <html>
    <head>
        <title>Student Management System</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 30px; background: #f4f4f4; }
            .container { max-width: 1200px; margin: auto; }
            .form-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; }
            .card { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
            label { display: block; margin-bottom: 5px; font-weight: bold; }
            input, select, textarea { width: 100%; padding: 10px; margin-bottom: 10px; border: 1px solid #ccc; border-radius: 5px; }
            button { background: #007bff; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; }
            .search-box { display: flex; gap: 10px; align-items: center; margin-bottom: 20px; }
            .search-box input { margin-bottom: 0; }
            .delete-btn { background: #dc3545; color: white; text-decoration: none; padding: 7px 12px; border-radius: 5px; }
            table { width: 100%; border-collapse: collapse; margin-top: 20px; }
            th, td { border: 1px solid #ddd; padding: 10px; text-align: left; }
            th { background: #007bff; color: white; }
        </style>
    </head>
    <body>
        <div class="topbar" style="background: #0f172a; color: white; padding: 18px 32px; display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px;">
            <div style="font-size: 1.5rem; font-weight: 700;">StudentHub</div>
            <div style="display: flex; gap: 12px; align-items: center;">
                <a href="{{ url_for('dashboard') }}" style="color: white; text-decoration: none; padding: 8px 14px; border-radius: 8px; background: rgba(255,255,255,0.08);">Dashboard</a>
                <a href="{{ url_for('home') }}" style="color: white; text-decoration: none; padding: 8px 14px; border-radius: 8px; background: rgba(255,255,255,0.08);">Manage Students</a>
            </div>
        </div>

        <div class="container">
            <h1>Student Management System</h1>

            <div class="card">
                <h2>Add Student</h2>
                <form method="POST">
                    <div class="form-grid">
                        <div>
                            <label>Full Name</label>
                            <input type="text" name="name" required>
                        </div>
                        <div>
                            <label>Student ID</label>
                            <input type="text" name="student_id" required>
                        </div>
                        <div>
                            <label>Email</label>
                            <input type="email" name="email" required>
                        </div>
                        <div>
                            <label>Phone</label>
                            <input type="text" name="phone" required>
                        </div>
                        <div>
                            <label>Course</label>
                            <input type="text" name="course" required>
                        </div>
                        <div>
                            <label>Department</label>
                            <input type="text" name="department" required>
                        </div>
                        <div>
                            <label>Year</label>
                            <input type="text" name="year" required>
                        </div>
                        <div>
                            <label>Semester</label>
                            <input type="text" name="semester" required>
                        </div>
                        <div>
                            <label>Date of Birth</label>
                            <input type="date" name="dob" required>
                        </div>
                        <div>
                            <label>Gender</label>
                            <select name="gender">
                                <option value="Male">Male</option>
                                <option value="Female">Female</option>
                                <option value="Other">Other</option>
                            </select>
                        </div>
                        <div>
                            <label>Nationality</label>
                            <input type="text" name="nationality">
                        </div>
                        <div>
                            <label>Religion</label>
                            <input type="text" name="religion">
                        </div>
                        <div>
                            <label>Guardian Name</label>
                            <input type="text" name="guardian_name">
                        </div>
                        <div>
                            <label>Guardian Phone</label>
                            <input type="text" name="guardian_phone">
                        </div>
                        <div>
                            <label>Emergency Contact</label>
                            <input type="text" name="emergency_contact">
                        </div>
                        <div>
                            <label>CGPA</label>
                            <input type="text" name="cgpa">
                        </div>
                        <div>
                            <label>Status</label>
                            <select name="status">
                                <option value="Active">Active</option>
                                <option value="Inactive">Inactive</option>
                                <option value="Graduated">Graduated</option>
                                <option value="Suspended">Suspended</option>
                            </select>
                        </div>
                        <div>
                            <label>Admission Date</label>
                            <input type="date" name="admission_date">
                        </div>
                        <div style="grid-column: 1 / -1;">
                            <label>Address</label>
                            <textarea name="address" rows="3" required></textarea>
                        </div>
                    </div>

                    <button type="submit">Add Student</button>
                </form>
            </div>

            <div class="card">
                <h2>Student List</h2>

                <form method="GET" class="search-box">
                    <input type="text" name="search" value="{{ request.args.get('search', '') }}" placeholder="Search by name, ID, email or course">
                    <button type="submit">Search</button>
                    <a href="{{ url_for('home') }}" style="text-decoration: none; color: #007bff;">Clear</a>
                </form>

                {% if filtered_students %}
                <table>
                    <thead>
                        <tr>
                            <th>Name</th>
                            <th>ID</th>
                            <th>Email</th>
                            <th>Phone</th>
                            <th>Course</th>
                            <th>Department</th>
                            <th>Year</th>
                            <th>Semester</th>
                            <th>Gender</th>
                            <th>DOB</th>
                            <th>Nationality</th>
                            <th>Religion</th>
                            <th>Guardian</th>
                            <th>Emergency</th>
                            <th>CGPA</th>
                            <th>Status</th>
                            <th>Admission</th>
                            <th>Address</th>
                            <th>Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for s in filtered_students %}
                        <tr>
                            <td>{{ s.name }}</td>
                            <td>{{ s.student_id }}</td>
                            <td>{{ s.email }}</td>
                            <td>{{ s.phone }}</td>
                            <td>{{ s.course }}</td>
                            <td>{{ s.department }}</td>
                            <td>{{ s.year }}</td>
                            <td>{{ s.semester }}</td>
                            <td>{{ s.gender }}</td>
                            <td>{{ s.dob }}</td>
                            <td>{{ s.nationality }}</td>
                            <td>{{ s.religion }}</td>
                            <td>{{ s.guardian_name }} / {{ s.guardian_phone }}</td>
                            <td>{{ s.emergency_contact }}</td>
                            <td>{{ s.cgpa }}</td>
                            <td>{{ s.status }}</td>
                            <td>{{ s.admission_date }}</td>
                            <td>{{ s.address }}</td>
                            <td><a class="delete-btn" href="{{ url_for('delete_student', student_id=s.id) }}" onclick="return confirm('Delete this student?')">Delete</a></td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
                {% else %}
                <p>No matching students found.</p>
                {% endif %}
            </div>
        </div>
    </body>
    </html>
    ''', filtered_students=filtered_students, request=request)

@app.route('/delete/<int:student_id>')
def delete_student(student_id):
    for index, student in enumerate(students):
        if student.get('id') == student_id:
            del students[index]
            break
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)