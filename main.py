import requests
from bs4 import BeautifulSoup
import json
import os

JSON_NAME = "output.json"

INTEREST_KEYWORD = "machine learning" # Change this for search query!

def findFaculty():
    
    print(f"Searching for faculty with a research interest in {INTEREST_KEYWORD}...\n")

    with open(JSON_NAME, "r") as f:
        results = json.load(f)

    def getResearchInterests(name, link):
        r = requests.get(link)
        soup = BeautifulSoup(r.content, "html.parser")
        
        h2_tags = soup.find_all("h2")
        for tag in h2_tags:
            if tag.get_text() == "Research Interests":
                interests = tag.find_next().find_all("li")
                for interest in interests:
                    if interest.get_text().lower().find(INTEREST_KEYWORD) != -1:
                        print(f"{name}: {link}")
                        print(f"{interest.get_text()}\n")

    for name in results:
        link = results[name]
        getResearchInterests(name, link)

if os.path.exists(JSON_NAME):

    print(f"{JSON_NAME} found.")

    findFaculty()

else:

    print("Scraping faculty profiles...")

    r = requests.get("https://siebelschool.illinois.edu/about/people/all-faculty")

    soup = BeautifulSoup(r.content, "html.parser")

    people = soup.find_all("div", class_="person")

    profiles = []

    for person in people:
        profiles.append(person.find(class_="name"))

    results = {}

    for profile in profiles:
        results[profile.get_text()] = "https://siebelschool.illinois.edu" + profile.find("a").get("href")

    with open(JSON_NAME, "w") as f:
        json.dump(results, f, indent=4)
    
    print(f"Output saved to {JSON_NAME}.\n")

    findFaculty()