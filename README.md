Personal Portfolio + Dashboard Project

https://www.youtube.com/watch?v=rQ5KlW-vX4Y

This project is a personal portfolio, developed for CS50 final project.
It is built with Flask, Bootstrap 5, HTML/CSS, and Plotly for interactive visualizations.

The portfolio presents information about professional background, projects, and cases, while the dashboard displays dynamic charts generated from processed datasets.

⸻

Features

🌐 Portfolio Website
	•	Landing page with sections such as About Me, Cases, Projects, and Contact.
	•	Responsive layout using Bootstrap 5.
	•	Navigation through anchored sections.
	•	Custom styling through external CSS.

📊 Dashboard
	•	Integrated dashboard accessible through /dashboard.
	•	Graphs and plots generated with Plotly.
	•	Data processing handled via Pandas.
	•	Display of structured tables, metrics, and other visual elements.

⚙️ Backend (Flask)
	•	Route-based page rendering using Flask + Jinja2 templates.
	•	Separation of templates into a clean structure:
	•	templates/layout.html
	•	templates/index.html
	•	templates/dashboard.html
	•	Static assets available through:
	•	static/css/
	•	static/js/
	•	static/images/

⸻

Project Structure

.
├── app.py
├── requirements.txt
├── static
│   ├── css
│   │   └── style.css
│   └── images
├── templates
│   ├── layout.html
│   ├── index.html
│   └── dashboard.html
└── data
    └── dataset.csv

Technologies Used
	•	Python 3
	•	Flask
	•	Jinja2
	•	Bootstrap 5
	•	Plotly
	•	Pandas
	•	HTML/CSS/JavaScript

Purpose

This project serves as:
	•	A personal online portfolio.
	•	A demonstration of Flask web development.
	•	A practical example of integrating data visualization into a web application.


