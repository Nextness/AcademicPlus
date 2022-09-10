import dearpygui.dearpygui as dpg
import AcademicPlus.CommonOperations as cmnops
import AcademicPlus.ResearchManager as resm
import AcademicPlus.InterfaceOperations as intops
import os
import json
import textwrap

TITLE_POS = (10, 40)
SAVE_BTN_POS = (1250, 40)
BODY_POS = (10, 80)

cwd = os.getcwd()
file = "Research_Analysis\dissertation_textual_content.json"
return_dict = cmnops.load_json_file(f"{cwd}\{file}")

dpg.create_context()

# Main window
with dpg.window(tag="MainWindow"):

    # TODO: Main menu: which needs to be worked on further.
    with dpg.menu_bar():
        with dpg.menu(label="View"):
            dpg.add_menu_item(label="File Metadata")

    # TODO: Minimap: contains metadata about the chapters of the reserach.
    # Requires further development to include more relevant informatio and be able
    # to open and close it at will.
    with dpg.window(tag="window_file_metadata"):

        for idx1, item in enumerate(return_dict):
            information = intops.reserach_metadata(return_dict, item)

            dpg.add_text(
                tag=f"text_file_metadata_{idx1}",
                default_value=information,
            )

            dpg.add_spacer(height=2)

    # TODO: Main tab bar with all the different chapters for the research.
    # Requires a save option which can get all the different fields and save into a
    # .json file format for later use.
    # TODO: Include different input_text widgets for each paragraph.
    # TODO: Make this section of code look better.
    with dpg.tab_bar(tag="ResearchTabBar"):
        input_list = []
        for idx, item in enumerate(return_dict):
            with dpg.tab(label=item, tag=f"tab{idx}"):
                title = return_dict[item]["Name"]
                result = ""
                for content in return_dict[item]["Content"]:
                    tmp = return_dict[item]["Content"][content]
                    tmp = textwrap.fill(tmp, 120)
                    result += tmp + "\n\n"

                dpg.add_text(
                    default_value=title,
                    label=title,
                    pos=TITLE_POS
                )

                input_text = dpg.add_input_text(
                    tag=f"input{idx}",
                    pos=BODY_POS,
                    multiline=True,
                    default_value=result,
                    tab_input=True,
                    width=1300,
                    height=1200,
                )

                input_list.append(f"input{idx}")

                dpg.add_button(
                    label="Save",
                    tag=f"button{idx}",
                    pos=SAVE_BTN_POS,
                    width=60,
                    height=30,
                    callback=resm.wrapper_save_file,
                    user_data=[dpg.get_value(
                        f"input{idx}"), f"test{idx}.json"]
                )
            print(input_list)

dpg.create_viewport(title="Reference Parser and Manager")
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("MainWindow", True)
dpg.start_dearpygui()
dpg.destroy_context()
