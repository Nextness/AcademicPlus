# Functions
def _load_file(file_location: str) -> str:
    """
    [Warning]
    | : 

    [Description]
    | :

    [Argument]
    | : 

    [Return]
    | :
    """
    with open(file_location) as rfile:
        data = rfile.read()
    return data


def _split_loaded_file(data: str, separator: str) -> list[str]:
    """
    [Warning]
    | : 

    [Description]
    | :

    [Argument]
    | : 

    [Return]
    | :
    """
    return data.split(separator)


def load_file_and_split(file_location: str, separator: str) -> list[str]:
    """
    [Description]
    | :

    [Argument]
    | : 

    [Return]
    | :
    """ 
    data = _load_file(file_location)
    split = _split_loaded_file(data, separator)
    return split


def _generate_code_sections(split: list[str], tokens: list[str]) -> list[tuple[int | str]]:
    """
    [Warning]
    | : 

    [Description]
    | :

    [Argument]
    | : 

    [Return]
    | :
    """
    sections = list()
    cur_line = int()
    for token in tokens:
        for idx, line in enumerate(split):
            if token.casefold() in line.casefold():
                sections += [(cur_line, idx, token)]
                cur_line = idx

    sections += [(cur_line, -1, 'EOF')]
    return sections


def _split_script_based_on_sections(split: list[str], sections: list[tuple[int | str]]) -> list[list[str]]:
    """
    [Warning]
    | : 

    [Description]
    | :

    [Argument]
    | : 

    [Return]
    | :
    """
    result = list()
    for pos, section in enumerate(sections):
        result += [split[section[0]:section[1]]]

        while "" in result[pos]:
            result[pos].remove("")

    result.remove([])
    return result


def cacatenate_data(string: list, separator: str) -> str:
    """
    [Description]
    | :

    [Argument]
    | : 

    [Return]
    | :
    """ 
    return separator.join(string)


def _configure_script_based_on_sections(input: list[str]) -> tuple[str]:
    """
    [Warning]
    | : 

    [Description]
    | :

    [Argument]
    | : 

    [Return]
    | :
    """
    return input[0], cacatenate_data(input[1:], "\n")
