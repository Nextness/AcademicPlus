import os
import hashlib as hs
import json
import matplotlib.pyplot as plt

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
            with open(folder_name + file, "r", encoding="utf8") as rfile:
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

    all_data = all_data.encode('utf-8', 'ignore').decode("utf-8")
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

    replace_dict = {
        "title": "Title",
        "journal": "Journal",
        "volume": "Volume",
        "pages": "Pages",
        "year": "Year",
        "issn": "ISSN",
        "doi": "DOI",
        "url": "URL",
        "author": "Author",
        "keywords": "Keywords",
        "abstract": "Abstract"
    }

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


def _processed_confirmation() -> str:
    confirmation = input("Do you want to save the file? Please type Y or N:")

    while not (confirmation == "Y" or confirmation == "N"):
        confirmation = input("Please type Y or N:")

    return str(confirmation)


def _save_file_unsafe(parser_result: dict, save_file_name_loc: str) -> None:
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


def _save_file_safe(parser_result: dict, save_file_name_loc: str) -> None:
    """
    This function has the objective of sabe the created dictionary file into a
    json file format to be later utilized.

    Keyword Arguments:
    parser_result: dictionary with .bib references
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
            json.dump(parser_result, wfile, indent=4, ensure_ascii=False)

        print(f"File {save_file_name_loc}.json has been saved.")

    return None


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
    _save_file_safe(formatted_dict, save_file_name_loc)

    return None


def load_json_bib_refences_from_file(references_location: str) -> dict:
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


def references_differential_from_file(new_references_location: str, old_references_location: str) -> list:
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

    new_references = load_json_bib_refences_from_file(new_references_location)
    old_references = load_json_bib_refences_from_file(old_references_location)

    for new_item in new_references:
        for old_item in old_references:
            if new_references[new_item]["Hashed DOI"] == old_references[old_item]["Hashed DOI"]:
                differential_dict.update({new_item: new_references[new_item]})

    return differential_dict


def include_notes_to_file(references_location: str, hashed_doi: str, note: str) -> None:
    """
    This function has the objective of including notes into the specific entry for later use.

    Keyword Argument:
    references_location: string containing the .json file to be loaded
    hashed_doi: hashed doi as string hexadecimal value to lookup and include the note
    note: the note to be included in the .json file

    Return:
    None
    """

    _references_location = load_json_bib_refences_from_file(
        references_location)
    references_location = references_location.replace(".json", "")

    for item in _references_location:
        if _references_location[item]["Hashed DOI"] == hashed_doi:
            _references_location[item]["Note"] = note
            _save_file_unsafe(_references_location, references_location)
            break
    else:
        print(f"No article associated to the Hashed DOI: {hashed_doi}.")

    return None


def search_words_in_fields_from_file(references_location: str, fields: list[str], words: list[str]) -> dict:
    """
    This function has the objective of looping through the entire .json referencial
    and look in each of the specified fields to search for specific words. When enabling
    the string_syntax, a binary representation for each specific word will be utilized per
    searched field.

    Keyword Arguments:
    references_location: string containing the .json file to be loaded
    fields: list of fields to look into
    words: list of words to search

    Return:
    return_dict: dictionary with a description if for a certain field the word
    was found or not (0 for not found and 1 for found)
    """
    return_dict = {}
    _references_location = load_json_bib_refences_from_file(
        references_location)

    for item in _references_location:
        idx = _references_location[item]["Hashed DOI"]
        return_dict[idx] = {"Name": _references_location[item]["Title"]}
        for field in fields:
            return_dict[idx][field] = {}
            for word in words:
                if word.upper() in _references_location[item][field]:
                    tmp_word = 1
                else:
                    tmp_word = 0
                return_dict[idx][field][word] = tmp_word

    return return_dict


def binary_search_words_in_fields_from_file(references_location: str, fields: list[str], words: list[str]) -> dict:
    """
    This function has the objective of looping through the entire .json referencial
    and look in each of the specified fields to search for specific words. When enabling
    the string_syntax, a binary representation for each specific word will be utilized per
    searched field.

    Keyword Arguments:
    references_location: string containing the .json file to be loaded
    fields: list of fields to look into
    words: list of words to search

    Return:
    return_dict: dictionary with a description if for a certain field the word
    was found or not (0 for not found and 1 for found)
    """

    return_dict = {}
    _references_location = load_json_bib_refences_from_file(
        references_location)

    for item in _references_location:
        idx = _references_location[item]["Hashed DOI"]
        return_dict[idx] = {"Name": _references_location[item]["Title"]}
        for field in fields:
            tmp_str = ""
            return_dict[idx][field] = {}
            for word in words:
                if word.upper() in _references_location[item][field]:
                    tmp_word = "1"
                else:
                    tmp_word = "0"
                tmp_str = tmp_word + tmp_str
            return_dict[idx][field] = tmp_str
    return return_dict


def binary_boolean_condition_math_from_file(references_location: str, fields: list[str], words: list[str], conditions: list[int]) -> dict:
    # TODO: Include description and make this piece of shit code, better.
    return_dict = {}
    binary_dict = binary_search_words_in_fields_from_file(
        references_location, fields, words)
    for bin_reps in binary_dict:
        return_dict[bin_reps] = {}

        for field in fields:
            flag = 0
            return_dict[bin_reps][field] = {}
            for condition in conditions:
                idx = conditions.index(condition)
                return_dict[bin_reps][field][f"Split Data {idx}"] = binary_dict[bin_reps][field][flag:condition]
                flag = condition

            idx = idx + 1
            return_dict[bin_reps][field][f"Split Data {idx}"] = binary_dict[bin_reps][field][condition:]
    return return_dict


def binary_string_syntax_parser_from_file(references_location: str, fields: list[str], words: list[str], conditions: list[int]) -> dict:
    # TODO: Include description and make this piece of shit code, better.
    return_dict = {}
    binary_match = binary_boolean_condition_math_from_file(
        references_location, fields, words, conditions)

    for item in binary_match:
        return_dict[item] = {}
        for topic in binary_match[item]:
            return_dict[item][topic] = {}
            tmp_str = ""
            for data in binary_match[item][topic]:
                tmp_bit = ""
                for bit in binary_match[item][topic][data]:
                    tmp_bit = bit + "|" + tmp_bit
                tmp_bit = "(" + tmp_bit[::-1].replace("|", "", 1) + ")"

                tmp_str = tmp_str + "&" + tmp_bit

            return_dict[item][topic] = tmp_str.replace("&", "", 1)

    return return_dict


def complete_binary_strin_syntax_parser_from_file(references_location: str, fields: list[str], words: list[str], conditions: list[int]) -> dict:
    # TODO: Include description and make this piece of shit code, better.
    return_dict = {}
    binary_match = binary_boolean_condition_math_from_file(
        references_location, fields, words, conditions)

    for item in binary_match:
        return_dict[item] = {}
        tmp_match = 0
        for topic in binary_match[item]:
            return_dict[item][topic] = {}
            tmp_word_condition = 1
            for data in binary_match[item][topic]:
                tmp_bit = 0
                for bit in binary_match[item][topic][data]:
                    tmp_bit = int(bit) | int(tmp_bit)
                tmp_word_condition = int(tmp_bit) & int(tmp_word_condition)
            tmp_match = int(tmp_word_condition) | int(tmp_match)
            return_dict[item][topic] = tmp_match
    return return_dict


def count_references_by_year_from_file(references_location: str) -> dict:
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
    _references_location = load_json_bib_refences_from_file(
        references_location)

    for item in _references_location:
        tmp = _references_location[item]["Year"]
        if tmp not in count_by_year_dict:
            count_by_year_dict.update({tmp: 1})
        else:
            count_by_year_dict[tmp] = count_by_year_dict[tmp] + 1

    for key in sorted(count_by_year_dict):
        sorted_count_by_year_dict.update({key: count_by_year_dict[key]})

    return sorted_count_by_year_dict


def check_duplicate_entries_from_file(references_location: str) -> dict:
    """
    This function has the objective of checking if there is duplicated articles
    based on the DOI inside the referencial provided.

    Keyword Arguments:
    references_location: string containing the .json file to be loaded

    Return:
    return_dict: count of all DOI inside a dictonary. If it is one, that it is not
    duplicated, else it is
    duplicated_dict: a dictonary with the duplicated DOIs. If empty, then no
    duplicates were found
    """
    _references_location = load_json_bib_refences_from_file(
        references_location)
    return_dict, duplicated_dict = {}, {}

    for item in _references_location:
        value = str(_references_location[item]["DOI"])
        value = value.replace("https://doi.org/", "")
        value = value.replace(",", "")
        if value not in return_dict:
            return_dict[value] = 1
        else:
            return_dict[value] = return_dict[value] + 1

    for item in return_dict:
        if return_dict[item] > 1:
            duplicated_dict[item] = "Duplicated"

    return return_dict, duplicated_dict


def count_article_years_from_file(references_location: str) -> dict:
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
    _references_location = load_json_bib_refences_from_file(
        references_location)

    for _, (idx, item) in enumerate(_references_location.items()):
        sum_year += item
        result_dict.update({idx: sum_year})

    return result_dict


def count_article_years_percentage_from_file(references_location: str) -> dict:
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
    tmp_dict = count_article_years_from_file(references_location)

    # This make a list out of a dictionary and gets the last value
    # to use in the division to get the percentage each year represents
    # of the total.
    total_articles = list(tmp_dict.values())[-1]

    for _, (idx, item) in enumerate(tmp_dict.items()):
        sum_percentage = item/total_articles * 100
        result_dict.update(
            {idx: {"Sum": item, "Sum Percentage": sum_percentage}})

    return result_dict


def plot_artcles_per_year_from_file(references_location: str) -> None:
    """
    This function has the objective of plotting a evolution of the
    article published over the years based on the .json
    created when parsing the .bib referencial.

    Keyword Arguments:
    references_location: string containing the .json file to be loaded

    Return:
    None
    """

    year_count_data = count_references_by_year_from_file(references_location)
    plt.figure(figsize=(10, 8))
    plt.bar(year_count_data.keys(), year_count_data.values(),
            0.9, color='darkblue', edgecolor='black', linewidth=2)
    return None
