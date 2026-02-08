import os
from datetime import datetime

SITE_CREATED = "2026-02-07 00:00"


def site_last_updated():
    root = os.path.dirname(__file__)
    watch_dirs = [
        root,
        os.path.join(root, "templates"),
        os.path.join(root, "static"),
    ]
    latest = 0.0
    for folder in watch_dirs:
        if not os.path.isdir(folder):
            continue
        for base, _, files in os.walk(folder):
            for name in files:
                if not name.endswith((".py", ".html", ".css", ".js", ".json")):
                    continue
                path = os.path.join(base, name)
                try:
                    mtime = os.path.getmtime(path)
                    if mtime > latest:
                        latest = mtime
                except OSError:
                    continue
    if latest:
        return datetime.fromtimestamp(latest).strftime("%Y-%m-%d %H:%M")
    return SITE_CREATED
