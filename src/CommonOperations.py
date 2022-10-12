# Imports
import src.DataStructures as Struct
from dataclasses import asdict
import hashlib as hs
import json
import os


# Functions
def _hash_string(hashable_value: str) -> str:
    """
    [Warning] 
    | : Private funtion: Do not use it.

    [Description] 
    | : This function has the objective of hashing values for
    | : later usage. The return will always be in hexadecimal.

    [Argument]
    | : <str::hashable_value>
    | : (Definition) Value to be hashed.

    [Return]
    | : <str::hash_content>
    | : (Definition) Hashed value using SHA1.
    """

    hash_content = hs.sha1()
    hash_content.update(str(hashable_value).encode('utf8'))

    return str(hash_content.hexdigest())


def _save_file_unsafe(dict_name: dict, save_file_name_loc: str) -> None | int:
    """
    #TODO: Fix this try except block to actually work and give relevant info + validate if the format .json is provided or not, and act upon that validation.

    [Warning] 
    | : Private funtion: Do not use it.
    
    [Description] 
    | : This function unsafely saves the a dictionary file
    | : into a .json file format.

    [Argument]
    | : <dict::dict_name>
    | : (Definition) Any dictionary.
    | :
    | : <dict::save_file_name_loc>
    | : (Definition) File location to save the dictonary.

    [Return]
    | : <(None|int)::None>
    | : (Definition) Possible values:
    | :   - None: Not succesful save.
    | :   - 0: Save is successful.
    """
    try:

        if type(dict_name) is not dict:
            return None

        with open(f"{save_file_name_loc}", "w", encoding="UTF-8") as wfile:
            json.dump(dict_name, wfile, indent=4, ensure_ascii=False)

    except RuntimeError:
        print(f"Not possible to save the file {save_file_name_loc}.")
        return None

    return 0


def _save_file_safe(dict_name: dict, save_file_name_loc: str) -> None | int:
    """
    #TODO: Fix this try except block to actually work and give relevant info + validate if the format .json is provided or not, and act upon that validation.

    [Description]
    | : This function safely saves the a dictionary file
    | : into a .json file format.

    [Argument]
    | : <dict::dict_name>
    | : (Definition) Any dictionary.
    | :
    | : <dict::save_file_name_loc>
    | : (Definition) File location to save the dictonary.

    [Return]
    | : <(None|int)::None>
    | : (Definition) Possible values:
    | :   - None: Not succesful save.
    | :   - 0: Save is successful.
    """

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

    return 0


def load_json_file(file_location: str) -> dict:
    """
    #TODO: Fix description.
    [Description] 
    | : This function has the objective of loading a json file into a dictonary
    | : to be utilized in different analysis.

    [Argument]
    | : <str::file_location>
    | : (Definition) File location.

    [Return]
    | : <dict::return_dict>
    | : (Definition)
    """
    with open(file_location, "r", encoding="utf-8") as rfile:
        return_dict = json.load(rfile)

    return return_dict


def j_print(dictonary: dict) -> None:
    """
    [Description] 
    | : #TODO: Include description for this function.

    [Argument]
    | : <dict::dictonary>
    | : (Definition) Dictionary to be pretty printed.

    [Return]
    | : <None::None>
    | : (Definition) Successfully printed.
    """
    indent = 4
    ensure_ascii = False
    print(json.dumps(dictonary, indent=indent, ensure_ascii=ensure_ascii))
    return None


def BibDataFormat_to_dict(input: Struct.BibDataFormat) -> dict[str]:
    """
    # TODO: Also update the name of the input variable to be more descriptive
    [Description] 
    | : #TODO: Include description for this function.

    [Argument]
    | : <Struct.BibDataFormat::input>
    | : (Definition)

    [Return]
    | : <dict::None> 
    | : (Definition)
    """
    return asdict(input)
