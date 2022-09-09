import os
import hashlib as hs
import AcademicPlus.CommonOperations as cmnops

NOT_AVAILABLE = "NOT AVAILABLE"


def _load_bib_files_from_folder(folder_name: str) -> list:
    """
    This function has to objetive of loading all .bib files from a folder
    and parse them into a string to be able to adjust the information it contains.

    Keyword arguments:
    folder_name: file location as a string

    Return:
    file_data: concatenation of all .bib data in a string
    """
    all_data = []
    folder = os.walk(folder_name)
    main_folder = next(folder)
    count_all_files = main_folder[2]

    for file in count_all_files:
        if ".bib" in file:
            with open(folder_name + file, "r", encoding="UTF-8") as rfile:
                file_data = rfile.read()
                all_data = all_data + [file_data]
        else:
            continue

    return str(all_data)


def _replace_unnecessary_charcters(all_data: str) -> str:
    """
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

    for key, value in replace_dic.items():
        all_data = all_data.replace(key, value)

    all_data = all_data.encode('UTF-8', 'ignore').decode("utf-8")
    return all_data


def _split_all_data(all_data_str: str) -> list:
    """
    This function has the objective of splitting the pre-processed reference string
    into a list utilizing a specific token called @article.

    NOTE: this step only considers @articles. Other .bib reference formats are not supported
    and might cause problems if contained in the referencial.

    Keyword arguments:
    all_data_str: pre-processed string formatted reference

    Return:
    data_split_topic: list of all the references splitted by "@article"
    """

    data_split = all_data_str.split("@article")

    data_split_topic = []
    for item in data_split:
        data_split_topic = [str(item).split("\\n")] + data_split_topic

    for item in data_split_topic:
        idx_i = data_split_topic.index(item)
        for topic in item:
            idx_t = item.index(topic)
            data_split_topic[idx_i][idx_t] = str(topic).split("=")
            content_length = len(data_split_topic[idx_i][idx_t])

            if content_length < 2:
                continue

            data_split_topic[idx_i][idx_t][0] = data_split_topic[idx_i][idx_t][0].replace(
                " ", "")
            if data_split_topic[idx_i][idx_t][1][0] == " ":
                data_split_topic[idx_i][idx_t][1] = data_split_topic[idx_i][idx_t][1].replace(
                    " ", "", 1)

    return data_split_topic


def _hash_doi(doi: str) -> str:
    """
    This function has the objective of hashing the DOI to
    make it easier to do computations later.

    Keyword Arguments:
    doi: str

    Return:
    hash_content: hexadecimal str
    """

    hash_content = hs.sha1()
    hash_content.update(str(doi).encode('utf8'))

    return hash_content.hexdigest()


def _structure_data_split(data_split_topic: list) -> dict:
    """
    This function has the objective of constructing the dictonary based on a
    parsed list with the data from .bib file.

    Keyword Arguments:
    data_split_topic: list with the information from the .bib file already preprocessed

    Return:
    parser_result: Dictionary with all entries and their description
    """

    idx = 0
    parser_result = {}
    data_split_topic.remove([['"']])
    for item in data_split_topic:
        tmp_dict = {}
        for topic in item:
            if len(topic) < 2:
                continue

            key = str(topic[0])
            value = str(topic[1])
            if key == "doi":
                tmp_dict["DOI"] = value[::-1].replace(",", "", 1)[::-1]
                tmp_dict["Hashed DOI"] = _hash_doi(value)
                continue

            value = str(topic[1]).upper()
            if key != "keywords" or key != "abstract":
                value = value.replace(",", "")
            elif key == "keywords":
                # This inversts the value to remove the first
                # occurance of the coma
                value = value[::-1].replace(",", "", 1)[::-1]
            elif key == "abstract":
                # This inversts the value to remove the first
                # occurance of the coma
                value = value[::-1].replace(",", "", 1)[::-1]

            if key == "title":
                tmp_dict["Title"] = value
                continue
            if key == "journal":
                tmp_dict["Journal"] = value
                continue
            if key == "volume":
                tmp_dict["Volume"] = value
                continue
            if key == "pages":
                tmp_dict["Pages"] = value
                continue
            if key == "year":
                tmp_dict["Year"] = int(value)
                continue
            if key == "issn":
                tmp_dict["ISSN"] = value
                continue
            if key == "url":
                tmp_dict["URL"] = value
                continue
            if key == "author":
                tmp_dict["Author"] = value
                continue
            if key == "keywords":
                tmp_dict["Keywords"] = value
                continue
            if key == "abstract":
                tmp_dict["Abstract"] = value
                continue
        parser_result[idx] = tmp_dict
        idx += 1

    return parser_result


def _format_structure_data(parser_result: dict) -> dict:
    """
    This function has the objective of including fields which could not
    be included as they were missing in the .bib file.

    Keyword Arguments:
    parser_result: Dictonary with .bib references already constructed

    Return:
    parser_result: Dictonary with .bib references with NOT_AVAILABLE included
    in the missing fields
    """

    for item in parser_result:
        print(parser_result[item])
        if "Title" not in parser_result[item]:
            parser_result[item]["Title"] = NOT_AVAILABLE
        if "Journal" not in parser_result[item]:
            parser_result[item]["Journal"] = NOT_AVAILABLE
        if "Volume" not in parser_result[item]:
            parser_result[item]["Volume"] = NOT_AVAILABLE
        if "Year" not in parser_result[item]:
            parser_result[item]["Year"] = NOT_AVAILABLE
        if "Pages" not in parser_result[item]:
            parser_result[item]["Pages"] = NOT_AVAILABLE
        if "ISSN" not in parser_result[item]:
            parser_result[item]["ISSN"] = NOT_AVAILABLE
        if "DOI" not in parser_result[item]:
            parser_result[item]["DOI"] = NOT_AVAILABLE
            parser_result[item]["Hashed DOI"] = NOT_AVAILABLE
        if "URL" not in parser_result[item]:
            parser_result[item]["URL"] = NOT_AVAILABLE
        if "Author" not in parser_result[item]:
            parser_result[item]["Author"] = NOT_AVAILABLE
        if "Keywords" not in parser_result[item]:
            parser_result[item]["Keywords"] = NOT_AVAILABLE
        if "Abstract" not in parser_result[item]:
            parser_result[item]["Abstract"] = NOT_AVAILABLE
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
    load_bib = _load_bib_files_from_folder(folder_name)
    unnecessary_chars = _replace_unnecessary_charcters(load_bib)
    split_data = _split_all_data(unnecessary_chars)
    structure_data = _structure_data_split(split_data)
    formatted_dict = _format_structure_data(structure_data)
    cmnops._save_file_safe(formatted_dict, save_file_name_loc)

    return None
