import os
from github import Github
from jinja2 import Template
from datetime import datetime

# GitHub token and repository names
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
SOURCE_REPO_NAME = 'NWMPHN-Data/projects/24'  # Replace with the source project URL
TARGET_REPO_NAME = 'targetowner/targetrepo'  # Replace with the target repository name

# Initialize GitHub client
g = Github(GITHUB_TOKEN)

# Fetch project data from the source organization project board
org = g.get_organization('NWMPHN-Data')
project = org.get_project(24)
columns = project.get_columns()

activities_completed = []
activities_planned = []
issues_risks = []

for column in columns:
    cards = column.get_cards()
    for card in cards:
        note = card.get_note()
        if note:
            if column.name == 'Done':
                activities_completed.append(note)
            elif column.name == 'In Progress':
                activities_planned.append(note)
            elif column.name == 'Issues/Risks':
                issues_risks.append(note)

# Load template
with open('status_update_template.md') as file:
    template = Template(file.read())

# Render template
output = template.render(
    current_milestone="Milestone 1",  # Set your current milestone
    next_milestone="Milestone 2",  # Set your next milestone
    activities_completed='\n'.join(f"- {item}" for item in activities_completed),
    activities_planned='\n'.join(f"- {item}" for item in activities_planned),
    issues_risks='\n'.join(f"- {item}" for item in issues_risks),
    date=datetime.now().strftime("%Y-%m-%d")
)

# Save output to file in the target repository
target_repo = g.get_repo(TARGET_REPO_NAME)
file_path = 'status_update.md'
try:
    file = target_repo.get_contents(file_path)
    target_repo.update_file(file_path, "Generated weekly status update", output, file.sha, branch="main")
except:
    target_repo.create_file(file_path, "Generated weekly status update", output, branch="main")
