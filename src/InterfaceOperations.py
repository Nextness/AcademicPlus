import src.ResearchManager as resm
import src.CommonOperations as cmnops
import dearpygui.dearpygui as dpg
import textwrap

MENU_DICTIONARY = {
    "File": {
        "new_file": ("New Academic File", "(Ctrl + N)"),
        "open_file": ("Open Existing File", "(Ctrl + O)"),
        "save_file": ("Save File", "(Ctrl + S)"),
        "save_file_as": ("Save File As", "(Ctrl + Shitf + N)"),
    },
    "Edit": {
        "undo": ("Undo Action", "(Ctrl + Z)"),
        "cut": ("Cut Actio", "(Ctrl + X)"),
        "copy": ("Copy Action", "(Ctrl + C)"),
        "paste": ("Paste Action", "(Ctrl + V)"),
        "find": ("Find Action", "(Ctrl + F)"),
        "replace": ("Replace Action", "(Ctrl + R)"),
    },
    "View": None,
    "Help": None

}


def make_menu_bar() -> None:
    with dpg.menu_bar():

        with dpg.menu(tag="tag_menu_file", label="File"):

            File = MENU_DICTIONARY["File"]
            for option in File:
                dpg.add_menu_item(
                    tag=f"tag_menu_item_file_{option}",
                    label=f"{File[option][0]:<20}{File[option][1]}",
                )

        with dpg.menu(tag="tab_menu_edit", label="Edit"):

            Edit = MENU_DICTIONARY["Edit"]
            for option in Edit:
                dpg.add_menu_item(
                    tag=f"tag_menu_item_edit_{option}",
                    label=f"{Edit[option][0]:<20}{Edit[option][1]}",
                )

        with dpg.menu(tag="tag_menu_view", label="View"):
            pass

        with dpg.menu(tag="tab_menu_help", label="Help"):
            pass

    return None


def make_research_metadata(input_dict: dict[str]) -> None:

    with dpg.window(tag="tag_window_file_metadata", label="Research Metadata", no_close=True, pos=(1350, 120)):
        for idx1, item in enumerate(input_dict):
            information = reserach_metadata(input_dict, item)
            dpg.add_text(
                tag=f"tag_add_text_chapter_{idx1 + 1}",
                default_value=information,
            )

    return None


def make_research_body(input_dict: dict[str]) -> None:

    for idx, item in enumerate(input_dict):

        title = input_dict[item]["Name"]
        with dpg.tab(label=item, tag=f"tab{idx}"):

            dpg.add_text(
                default_value=title,
                label=title,
            )

            dpg.add_button(
                label="Save",
                tag=f"button{idx}",
                width=60,
                height=30,
                callback=resm.wrapper_save_file,
                user_data=[
                    dpg.get_value(f"input{idx}"),
                    f"test{idx}.json"
                ]
            )

            for idx3, content in enumerate(input_dict[item]["Content"]):
                tmp = input_dict[item]["Content"][content]

                dpg.add_text(
                    default_value=f"{content} - Saved Paragraph Hash:{cmnops._hash_string(tmp)}",
                    pos=[
                        10,
                        idx3 * 260 + 140
                    ]
                )

                dpg.add_text(
                    default_value=f"Current Paragraph Hash:{cmnops._hash_string(tmp)}",
                    pos=[
                        620,
                        idx3 * 260 + 140
                    ]
                )

                dpg.add_text(
                    default_value=f"Current Paragraph Hash:{cmnops._hash_string(tmp)}",
                    pos=[
                        620,
                        idx3 * 260 + 160
                    ]
                )

                tmp = textwrap.fill(tmp, 80)
                dpg.add_input_text(
                    readonly=True,
                    tag=f"tag_add_input_text_paragraph_{idx}{idx3}_read_only",
                    multiline=True,
                    pos=[
                        10,
                        idx3 * 260 + 180
                    ],
                    default_value=tmp,
                    tab_input=True,
                    width=600,
                    height=200
                )

                dpg.add_input_text(
                    tag=f"tag_add_input_text_paragraph_{idx}{idx3}_write",
                    multiline=True,
                    pos=[
                        620,
                        idx3 * 260 + 180
                    ],
                    default_value=tmp,
                    tab_input=True,
                    width=600,
                    height=200
                )

    return None


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
