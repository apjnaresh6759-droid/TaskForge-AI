import sys
import os
import json
import argparse
from datetime import datetime, timedelta

DATA_FILE = "taskforge_data.json"

# Color Codes for CLI
BOLD = "\033[1m"
GREEN = "\033[92m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
RED = "\033[91m"
DIM = "\033[2m"
RESET = "\033[0m"

TAG_CATEGORIES = {
    "#Design": ["design", "ui", "ux", "layout", "figma"],
    "#Coding": ["code", "script", "develop", "function", "program"],
    "#Backend": ["backend", "api", "database", "server", "sql"],
    "#Testing": ["test", "debug", "qa", "verify"],
    "#DevOps": ["deploy", "docker", "ci/cd", "pipeline"],
    "#Marketing": ["market", "seo", "ad", "social"],
    "#Security": ["auth", "security", "encrypt", "token"],
    "#Database": ["db", "query", "schema", "mongo"],
    "#Mobile": ["app", "android", "ios", "flutter"],
    "#Docs": ["doc", "readme", "guide", "paper"],
    "#Planning": ["plan", "structure", "roadmap"]
}

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except:
            pass
    return {"tasks": []}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def auto_tag(title):
    tags = []
    lower_title = title.lower()
    for tag, keywords in TAG_CATEGORIES.items():
        if any(kw in lower_title for kw in keywords):
            tags.append(tag)
    return tags if tags else ["#General"]

def calculate_deadlines(tasks):
    current_time = datetime.now()
    accumulated_hours = 0
    for task in tasks:
        if not task.get("done", False):
            est = task.get("estimate_hours", 2)
            accumulated_hours += est
            days_to_add = accumulated_hours / 6
            due = current_time + timedelta(days=days_to_add)
            task["due_date"] = due.strftime("%a %b %d")
    return tasks

def cmd_generate(goal):
    data = load_data()
    print(f"\n{GREEN}Generating task breakdown for:{RESET} {goal}\n")
    new_tasks = [
        {"id": len(data["tasks"]) + 1, "title": f"Define requirements for {goal}", "estimate_hours": 2, "done": False},
        {"id": len(data["tasks"]) + 2, "title": f"Design architecture & UI layout", "estimate_hours": 4, "done": False},
        {"id": len(data["tasks"]) + 3, "title": f"Implement core logic & features", "estimate_hours": 6, "done": False},
        {"id": len(data["tasks"]) + 4, "title": f"Test & verify edge cases", "estimate_hours": 3, "done": False},
        {"id": len(data["tasks"]) + 5, "title": f"Deploy & document project", "estimate_hours": 2, "done": False},
    ]
    for t in new_tasks:
        t["tags"] = auto_tag(t["title"])
        data["tasks"].append(t)
    
    data["tasks"] = calculate_deadlines(data["tasks"])
    save_data(data)
    print(f"{GREEN}✓ Added 5 new tasks to TaskForge!{RESET}")

def cmd_list(show_all=False):
    data = load_data()
    tasks = data.get("tasks", [])
    if not tasks:
        print(f"\n{YELLOW}No tasks found. Use generate command first!{RESET}")
        return

    print(f"\n{BOLD}{CYAN}=== TASKFORGE AI - TASK LIST ==={RESET}\n")
    for t in tasks:
        if t.get("done") and not show_all:
            continue
        status = f"{GREEN}[✓]{RESET}" if t.get("done") else f"{RED}[ ]{RESET}"
        tags_str = " ".join([f"{YELLOW}{tag}{RESET}" for tag in t.get("tags", [])])
        due_str = f"{DIM}(Due: {t.get('due_date', 'N/A')}){RESET}" if not t.get("done") else ""
        print(f"{t['id']}. {status} {BOLD}{t['title']}{RESET} {tags_str} {due_str}")
    print()

def cmd_done(task_id):
    data = load_data()
    found = False
    for t in data["tasks"]:
        if str(t["id"]) == str(task_id):
            t["done"] = True
            found = True
            break
    if found:
        data["tasks"] = calculate_deadlines(data["tasks"])
        save_data(data)
        print(f"\n{GREEN}✓ Task {task_id} marked as complete!{RESET}\n")
    else:
        print(f"\n{RED}Task ID {task_id} not found.{RESET}\n")

def main():
    parser = argparse.ArgumentParser(prog="taskforge", description="TaskForge AI - Task Manager")
    sub = parser.add_subparsers(dest="command")

    p_gen = sub.add_parser("generate")
    p_gen.add_argument("goal", nargs="?", default="Build Project")

    p_ls = sub.add_parser("list")
    p_ls.add_argument("--all", action="store_true")

    p_dn = sub.add_parser("done")
    p_dn.add_argument("task_id", nargs="?")

    args = parser.parse_args()

    if args.command == "generate":
        cmd_generate(args.goal)
    elif args.command == "list":
        cmd_list(args.all)
    elif args.command == "done":
        cmd_done(args.task_id)
    else:
        cmd_list(True)

if __name__ == "__main__":
    main()
  
