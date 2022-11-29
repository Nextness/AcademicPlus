<<<<<<<< HEAD:academicplus/reference/parser.py

# ===================================================== #
#                 ~~~~ < Imports > ~~~~                 #
# ===================================================== #

import academicplus.Common.Operations as cmnops
import academicplus.Data.Structures as Struct
import os


# ===================================================== #
#                ~~~~ < Functions > ~~~~                #
# ===================================================== #

def _load_bib_files_from_folder(folder_name: list[str]) -> tuple[list[str], list[str]]:
    """
    [tags v1.0]: *maintained *private;
    [warning v1.0]: Private funtion - Do not use it;
    [description v1.0]: This function loads all .bib files from a specified folder - 
    The data is stored into a list of strings which is used in another step - A list
    with all the original file names is also generated for the same purpose;
    [arg_val v1.0] strfolder_name: Folder with .bib files location;
    [ret_val v1.0] list[str] all_data: List with all .bib data;
    [ret_val v1.0] list[str] list_file_name: List with all original file names;
    """
    return_list = list()
    return_file_names_list = list()

    folder = os.walk(folder_name)
    main_folder = next(folder)
    count_all_files = main_folder[2]

    for file in count_all_files:
        if file[-4:] == ".bib":
            with open(folder_name + file, "r", encoding="UTF-8") as rfile:
                file_data = rfile.read()
                return_list += [file_data]
                return_file_names_list += [file]

    return return_list, return_file_names_list


def _replace_unnecessary_charcters(list_references: list[str]) -> list[str]:
    """ 
    [tags v1.0]: *maintained *private;
    [warning v1.0]: Private funtion - Do not use it;
    [description v1.0]: This function replaces unnecessary characters from the
    .bib list, generated on a previous step, to continue processing the data;
    [arg_val v1.0] list[str] list_references: List with all .bib data;
    [ret_val v1.0] list[str] list_references: List with all .bib pre-processed data;
    """
    replace_dic = {
        "@ARTICLE": "@article",
        "[": "",
        "]": "",
        "{": "",
        "}": "",
        "https://doi.org/": ""
    }

    for idx, _ in enumerate(list_references):
        for key, value in replace_dic.items():
            list_references[idx] = list_references[idx].replace(key, value)

    return list_references


def _split_all_data(list_references: list[str], list_file_name: list[str]) -> list[str]:
    """
    [tags v1.0]: *maintained *private;
    [warning v1.0]: Private funtion - Do not use it;
    [description v1.0]: This function has the objective of splitting the pre-processed
    .bib list into a multiple items - This function only considers @articles;
    [arg_val v1.0] str list_references: List with all .bib pre-processed data;
    [arg_val v1.0] str list_file_name: List with all original file names;
    [ret_val v1.0] list[str] data_split: List of all the references splitted by @article;
    """

    data_split = list()
    for idx1, _ in enumerate(zip(list_references, list_file_name)):
        data_split += [list_references[idx1].split("@article")]
        while "" in data_split[idx1]:
            data_split[idx1].remove("")

        for idx2, _ in enumerate(data_split[idx1]):
            if data_split[idx1][idx2] == '\n':
                del data_split[idx1][idx2]
            data_split[idx1][idx2] = data_split[idx1][idx2].split("\n")
            while "" in data_split[idx1][idx2]:
                data_split[idx1][idx2].remove("")

            for idx3, topic in enumerate(data_split[idx1][idx2]):
                if "url" in data_split[idx1][idx2][idx3]:
                    data_split[idx1][idx2][idx3] = topic.split("=", 1)
                else:
                    data_split[idx1][idx2][idx3] = topic.split("=")

            data_split[idx1][idx2].append(["originalfile", list_file_name[idx1]])

    return data_split


