import requests
import os
from datetime import datetime

# Replace with your details
ORG = 'NWMPHN-Data'
PROJECT_ID = '24'
TOKEN = os.getenv('GITHUB_TOKEN')

headers = {
    'Authorization': f'token {TOKEN}',
    'Accept': 'application/vnd.github.inertia-preview+json'
}

# Check token scopes for debugging
token_info_url = 'https://api.github.com/user'
token_info_response = requests.get(token_info_url, headers=headers)
print("Token Scopes:", token_info_response.headers.get('x-oauth-scopes'))
token_info_response.raise_for_status()

# Fetch columns in the project board
columns_url = f'https://api.github.com/orgs/{ORG}/projects/{PROJECT_ID}/columns'
columns_response = requests.get(columns_url, headers=headers)

# Debug print to check the API response
print("Columns Response:", columns_response.json())

columns_response.raise_for_status()
columns = columns_response.json()

tasks = []

# Fetch tasks in each column
for column in columns:
    print("Processing column:", column)  # Debug print
    column_id = column['id']
    cards_url = f'https://api.github.com/projects/columns/{column_id}/cards'
    cards_response = requests.get(cards_url, headers=headers)
    cards_response.raise_for_status()
    cards = cards_response.json()

    for card in cards:
        task = {
            'column': column['name'],
            'note': card['note'],
            'content_url': card.get('content_url', '')
        }
        tasks.append(task)

# Create the status report content
report_date = datetime.now().strftime('%Y-%m-%d')
report_content = f"""# Project Status Report

**Project Name:** Head to Health GP eReferral Prototype

**Date:** {report_date}

## Current Status
- **Project Phase:** [e.g., Planning/Development/Testing]
- **Overall Status:** [e.g., On Track/Delayed]

## Summary
- Brief summary of the project’s current state.

## Timeline
[View Project Timeline](your-timeline-link) <!-- Replace "your-timeline-link" with the actual link to your timeline -->

## Tasks Completed This Week
"""

for task in tasks:
    if task['column'] == 'Done':
        report_content += f"- {task['note']} ([Link]({task['content_url']}))\n"

report_content += """
## Tasks Planned for Next Week
"""

for task in tasks:
    if task['column'] == 'To Do':
        report_content += f"- {task['note']} ([Link]({task['content_url']}))\n"

report_content += """
## Risks and Issues
| Risk/Issue        | Description                                       | Mitigation Plan                              | Status     |
|-------------------|---------------------------------------------------|---------------------------------------------|------------|
| Risk/Issue 1      | Brief description of the risk/issue               | Plan to mitigate the risk or resolve issue  | Open/Closed|
| Risk/Issue 2      | Brief description of the risk/issue               | Plan to mitigate the risk or resolve issue  | Open/Closed|

## Decisions Made
- Decision 1
- Decision 2
"""

# Save the report to the status_updates folder
report_filename = f'status_updates/status-report-{report_date}.md'
with open(report_filename, 'w') as file:
    file.write(report_content)

# Commit and push the changes
os.system('git add .')
os.system(f'git commit -m "Add status report for week ending {report_date}"')
os.system('git push')

