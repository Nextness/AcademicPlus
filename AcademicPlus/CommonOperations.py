import json
import os


def _processed_confirmation() -> str:
    confirmation = input("Do you want to save the file? Please type Y or N:")

    while not (confirmation == "Y" or confirmation == "N"):
        confirmation = input("Please type Y or N:")

    return str(confirmation)


def _save_file_unsafe(dict_name: dict, save_file_name_loc: str) -> None:
    """
    This function has the objective of sabe the created dictionary file into a
    json file format to be later utilized.

    Keyword Arguments:
    dict_name: dictionary with .bib references
    save_file_name_loc: string containing the location to save the file and the name to be utilized

    Return:
    None
    """

    with open(save_file_name_loc + ".json", "w", encoding="UTF-8") as wfile:
        json.dump(dict_name, wfile, indent=4, ensure_ascii=False)

    return None


def _save_file_safe(dict_name: dict, save_file_name_loc: str) -> None:
    """
    This function has the objective of sabe the created dictionary file into a
    json file format to be later utilized.

    Keyword Arguments:
    dict_name: dictionary with .bib references
    save_file_name_loc: string containing the location to save the file and the name to be utilized
    without the extesion (it is automatically sabed as .json)

    Return:
    None
    """

    validation = _processed_confirmation()

    if validation == "N":
        print("File not saved.")
        return None

    if validation == "Y":

        tmp_name = save_file_name_loc + ".json"

        if "/" in save_file_name_loc:
            tmp_file_name = save_file_name_loc[::-1].split("/", 1)[::-1][1]
            file_names = next(os.walk(tmp_file_name))[2]

            for name in file_names:
                tmp_name = name + ".json"
                if tmp_name in tmp_file_name[0]:
                    print("File with name already saved. Please select another name.")
                    return None

        elif tmp_name in os.listdir(os.curdir):
            print("File with name already saved. Please select another name.")
            return None

        with open(save_file_name_loc + ".json", "w", encoding="UTF-8") as wfile:
            json.dump(dict_name, wfile, indent=4, ensure_ascii=False)

        print(f"File {save_file_name_loc}.json has been saved.")

    return None


def load_json_file(references_location: str) -> dict:
    """
    This function has the objective of loading a json file into a dictonary
    to be utilized in different analysis.

    Keyword Arguments:
    references_location: string containing the .json file to be loaded

    Return:
    references: dicitonary
    """
    with open(references_location, "r", encoding="utf-8") as rfile:
        references = json.load(rfile)

    return references


def j_print(dictonary: dict, indent: int = 4, ensure_ascii: bool = False) -> None:
    # TODO: Include description for this function.
    print(json.dumps(dictonary, indent=indent, ensure_ascii=ensure_ascii))
    return None
