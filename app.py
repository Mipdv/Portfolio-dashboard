from flask import Flask, render_template, request, redirect, url_for
from flask_mail import Mail, Message
import os
from dotenv import load_dotenv
import pandas as pd
import json
import plotly
import plotly.express as px
import plotly.io as pio

load_dotenv()

app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/submit', methods=['POST'])
def submit():
    email = request.form['email']
    subject = request.form['subject']
    message = request.form['message']
    origin = request.form.get("orign", "index")
    msg = Message('New Message!', sender=os.getenv('MAIL_USERNAME'), recipients=[os.getenv('MAIL_USERNAME')])
    msg.body = f"Message from: {email}\n{subject}\n\n{message}"
    mail.send(msg)
    if origin == "dashboard": #just a route adjust
        return redirect(url_for("dashboard") + "#contact-me")
    else: 
        return redirect(url_for("index") + "#contact-me")

@app.route("/dashboard")
def dashboard():

    pio.templates["darkbg"] = pio.templates["plotly_white"].update({ #Graphics styles
    "layout": {
        "paper_bgcolor": "#2E2E2E",
        "plot_bgcolor": "#2E2E2E",
        "font": {"color": "white"}
    }   
})

    pio.templates.default = "darkbg"
    
    df_demo = pd.read_csv("demographics.csv", dtype=str)

    df_demo["Race or Ethnicity"] = df_demo["Race or Ethnicity"].str.strip()

    rcount = df_demo["Race or Ethnicity"].value_counts().reset_index()
    rcount.columns = ["Race or Ethnicity", "Count"]

    fig1 = px.bar(
        rcount,
        x="Race or Ethnicity",
        y="Count",
        title="Number of Judges by Ethinic Group",
        text="Count",
        labels={"Count": "Number of Judges"}#rename the Y label
    )

    fig1.update_traces(textposition="outside")
    fig1.update_layout(xaxis_tickangle=-45, height=600)

    graph1 = fig1.to_html(full_html=False)

    df_demo["Gender"] = df_demo["Gender"].str.strip()

    gender = df_demo["Gender"].value_counts().reset_index()
    gender.columns = ["Gender", "Count"]

    fig2 = px.pie(
        gender,
        names="Gender",
        values="Count",
        title="Gender distribution",
        labels={"Count": "Number of Judges"}
    )
    graph2 = fig2.to_html(full_html=False, include_plotlyjs=False)
    
    df_service = pd.read_csv("federal-judicial-service.csv", dtype=str)

    df_gender = df_demo[["nid", "Gender"]].copy()
    df_date = df_service[["nid", "Commission Date"]].copy()

    df_merged = pd.merge(df_date, df_gender, on="nid", how="inner")
    
    df_merged['Commission Date'] = pd.to_datetime(df_merged['Commission Date'], errors='coerce')
    df_merged.dropna(subset=['Commission Date', 'Gender'], inplace=True)
    
    df_female_appointments = df_merged[df_merged['Gender'] == 'Female'].copy()
    
    start_date = pd.to_datetime('1995-01-01')
    df_recent = df_female_appointments[df_female_appointments['Commission Date'] >= start_date].copy()
    
    bins = pd.to_datetime(['1995-01-01', '2000-01-01', '2005-01-01', '2010-01-01', '2015-01-01', '2020-01-01', '2025-01-01'])
    labels = ['1995-1999', '2000-2004', '2005-2009', '2010-2014', '2015-2019', '2020-2024']
    
    df_recent['Time_Group'] = pd.cut(
        df_recent['Commission Date'], 
        bins=bins, 
        labels=labels, 
        right=False
    )
    
    time_counts = df_recent['Time_Group'].value_counts().sort_index().reset_index()
    time_counts.columns = ['Time_Group', 'Count']

    fig3 = px.bar(
        time_counts,
        x="Time_Group",
        y="Count",
        title="Number of Female Judges Appointed (Last 30 Years)",
        labels={"Time_Group": "Appointment Period", "Count": "Number of Female Judges Appointed"},
        text="Count",
        template="plotly_white"
    )
    
    fig3.update_traces(textposition="outside")
    fig3.update_layout(xaxis_tickangle=-45, height=600)

    graph3 = fig3.to_html(full_html=False, include_plotlyjs=False)

    df_scdb = pd.read_csv("SCDB_2025_01_justiceCentered_Citation.csv")

    df_scdb['dateDecision'] = pd.to_datetime(df_scdb['dateDecision'], errors='coerce')
    df_scdb.dropna(subset=['dateDecision'], inplace=True)
    df_scdb['Year'] = df_scdb['dateDecision'].dt.year

    df_cases = df_scdb.drop_duplicates(subset=['caseId'])

    decisions_count = df_cases[df_cases['Year'].isin([2023, 2024])]['Year'].value_counts().reset_index()
    decisions_count.columns = ['Year', 'Total Cases Decided']
    decisions_count['Year'] = decisions_count['Year'].astype(str)

    fig4 = px.bar(
        decisions_count,
        x='Year',
        y='Total Cases Decided',
        title='Total Supreme Court Decisions (2023 vs 2024)',
        labels={'Year': 'Year of Decision', 'Total Cases Decided': 'Number of Unique Cases Decided'},
        text='Total Cases Decided',
        template='plotly_white'
    )

    fig4.update_traces(marker_color=['#1f77b4', '#ff7f0e'], textposition="outside")
    fig4.update_layout(height=600, yaxis_title='Number of unique cases decided')

    graph4 = fig4.to_html(full_html=False, include_plotlyjs=False)
    df_race = df_demo[["nid", "Race or Ethnicity"]].copy()
    
    df_merged_race = pd.merge(df_date, df_race, on="nid", how="inner")
    
    df_merged_race['Commission Date'] = pd.to_datetime(df_merged_race['Commission Date'], errors='coerce')
    df_merged_race.dropna(subset=['Commission Date', 'Race or Ethnicity'], inplace=True)
    
    start_date_10yr = pd.to_datetime('2015-01-01')
    df_recent_race = df_merged_race[df_merged_race['Commission Date'] >= start_date_10yr].copy()
    
    race_counts = df_recent_race['Race or Ethnicity'].value_counts().reset_index()
    race_counts.columns = ['Race or Ethnicity', 'Count']
    
    fig5 = px.bar(
        race_counts,
        x='Race or Ethnicity',
        y='Count',
        title='Judge Appointments by Ethnicity (Last 10 Years)',
        labels={'Race or Ethnicity': 'Race or Ethnicity', 'Count': 'Number of Judges Appointed'},
        text='Count',
        template='plotly_white'
    )

    fig5.update_traces(textposition="outside")
    fig5.update_layout(xaxis_tickangle=-45, height=600)

    graph5 = fig5.to_html(full_html=False, include_plotlyjs=False)
    
    df_b_state = df_demo.dropna(subset=["Birth State"]).copy()
    df_b_state["Birth State"] = df_b_state["Birth State"].str.strip()

    state_counts = df_b_state["Birth State"].value_counts().reset_index()
    state_counts.columns = ["Birth State", "Count"]

    fig6 = px.choropleth(
        state_counts, 
        locations='Birth State', 
        locationmode='USA-states', 
        color='Count',
        scope='usa',
        title='Federal Judges by Birth State',
        color_continuous_scale=px.colors.sequential.Plasma,
        hover_name='Birth State',
        labels={'Count': 'Number of Judges'}
    )

    mp_background = '#2E2E2E'
    
    fig6.update_layout(margin={"r":0,"t":50,"l":0,"b":0},

        geo=dict( #chaging the US map background color
                bgcolor=mp_background,
                lakecolor=mp_background, 
                landcolor='#3A3A3A'
            )
    )

    graph6 = fig6.to_html(full_html=False, include_plotlyjs=False)

    df_docket = pd.read_csv("SCDB_2025_01_justiceCentered_Docket.csv")

    
    df_docket['dateDecision'] = pd.to_datetime(df_docket['dateDecision'], errors='coerce')
    df_docket['year'] = df_docket['dateDecision'].dt.year

    cases_per_year = df_docket['year'].value_counts().sort_index().reset_index()
    cases_per_year.columns = ["year", "count"]

    fig7 = px.line(
        cases_per_year,
        x="year",
        y="count",
        title="Cases per Year",
        labels={"count": "Number of Cases"}
    )
    graph7 = fig7.to_html(full_html=False)

    decision_labels = {
    1: "Oral Argument",
    2: "Rehearing",
    3: "Judgment of the Court",
    4: "Per Curiam",
    5: "Dismissed for Want of Jurisdiction",
    6: "Dismissed",
    7: "Affirmed",
    8: "Reversed",
    9: "Vacated",
    10: "Denied",
    11: "Other"
}

    df_docket["decisionLabel"] = df_docket["decisionType"].map(decision_labels)
    fig8 = px.pie(
        df_docket,
        names= "decisionLabel",
        title= "Decision Types in 2024"
    )

    graph8 = fig8.to_html(full_html= False)
    return render_template("dashboard.html", graph1=graph1, graph2=graph2, graph3=graph3, graph4=graph4, graph5=graph5, graph6=graph6, graph7=graph7, graph8=graph8)

if __name__ == "__main__":
    app.run()