def _transform_list_to_BibDataFormat(dict_key: str, dict_value: str | int, data_entry: Struct.BibDataFormat) -> Struct.BibDataFormat:
    """
    #TODO: Maybe refactor this Function.
    [Warning] 
    | : Private funtion: Do not use it.

    [Description] 
    | : This function converts a key and value pair into a data structure
    | : which can be more easily manibulated.

    [Note]
    | This function not only is private but also, if python had the option,
    | an inline function.
    
    [Argument]
    | : <str::dict_key> 
    | : (Definition) Dictonary key which will be used to map into the BibDataFormat.
    | :
    | : <(str|int)::dict_value> 
    | : (Definition) Dictonary value which will be mapped.
    | : 
    | : <Struct.BibDataFormat::data_entry> 
    | : (Definition) Data structure which is being mapped into.

    [Return]
    | : <Struct.BibDataFormat::data_entry> 
    | : (Definition) Mapped structure.
    """
    if dict_key == "title":
        data_entry.Title = dict_value
    elif dict_key == "journal":
        data_entry.Journal = dict_value
    elif dict_key == "volume":
        data_entry.Volume = dict_value
    elif dict_key == "pages":
        data_entry.Pages = dict_value
    elif dict_key == "year":
        data_entry.Year = dict_value
    elif dict_key == "issn":
        data_entry.ISSN = dict_value
    elif dict_key == "doi":
        data_entry.DOI = dict_value
        data_entry.Hashed_DOI = cmnops.hash_string(dict_value)
    elif dict_key == "url":
        data_entry.URL = dict_value
    elif dict_key == "author":
        dict_value = dict_value.split(" and ")
        data_entry.Author = dict_value
    elif dict_key == "keywords":
        if "," in dict_value:
            dict_value = dict_value.replace(",", ";")
        dict_value = dict_value.split(";")
        for idx, keyword in enumerate(dict_value):
            keyword = keyword.lstrip()
            dict_value[idx] = keyword
        data_entry.Keywords = dict_value
    elif dict_key == "abstract":
        dict_value = dict_value.replace("\n", "")
        data_entry.Abstract = dict_value
    elif dict_key == "originalfile":
        data_entry.Original_File_Name = dict_value

    return data_entry


def _structure_data_split(list_references: list[str]) -> dict[dict[str]]:
    """
    [Warning] 
    | : Private funtion: Do not use it.

    [Description] 
    | : This function constructs a dictonary based on a
    | : parsed list with the data from a pre-processed .bib file.

    [Argument]
    | : <list[str]::data_split> 
    | : (Definition) List of all the references splitted by "@article".

    [Return]
    | : <dict[dict[str]]::parser_result>
    | : (Definition) Dictionary with all entries and their description.
    """

    iterator = 0
    parser_result = dict()

    for file in list_references:

        for item in file:
            entry = Struct.BibDataFormat()

            for topic in item:
                if len(topic) == 1:
                    entry.Default_Key = topic[0].replace(",", "")
                    continue

                key, value = topic[0].casefold(), topic[1]
                key, value = key.strip(), value.strip()

                if value[-1] == ",":
                    value = value[::-1].replace(",", "", 1)[::-1]

                entry = _transform_list_to_BibDataFormat(key, value, entry)

            parser_result[iterator] = cmnops.BibDataFormat_to_dict(entry)
            iterator += 1

    return parser_result


def parse_save_bib_references_to_file(folder_name: str, save_file_name_loc: str) -> None:
    """
    [Description]
    | : This function has the objective of parse all data from a folder location and save it
    | : in a specific location as a .json file.

    [Argument]
    | : <str::folder_name>
    | : (Definition) Folder with .bib files location.
    | :
    | : <str::save_file_name_loc>
    | : (Definition) File location to save parsed data.

    [Return]
    | : <None::None>
    | : (Definition) Succesfully parsed file.
    """
    loaded_references, orignal_files = _load_bib_files_from_folder(folder_name)
    remove_chars = _replace_unnecessary_charcters(loaded_references)
    split_data = _split_all_data(remove_chars, orignal_files)
    structure_data = _structure_data_split(split_data)
    cmnops._save_file_safe(structure_data, save_file_name_loc)

    return None
========
# ===================================================== #
#                 ~~~~ < Imports > ~~~~                 #
# ===================================================== #

