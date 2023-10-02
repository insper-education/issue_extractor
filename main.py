import subprocess
import csv
import json
from tqdm import tqdm
import os
import sys


def get_repo_grades():
    output = os.system("gh classroom assignment-grades")
    if not os.path.exists("grades.csv"):
        return False
    return True


def extract_repo_from_grades():
    repos = []
    with open("grades.csv", encoding="utf-8", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            repos.append(
                {"user": row["roster_identifier"], "url": row["student_repository_url"]}
            )
            assignment_name = row["assignment_name"]
    return assignment_name, repos


def extract_issues_actions(repo):
    data = {}
    output = subprocess.check_output(
        ["gh", "issue", "list", "-R", repo["url"], "--json", "title,state"],
        encoding="utf-8",
    )
    issues = json.loads(output)

    actions_output = subprocess.check_output(
        ["gh", "run", "list", "-R", repo["url"], "--json", "workflowName,conclusion"],
        encoding="utf-8",
    )
    actions = json.loads(actions_output)

    latest_runs = {}
    for action in actions:
        if action["workflowName"] not in latest_runs:
            latest_runs[action["workflowName"]] = action["conclusion"].upper()

    data["actions"] = latest_runs
    data["name"] = repo
    data["issues"] = issues

    return data


def export_csv(assgiment_name, data):
    # find issues titles
    issues_head = []
    actions_head = []
    for repo in data:
        for issue in repo["issues"]:
            if issue["title"] not in issues_head:
                issues_head.append(issue["title"])

        for action in repo["actions"]:
            if action not in actions_head:
                actions_head.append(action)

    # Prepare CSV data
    csv_data = []
    headers = ["user"] + ["url"] + actions_head + issues_head
    csv_data.append(headers)

    for repo in data:
        data_dict = dict.fromkeys(issues_head, "CLOSED")
        actions_dict = dict.fromkeys(actions_head, "")

        row = [repo["name"]["user"], repo["name"]["url"]]
        for issue in repo["issues"]:
            data_dict[issue["title"]] = issue["state"]

        for action in repo["actions"]:
            actions_dict[action] = repo["actions"][action]

        for key in actions_dict:
            row.append(actions_dict[key])

        for key in data_dict:
            row.append(data_dict[key])

        csv_data.append(row)

    # Write to CSV
    with open(f"{assignment_name}.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(csv_data)


if __name__ == "__main__":
    if not get_repo_grades():
        print("Fail to download grade.csv")

    assignment_name, repos = extract_repo_from_grades()

    print("Extracting data from repos...")
    data = []
    for repo in tqdm(repos):
        data.append(extract_issues_actions(repo))

    print(f"Exporting data to CSV: {assignment_name}.csv...")
    export_csv(assignment_name, data)
