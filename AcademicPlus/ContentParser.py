import os


def load_tex_files_from_folder(folder_name: str, dict_chapter_struc: dict[str]) -> dict[str]:
    """
    This function has to objetive of loading all .tex files from a folder
    and parse them into a string to be able to adjust the information it contains.

    Keyword arguments:
    folder_name: file location as a string
    dict_chapter_struc: dictonary structure with research project chapters

    Return:
    dict_chapter_struc: updated dictonary
    """
    all_data = []
    folder = os.walk(folder_name)
    main_folder = next(folder)
    count_all_files = main_folder[2]

    for file, name in zip(count_all_files, dict_chapter_struc):
        with open(folder_name + file, "r", encoding="UTF-8") as rfile:
            file_data = rfile.read()
            data_split = file_data.split("\n\n")
            for idx, paragraph in enumerate(data_split):
                dict_chapter_struc[name]["Content"].update(
                    {f"Paragraph {idx + 1}": paragraph})
                dict_chapter_struc[name]["Content"][f"Paragraph {idx + 1}"] = str(
                    dict_chapter_struc[name]["Content"][f"Paragraph {idx + 1}"])

    return dict_chapter_struc
