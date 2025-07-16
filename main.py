import json
import os
from datetime import datetime

FILENAME = "tasks.json"

def load_tasks():
    if os.path.exists(FILENAME):
        try:
            with open(FILENAME, "r", encoding="utf-8") as file:
                content = file.read().strip()
                if not content:
                    return []
                return json.loads(content)
        except json.JSONDecodeError:
            print("Ошибка: файл tasks.json повреждён. Загружается пустой список задач.")
            return []
    return []

def save_tasks(tasks):
    with open(FILENAME, "w", encoding="utf-8") as file:
        json.dump(tasks, file, ensure_ascii=False, indent=4)

def show_menu():
    print("\nМеню:")
    print("1. Добавить задачу")
    print("2. Показать все задачи")
    print("3. Показать выполненные задачи")
    print("4. Показать невыполненные задачи")
    print("5. Отметить задачу как выполненную")
    print("6. Удалить задачу")
    print("0. Выход")

def add_task(tasks):
    title = input("Введите описание задачи: ").strip()
    if title:
        task = {
            "title": title,
            "done": False,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        tasks.append(task)
        save_tasks(tasks)
        print("Задача успешно добавлена.")
    else:
        print("Задача не может быть пустой.")

def display_tasks(tasks, only_done=None):
    if only_done is True:
        filtered = [t for t in tasks if t["done"]]
    elif only_done is False:
        filtered = [t for t in tasks if not t["done"]]
    else:
        filtered = tasks

    if not filtered:
        print("Нет задач для отображения.")
        return

    for idx, task in enumerate(filtered, start=1):
        status = "✔" if task["done"] else "✗"
        print(f"{idx}. [{status}] {task['title']} (создана: {task['created_at']})")

def mark_task_done(tasks):
    display_tasks(tasks, only_done=False)
    try:
        index = int(input("Введите номер задачи для отметки: ")) - 1
        if 0 <= index < len(tasks):
            tasks[index]["done"] = True
            save_tasks(tasks)
            print("Задача отмечена как выполненная.")
        else:
            print("Неверный номер задачи.")
    except ValueError:
        print("Введите корректный номер.")

def delete_task(tasks):
    display_tasks(tasks)
    try:
        index = int(input("Введите номер задачи для удаления: ")) - 1
        if 0 <= index < len(tasks):
            deleted = tasks.pop(index)
            save_tasks(tasks)
            print(f"Удалена задача: {deleted['title']}")
        else:
            print("Неверный номер задачи.")
    except ValueError:
        print("Введите корректный номер.")

def main():
    tasks = load_tasks()
    while True:
        show_menu()
        choice = input("Выберите пункт меню: ").strip()
        if choice == "1":
            add_task(tasks)
        elif choice == "2":
            display_tasks(tasks)
        elif choice == "3":
            display_tasks(tasks, only_done=True)
        elif choice == "4":
            display_tasks(tasks, only_done=False)
        elif choice == "5":
            mark_task_done(tasks)
        elif choice == "6":
            delete_task(tasks)
        elif choice == "0":
            print("Выход из программы.")
            break
        else:
            print("Некорректный выбор. Попробуйте ещё раз.")

if __name__ == "__main__":
    main()
