
def reserach_metadata(input_dict: dict[str], iteration: str) -> str:

    title = input_dict[iteration]["Name"]
    paragraph_count = len(input_dict[iteration]["Content"])
    count_char, count_words = 0, 0
    for char in input_dict[iteration]["Content"]:
        tmp_words = len(
            str(input_dict[iteration]["Content"][char]).split(" "))
        tmp_chars = len(input_dict[iteration]["Content"][char])
        count_words += tmp_words
        count_char += tmp_chars

        information = f"{iteration}: {title}\n"\
                      f" - Number of Paragraphs: {paragraph_count}\n"\
                      f" - Number of Words: {count_words}\n"\
                      f" - Number of Characters: {count_char}"

    return information
