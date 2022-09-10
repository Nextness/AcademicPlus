import dearpygui.dearpygui as dpg
import AcademicPlus.CommonOperations as cmnops
import AcademicPlus.ResearchManager as resm
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

with dpg.window(tag="MainWindow"):

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
