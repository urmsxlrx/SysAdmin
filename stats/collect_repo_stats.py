import os
from collections import defaultdict

ROOT_DIR = "."
OUTPUT_FILE = "repo-statistics.md"

stats = defaultdict(lambda: {"count": 0, "size": 0})
total_files = 0
total_size = 0
tree = []

def human_size(size):
    for unit in ["B", "KB", "MB", "GB"]:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} TB"

for root, dirs, files in os.walk(ROOT_DIR):
    if ".git" in root or ".github" in root:
        continue

    level = root.replace(ROOT_DIR, "").count(os.sep)
    indent = "  " * level
    tree.append(f"{indent}{os.path.basename(root) or 'root'}")

    for file in files:
        if file == OUTPUT_FILE:
            continue

        path = os.path.join(root, file)
        ext = os.path.splitext(file)[1] or "no_extension"

        try:
            size = os.path.getsize(path)
        except OSError:
            continue

        stats[ext]["count"] += 1
        stats[ext]["size"] += size
        total_files += 1
        total_size += size

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write("# Статистика репозитория\n\n")

    f.write("## Общая информация\n")
    f.write(f"- Всего файлов: **{total_files}**\n")
    f.write(f"- Общий размер: **{human_size(total_size)}**\n\n")

    f.write("## Дерево каталогов\n")
    f.write("```\n")
    f.write("\n".join(tree))
    f.write("\n```\n\n")

    f.write("## Статистика по типам файлов\n")
    f.write("| Тип файла | Количество | Общий размер |\n")
    f.write("|----------|------------|--------------|\n")

    for ext, data in sorted(stats.items()):
        f.write(
            f"| `{ext}` | {data['count']} | {human_size(data['size'])} |\n"
        )
