import json


def create_research_chapters(chapter_names: list[str]) -> dict[str]:
    return_dict = {}
    for idx, name in enumerate(chapter_names):
        return_dict[f"Chapter {idx + 1}"] = {"Name": name, "Content": {}}
    return return_dict


def _save_file(string_data: str, file_name: str) -> None:
    with open(file_name, "w", encoding="UTF-8") as wfile:
        json.dump(string_data, wfile, indent=4, ensure_ascii=False)
    return None


def wrapper_save_file(sender, app_data, user_data):
    _save_file(user_data[0], user_data[1])
    return None