import src.Common.Operations as cmnops
import src.Data.Structures as Struct
import os


# ===================================================== #
#                ~~~~ < Functions > ~~~~                #
# ===================================================== #

def _load_bib_files_from_folder(folder_name: list[str]) -> tuple[list[str], list[str]]:
    """
    [Warning] 
    | : Private funtion: Do not use it.

    [Description] 
    | : This function loads all .bib files from a specified folder. The data is stored
    | : into a list of strings which is used in another step. A list with all the original file
    | : names is also generated for the same purpose.

    [Argument]
    | : <str::folder_name>
    | : (Definition) Folder with .bib files location.

    [Return]
    | : <list[str]::all_data> 
    | : (Definition) List with all .bib data.
    | : 
    | : <list[str]::list_file_name>
    | : (Definition) List with all original file names.
    """
    return_list = list()
    return_file_names_list = list()

    folder = os.walk(folder_name)
    main_folder = next(folder)
    count_all_files = main_folder[2]

    for file in count_all_files:
        if file[-4:] == ".bib":
            with open(folder_name + file, "r", encoding="UTF-8") as rfile:
                file_data = rfile.read()
                return_list += [file_data]
                return_file_names_list += [file]

    return return_list, return_file_names_list


def _replace_unnecessary_charcters(list_references: list[str]) -> list[str]:
    """ 
    [Warning]
    | : Private funtion: Do not use it.

    [Description] 
    | : This function replaces unnecessary characters from the .bib list, generated on a 
    | : previous step, to continue processing the data.

    [Argument]
    | : <list[str]::list_references> 
    | : (Definition) List with all .bib data.

    [Return]
    | : <list[str]::list_references> 
    | : (Definition) List with all .bib pre-processed data.
    """
    replace_dic = {
        "@ARTICLE": "@article",
        "[": "",
        "]": "",
        "{": "",
        "}": "",
        "https://doi.org/": ""
    }

    for idx, _ in enumerate(list_references):
        for key, value in replace_dic.items():
            list_references[idx] = list_references[idx].replace(key, value)

    return list_references


def _split_all_data(list_references: list[str], list_file_name: list[str]) -> list[str]:
    """
    [Warning]
    | : Private funtion: Do not use it.

    [Description] 
    | : This function has the objective of splitting the pre-processed .bib list
    | : into a multiple items.

    [Note] 
    | : This function only considers @articles. Other .bib reference formats are not supported
    | : and might cause problems if contained in the referencial.

    [Argument] 
    | : <str::list_references> 
    | : (Definition) List with all .bib pre-processed data.
    | :
    | : <str::list_file_name>
    | : (Definition) List with all original file names.

    [Return]
    | : <list[str]::data_split>
    | : (Definition) List of all the references splitted by "@article".
    """

    data_split = list()
    for idx1, _ in enumerate(zip(list_references, list_file_name)):
        data_split += [list_references[idx1].split("@article")]
        while "" in data_split[idx1]:
            data_split[idx1].remove("")

        for idx2, _ in enumerate(data_split[idx1]):
            if data_split[idx1][idx2] == '\n':
                del data_split[idx1][idx2]
            data_split[idx1][idx2] = data_split[idx1][idx2].split("\n")
            while "" in data_split[idx1][idx2]:
                data_split[idx1][idx2].remove("")

            for idx3, topic in enumerate(data_split[idx1][idx2]):
                if "url" in data_split[idx1][idx2][idx3]:
                    data_split[idx1][idx2][idx3] = topic.split("=", 1)
                else:
                    data_split[idx1][idx2][idx3] = topic.split("=")

            data_split[idx1][idx2].append(["originalfile", list_file_name[idx1]])

    return data_split


