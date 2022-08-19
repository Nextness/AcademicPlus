import os
import hashlib as hs
import json
import matplotlib.pyplot as plt

NOT_AVAILABLE = "NOT AVAILABLE"


def _load_bib_files_from_folder(folder_name: str) -> str:
    """
    This function has to objetive of loading all .bib files from a folder
    and parse them into a string to be able to adjust the information it contains.

    Keyword arguments:
    folder_name: file location as a string

    Return:
    all_data: concatenation of all .bib data in a string
    """
    count_all_files = next(os.walk(folder_name))[2]
    number_files = len(count_all_files)
    all_data = []

    for file in range(number_files):
        with open(folder_name + count_all_files[file], "r", encoding="utf8") as rfile:
            file_data = rfile.read()
            all_data = all_data + [file_data]

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
        "}": ""
    }

    for key, value in replace_dic.items():
        all_data = all_data.replace(key, value)

    return all_data


def _split_all_data(all_data_str: str) -> list:
    """
    This function has the objective of splitting the pre-processed reference string
    into a list utilizing a specific token called @article.

    NOTE: this step only considers articles. Other .bib reference formats are not supported
    and might cause problems if contained in the referencial.

    Keyword arguments:
    all_data_str: pre-processed string formatted reference

    Return:
    data_split_topic: list of all the references splitted by "@article"
    """

    data_split = all_data_str.split("@article")
    length_data = len(data_split)

    data_split_topic = []
    for item in range(length_data):
        data_split_topic = [data_split[item].split('\\n')] + data_split_topic

    for item in range(length_data):
        length_topics = len(data_split_topic[item])
        for topic in range(length_topics):
            data_split_topic[item][topic] = data_split_topic[item][topic].split(
                "=")

    for item in range(length_data):
        length_topics = len(data_split_topic[item])
        for topic in range(length_topics):

            length_content = len(data_split_topic[item][topic])
            if length_content < 2:
                continue

            data_split_topic[item][topic][0] = data_split_topic[item][topic][0].replace(
                " ", "")

            if data_split_topic[item][topic][1][0] == " ":
                data_split_topic[item][topic][1] = data_split_topic[item][topic][1].replace(
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

    for item in data_split_topic:
        tmp_construct = {}

        for topic in item:
            length_content = len(topic)

            if length_content < 2:
                continue

            key, value = str(topic[0]), str(topic[1]).upper()

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
                tmp_construct["Title"] = value
                continue
            if key == "journal":
                tmp_construct["Journal"] = value
                continue
            if key == "volume":
                tmp_construct["Volume"] = value
                continue
            if key == "pages":
                tmp_construct["Pages"] = value
                continue
            if key == "year":
                tmp_construct["Year"] = int(value)
                continue
            if key == "issn":
                tmp_construct["ISSN"] = value
                continue
            if key == "doi":
                tmp_construct["DOI"] = value
                tmp_construct["Hashed DOI"] = _hash_doi(value)
                continue
            if key == "url":
                tmp_construct["URL"] = value
                continue
            if key == "author":
                tmp_construct["Author"] = value
                continue
            if key == "keywords":
                tmp_construct["Keywords"] = value
                continue
            if key == "abstract":
                tmp_construct["Abstract"] = value
                continue
        parser_result[idx] = tmp_construct
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


def _save_file(parser_result: dict, save_file_name_loc: str) -> None:
    """
    This function has the objective of sabe the created dictionary file into a
    json file format to be later utilized.

    Keyword Arguments:
    parser_result: dictionary with .bib references
    save_file_name_loc: string containing the location to save the file and the name to be utilized

    Return:
    None
    """

    with open(save_file_name_loc + ".json", "w", encoding="UTF-8") as wfile:
        json.dump(parser_result, wfile, indent=4, ensure_ascii=False)

    return None


def parse_save_bib_references(folder_name: str, save_file_name_loc: str) -> None:
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
    _save_file(formatted_dict, save_file_name_loc)

    return None


def load_json_bib_refences(references_location: str) -> dict:
    """
    This function has the objective of loading a json file into a dictonary
    to be utilized in different analysis.

    Keyword Arguments:
    references_location: string containing the .json file to be loaded

    Return:
    references: dicitonary
    """
    with open(references_location, "r", encoding="utf8") as rfile:
        references = json.load(rfile)

    return references


def references_differential(new_references_location: str, old_references_location: str) -> list:
    """
    This function has the objetive of getting the differential between two a new referencial and 
    a old referencial.

    Keyword Arguments: 
    new_references_location: string containing the new .json file to be compared
    old_references_location: string containing the old .json file to be compared

    Return:
    differential_dict: Dictionary with the entries from the new file which are not
    part of the old file
    """
    differential_dict = {}

    new_references, old_references = load_json_bib_refences(
        new_references_location), load_json_bib_refences(old_references_location)

    for new_item in new_references:
        for old_item in old_references:
            if new_references[new_item]["Hashed DOI"] == old_references[old_item]["Hashed DOI"]:
                differential_dict.update({new_item: new_references[new_item]})

    return differential_dict


def include_notes(references_location: str, hashed_doi: str, note: str) -> None:
    """
    This function has the objective of including notes into the specific entry for later use.

    Keyword Argument:
    references_location: string containing the .json file to be loaded
    hashed_doi: hashed doi as string hexadecimal value to lookup and include the note
    note: the note to be included in the .json file

    Return:
    None
    """

    _references_location = load_json_bib_refences(references_location)
    references_location = references_location.replace(".json", "")

    for item in _references_location:
        if _references_location[item]["Hashed DOI"] == hashed_doi:
            _references_location[item]["Note"] = note
            _save_file(_references_location, references_location)
        else:
            print(f"No article associated to the Hashed DOI: {hashed_doi}.")

    return None


def count_references_by_year(references_location: str) -> dict:
    """
    This function has the objective of counting the number of articles per year
    based on the .json created when parsing the .bib referencial.

    Keyword Arguments:
    references_location: string containing the .json file to be loaded

    Return:
    sorted_count_by_year_dict: dictionary with all count per year of published
    articles in the .json file
    """
    count_by_year_dict, sorted_count_by_year_dict = {}, {}
    _references_location = load_json_bib_refences(references_location)

    for item in _references_location:
        tmp = _references_location[item]["Year"]
        if tmp not in count_by_year_dict:
            count_by_year_dict.update({tmp: 1})
        else:
            count_by_year_dict[tmp] = count_by_year_dict[tmp] + 1

    for key in sorted(count_by_year_dict):
        sorted_count_by_year_dict.update({key: count_by_year_dict[key]})

    return sorted_count_by_year_dict


def count_article_years(references_location: str) -> dict:
    """
    This function has the objective of summing the count of articles per
    year based on the .json created when parsing the .bib referencial.

    Keyword Arguments:
    references_location: string containing the .json file to be loaded

    Return:
    result_dict: dictionary with yearly sum of articles published
    """
    sum_year = 0
    result_dict = {}
    _references_location = count_references_by_year(references_location)

    for _, (idx, item) in enumerate(_references_location.items()):
        sum_year += item
        result_dict.update({idx: sum_year})

    return result_dict


def count_article_years_percentage(references_location: str) -> dict:
    """
    This function has the objective of summing the count of articles per
    year and the percentage it represent over all based on the .json
    created when parsing the .bib referencial.

    Keyword Arguments:
    references_location: string containing the .json file to be loaded

    Return:
    result_dict: dictionary with yearly sum of articles published and the
    percentage it represents overall the article published in the specific
    referencial
    """
    result_dict = {}
    tmp_dict = count_article_years(references_location)

    # This make a list out of a dictionary and gets the last value
    # to use in the division to get the percentage each year represents
    # of the total.
    total_articles = list(tmp_dict.values())[-1]

    for _, (idx, item) in enumerate(tmp_dict.items()):
        sum_percentage = item/total_articles * 100
        result_dict.update(
            {idx: {"Sum": item, "Sum Percentage": sum_percentage}})

    return result_dict


def search_words_in_fields(references_location: str, fields: list[str], words: list[str]) -> dict:
    """
    This function has the objective of looping through the entire .json referencial
    and look in each of the specified fields to search for specific words.

    Keyword Arguments:
    references_location: string containing the .json file to be loaded
    fields: list of fields to look into
    words: list of words to search

    Return:
    return_dict: dictionary with a description if for a certain field the word
    was found or not (0 for not found and 1 for found)
    """
    return_dict = {}
    _references_location = load_json_bib_refences(references_location)

    for item in _references_location:
        return_dict[item] = {}
        for field in fields:
            return_dict[item][field] = {}
            for word in words:
                if word.upper() in _references_location[item][field]:
                    tmp_word = 1
                else:
                    tmp_word = 0
                return_dict[item][field][word] = tmp_word

    return return_dict


def plot_artcles_per_year(references_location: str) -> None:
    """
    This function has the objective of plotting a evolution of the
    article published over the years based on the .json
    created when parsing the .bib referencial.

    Keyword Arguments:
    references_location: string containing the .json file to be loaded

    Return:
    None
    """

    year_count_data = count_references_by_year(references_location)
    plt.figure(figsize=(10, 8))
    plt.bar(year_count_data.keys(), year_count_data.values(),
            0.9, color='darkblue', edgecolor='black', linewidth=2)
    return None
