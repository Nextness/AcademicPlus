import src.CommonOperations as cmnops
import src.DataStructures as Struct
import os


def _load_bib_files_from_folder(folder_name: str) -> tuple[list[str], list[str]]:
    """
    TODO: Update description for this function.
    This function has to objetive of loading all .bib files from a folder
    and parse them into a string to be able to adjust the information it contains.

    Keyword arguments:
    folder_name: file location as a string

    Return:
    file_data: concatenation of all .bib data in a string
    """
    all_data = list()
    list_file_name = list()
    folder = os.walk(folder_name)
    main_folder = next(folder)
    count_all_files = main_folder[2]

    for file in count_all_files:
        validation = ".bib" == file[-4:]
        if validation:
            with open(folder_name + file, "r", encoding="UTF-8") as rfile:
                file_data = rfile.read()
                all_data += [file_data]
                list_file_name += [file]
        else:
            continue

    return all_data, list_file_name


def _replace_unnecessary_charcters(all_data: list[str]) -> list[str]:
    """
    TODO: Update description for this function.
    This function has the objective of replacing characters from the entire .bib string
    to be able to continue processing the data. This step is basically a pre-processing step
    for the next steps.

    Keyword arguments:
    all_data: string formatted reference

    Return:
    all_data: pre-processed concatenation of all .bib data in a string
    """
    replace_dic = {
        "@ARTICLE": "@article",
        "[": "",
        "]": "",
        "{": "",
        "}": "",
        "https://doi.org/": ""
    }

    for idx, _ in enumerate(all_data):
        for key, value in replace_dic.items():
            all_data[idx] = all_data[idx].replace(key, value)

    return all_data


def _split_all_data(all_data: list[str], file_name: list[str]) -> list[str]:
    """
    TODO: Update description for this function.
    This function has the objective of splitting the pre-processed reference string
    into a list utilizing a specific token called @article.

    NOTE: this step only considers @articles. Other .bib reference formats are not supported
    and might cause problems if contained in the referencial.

    Keyword arguments:
    all_data_str: pre-processed string formatted reference

    Return:
    data_split: list of all the references splitted by "@article"
    """

    data_split = list()
    for idx1, _ in enumerate(zip(all_data, file_name)):
        data_split += [all_data[idx1].split("@article")]
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
            data_split[idx1][idx2].append(["originalfile", file_name[idx1]])

    return data_split


def _transform_list_to_BibDataFormat(dict_key: str, dict_value: str | int,
                                     data_entry: Struct.BibDataFormat) -> Struct.BibDataFormat:

    # TODO: include description of this function.
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
        data_entry.Abstract = dict_value
    elif dict_key == "originalfile":
        data_entry.Original_File_Name = dict_value

    return data_entry


def _structure_data_split(data_split: list[str]) -> dict[dict[str]]:
    """
    TODO: Update description for this function.
    This function has the objective of constructing the dictonary based on a
    parsed list with the data from .bib file.

    Keyword Arguments:
    data_split: list with the information from the .bib file already preprocessed

    Return:
    parser_result: Dictionary with all entries and their description
    """

    iterator = 0
    parser_result = dict()

    for file in data_split:

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
    This function has the objective of parse all data from a folder location and save it
    in a specific location as a .json file to be utilized for later analysis.

    Keyword Arguments:
    folder_name: folder in which all .bib files are stored
    save_file_name_loc: string containing the location to save the file and the name to be utilized

    Return:
    None
    """
    load_bib, orignal_files = _load_bib_files_from_folder(folder_name)
    unnecessary_chars = _replace_unnecessary_charcters(load_bib)
    split_data = _split_all_data(unnecessary_chars, orignal_files)
    structure_data = _structure_data_split(split_data)
    cmnops._save_file_safe(structure_data, save_file_name_loc)

    return None
