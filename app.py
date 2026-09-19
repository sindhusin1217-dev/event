from flask import Flask, request, redirect, session, render_template_string
import csv
import os
import re
from datetime import datetime

app = Flask(__name__)
app.secret_key = "event_management_secret_2026"

# =========================================================
# DATABASE / CSV FILE
# =========================================================

DATA_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "registrations.csv"
)

FIELDS = ["Name", "Email", "Phone", "Event", "Date"]


def create_csv():
    """Create CSV file automatically if it does not exist."""
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=FIELDS)
            writer.writeheader()


create_csv()


# =========================================================
# READ REGISTRATIONS
# =========================================================

def read_data():
    create_csv()

    records = []

    with open(DATA_FILE, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            records.append({
                "Name": row.get("Name", ""),
                "Email": row.get("Email", ""),
                "Phone": row.get("Phone", ""),
                "Event": row.get("Event", ""),
                "Date": row.get("Date", "")
            })

    return records


# =========================================================
# SAVE REGISTRATIONS
# =========================================================

def save_data(records):

    with open(DATA_FILE, "w", newline="", encoding="utf-8") as file:

        writer = csv.DictWriter(file, fieldnames=FIELDS)

        writer.writeheader()

        for record in records:

            writer.writerow({
                "Name": record.get("Name", ""),
                "Email": record.get("Email", ""),
                "Phone": record.get("Phone", ""),
                "Event": record.get("Event", ""),
                "Date": record.get("Date", "")
            })


# =========================================================
# CSS
# =========================================================

CSS = """

* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

body {
    font-family: Arial, Helvetica, sans-serif;
    background: linear-gradient(135deg, #eef2ff, #f8fafc);
    color: #1e293b;
    min-height: 100vh;
}

/* NAVBAR */

.navbar {
    background: linear-gradient(135deg, #4f46e5, #7c3aed);
    color: white;
    padding: 18px 7%;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 5px 20px rgba(0,0,0,0.15);
}

.logo {
    font-size: 23px;
    font-weight: bold;
}

.navbar a {
    color: white;
    text-decoration: none;
    margin-left: 20px;
    font-weight: bold;
}

.navbar a:hover {
    opacity: 0.8;
}

/* CONTAINER */

.container {
    width: 90%;
    max-width: 1100px;
    margin: 40px auto;
}

/* HERO */

.hero {
    text-align: center;
    margin-bottom: 30px;
}

.hero h1 {
    font-size: 38px;
    color: #4f46e5;
    margin-bottom: 10px;
}

.hero p {
    color: #64748b;
    font-size: 17px;
}

/* CARD */

.card {
    background: white;
    border-radius: 18px;
    padding: 30px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.08);
    margin-bottom: 25px;
}

.card h2 {
    color: #4f46e5;
    margin-bottom: 20px;
}

/* FORM */

.form-group {
    margin-bottom: 18px;
}

label {
    display: block;
    font-weight: bold;
    margin-bottom: 7px;
}

input,
select {
    width: 100%;
    padding: 13px;
    border: 1px solid #cbd5e1;
    border-radius: 10px;
    font-size: 15px;
    outline: none;
}

input:focus,
select:focus {
    border-color: #4f46e5;
    box-shadow: 0 0 0 3px rgba(79,70,229,0.1);
}

/* BUTTON */

.btn {
    display: inline-block;
    border: none;
    padding: 13px 22px;
    border-radius: 10px;
    background: linear-gradient(135deg, #4f46e5, #7c3aed);
    color: white;
    font-weight: bold;
    cursor: pointer;
    text-decoration: none;
    transition: 0.2s;
}

.btn:hover {
    transform: translateY(-2px);
}

.btn-danger {
    background: #dc2626;
}

.btn-edit {
    background: #f59e0b;
}

.btn-green {
    background: #16a34a;
}

.center {
    text-align: center;
}

/* STATS */

.stats {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 18px;
    margin-bottom: 25px;
}

.stat {
    background: white;
    padding: 25px;
    border-radius: 16px;
    text-align: center;
    box-shadow: 0 8px 25px rgba(0,0,0,0.08);
}

.stat h3 {
    font-size: 30px;
    color: #4f46e5;
}

.stat p {
    margin-top: 8px;
    color: #64748b;
}

/* TABLE */

.table-container {
    overflow-x: auto;
}

table {
    width: 100%;
    border-collapse: collapse;
    background: white;
}

th {
    background: #4f46e5;
    color: white;
    padding: 14px;
    text-align: left;
}

td {
    padding: 13px;
    border-bottom: 1px solid #e2e8f0;
}

tr:hover {
    background: #f8fafc;
}

/* SEARCH */

.search-box {
    display: flex;
    gap: 10px;
    margin-bottom: 20px;
}

.search-box input {
    flex: 1;
}

/* ACTIONS */

.actions {
    display: flex;
    gap: 8px;
}

/* SUCCESS */

.success {
    text-align: center;
    padding: 50px 20px;
}

.success-icon {
    font-size: 65px;
    margin-bottom: 15px;
}

.success h1 {
    color: #16a34a;
    margin-bottom: 12px;
}

/* LOGIN */

.login-card {
    max-width: 450px;
    margin: 70px auto;
}

/* INFO */

.info {
    background: #eef2ff;
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 20px;
    color: #4338ca;
}

/* FOOTER */

.footer {
    text-align: center;
    padding: 25px;
    color: #64748b;
}

/* EMPTY */

.empty {
    text-align: center;
    padding: 35px;
    color: #64748b;
}

/* MOBILE */

@media(max-width: 800px) {

    .stats {
        grid-template-columns: repeat(2, 1fr);
    }

    .navbar {
        flex-direction: column;
        gap: 12px;
    }

    .navbar a {
        margin: 0 7px;
    }
}

@media(max-width: 500px) {

    .stats {
        grid-template-columns: 1fr;
    }

    .hero h1 {
        font-size: 28px;
    }

    .search-box {
        flex-direction: column;
    }

    .actions {
        flex-direction: column;
    }
}

"""


# =========================================================
# HOME PAGE
# =========================================================

@app.route("/")
def home():

    return render_template_string("""
<!DOCTYPE html>

<html>

<head>

    <title>Event Registration System</title>

    <style>
        {{ css }}
    </style>

</head>

<body>

<nav class="navbar">

    <div class="logo">
        🎉 Event Registration System
    </div>

    <div>

        <a href="/">
            Home
        </a>

        <a href="/login">
            Admin
        </a>

    </div>

</nav>


<div class="container">

    <div class="hero">

        <h1>
            🎓 College Event Registration
        </h1>

        <p>
            Register for workshops, seminars, hackathons and college events.
        </p>

    </div>


    <div class="card">

        <h2>
            📝 Student Registration
        </h2>


        <form
            action="/register"
            method="POST"
            onsubmit="return validateForm()"
        >


            <div class="form-group">

                <label>
                    Student Name
                </label>

                <input
                    type="text"
                    name="name"
                    id="name"
                    placeholder="Enter your full name"
                    required
                >

            </div>


            <div class="form-group">

                <label>
                    Email Address
                </label>

                <input
                    type="email"
                    name="email"
                    id="email"
                    placeholder="example@gmail.com"
                    required
                >

            </div>


            <div class="form-group">

                <label>
                    Phone Number
                </label>

                <input
                    type="text"
                    name="phone"
                    id="phone"
                    maxlength="10"
                    placeholder="Enter 10 digit phone number"
                    required
                >

            </div>


            <div class="form-group">

                <label>
                    Select Event
                </label>

                <select
                    name="event"
                    required
                >

                    <option value="">
                        -- Select Event --
                    </option>

                    <option value="Workshop">
                        💻 Workshop
                    </option>

                    <option value="Seminar">
                        🎤 Seminar
                    </option>

                    <option value="Hackathon">
                        👨‍💻 Hackathon
                    </option>

                    <option value="Cultural Fest">
                        🎭 Cultural Fest
                    </option>

                    <option value="Technical Fest">
                        ⚙️ Technical Fest
                    </option>

                </select>

            </div>


            <button
                class="btn"
                type="submit"
            >
                🚀 Register Now
            </button>


        </form>

    </div>

</div>


<div class="footer">

    Event Registration Management System © 2026

</div>


<script>

function validateForm() {

    let name =
        document.getElementById("name").value.trim();

    let email =
        document.getElementById("email").value.trim();

    let phone =
        document.getElementById("phone").value.trim();


    /* Correct name validation */

    let namePattern =
        /^[A-Za-z ]+$/;


    /* Correct email validation */

    let emailPattern =
        /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/;


    /* Correct 10 digit phone validation */

    let phonePattern =
        /^[0-9]{10}$/;


    if (!namePattern.test(name)) {

        alert("Please enter a valid name.");

        return false;
    }


    if (!emailPattern.test(email)) {

        alert("Please enter a valid email address.");

        return false;
    }


    if (!phonePattern.test(phone)) {

        alert(
            "Phone number must contain exactly 10 digits."
        );

        return false;
    }


    return true;

}

</script>


</body>

</html>

""", css=CSS)


# =========================================================
# REGISTER STUDENT
# =========================================================

@app.route("/register", methods=["POST"])
def register():

    name = request.form.get("name", "").strip()

    email = request.form.get("email", "").strip()

    phone = request.form.get("phone", "").strip()

    event = request.form.get("event", "").strip()


    # -------------------------
    # SERVER SIDE VALIDATION
    # -------------------------

    if not re.match(r"^[A-Za-z ]+$", name):

        return """
        <h2>Invalid Name</h2>
        <a href="/">Go Back</a>
        """


    # IMPORTANT:
    # Correct email pattern

    if not re.match(
        r"^[^\s@]+@[^\s@]+\.[^\s@]+$",
        email
    ):

        return """
        <h2>Invalid Email</h2>
        <p>Please enter a valid email address.</p>
        <br>
        <a href="/">Go Back</a>
        """


    if not re.match(
        r"^[0-9]{10}$",
        phone
    ):

        return """
        <h2>Invalid Phone Number</h2>
        <p>Phone number must contain exactly 10 digits.</p>
        <br>
        <a href="/">Go Back</a>
        """


    if event == "":

        return """
        <h2>Please select an event.</h2>
        <a href="/">Go Back</a>
        """


    # -------------------------
    # READ EXISTING DATA
    # -------------------------

    records = read_data()


    # -------------------------
    # DUPLICATE PHONE CHECK
    # -------------------------

    for record in records:

        if record["Phone"] == phone:

            return """
            <div style="
                text-align:center;
                margin-top:100px;
                font-family:Arial;
            ">

                <h2 style="color:#dc2626;">
                    ⚠️ This phone number is already registered.
                </h2>

                <br>

                <a
                    href="/"
                    style="
                        background:#4f46e5;
                        color:white;
                        padding:12px 20px;
                        text-decoration:none;
                        border-radius:8px;
                    "
                >
                    Go Back
                </a>

            </div>
            """


    # -------------------------
    # CREATE REGISTRATION
    # -------------------------

    new_record = {

        "Name": name,

        "Email": email,

        "Phone": phone,

        "Event": event,

        "Date": datetime.now().strftime(
            "%d-%m-%Y %I:%M %p"
        )

    }


    # -------------------------
    # SAVE REGISTRATION
    # -------------------------

    records.append(new_record)

    save_data(records)


    return redirect("/success")


# =========================================================
# SUCCESS PAGE
# =========================================================

@app.route("/success")
def success():

    return render_template_string("""
<!DOCTYPE html>

<html>

<head>

    <title>Registration Successful</title>

    <style>
        {{ css }}
    </style>

</head>

<body>


<nav class="navbar">

    <div class="logo">
        🎉 Event Registration System
    </div>

    <div>

        <a href="/">
            Home
        </a>

        <a href="/login">
            Admin
        </a>

    </div>

</nav>


<div class="container">

    <div class="card success">

        <div class="success-icon">
            ✅
        </div>


        <h1>
            Registration Successful!
        </h1>


        <p>
            Your event registration has been saved successfully.
        </p>


        <br>


        <a
            href="/"
            class="btn"
        >
            Register Another Student
        </a>

    </div>

</div>


</body>

</html>

""", css=CSS)


# =========================================================
# ADMIN LOGIN
# =========================================================

@app.route("/login", methods=["GET", "POST"])
def login():

    error = ""


    if request.method == "POST":

        username = request.form.get(
            "username",
            ""
        ).strip()


        password = request.form.get(
            "password",
            ""
        ).strip()


        if username == "admin" and password == "1234":

            session["admin"] = True

            return redirect("/dashboard")


        error = "Invalid username or password."


    return render_template_string("""
<!DOCTYPE html>

<html>

<head>

    <title>Admin Login</title>

    <style>
        {{ css }}
    </style>

</head>

<body>


<nav class="navbar">

    <div class="logo">
        🔐 Admin Panel
    </div>


    <div>

        <a href="/">
            Home
        </a>

    </div>

</nav>


<div class="container">

    <div class="card login-card">


        <h2 class="center">
            🔐 Admin Login
        </h2>


        {% if error %}

        <div style="
            background:#fee2e2;
            color:#b91c1c;
            padding:12px;
            border-radius:10px;
            margin-bottom:15px;
        ">

            {{ error }}

        </div>

        {% endif %}


        <form method="POST">


            <div class="form-group">

                <label>
                    Username
                </label>

                <input
                    type="text"
                    name="username"
                    placeholder="Enter admin username"
                    required
                >

            </div>


            <div class="form-group">

                <label>
                    Password
                </label>

                <input
                    type="password"
                    name="password"
                    placeholder="Enter admin password"
                    required
                >

            </div>


            <button
                class="btn"
                type="submit"
            >
                Login
            </button>


        </form>


        <br>


        <div class="info">

            <strong>
                Demo Admin Login
            </strong>

            <br><br>

            Username:
            <b>admin</b>

            <br>

            Password:
            <b>1234</b>

        </div>


    </div>

</div>


</body>

</html>

""", css=CSS, error=error)


# =========================================================
# ADMIN DASHBOARD
# =========================================================

@app.route("/dashboard")
def dashboard():

    if not session.get("admin"):

        return redirect("/login")


    records = read_data()


    total = len(records)


    workshop = sum(
        1
        for r in records
        if r["Event"] == "Workshop"
    )


    seminar = sum(
        1
        for r in records
        if r["Event"] == "Seminar"
    )


    hackathon = sum(
        1
        for r in records
        if r["Event"] == "Hackathon"
    )


    cultural = sum(
        1
        for r in records
        if r["Event"] == "Cultural Fest"
    )


    technical = sum(
        1
        for r in records
        if r["Event"] == "Technical Fest"
    )


    return render_template_string("""
<!DOCTYPE html>

<html>

<head>

    <title>Admin Dashboard</title>

    <style>
        {{ css }}
    </style>

</head>

<body>


<nav class="navbar">

    <div class="logo">
        📊 Admin Dashboard
    </div>


    <div>

        <a href="/dashboard">
            Dashboard
        </a>

        <a href="/view">
            Registrations
        </a>

        <a href="/report">
            Reports
        </a>

        <a href="/logout">
            Logout
        </a>

    </div>

</nav>


<div class="container">


    <div class="hero">

        <h1>
            Welcome Admin 👋
        </h1>

        <p>
            Manage and monitor student event registrations.
        </p>

    </div>


    <div class="stats">


        <div class="stat">

            <h3>
                {{ total }}
            </h3>

            <p>
                👥 Total Registrations
            </p>

        </div>


        <div class="stat">

            <h3>
                {{ workshop }}
            </h3>

            <p>
                💻 Workshops
            </p>

        </div>


        <div class="stat">

            <h3>
                {{ seminar }}
            </h3>

            <p>
                🎤 Seminars
            </p>

        </div>


        <div class="stat">

            <h3>
                {{ hackathon }}
            </h3>

            <p>
                👨‍💻 Hackathons
            </p>

        </div>


    </div>


    <div class="card center">


        <h2>
            📋 Registration Management
        </h2>


        <p>
            View all students who have registered.
        </p>


        <br>


        <a
            href="/view"
            class="btn"
        >
            View Registration List
        </a>


        <a
            href="/report"
            class="btn btn-green"
        >
            View Reports
        </a>


    </div>


</div>


</body>

</html>

""",
                              css=CSS,
                              total=total,
                              workshop=workshop,
                              seminar=seminar,
                              hackathon=hackathon)


# =========================================================
# VIEW REGISTRATIONS
# =========================================================

@app.route("/view")
def view():

    if not session.get("admin"):

        return redirect("/login")


    search = request.args.get(
        "search",
        ""
    ).strip().lower()


    # IMPORTANT:
    # Read latest registration data from CSV

    records = read_data()


    # Search

    if search:

        records = [

            r for r in records

            if search in r["Name"].lower()
            or search in r["Email"].lower()
            or search in r["Phone"].lower()
            or search in r["Event"].lower()

        ]


    return render_template_string("""
<!DOCTYPE html>

<html>

<head>

    <title>Registration List</title>

    <style>
        {{ css }}
    </style>

</head>

<body>


<nav class="navbar">


    <div class="logo">
        📋 Registration List
    </div>


    <div>

        <a href="/dashboard">
            Dashboard
        </a>

        <a href="/view">
            Registrations
        </a>

        <a href="/report">
            Reports
        </a>

        <a href="/logout">
            Logout
        </a>

    </div>


</nav>


<div class="container">


    <div class="hero">

        <h1>
            👥 Student Registrations
        </h1>

        <p>
            All registered students are displayed below.
        </p>

    </div>


    <div class="card">


        <form
            action="/view"
            method="GET"
            class="search-box"
        >


            <input
                type="text"
                name="search"
                value="{{ search }}"
                placeholder="🔍 Search by name, email, phone or event..."
            >


            <button
                class="btn"
                type="submit"
            >
                Search
            </button>


            <a
                href="/view"
                class="btn btn-green"
            >
                Show All
            </a>


        </form>


        {% if records %}


        <div class="table-container">


            <table>


                <thead>

                    <tr>

                        <th>
                            No.
                        </th>

                        <th>
                            Name
                        </th>

                        <th>
                            Email
                        </th>

                        <th>
                            Phone
                        </th>

                        <th>
                            Event
                        </th>

                        <th>
                            Date
                        </th>

                        <th>
                            Actions
                        </th>

                    </tr>

                </thead>


                <tbody>


                {% for record in records %}


                    <tr>


                        <td>
                            {{ loop.index }}
                        </td>


                        <td>

                            <strong>
                                {{ record["Name"] }}
                            </strong>

                        </td>


                        <td>
                            {{ record["Email"] }}
                        </td>


                        <td>
                            {{ record["Phone"] }}
                        </td>


                        <td>
                            {{ record["Event"] }}
                        </td>


                        <td>
                            {{ record["Date"] }}
                        </td>


                        <td>


                            <div class="actions">


                                <a
                                    href="/edit/{{ record['Phone'] }}"
                                    class="btn btn-edit"
                                >
                                    Edit
                                </a>


                                <a
                                    href="/delete/{{ record['Phone'] }}"
                                    class="btn btn-danger"
                                    onclick="return confirm('Delete this registration?')"
                                >
                                    Delete
                                </a>


                            </div>


                        </td>


                    </tr>


                {% endfor %}


                </tbody>


            </table>


        </div>


        {% else %}


        <div class="empty">


            <h2>
                📭 No registrations found
            </h2>


            <p>
                When a student registers,
                the registration will automatically appear here.
            </p>


        </div>


        {% endif %}


    </div>


</div>


</body>

</html>

""",
                              css=CSS,
                              records=records,
                              search=search)


# =========================================================
# EDIT REGISTRATION
# =========================================================

@app.route("/edit/<phone>", methods=["GET", "POST"])
def edit(phone):

    if not session.get("admin"):

        return redirect("/login")


    records = read_data()


    record = None


    for r in records:

        if r["Phone"] == phone:

            record = r

            break


    if record is None:

        return redirect("/view")


    if request.method == "POST":


        new_name = request.form.get(
            "name",
            ""
        ).strip()


        new_email = request.form.get(
            "email",
            ""
        ).strip()


        new_phone = request.form.get(
            "phone",
            ""
        ).strip()


        new_event = request.form.get(
            "event",
            ""
        ).strip()


        if not re.match(
            r"^[A-Za-z ]+$",
            new_name
        ):

            return "Invalid name"


        if not re.match(
            r"^[^\s@]+@[^\s@]+\.[^\s@]+$",
            new_email
        ):

            return "Invalid email"


        if not re.match(
            r"^[0-9]{10}$",
            new_phone
        ):

            return "Invalid phone number"


        record["Name"] = new_name

        record["Email"] = new_email

        record["Phone"] = new_phone

        record["Event"] = new_event


        save_data(records)


        return redirect("/view")


    return render_template_string("""
<!DOCTYPE html>

<html>

<head>

    <title>Edit Registration</title>

    <style>
        {{ css }}
    </style>

</head>

<body>


<nav class="navbar">


    <div class="logo">
        ✏️ Edit Registration
    </div>


    <div>

        <a href="/view">
            Back
        </a>

    </div>


</nav>


<div class="container">


    <div class="card">


        <h2>
            ✏️ Edit Student Registration
        </h2>


        <form method="POST">


            <div class="form-group">

                <label>
                    Name
                </label>

                <input
                    type="text"
                    name="name"
                    value="{{ record['Name'] }}"
                    required
                >

            </div>


            <div class="form-group">

                <label>
                    Email
                </label>

                <input
                    type="email"
                    name="email"
                    value="{{ record['Email'] }}"
                    required
                >

            </div>


            <div class="form-group">

                <label>
                    Phone
                </label>

                <input
                    type="text"
                    name="phone"
                    value="{{ record['Phone'] }}"
                    maxlength="10"
                    required
                >

            </div>


            <div class="form-group">

                <label>
                    Event
                </label>


                <select
                    name="event"
                    required
                >


                    <option
                        value="Workshop"
                        {% if record['Event'] == 'Workshop' %}
                        selected
                        {% endif %}
                    >
                        Workshop
                    </option>


                    <option
                        value="Seminar"
                        {% if record['Event'] == 'Seminar' %}
                        selected
                        {% endif %}
                    >
                        Seminar
                    </option>


                    <option
                        value="Hackathon"
                        {% if record['Event'] == 'Hackathon' %}
                        selected
                        {% endif %}
                    >
                        Hackathon
                    </option>


                    <option
                        value="Cultural Fest"
                        {% if record['Event'] == 'Cultural Fest' %}
                        selected
                        {% endif %}
                    >
                        Cultural Fest
                    </option>


                    <option
                        value="Technical Fest"
                        {% if record['Event'] == 'Technical Fest' %}
                        selected
                        {% endif %}
                    >
                        Technical Fest
                    </option>


                </select>


            </div>


            <button
                class="btn"
                type="submit"
            >
                💾 Save Changes
            </button>


            <a
                href="/view"
                class="btn btn-danger"
            >
                Cancel
            </a>


        </form>


    </div>


</div>


</body>

</html>

""",
                              css=CSS,
                              record=record)


# =========================================================
# DELETE REGISTRATION
# =========================================================

@app.route("/delete/<phone>")
def delete(phone):

    if not session.get("admin"):

        return redirect("/login")


    records = read_data()


    records = [
        r for r in records
        if r["Phone"] != phone
    ]


    save_data(records)


    return redirect("/view")


# =========================================================
# REPORT
# =========================================================

@app.route("/report")
def report():

    if not session.get("admin"):

        return redirect("/login")


    records = read_data()


    total = len(records)


    events = {}


    for r in records:

        event = r["Event"]

        events[event] = events.get(
            event,
            0
        ) + 1


    return render_template_string("""
<!DOCTYPE html>

<html>

<head>

    <title>Reports</title>

    <style>
        {{ css }}
    </style>

</head>

<body>


<nav class="navbar">


    <div class="logo">
        📊 Event Report
    </div>


    <div>

        <a href="/dashboard">
            Dashboard
        </a>

        <a href="/view">
            Registrations
        </a>

        <a href="/logout">
            Logout
        </a>

    </div>


</nav>


<div class="container">


    <div class="hero">

        <h1>
            📊 Registration Report
        </h1>

        <p>
            Event-wise registration summary.
        </p>

    </div>


    <div class="stats">


        <div class="stat">

            <h3>
                {{ total }}
            </h3>

            <p>
                Total Students
            </p>

        </div>


        {% for event, count in events.items() %}


        <div class="stat">

            <h3>
                {{ count }}
            </h3>

            <p>
                {{ event }}
            </p>

        </div>


        {% endfor %}


    </div>


    <div class="card">


        <h2>
            📋 Event-wise Registration
        </h2>


        <div class="table-container">


            <table>


                <tr>

                    <th>
                        Event
                    </th>

                    <th>
                        Registrations
                    </th>

                </tr>


                {% for event, count in events.items() %}


                <tr>

                    <td>
                        {{ event }}
                    </td>

                    <td>
                        <strong>
                            {{ count }}
                        </strong>
                    </td>

                </tr>


                {% endfor %}


            </table>


        </div>


    </div>


</div>


</body>

</html>

""",
                              css=CSS,
                              total=total,
                              events=events)


# =========================================================
# LOGOUT
# =========================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")


# =========================================================
# START FLASK
# =========================================================

if __name__ == "__main__":

    print()
    print("==========================================")
    print("     EVENT REGISTRATION SYSTEM")
    print("==========================================")
    print("Admin Username : admin")
    print("Admin Password : 1234")
    print("Registration File:")
    print(DATA_FILE)
    print("==========================================")
    print("Open this address:")
    print("http://127.0.0.1:5000")
    print("==========================================")
    print()

    app.run(debug=True)