# ===================================================== #
#                 ~~~~ < Imports > ~~~~                 #
# ===================================================== #

from attr import asdict
import academicplus.common.operations as cmnops
import matplotlib.pyplot as plt


# ===================================================== #
#                ~~~~ < Functions > ~~~~                #
# ===================================================== #

def pos_based_on_hash(reference_location: str, hashed_id: str) -> None:
    """
    [Description]
    | : #TODO: Include description.

    [Argument]
    | : #TODO: Include arguments and definition.

    [Return]
    | : #TODO: Include return and definition.
    """
    lookup_dict = cmnops.load_json_file(reference_location)
    for article in lookup_dict:
        if lookup_dict[article]["Hashed_DOI"] == hashed_id:
            print(article)
    return


def references_differential_from_file(new_references_location: str, old_references_location: str) -> dict[str]:
    """
    [Description]
    | : This function has the objetive of getting the differential between two a new referencial and
    | : a old referencial.

    [Argument]
    | : <str::new_references_location> 
    | : (Definition) Location of the new .json file to be compared.
    | :
    | : <str::old_references_location> 
    | : (Definition) Location of the old .json file to be compared.

    [Return]
    | : <dict[str]::differential_dict>
    | : (Definition) Dictionary with the entries from the new file which are not part of the old file
    """
    differential_dict = {}

    new_references = cmnops.load_json_file(new_references_location)
    old_references = cmnops.load_json_file(old_references_location)

    for new_item in new_references:
        for old_item in old_references:
            if new_references[new_item]["Hashed DOI"] == old_references[old_item]["Hashed DOI"]:
                differential_dict.update({new_item: new_references[new_item]})

    return differential_dict


def include_notes_to_file(references_location: str, hashed_doi: str, note: str) -> None:
    """
    [Description]
    | : This function has the objective of including notes into the specific entry for later use.

    [Argument]
    | : <str::references_location> 
    | : (Definition) Location of the .json file to include notes.
    | :
    | : <str::hashed_doi> 
    | : (Definition) Hashed DOI to lookup and include the note.
    | :
    | : <str::note> 
    | : (Definition) Note to be included.

    [Return]
    | : <None::None>
    | : (Definition)
    """

    _references_location = cmnops.load_json_file(references_location)
    references_location = references_location.replace(".json", "")

    for item in _references_location:
        if _references_location[item]["Hashed DOI"] == hashed_doi:
            _references_location[item]["Note"] = note
            cmnops._save_file_unsafe(_references_location, references_location)
            break
    else:
        print(f"No article associated to the Hashed DOI: {hashed_doi}.")

    return None


