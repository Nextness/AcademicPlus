<<<<<<<< HEAD:academicplus/research/manager.py
# ===================================================== #
#                 ~~~~ < Imports > ~~~~                 #
# ===================================================== #

import json


# ===================================================== #
#                ~~~~ < Functions > ~~~~                #
# ===================================================== #

def create_research_chapters(chapter_names: list[str]) -> dict[str]:
    """
    [Description]
    | : 

    [Argument]
    | : (Definition)

    [Return]
    | : (Definition)
    """
    return_dict = {}
    for idx, name in enumerate(chapter_names):
        return_dict[f"Chapter {idx + 1}"] = {"Name": name, "Content": {}}
    return return_dict


def _save_file(string_data: str, file_name: str) -> None:
    """
    [Description]
    | : 

    [Argument]
    | : (Definition)

    [Return]
    | : (Definition)
    """
    with open(file_name, "w", encoding="UTF-8") as wfile:
        json.dump(string_data, wfile, indent=4, ensure_ascii=False)
    return None


def wrapper_save_file(sender, app_data, user_data):
    """
    [Description]
    | : 

    [Argument]
    | : (Definition)

    [Return]
    | : (Definition)
    """
    _save_file(user_data[0], user_data[1])
    return None
========
# ===================================================== #
#                 ~~~~ < Imports > ~~~~                 #
# ===================================================== #

import json


# ===================================================== #
#                ~~~~ < Functions > ~~~~                #
# ===================================================== #

def create_research_chapters(chapter_names: list[str]) -> dict[str]:
    """
    [Description]
    | : 

    [Argument]
    | : (Definition)

    [Return]
    | : (Definition)
    """
    return_dict = {}
    for idx, name in enumerate(chapter_names):
        return_dict[f"Chapter {idx + 1}"] = {"Name": name, "Content": {}}
    return return_dict


def _save_file(string_data: str, file_name: str) -> None:
    """
    [Description]
    | : 

    [Argument]
    | : (Definition)

    [Return]
    | : (Definition)
    """
    with open(file_name, "w", encoding="UTF-8") as wfile:
        json.dump(string_data, wfile, indent=4, ensure_ascii=False)
    return None


def wrapper_save_file(sender, app_data, user_data):
    """
    [Description]
    | : 

    [Argument]
    | : (Definition)

    [Return]
    | : (Definition)
    """
    _save_file(user_data[0], user_data[1])
    return None
>>>>>>>> d39f3a1cd4c740e39d4523e310b3d69979c6b16f:src/Research/Manager.py
