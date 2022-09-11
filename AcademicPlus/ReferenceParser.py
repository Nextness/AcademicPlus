import AcademicPlus.CommonOperations as cmnops
import AcademicPlus.DataStructures as Struct
import hashlib as hs
import os


def _load_bib_files_from_folder(folder_name: str) -> list:
    """
    This function has to objetive of loading all .bib files from a folder
    and parse them into a string to be able to adjust the information it contains.

    Keyword arguments:
    folder_name: file location as a string

    Return:
    file_data: concatenation of all .bib data in a string
    """
    all_data = list()
    folder = os.walk(folder_name)
    main_folder = next(folder)
    count_all_files = main_folder[2]

    for file in count_all_files:
        validation = ".bib" == file[-4:]
        if validation:
            with open(folder_name + file, "r", encoding="UTF-8") as rfile:
                file_data = rfile.read()
                all_data += [file_data]
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

    all_data = all_data.encode('UTF-8', 'ignore').decode("UTF-8")
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

    data_split_topic = list()
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
        data_entry.Hashed_DOI = _hash_doi(dict_value)
    elif dict_key == "url":
        data_entry.URL = dict_value
    elif dict_key == "author":
        data_entry.Author = dict_value
    elif dict_key == "keywords":
        data_entry.Keywords = dict_value
    elif dict_key == "abstract":
        data_entry.Abstract = dict_value

    return data_entry


def _structure_data_split(data_split_topic: list) -> dict:
    """
    This function has the objective of constructing the dictonary based on a
    parsed list with the data from .bib file.

    Keyword Arguments:
    data_split_topic: list with the information from the .bib file already preprocessed

    Return:
    parser_result: Dictionary with all entries and their description
    """

    parser_result = dict()
    for idx, item in enumerate(data_split_topic):

        entry = Struct.BibDataFormat()
        for topic in item:

            topic = str(topic)
            if topic[0] == '':
                continue

            if len(topic) == 1:
                entry.Default_Key = topic[0].replace(",", "")
                continue

            key, value = topic[0].casefold(), topic[1]
            if value[-1] == ",":
                value = value[::-1].replace(",", "", 1)[::-1]

            entry = _transform_list_to_BibDataFormat(key, value, entry)

        parser_result[idx] = cmnops.BibDataFormat_to_dict(entry)

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
    cmnops._save_file_safe(structure_data, save_file_name_loc)

    return None
