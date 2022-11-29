# ===================================================== #
#                 ~~~~ < Imports > ~~~~                 #
# ===================================================== #

import academicplus.Common.Operations as cmnops
import academicplus.Interface.Operations as intops
import dearpygui.dearpygui as dpg
import os


# ===================================================== #
#                ~~~~ < Variables > ~~~~                #
# ===================================================== #

cwd = os.getcwd()
file = "..\Research_Analysis\dissertation_textual_content.json"
return_dict = cmnops.load_json_file(f"{cwd}\{file}")


# ===================================================== #
#                ~~~~ < Functions > ~~~~                #
# ===================================================== #

def load_application() -> None:
    """
    [Description]
    | :

    [Argument]
    | : (Definition)

    [Return]
    | : (Definition)
    """

    # Creates static widgets for the interface:
    dpg.create_context()
    dpg.configure_app(docking=True, docking_space=True)

    with dpg.window(tag="tag_window_main_window") as main:

        # Wrapper to make the body of the application
        with dpg.window(tag="tag_window_research_body", label="Research Text Comparisson"):

            # Wrapper to make top menu bar
            intops.make_menu_bar()

            with dpg.tab_bar(tag="ResearchTabBar"):
                intops.make_research_body(return_dict)

        # Wrapper to make reserach metadata
        intops.make_research_metadata(return_dict)

    dpg.create_viewport(
        title="Academic Plus",
        width=1920,
        height=1080
    )
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.set_primary_window(main, True)

    # Creates dinamic widgets for the interface
    while dpg.is_dearpygui_running():
        # readonly = dpg.get_value(
        #     f"tag_add_input_text_paragraph_00_read_only")
        # write = dpg.get_value(
        #     f"tag_add_input_text_paragraph_00_write")
        # print(readonly == write)
        dpg.render_dearpygui_frame()
    dpg.destroy_context()
    return None
