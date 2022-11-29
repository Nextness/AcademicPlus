# ===================================================== #
# =               ~~~~ < Imports > ~~~~                 #
# ===================================================== #

import academicplus.data.structures as Struct
from dataclasses import asdict
from typing import Any
import hashlib as hs
import json
import os


# ===================================================== #
#                ~~~~ < Functions > ~~~~                #
# ===================================================== #

def hash_string(hashable_value: str) -> str:
    """
    [tags v1.0]: *maintained;
    [description v1.0]: This function has the objective of hashing values for later usage - the return will always be in hexadecimal;
    [arg_val v1.0] str hashable_value: Value to be hashed;
    [ret_val v1.0] str hash_content: Hashed value using SHA1;
    """
    # try:
        # if not isinstance(hashable_value, str):
        #     raise #Include error
    hash_content = hs.sha1()
    hash_content.update(str(hashable_value).encode('utf8'))

    return str(hash_content.hexdigest())

    # except #Include error as err:
    #     raise err


def _save_file_unsafe(dict_name: dict, save_file_name_loc: str) -> None | int:
    """
    # TODO: Fix this try except block to actually work and give 
    # relevant info + validate if the format .json is provided or
    # not, and act upon that validation.

    [tags v1.0]: *maintained *private;
    [warning v1.0]: Private funtion - Do not use it - This functions will override any data in the specified file
    and will not validate beforehand;
    [description v1.0]: This function unsafely saves dictionaries as .json file;
    [arg_val v1.0] dict dict_name: Any dictionary;
    [arg_val v1.0] str save_file_name_loc: File location to save the dictonary;
    [ret_val v1.0] None None: Not succesful save;
    [ret_val v1.0] int 0: Save is successful;
    """
    try:
        if not isinstance(dict_name, dict):
            return None

        with open(f"{save_file_name_loc}", "w", encoding="UTF-8") as wfile:
            json.dump(dict_name, wfile, indent=4, ensure_ascii=False)
    # TODO: Fix exception error.
    except RuntimeError:
        print(f"Not possible to save the file {save_file_name_loc}.")
        return None

    return 0


def _save_file_safe(dict_name: dict, save_file_name_loc: str) -> None | int:
    """
    # TODO: Fix this try except block to actually work and give 
    # relevant info + validate if the format .json is provided or
    # not, and act upon that validation.

    [tags v1.0]: *maintained *private;
    [warning v1.0]: Private funtion - Do not use it;
    [description v1.0]: This function safely saves dictionaries as .json file;
    [arg_val v1.0] dict dict_name: Any dictionary;
    [arg_val v1.0] str save_file_name_loc: File location to save the dictonary;
    [ret_val v1.0] None None: Not succesful save;
    [ret_val v1.0] int 0: Save is successful;
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

    if dict_name is None:
        dict_name = {}

    with open(save_file_name_loc + ".json", "w", encoding="UTF-8") as wfile:
        json.dump(dict_name, wfile, indent=4, ensure_ascii=False)

    print(f"File {save_file_name_loc}.json has been saved.")

    return 0


def load_json_file(file_location: str) -> dict:
    """
    #TODO: Inclue definition for return value.
    [tags v1.0]: *maintained;
    [description v1.0]: This function has the objective of loading a json file into a dictonary to be utilized in different analysis;
    [arg_val v1.0] str file_location: File location;
    [ret_val v1.0] dict return_dict: ;
    """
    with open(file_location, "r", encoding="utf-8") as rfile:
        return_dict = json.load(rfile)

    return return_dict


def j_print(dictonary: dict) -> None:
    """
    #TODO: Include description for this function.
    [tags v1.0]: *maintained;
    [warning v1.0]: ;
    [description v1.0]: ;
    [arg_val v1.0] dict dictonary: Dictionary to be pretty printed;
    [ret_val v1.0] None None: Successfully printed;
    """
    # try:
    #     if not isinstance(dictonary, dict):
    #         raise #error
        
    indent = 4
    ensure_ascii = False
    print(json.dumps(dictonary, indent=indent, ensure_ascii=ensure_ascii))
    return None

    # except #Include error as err:
    #     raise err


def dataclass_to_dict(input: Any):
    """
    #TODO: Include documentation.
    """
    return asdict(input)


def BibDataFormat_to_dict(input: Struct.BibDataFormat) -> dict[str]:
    """
    # TODO: Also update the name of the input variable to be more descriptive
    #TODO: Include description for this function.
    [tags v1.0]: *maintained;
    [description v1.0]: ;
    [arg_val v1.0] Struct.BibDataFormat input: ;
    [ret_val v1.0] dict None: ;
    """
    return asdict(input)


def pr_debug(*args):
    global debug
    if debug: print(*args)
    else: None


def recursive_dict_lookup(key: str, lookup_dict: dict):
    if key in lookup_dict: return True
    for value in lookup_dict.values(): 
        return recursive_dict_lookup(key, value) if isinstance(value, dict) else False
