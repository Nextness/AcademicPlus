# ===================================================== #
# =               ~~~~ < Imports > ~~~~                 #
# ===================================================== #

import src.Data.Structures as Struct
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
    @StartDocumentation
    ==========================================================================================
    [Tags]
    | {IsMaintained} True
    | {IsPrivate} False
    | {IsDemoCompliant} False
    | {ToBeDeprecated} False
    ==========================================================================================
    [Description] 
    | This function has the objective of hashing values for
    | later usage. The return will always be in hexadecimal.
    ==========================================================================================
    [Argument]
    | {Variable} str::hashable_value
    | {Definition} Value to be hashed.
    ==========================================================================================
    [Exceptions]
    | : 
    ==========================================================================================
    [Return]
    | {Variable} str::hash_content
    | {Text Definition} Hashed value using SHA1.
    ==========================================================================================
    [Video Demonstration]
    | {U0RL} url.
    | {VideoVersion} int
    | {Duration} HH:MM:SS
    | {MinimumQuality} 1080p =< #
    | {PublicationDate} YYYY-MM-DD
    | {FollowsDemonstrationCriteria} bool
    | {URL_HASH} hashed_url.
    ==========================================================================================
    @EndDocumentation
    """
    # try:
        # if not isinstance(hashable_value, str):
        #     raise #Include error
    hash_content = hs.sha1()
    hash_content.update(str(hashable_value).encode('utf8'))

    return str(hash_content.hexdigest())

    # except #Include error as err:
    #     raise err


def test():
    """
    @StartDocumentation
    ==========================================================================================
    [Tags]
    | {IsMaintained} True
    | {IsPrivate} False
    | {IsDemoCompliant} Flase
    | {ToBeDeprecated} False
    ==========================================================================================
    [Deprecation Info]
    | {Date} YYYY-MM-DD
    | {Reason} sdfsfsf
    | {Replacement} asfasfasfa
    ==========================================================================================
    [Warning]
    | {Warning_1} Description for the warning. It can be 
    | also multiline.
    | {Warning_2} Description for the warning. It can be
    | also multiline.
    ==========================================================================================
    [Description]
    | asdafasf
    ==========================================================================================
    [Arguments]
    | <type::argument>
    | {Definition} Explanation of the argument.
    |   -> FLAG_VALUE_1: Meaning of the flag.
    |   -> FLAG_VALUE_2: Meaning of the flag.
    |   -> FLAG_VALUE_3: Meaning of the flag.
    ==========================================================================================
    [Exceptions]
    | {ValueError_1} Description of the error and what may cause it.
    | {ValueError_2} Description of the error and what may cause it.
    ==========================================================================================
    [Return]
    | <type::return_value>
    | {Definition} Explanation of the return.
    |   -> RETURN_VALUE_1: Meaning of this return value.
    |   -> RETURN_VALUE_2: Meaning of this return value.
    ==========================================================================================
    [Video Demonstration]
    | {URL} youtube-url
    | {HASH} youtube-url SHA1 value
    | {VideoVersion} int
    | {Duration} HH:MM:SS
    | {MinimumQuality} 1080p
    | {PublicationDate} YYYY-MM-DD
    ==========================================================================================
    [References]
    | {URL} reference-url
    | {HASH} reference-url SHA1 value
    | {AccessDate} YYYY-MM-DD
    | {Title} title
    | {Auhtors} FirstName LastName, FirstName LastName, ...
    ==========================================================================================
    @EndDocumentation
    """
    pass



def _save_file_unsafe(dict_name: dict, save_file_name_loc: str) -> None | int:
    """
    #TODO: Fix this try except block to actually work and give relevant info + validate if the format .json is provided or not, and act upon that validation.

    [Tags]
    | : @IsMaintained <True>
    | : @IsPrivate <True>
    | : @IsDemoCompliant <False>
    | : @ToBeDeprecated <False>
    | : @IsDeprecated <False>

    [Exceptions]
    | :

    [Warning] 
    | : This functions will override any data in the specified file
    | : and will not validate beforehand.
    
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
    #TODO: Fix this try except block to actually work and give relevant info + validate if the format .json is provided or not, and act upon that validation.

    [Tags]
    | : @IsMaintained <True>
    | : @IsPrivate <True>
    | : @IsDemoCompliant <False>
    | : @ToBeDeprecated <False>
    | : @IsDeprecated <False>

    [Warning] 
    | : Private funtion: Do not use it.

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

    if dict_name is None:
        dict_name = {}

    with open(save_file_name_loc + ".json", "w", encoding="UTF-8") as wfile:
        json.dump(dict_name, wfile, indent=4, ensure_ascii=False)

    print(f"File {save_file_name_loc}.json has been saved.")

    return 0


def load_json_file(file_location: str) -> dict:
    """
    [Tags]
    | : @IsMaintained <True>
    | : @IsPrivate <False>
    | : @IsDemoCompliant <False>
    | : @ToBeDeprecated <False>
    | : @IsDeprecated <False>

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
    [Tags]
    | : @IsMaintained <True>
    | : @IsPrivate <False>
    | : @IsDemoCompliant <False>
    | : @ToBeDeprecated <False>
    | : @IsDeprecated <False>

    [Description] 
    | : #TODO: Include description for this function.

    [Argument]
    | : <dict::dictonary>
    | : (Definition) Dictionary to be pretty printed.

    [Return]
    | : <None::None>
    | : (Definition) Successfully printed.
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
    | : #TODO: Include documentation.
    """
    return asdict(input)


def BibDataFormat_to_dict(input: Struct.BibDataFormat) -> dict[str]:
    """
    [Tags]
    | : @IsMaintained <True>
    | : @IsPrivate <False>
    | : @IsDemoCompliant <False>
    | : @ToBeDeprecated <False>
    | : @IsDeprecated <False>

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
