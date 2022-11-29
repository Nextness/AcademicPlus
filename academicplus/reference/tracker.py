# ===================================================== #
#                 ~~~~ < Imports > ~~~~                 #
# ===================================================== #

import academicplus.Common.Operations as cmnops
import academicplus.Data.Structures as Struct


# ===================================================== #
#                ~~~~ < Functions > ~~~~                #
# ===================================================== #

def create_reference_tracker(reference_location_name: str) -> None:
    """
    | : #TODO: Include documentation for this function.
    """
    cmnops._save_file_safe(None, reference_location_name)
    return


def add_reference_tracker(reference_tracker_struct: Struct.ReferenceTracker, reference_tracker_location: str) -> None:
    """
    | : #TODO: Include documentation for this function.
    """
    _refence_tracker_location = cmnops.load_json_file(reference_tracker_location)
    dict_length = len(_refence_tracker_location)
    _refence_tracker_location[dict_length + 1] = cmnops.dataclass_to_dict(reference_tracker_struct)
    cmnops._save_file_unsafe(_refence_tracker_location, reference_tracker_location)
    return


def update_reference_tracker(reference_tracker_struct: Struct.ReferenceTracker, reference_tracker_location: str, index: int) -> None:
    """
    | : #TODO: Include documentation for this function.
    """
    try:
        _refence_tracker_location = cmnops.load_json_file(reference_tracker_location)
        dict_length = len(_refence_tracker_location)
        
        if index > dict_length:
            raise IndexError("The index provided is greater than the number of articles in the reference tracker provided.")

        _refence_tracker_location[str(index)] = cmnops.dataclass_to_dict(reference_tracker_struct)
        cmnops._save_file_unsafe(_refence_tracker_location, reference_tracker_location)
        return

    except IndexError as err:
        raise err


def update_reference_tracker_from_file(reference_tracker_struct: Struct.ReferenceTracker, reference_tracker_location: str, index: int) -> None:
    pass


def define_tier(number_of_hierarchy_paper: int) -> str:
    TIER_LOGIC =[
        "Primary", "Secondary",
        "Tertiary", "Quarternary"
    ]
    for idx, tier in enumerate(TIER_LOGIC):
        if number_of_hierarchy_paper == idx + 1:
            return tier
        else:
            return "Out of Scope"
