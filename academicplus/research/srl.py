
import re


def load_file(f_path: str) -> list[str]:
    srl_data = list()
    with open(f_path, "rb") as r_b_data:
        lines = [line for line in r_b_data]

        for line in lines:
            line = line.strip()
            line = line.decode("utf-8")

            if not line: continue
            srl_data.append(line)

    return srl_data


def parsed_srl(loaded_file) -> tuple[dict[str, str|list[bool]], int]:
    ret_dict = dict()
    slr_dict = dict()
    tmp_dict = dict()
    charac_it = cmt_it = tmp_inc = char_art = entry_pos = it = 0
    inclusion_criteria_lookup = inclusion_criteria_eval = conclude_criteria_eval = False
    condition = store_comment = False

    for field in loaded_file:

        # Returns the hashed Doi + the current label
        if re.match("@PRA_ENTRY\((.*)\){", field):
            reg = re.search("@PRA_ENTRY\((.*)\){", field).group(1)
            slr_dict["doi"] = reg
            continue

        # If there is no rule, then include the information to dict
        if re.match("&(.*);", field):
            it += 1
            arg = re.search("(?<=&)(.*)(?=;)", field).group(1)
            slr_dict[f"val->{it}"] = arg
            continue

        # Enables parsing the inclusion criteria bools
        if re.match("\$(.*){", field):
            inclusion_criteria_lookup = True
            continue
        
        # Parsing Inclusion criteria bools logic
        if inclusion_criteria_lookup:
            field = field.rstrip(";")
            bool_criteria = field.split(" # ")
            bool_criteria = [True if value == "True" else False for value in bool_criteria]
            slr_dict["inclusion_criteria"] = bool_criteria
            inclusion_criteria_lookup = False
            inclusion_criteria_eval = True
            continue
        
        # Evaluating the criteria logic
        if inclusion_criteria_eval:
            condition = ( 
                not (bool_criteria[0] or bool_criteria[1] or bool_criteria[3] or 
                    bool_criteria[4] or bool_criteria[5] or bool_criteria[6] or 
                    bool_criteria[7]) 
                    and ( bool_criteria[8] or bool_criteria[9] or 
                    bool_criteria[10] or bool_criteria[11])
            )
            inclusion_criteria_eval = False
            conclude_criteria_eval = True

        # Writting Evaluate criteria
        if re.match("}\((True|False)\);", field) and conclude_criteria_eval:
            slr_dict["evaluation"] = condition
            condition = False
            conclude_criteria_eval = False
            continue
        
        # Article Characteristics
        if re.match("((True|False)::(True|False)){", field):
            charac_it += 1
            arg1 = bool(re.search("(.*)::", field).group(1))
            arg2 = bool(re.search("::(.*){", field).group(1))
            if not slr_dict.get("characteristic", {}):
                slr_dict["characteristic"] = dict()
            slr_dict["characteristic"].update({f"logic->{charac_it}": {"Evaluation": [arg1, arg2]}})
            continue
        
        # Comments for each Characteristc
        if re.match("(\(pg.*::p.*.*;)", field):
            tmp_inc += 1
            arg1 = re.search("(\(pg.*::p.*\))", field).group(1)
            arg2 = re.search("(?<=\))(.*)(?=;)", field).group(1)
            tmp_dict[f"{arg1}->{tmp_inc}"] = arg2
            store_comment = True
            continue
        
        # Allows parsing all Article Characteristics
        if field.startswith("}") and store_comment: 
            tmp_inc = 0
            cmt_it += 1
            slr_dict["characteristic"].update({f"comment->{charac_it}": tmp_dict})
            tmp_dict = dict()
            store_comment = False
            continue
        
        # More Article Characteristics - Bool Only
        if re.match("(((True|False)::)+(True|False);)", field):
            char_art += 1
            field = field.strip(";").split("::")
            field = [True if value == "True" else False for value in field]
            if not slr_dict.get("bool_characteristic", {}):
                slr_dict["bool_characteristic"] = dict()
            slr_dict["bool_characteristic"].update({char_art: field})
            continue
        
        # Validates the entry has ended and moves to the next one
        if re.match("(}\((True|False)\);)", field):
            entry_pos += 1
            arg = re.search("(?<=\()(.*)(?=\);)", field).group(1)
            slr_dict["valid_article"] = arg
            ret_dict[entry_pos] = slr_dict
            slr_dict = dict()
            charac_it = cmt_it = tmp_inc = char_art = it = 0
            continue

    return ret_dict


def save_srl_file(parsed_dict, f_path: str):
    ret_string_save = str()
    for entry in parsed_dict:
        res = parsed_dict[entry]    

        doi = res['doi']
        id = res['val->1']
        inc_criteria = ["True" if value else "False" for value in res['inclusion_criteria']]
        eval_criteria = res['evaluation']

        if not eval_criteria: 
            save_data_srl = (
            f"@PRA_ENTRY({doi}){{\n"
            f"\t&{id};\n"
            f"\t$Inclusion_Criteria_Data{{\n"
            f"\t\t{' # '.join(inc_criteria)};\n"
            f"}}({eval_criteria});\n\n"
            )
            ret_string_save += save_data_srl
            continue

        count_cit = res['val->2']
        count_ref = res['val->3']
        fields = res['val->4']

        ret_str = str()
        for item in res['characteristic']:
            buffer_str = str()
            if item.startswith("logic->"):
                buffer = ["True" if value else "False" for value in res['characteristic'][item]['Evaluation']]
                evaluation = '::'.join(buffer)
                ret_eval = f"\t{evaluation}{{\n"

            elif item.startswith("comment->"):
                for topic in res['characteristic'][item]:
                    arg1 = re.match("(\(pg.*::p.*\))", topic).group(1)
                    arg2 = res['characteristic'][item][topic]
                    buffer_str += f"\t\t{arg1}{arg2};\n"
                    continue
            if buffer_str:
                ret_str += f"{ret_eval}{buffer_str}\t}}\n"

        cs_ar_applied = res['val->5']
        cs_vr_applied = res['val->6']

        ret_bool = str()
        for bool in res['bool_characteristic']:
            buffer = ["True" if value else "False" for value in res['bool_characteristic'][bool]]
            ret_bool += f"\t{'::'.join(buffer)};\n"

        ret_result = str()
        for val in range(7, 23):
            val_iteration = res[f"val->{val}"]
            ret_result += f"\t&{val_iteration};\n"

        valid_article = res["valid_article"]

        save_data_srl = (
            f"@PRA_ENTRY({doi}){{\n"
            f"\t&{id};\n"
            f"\t$Inclusion_Criteria_Data{{\n"
            f"\t\t{' # '.join(inc_criteria)};\n"
            f"\t}}({eval_criteria});\n"
            f"\t&{count_cit};\n"
            f"\t&{count_ref};\n"
            f"\t&{fields};\n"
            f"{ret_str}"
            f"\t&{cs_ar_applied};\n"
            f"\t&{cs_vr_applied};\n"
            f"{ret_bool}"
            f"{ret_result}"
            f"}}({valid_article});\n\n"
        )   
        ret_string_save += save_data_srl
    
    with open(f"{f_path}.slr", "wb") as b_data:
        b_data.write(ret_string_save.encode("utf-8"))

    return None