def search_words_in_fields_from_file(references_location: str, fields: list[str], words: list[str]) -> dict:
    """
    [Description]
    | : This function has the objective of looping through the entire .json referencial
    | : and look in each of the specified fields to search for specific words. When enabling
    | : the string_syntax, a binary representation for each specific word will be utilized per
    | : searched field.

    [Argument]
    | : <str::references_location> 
    | : (Definition) Location of the .json file to include notes.
    | :
    | : <list[str]::fields>
    | : (Definition) Fields to search.
    | :
    | : <list[str]::words> 
    | : (Definition) Words to search in each field.

    [Return]
    | : <dict::return_dict> 
    | : (Definition) Description for a certain field.
    | :     0 - Word not found in the specified field.
    | :     1 - Word found in the specified field.
    """
    return_dict = {}
    _references_location = cmnops.load_json_file(references_location)

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
    [Description] 
    | : This function has the objective of looping through the entire .json referencial
    | : and look in each of the specified fields to search for specific words. When enabling
    | : the string_syntax, a binary representation for each specific word will be utilized per
    | : searched field.

    [Argument]
    | : <str::references_location> 
    | : (Definition) Location of the .json file to include notes.
    | :
    | : <list[str]::fields>
    | : (Definition) Fields to search.
    | :
    | : <list[str]::words> 
    | : (Definition) Words to search in each field.

    [Return]
    | : <dict::return_dict> 
    | : (Definition) Description for a certain field.
    | :     0 - Word not found in the specified field.
    | :     1 - Word found in the specified field.
    """

    return_dict = {}
    _references_location = cmnops.load_json_file(references_location)

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
                tmp_str = tmp_str + tmp_word
            return_dict[idx][field] = tmp_str
    return return_dict


def binary_boolean_condition_match_from_file(references_location: str, fields: list[str], words: list[str], conditions: list[int]) -> dict:
    """
    # TODO: Include description and make this piece of shit code, better.
    [Description]
    | :
    | :
    | :
    
    [Argument]
    | : <str::references_location> 
    | : (Definition) Location of the .json file to include notes.
    | :
    | : <list[str]::fields>
    | : (Definition) Fields to search.
    | :
    | : <list[str]::words>
    | : (Definition) Words to search in each field.
    | :
    | : <list[int]::conditions> 
    | : (Definition)

    [Return]
    | :
    """
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
    """
    # TODO: Include description and make this piece of shit code, better.
    [Description]
    | :
    | :
    | :
    
    [Argument]
    | : <str::references_location> 
    | : (Definition) Location of the .json file to include notes.
    | :
    | : <list[str]::fields>
    | : (Definition) Fields to search.
    | :
    | : <list[str]::words>
    | : (Definition) Words to search in each field.
    | :
    | : <list[int]::conditions> 
    | : (Definition)

    [Return]
    | :
    """
    return_dict = {}
    binary_match = binary_boolean_condition_match_from_file(
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


def binary_string_syntax_evaluation_from_file(references_location: str, fields: list[str], words: list[str], conditions: list[int]) -> dict:
    """
    # TODO: Include description and make this piece of shit code, better.
    [Description]
    | :
    | :
    | :
    
    [Argument]
    | : <str::references_location> 
    | : (Definition) Location of the .json file to include notes.
    | :
    | : <list[str]::fields>
    | : (Definition) Fields to search.
    | :
    | : <list[str]::words>
    | : (Definition) Words to search in each field.
    | :
    | : <list[int]::conditions> 
    | : (Definition)

    [Return]
    | :
    """
    return_dict = {}
    string_syntax_dict = binary_string_syntax_parser_from_file(
        references_location, fields, words, conditions)

    for item in string_syntax_dict:
        value = string_syntax_dict[item]
        return_dict[item] = {}
        for topic in string_syntax_dict[item]:
            return_dict[item][topic] = eval(value[topic])

    return return_dict


def _count_from_json_file(references_location: str, field_name: str) -> dict:
    """
    [Warning] 
    | : (Private funtion) Do not use it.

    [Description]
    | :
    | :
    
    [Argument]
    | : <str::references_location>  
    | : (Definition)
    | :
    | : <str::field_name> 
    | : (Definition)

    [Return]
    | :
    """
    # TODO: Inclue documentation for this function.
    count_by_year_dict = {}
    _references_location = cmnops.load_json_file(
        references_location)

    for item in _references_location:
        tmp = _references_location[item][field_name]
        if tmp not in count_by_year_dict:
            count_by_year_dict.update({tmp: 1})
        else:
            count_by_year_dict[tmp] = count_by_year_dict[tmp] + 1

    return count_by_year_dict


def _count_loaded_dict_file(dict_name: dict[str], field_name: str) -> dict:
    """
    [Description]
    | :
    | :
    
    [Argument]
    | : <str::references_location>  
    | : (Definition)
    | :
    | : <str::field_name> 
    | : (Definition)

    [Return]
    | :
    | : (Definition)
    """
    # TODO: Include documentation for this function.
    count_by_year_dict = {}

    for item in dict_name:
        tmp = dict_name[item][field_name]
        if tmp not in count_by_year_dict:
            count_by_year_dict[tmp] = 1
        else:
            count_by_year_dict[tmp] = count_by_year_dict[tmp] + 1

    return count_by_year_dict


def count_references_by_year_from_loaded_dict(references_location: str) -> dict:
    """
    [Description] 
    | : This function has the objective of counting the number of articles per year
    | : based on the .json created when parsing the .bib referencial.

    [Argument]
    | : <str::references_location> 
    | : (Definition) Location of the .json file to count.

    [Return]
    | : <dict::sorted_count_by_year_dict> 
    | : (Definition) Count per year of published articles.
    """
    sorted_count_by_year_dict = dict()
    _references_location = cmnops.load_json_file(references_location)

    count_references_dict = _count_loaded_dict_file(_references_location, "Year")

    for key in sorted(count_references_dict):
        sorted_count_by_year_dict.update({key: count_references_dict[key]})

    return sorted_count_by_year_dict


def count_number_journals_from_loaded_dict(references_location: str) -> dict:
    """
    [Description]
    | : This function has the objective of counting the number of articles per year
    | : based on the .json created when parsing the .bib referencial.

    [Argument]
    | : <str::references_location>
    | : (Definition) Location of the .json file to count.

    [Return]
    | : <dict::sorted_count_by_year_dict> 
    | : (Definition) Count per year of published articles.
    """
    sorted_count_by_year_dict = dict()
    _references_location = cmnops.load_json_file(
        references_location)

    count_references_dict = _count_loaded_dict_file(
        _references_location, "Journal")

    for key in sorted(count_references_dict):
        sorted_count_by_year_dict.update({key: count_references_dict[key]})

    return sorted_count_by_year_dict


def check_duplicate_entries_from_file(references_location: str) -> dict:
    """
    [Description]
    | : This function has the objective of checking if there is duplicated articles
    | : based on the DOI inside the referencial provided.

    [Argument]
    | : <str::references_location> 
    | : (Definition) Location of the .json file.

    [Return]
    | : <dict::return_dict>  
    | : (Definition) Count of all DOI inside a dictonary.
    | :     1 : Not duplicated entry. 
    | :     # > 1 : Duplicated entry.
    | : 
    | : <dict::duplicated_dict> 
    | : (Definition) Duplicated DOIs.
    | :     0 : Not duplicated entry.
    | :     # > 0 : Duplicated entry.
    """
    _references_location = cmnops.load_json_file(references_location)
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


def remove_duplicated_entries(references_location: str):
    _references_location = cmnops.load_json_file(references_location)
    duplicated_count, _ = check_duplicate_entries_from_file(references_location)

    for item in _references_location.copy():
        for dup in duplicated_count.copy():
            if _references_location[item]["DOI"] == dup and duplicated_count[dup] > 1:
                _references_location.pop(item)
                duplicated_count[dup] -= 1
                break
    return _references_location


def count_article_years_from_file(references_location: str) -> dict:
    """
    [Description]
    | : This function has the objective of summing the count of articles per
    | : year based on the .json created when parsing the .bib referencial.

    [Argument]
    | : <str::references_location> 
    | : (Definition) Location of the .json file;

    [Return]
    | : <dict::result_dict> 
    | : (Definition) Yearly sum of published articles.
    """
    sum_year = 0
    result_dict = {}
    _references_location = cmnops.load_json_file(
        references_location)

    for _, (idx, item) in enumerate(_references_location.items()):
        sum_year += item
        result_dict.update({idx: sum_year})

    return result_dict


def count_article_years_percentage_from_file(references_location: str) -> dict:
    """
    DOCUMENTATION

    [Description]
    | : This function has the objective of summing the count of articles per
    | : year and the percentage it represent over all based on the .json
    | : created when parsing the .bib referencial.

    [Argument]
    | : <str::references_location> 
    | : (Definition) Location of the .json file.

    [Return]
    | : <dict::result_dict> 
    | : (Definition) Yearly sum of published articles and the percentage it represents
    | : overall the article published in the specific referencial.
    | : 
    | : <dict::result_dict>
    | : (Definition) Yearly sum of published articles and the  percentage it represents
    | : overall the article published in the specific referencial.
    
    """
    result_dict = {}
    tmp_dict = count_article_years_from_file(references_location)

    #TODO: This make a list out of a dictionary and gets the last value
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
    [Description]
    | : This function has the objective of plotting a evolution of the
    | : article published over the years based on the .json
    | : created when parsing the .bib referencial.

    [Argument]
    | : <str::references_location>
    | : (Definition) Location of the .json file.

    [Return]
    | : <None::None> 
    | : (Definition) Plot Successfully displayed.
    """

    # year_count_data = count_references_by_year_from_file(references_location)
    # plt.figure(figsize=(10, 8))
    # plt.bar(year_count_data.keys(), year_count_data.values(),
    #         0.9, color='darkblue', edgecolor='black', linewidth=2)
    return None
