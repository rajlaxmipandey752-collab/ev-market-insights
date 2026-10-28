"""Flask web app that embeds the Tableau Public dashboard and story.

Set your published Tableau Public URLs below (or via environment variables),
then run:  python app.py   ->  http://127.0.0.1:5000
"""
import os

from flask import Flask, render_template

app = Flask(__name__)

# Replace with your own Tableau Public view URLs after publishing.
DASHBOARD_URL = os.getenv(
    "TABLEAU_DASHBOARD_URL",
    "https://public.tableau.com/views/EVMarketPerformanceInsights/ExecutiveOverview",
)
DASHBOARD_2_URL = os.getenv(
    "TABLEAU_DASHBOARD_2_URL",
    "https://public.tableau.com/views/EVMarketPerformanceInsights/TechnologyManufacturing",
)
STORY_URL = os.getenv(
    "TABLEAU_STORY_URL",
    "https://public.tableau.com/views/EVMarketPerformanceInsights/EVMarketStory",
)


@app.route("/")
def home():
    return render_template("index.html", active="home")


@app.route("/dashboard")
def dashboard():
    return render_template(
        "embed.html", active="dashboard", title="Interactive Dashboards",
        views=[("Executive Market Overview", DASHBOARD_URL),
               ("Battery Technology & Manufacturing", DASHBOARD_2_URL)],
    )


@app.route("/story")
def story():
    return render_template(
        "embed.html", active="story", title="EV Market Story",
        views=[("EV Market Story", STORY_URL)],
    )


@app.route("/about")
def about():
    return render_template("about.html", active="about")


if __name__ == "__main__":
    app.run(debug=True)
