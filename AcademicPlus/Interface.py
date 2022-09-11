import AcademicPlus.CommonOperations as cmnops
import AcademicPlus.InterfaceOperations as intops
import dearpygui.dearpygui as dpg
import os


cwd = os.getcwd()
file = "Research_Analysis\dissertation_textual_content.json"
return_dict = cmnops.load_json_file(f"{cwd}\{file}")

dpg.create_context()

with dpg.window(tag="tag_window_main_window"):

    # Wrapper to make top menu bar
    intops.make_menu_bar()

    # Wrapper to make the body of the application
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
dpg.set_primary_window("tag_window_main_window", True)
dpg.start_dearpygui()
dpg.destroy_context()
