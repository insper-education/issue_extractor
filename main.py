import subprocess
import csv
import json
from tqdm import tqdm
import os


def get_repo_grades():
    output = os.system("gh classroom assignment-grades")
    if not os.path.exists("grades.csv"):
        return False
    return True


def extract_repo_from_grades():
    repos = []
    with open("grades.csv", encoding="utf8", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            repos.append( {"user": row["roster_identifier"], "url": row["student_repository_url"]} )            
    return repos


def extract_issues(repo):
    data = {}
    output = subprocess.check_output(
        ["gh", "issue", "list", "-R", repo["url"], "--json", "title,state"]
    )
    issues = json.loads(output)

    data["name"] = repo
    data["issues"] = issues
    return data


def export_csv(data):
    # find issues titles
    issues_head = []
    for repo in data:
        for issue in repo["issues"]:
            if issue["title"] not in issues_head:
                print(issue["title"])
                issues_head.append(issue["title"])

    # Prepare CSV data
    csv_data = []
    headers = ["user"] + ["url"] + issues_head
    csv_data.append(headers)

    for repo in data:
        a = dict.fromkeys(issues_head, "CLOSED")
        row = [repo["name"]["user"], repo["name"]["url"]]
        for issue in repo["issues"]:
            a[issue["title"]] = issue["state"]

        for key in a:
            row.append(a[key])

        csv_data.append(row)

    # Write to CSV
    with open("issues.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(csv_data)


if __name__ == "__main__":
    if not get_repo_grades():
        print("Fail to download grade.csv")

    repos = extract_repo_from_grades()

    data = []
    for repo in tqdm(repos):
        data.append(extract_issues(repo))

    export_csv(data)
