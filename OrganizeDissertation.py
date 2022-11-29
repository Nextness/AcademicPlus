import dearpygui.dearpygui as dpg
import academicplus.research.nodeformatting as fmt
import os
import sys

PROJECT_PATH = os.getcwd()
SOURCE_PATH = os.path.join(PROJECT_PATH, "src")
sys.path.append(SOURCE_PATH)

if __name__ == "__main__":

    # Creates static widgets for the interface:
    dpg.create_context()
    dpg.configure_app(docking=True, docking_space=True)
                        
    dpg.create_viewport(
        title="Academic Plus",
        width=1080,
        height=720
    )

    with dpg.window(label="Example Window", width = 600, height=500):
        
            with dpg.node_editor(callback=lambda sender, 
                                app_data: dpg.add_node_link(
                                    app_data[0], 
                                    app_data[1], 
                                    parent=sender
                                ), 
                                delink_callback=lambda sender, 
                                app_data: dpg.delete_item(app_data),
                                minimap=True,
                                minimap_location=dpg.mvNodeMiniMap_Location_BottomRight) as teste:
                
                def make_node(id: int, title: str, authors: str, doi: str, hashed_doi: str, journal: str, keywords: str, node_info: dict[str, str|tuple[int]]) -> None:

                    with dpg.node(tag=f"node_{id}", label=journal, pos=node_info["pos"]):
                        with dpg.node_attribute(tag=f"node_attr_out_{id}",attribute_type=dpg.mvNode_Attr_Output): pass
                        with dpg.node_attribute(tag=f"node_attr_in_{id}", attribute_type=dpg.mvNode_Attr_Input): pass
                        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Static):
                            dpg.add_text(default_value=f"https://doi.org/{doi} [{hashed_doi}]")
                            dpg.add_text(default_value=title, wrap=600)
                            dpg.add_text(default_value=f"{keywords}.", wrap=500)
                            dpg.add_text(default_value=authors, wrap=500)
                            dpg.add_input_text(default_value=node_info["citation"], multiline=True, width=500, height=100)
                            dpg.add_input_text(default_value=node_info["comment"], multiline=True, width=500, height=100)
                
                dict_test1 = {
                    "pos": (10, 10),
                    "citation": "Difficulties of students of science-related subjects often stem from the abstractness and complexity of learned concepts and the fact that those concepts process are not easily applied in practice",
                    "comment": "The article mentions one condition of abstract such as not easy to apply in real-life"
                }
                dict_test2 = {
                    "pos": (500, 10),
                    "citation": "Difficulties of students of science-related subjects often stem from the abstractness and complexity of learned concepts and the fact that those concepts process are not easily applied in practice",
                    "comment": "The article mentions one condition of abstract such as not easy to apply in real-life"
                }

                make_node(1, "Deep-Learning-Incorporated Augmented Reality Application for Engineering Lab Training",
                        "Estrada, John et al.", "10.3390/app12105159", "08ce254a27bd7ac6cb96ed1f18b5317dafbb48da", "Applied Sciences Basel",
                        "artificial intelligence, augmented reality, machine learning, object detection, computer in education, lab equipment tutorial",
                        dict_test1
                )

                make_node(2, "Virtual Reality-Based Training: Case Study in Mechatronics",
                        "Kaminska, D. et al.", "10.1007/s10758-020-09469-z", "da94c69aa8165abfc9dc8b3926476160fd00c947", "Technology Knowledge and Learing",
                        "Virtual reality, Education, Human-computer interface, Teaching/learning Strategies",
                        dict_test2
                )

                dpg.add_node_link("node_attr_out_1", "node_attr_in_2", parent=teste)

    dpg.setup_dearpygui()
    dpg.show_viewport()

    # Creates dinamic widgets for the interface
    while dpg.is_dearpygui_running():
            dpg.render_dearpygui_frame()

    dpg.destroy_context()