def _transform_list_to_BibDataFormat(dict_key: str, dict_value: str | int, data_entry: Struct.BibDataFormat) -> Struct.BibDataFormat:
    """
    #TODO: Maybe refactor this Function.
    [Warning] 
    | : Private funtion: Do not use it.

    [Description] 
    | : This function converts a key and value pair into a data structure
    | : which can be more easily manibulated.

    [Note]
    | This function not only is private but also, if python had the option,
    | an inline function.
    
    [Argument]
    | : <str::dict_key> 
    | : (Definition) Dictonary key which will be used to map into the BibDataFormat.
    | :
    | : <(str|int)::dict_value> 
    | : (Definition) Dictonary value which will be mapped.
    | : 
    | : <Struct.BibDataFormat::data_entry> 
    | : (Definition) Data structure which is being mapped into.

    [Return]
    | : <Struct.BibDataFormat::data_entry> 
    | : (Definition) Mapped structure.
    """
    if dict_key == "title":
        data_entry.Title = dict_value
    elif dict_key == "journal":
        data_entry.Journal = dict_value
    elif dict_key == "volume":
        data_entry.Volume = dict_value
    elif dict_key == "pages":
        data_entry.Pages = dict_value
    elif dict_key == "year":
        data_entry.Year = dict_value
    elif dict_key == "issn":
        data_entry.ISSN = dict_value
    elif dict_key == "doi":
        data_entry.DOI = dict_value
        data_entry.Hashed_DOI = cmnops._hash_string(dict_value)
    elif dict_key == "url":
        data_entry.URL = dict_value
    elif dict_key == "author":
        dict_value = dict_value.split(" and ")
        data_entry.Author = dict_value
    elif dict_key == "keywords":
        if "," in dict_value:
            dict_value = dict_value.replace(",", ";")
        dict_value = dict_value.split(";")
        for idx, keyword in enumerate(dict_value):
            keyword = keyword.lstrip()
            dict_value[idx] = keyword
        data_entry.Keywords = dict_value
    elif dict_key == "abstract":
        dict_value = dict_value.replace("\n", "")
        data_entry.Abstract = dict_value
    elif dict_key == "originalfile":
        data_entry.Original_File_Name = dict_value

    return data_entry


def _structure_data_split(list_references: list[str]) -> dict[dict[str]]:
    """
    [Warning] 
    | : Private funtion: Do not use it.

    [Description] 
    | : This function constructs a dictonary based on a
    | : parsed list with the data from a pre-processed .bib file.

    [Argument]
    | : <list[str]::data_split> 
    | : (Definition) List of all the references splitted by "@article".

    [Return]
    | : <dict[dict[str]]::parser_result>
    | : (Definition) Dictionary with all entries and their description.
    """

    iterator = 0
    parser_result = dict()

    for file in list_references:

        for item in file:
            entry = Struct.BibDataFormat()

            for topic in item:
                if len(topic) == 1:
                    entry.Default_Key = topic[0].replace(",", "")
                    continue

                key, value = topic[0].casefold(), topic[1]
                key, value = key.strip(), value.strip()

                if value[-1] == ",":
                    value = value[::-1].replace(",", "", 1)[::-1]

                entry = _transform_list_to_BibDataFormat(key, value, entry)

            parser_result[iterator] = cmnops.BibDataFormat_to_dict(entry)
            iterator += 1

    return parser_result


def parse_save_bib_references_to_file(folder_name: str, save_file_name_loc: str) -> None:
    """
    [Description]
    | : This function has the objective of parse all data from a folder location and save it
    | : in a specific location as a .json file.

    [Argument]
    | : <str::folder_name>
    | : (Definition) Folder with .bib files location.
    | :
    | : <str::save_file_name_loc>
    | : (Definition) File location to save parsed data.

    [Return]
    | : <None::None>
    | : (Definition) Succesfully parsed file.
    """
    loaded_references, orignal_files = _load_bib_files_from_folder(folder_name)
    remove_chars = _replace_unnecessary_charcters(loaded_references)
    split_data = _split_all_data(remove_chars, orignal_files)
    structure_data = _structure_data_split(split_data)
    cmnops._save_file_safe(structure_data, save_file_name_loc)

    return None
>>>>>>>> d39f3a1cd4c740e39d4523e310b3d69979c6b16f:src/Reference/Parser.py
