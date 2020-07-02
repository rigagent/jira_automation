#! /usr/bin/python3

import sys
from jira import JIRA
from jira.exceptions import JIRAError

from config import Config


class JiraBase():

    def __init__(self):
        try:
            self.jira = JIRA(Config["jira_server"], basic_auth=(Config["jira_login"], Config["jira_password"]))
        except JIRAError as e:
            print("You can't authenticate to Jira due to '{text}' error".format(text=e.text))
            print("You got '{code}' HTTP status code".format(code=e.status_code))
            print("Exiting...")
            sys.exit()


    def epic_template(self, ticket_type, ticket_summary):
        return {"project": {"key": Config["project_name"]},
                # Epic Name field
                "customfield_10732": ticket_summary,
                "summary": ticket_summary,
                "components": [{"name": Config["component"]}],
                "versions": [{"name": "{release}".format(release=Config["release"])}],
                # Target version field
                "customfield_10815": [{"name": "{release}".format(release=Config["release"])}],
                "labels": [Config["label_epic"]],
                "duedate": Config["duedate"],
                "issuetype": {"name": ticket_type},
                "assignee": {"name": Config["assignee"]},
                # CC field
                "customfield_10020": [{"name": Config["cc"][0]},
                                      {"name": Config["cc"][1]},
                                      {"name": Config["cc"][2]}]
                }


    def task_template(self, ticket_type, ticket_summary):
        return {"project": {"key": Config["project_name"]},
                "summary": ticket_summary,
                "components": [{"name": Config["component"]}],
                "versions": [{"name": "{release}".format(release=Config["release"])}],
                # Target version field
                "customfield_10815": [{"name": "{release}".format(release=Config["release"])}],
                "labels": [Config["label_task"]],
                "duedate": Config["duedate"],
                "issuetype": {"name": ticket_type},
                "assignee": {"name": Config["assignee"]},
                # CC field
                "customfield_10020": [{"name": Config["cc"][0]},
                                      {"name": Config["cc"][1]},
                                      {"name": Config["cc"][2]}]
                }


    def create_ticket(self, ticket_type, ticket_summary):
        if self.search_ticket(ticket_summary):
            print("'{summary}' {type} ticket is already exist. Skipping this action...".format(summary=ticket_summary,
                                                                                               type=ticket_type))
        else:
            print("Create '{summary}' {type} ticket".format(summary=ticket_summary, type=ticket_type))\
            if ticket_type == "Epic":
                new_ticket = self.epic_template(ticket_type, ticket_summary)
            elif ticket_type == "Task":
                new_ticket = self.task_template(ticket_type, ticket_summary)
            self.jira.create_issue(fields=new_ticket)


    def search_ticket(self, ticket_summary):
        try:
            result = self.jira.search_issues('text ~ "{summary}"'.format(summary=ticket_summary))[0]
        except IndexError as e:
            return None
        else:
            return result


if __name__ == "__main__":
    jira = JiraBase()
    jira.create_ticket("Epic", Config["summary_epic"])
    jira.create_ticket("Task", Config["summary_task"])
