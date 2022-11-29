import re

from academicplus.common.operations import recursive_dict_lookup
from datetime import datetime

def line_formatting(line_input: str) -> str|None:
    prefix = ["#", "}"]
    line_input = line_input.strip().decode("utf-8")

    if line_input.startswith(tuple(prefix)) or line_input.isspace(): 
        return None
    if line_input.startswith("@"): 
        return line_input.rstrip("{")
    if line_input.endswith(";"): 
        return line_input.rstrip(";")

def header_parser(parsed_data, number_fields):
    header_list = list()
    number_fields = number_fields + 1
    for p_d_pos, info in enumerate(parsed_data):
        if info.startswith("@FILE_METADATA"): continue
        if p_d_pos in range(1, number_fields): header_list.append(info)
        else: return p_d_pos, header_list

def body_parser(ret_pos, parsed_data, number_fields):
    body_list = list()
    tmp_list = list()
    for pos1, info1 in enumerate(parsed_data[ret_pos:]):
        interval = pos1 % number_fields
        if info1.startswith("@PRA_ENTRY"): tmp_list = list() 
        if interval in range(1, number_fields): 
            tmp_list.append(info1)
            continue
        else:
            body_list.append(tmp_list)
              
    return body_list

def parse_ndpos_file(p_bin_data) -> list[str]:

    parsed_data = list()
    with open(p_bin_data, "rb") as b_data:
        lines = [line for line in b_data]

    for line in lines:
        line = line_formatting(line)
        if line is None: continue
        parsed_data.append(line)
        
    ret_pos, header_list = header_parser(parsed_data, 3)
    body_list = body_parser(ret_pos, parsed_data, 10)

    return [
        header_list, 
        body_list
        ]

def header_formater(data: list[str]) -> str:
    new_line = ';\n\t'
    result = f"@FILE_METADATA{{\n\t{new_line.join(data)};\n}}\n\n"
    return result

def body_formatter(data: list[list[str]]) -> str:
    new_line = ';\n\t'
    result = str()
    for item in data:
        result += f"@ENTRY{{\n\t{new_line.join(item)};\n}}\n\n"
    return result

def validation(hdr, bdy):
    
    bdy_len = len(bdy)
    if bdy_len != hdr[0]: hdr[0] = str(bdy_len)

    cur_date = datetime.today().strftime('%Y-%m-%d')
    if cur_date != hdr[1]: hdr[1] = str(cur_date)

    cur_time = datetime.today().strftime('%H-%M-%S')
    if cur_time != hdr[2]: hdr[2] = str(cur_time)

    return hdr, bdy

def save_ndpos(f_name, hdr, bdy) -> None:
    hdr, bdy = validation(hdr, bdy)
    str_hdr = header_formater(hdr)
    str_bdy = body_formatter(bdy)
    b_hdr_bdy = f"{str_hdr}{str_bdy}".encode("utf-8")
    with open(f"{f_name}.ndpos", "wb") as b_data:
        b_data.write(b_hdr_bdy)





def load_ndpos_file(p_name: str, mode: str) -> list[str]:
    with open(p_name, mode) as b_data:
        lines = [line for line in b_data]

    ndpos_data = list()
    for line in lines:
        line = line.decode("utf-8")
        line, _, _ = line.partition("\\\\")
        line = line.strip()

        if not line: continue
        ndpos_data.append(line)
    
    return ndpos_data


def parse_generic_info(list_data) -> tuple[dict, int]:
    
    pos = int()
    return_dict = dict()
    while True:

        key = list_data[pos]
        def increment(value): return value + 1

        if re.match("(@FILE_METADATA{)", key):
            return_dict = {"FileMetada": {}}
            pos = increment(pos)
            continue
        
        if re.match("(\[\d\|\d\|\d\|\d\|\d\])", key):
            key = re.search("(?<=\[)(.*)(?=\])", key).group(1)
            key = key.split("|")
            return_dict["FileMetada"] = {"Counts": key}
            pos = increment(pos)
            continue

        if re.match("([\d]{4}-[\d]{2}-[\d]{2};)", key):
            key = re.search("(.*)(?=;)", key).group(1)
            return_dict["FileMetada"].update({"LastSaveDate": key})
            pos = increment(pos)
            continue
        
        if re.match("([\d]{2}:[\d]{2}:[\d]{2};)", key):
            key = re.search("(.*)(?=;)", key).group(1)
            return_dict["FileMetada"].update({"LastSaveTime": key})
            pos = increment(pos)
            continue

        if pos >= 4:
            return  pos, return_dict


def parse_search_info(list_name: list[str], start_pos: int) -> dict:

    make_root = False
    new_list = list()
    new_dict = dict()
    list_length = len(list_name)
    while True:

        if start_pos >= list_length or list_name[start_pos].startswith("}"): 
            return start_pos + 1, new_dict

        key = list_name[start_pos]

        if re.match("(\$SEARCH_TERM{)", key):
            new_dict["SearchTerm"] = {}
            start_pos += 1
            make_root = True
            continue

        # Sanity check
        if recursive_dict_lookup(key, new_dict):
            start_pos += 1
            continue
        
        # Creates root node
        if make_root:
            key = re.search("(?<=\.)(.*)(?=:)", key).group(1)
            root = key
            new_dict["SearchTerm"].update({key: dict()})
            start_pos += 1
            make_root = False
            continue

        
        # Creates platform leafs
        if re.match("(\.[a-zA-Z]*:)", key):
            key = re.search("(?<=\.)(.*)(?=:)", key).group(1)
            new_dict["SearchTerm"][root].update({key: {}})
            platform = key
            start_pos += 1
            continue
        
        # Create research idx
        if re.match("(\.\d*:)", key):
            key = re.search("(?<=\.)(.*)(?=:)", key).group(1)
            idx = key
            new_dict["SearchTerm"][root][platform].update({key: {}})
            start_pos += 1
            continue
        
        # Lists information for the specified idx
        if re.match(".*;", key):
            key = re.search("(.*)(?=;)", key).group(1)
            new_list.append(key)
            start_pos += 1

        # Upates the research idx with corresponding data
        if len(new_list) == 7:
            new_dict["SearchTerm"][root][platform].update({idx: new_list})
            new_list = []
            continue



def parse_criteria(list_name: list[str], start_pos: int) -> tuple[int, dict]:

    make_root = False
    new_list = list()
    new_dict = dict()
    list_length = len(list_name)
    while True:

        # print(list_name[start_pos])
        if start_pos >= list_length or list_name[start_pos].startswith("}"): 
            return start_pos, new_dict

        key = list_name[start_pos]

        if re.match("(\$.*{)", key):
            key = re.search("(?<=\$)(.*)(?={)", key).group(1)
            tmp = key
            new_dict[key] = {}
            start_pos += 1
            make_root = True
            continue

        # Sanity check
        if recursive_dict_lookup(key, new_dict):
            start_pos += 1
            continue
        
        # Creates root node
        if make_root:
            key = re.search("(?<=\.)(.*)(?=:)", key).group(1)
            root = key
            new_dict[tmp].update({key: dict()})
            start_pos += 1
            make_root = False
            continue

        
        # Creates platform leafs
        if re.match("(\.[a-zA-Z]*:)", key):
            key = re.search("(?<=\.)(.*)(?=:)", key).group(1)
            new_dict[tmp][root].update({key: {}})
            platform = key
            start_pos += 1
            continue

        elif re.match("(\.\".*\":)", key):
            key = re.search("(?<=\.\")(.*)(?=\":)", key).group(1)
            new_dict[tmp][root].update({key: {}})
            platform = key
            start_pos += 1
            continue
        
        # Create research idx
        if re.match("(\.\d*:)", key):
            key = re.search("(?<=\.)(.*)(?=:)", key).group(1)
            idx = key
            new_dict[tmp][root][platform].update({key: {}})
            start_pos += 1
            continue

        elif re.match("(\.\d*\s->\s\".*\":)", key):
            key = re.search("(?<=\.)(.*)(?= \-)", key).group(1)
            idx = key
            new_dict[tmp][root][platform].update({key: {}})
            start_pos += 1
            continue

        
        # Lists information for the specified idx
        if re.match(".*;", key):
            key = re.search("(.*)(?=;)", key).group(1)
            new_list.append(key)
                    
        next_item = list_name[start_pos + 1]
        # print(platform, start_pos, key, next_item)
        if re.match("(\.\d*\s->\s\".*\":)", next_item) or re.match("(\.\".*\":)", next_item) or next_item.startswith("}"):
            new_dict[tmp][root][platform].update({idx: new_list})
            new_list = []
            start_pos += 1
            continue

        start_pos += 1


def parse_relationship(list_name: list[str], start_pos: int) -> tuple[int, dict]:
    
    list_length = len(list_name)
    new_list = list()
    new_dict = dict()
    while True:

        key = list_name[start_pos]
        next_item = list_name[start_pos + 1]

        if start_pos  >= list_length or list_name[start_pos].startswith("}"): 
            return start_pos, new_dict

        if re.match("(\$.*{)", key):
            key = re.search("(?<=\$)(.*)(?={)", key).group(1)
            tmp = key
            new_dict[key] = {}
            start_pos += 1
            continue

        if re.match("(\.\".*\":)", key):
            key = re.search("(?<=\.\")(.*)(?=\":)", key).group(1)
            new_dict[tmp].update({key: {}})
            tmp_2 = key
            start_pos += 1
            continue

        if re.match(".*;", key):
            key = re.search("(.*)(?=;)", key).group(1)
            new_list.append(key)

        if re.match("(\.\".*\":)", next_item) or next_item.startswith("}"):
            new_dict[tmp].update({tmp_2: new_list})
            new_list = []
            start_pos += 1
            continue

        start_pos += 1



def parse_entries(list_name: list[str], start_pos: int) -> tuple[int, dict]:

    entry_increment = int()
    new_dict = dict()
    while True:

        previous_item = list_name[start_pos - 1]
        key = list_name[start_pos]
        next_item = list_name[start_pos + 1]

        # New entry
        if re.match("(@[\w]*\(\d*\){)", key):
            entry = re.search("(?<=\()(.*)(?=\))", key).group(1)
            key = re.search("(?<=@)(.*)(?=\()", key).group(1)
            tmp = key
            if new_dict.get(key, {}):
                new_dict[key].update({entry: {}})
            else:
                tmp_dir = {key: {entry: {}}}
                new_dict.update(tmp_dir)
                new_dict[key].update({entry: dict()})
            start_pos += 1
            entry_increment += 1
            continue
        
        # Creates Title
        if entry_increment == 1:
            key = re.search("(.*)(?=;)", key).group(1)
            new_dict[tmp][entry].update({"Title": key})
            start_pos += 1
            entry_increment += 1
            continue
        
        # Create Authors
        if entry_increment == 2:
            key = re.search("(?<=\[)(.*)(?=\];)", key).group(1)
            new_dict[tmp][entry].update({"Authors": key.split("|")})
            start_pos += 1
            entry_increment += 1
            continue

        # Create DOI
        if entry_increment == 3:
            key = re.search("(.*)(?=;)", key).group(1)
            new_dict[tmp][entry].update({"DOI": key})
            start_pos += 1
            entry_increment += 1
            continue

        # Create Hashed DOI
        if entry_increment == 4:
            key = re.search("(.*)(?=;)", key).group(1)
            new_dict[tmp][entry].update({"Hashed DOI": key})
            start_pos += 1
            entry_increment += 1
            continue

        # Create Journal
        if entry_increment == 5:
            key = re.search("(.*)(?=;)", key).group(1)
            new_dict[tmp][entry].update({"Journal": key})
            start_pos += 1
            entry_increment += 1
            continue
        
        # Create Keywords
        if entry_increment == 6:
            key = re.search("(?<=\[)(.*)(?=\];)", key).group(1)
            new_dict[tmp][entry].update({"Keywords": key.split("|")})
            start_pos += 1
            entry_increment += 1
            continue



            # new_dict[tmp][entry].update({chapter: {}})
            # new_dict[tmp][entry][chapter].update({key: {}})
            
        if re.match("(\$[\w]*\(\"[\w]*\"\){)", key):
            chapter = re.search("(?<=\(\")(.*)(?=\"\))", key).group(1)
            key = re.search("(?<=\$)(.*)(?=\()", key).group(1)
            node = key
            if new_dict.get(tmp).get(entry).get(chapter, {}):
                new_dict[tmp][entry].update({chapter: {}})
            else:
                new_dict[tmp][entry].update({chapter: {}})
                new_dict[tmp][entry][chapter].update({key: {}})
            start_pos += 1

            new_list_2 = list()
            while True:
            
                previous_item = list_name[start_pos - 1]
                key = list_name[start_pos]
                next_item = list_name[start_pos + 1]
            
                # Creates node idx
                if re.match("(\.[\d]*_[\w]*:)", key):
                    key = re.search("(?<=\.)(.*)(?=:)", key).group(1)
                    idx = key
                    new_dict[tmp][entry][chapter][node].update({key: {}})
                    start_pos += 1
                    continue
                
                # Creates node input and output idx
                if re.match("(\[[\d]*_[\D]*\|[\d]*_[\D]*\];)", key):
                    key = re.search("(?<=\[)(.*)(?=\];)", key).group(1)
                    new_dict[tmp][entry][chapter][node][idx].update({"InputOutput": key.split("|")})
                    start_pos += 1
                    continue

                # Creates node positions
                if re.match("(\[[\d]*\|[\d]*\];)", key):
                    key = re.search("(?<=\[)(.*)(?=\];)", key).group(1)
                    new_dict[tmp][entry][chapter][node][idx].update({"pos": key.split("|")})
                    start_pos += 1
                    continue
                
                # Create list with node citation and comment
                if re.match("(.*;)", key):
                    key = re.search("(.*)(?=;)", key).group(1)
                    new_list_2.append(key)

                # Includes citation and comment list
                if re.match("(\..*:)", next_item) or (next_item.startswith("}") and not key.startswith("}")):
                    new_dict[tmp][entry][chapter][node][idx].update({"CitationComment": new_list_2})
                    new_list_2 = []
                    start_pos += 1
                    continue
                
                # Validates entry has ended
                if key.startswith("}") and previous_item.startswith("}"):
                    entry_increment = 0
                    break
                
                start_pos += 1
        
        if key.startswith("}") and previous_item.startswith("}") and next_item.startswith("@LINKED_NODES"):
            return start_pos, new_dict

        start_pos += 1
        continue


def parse_link_nodes(list_name: list[str], start_pos: int) -> tuple[int, dict]:
    
    new_dict = dict()
    while True:

        key = list_name[start_pos] 
        

        if re.match("(@.*{)", key):
            key = re.search("(?<=@)(.*)(?={)", key).group(1)
            tmp = key
            new_dict = {key: []}
            start_pos += 1
            continue
        
        if re.match("(\d*_\D* -> \d*_\D*;)", key):
            key = re.search("(.*)(?=;)", key).group(1)
            val = key.split(" -> ")
            new_dict[tmp].append((val[0], val[1]))
            start_pos += 1
            continue
        
        if key.startswith("}"):
            return start_pos, new_dict


def parse_ndpos_file(p_name: str) -> dict[str]:
    
    result = load_ndpos_file(p_name, "rb")
    pos1_continue, p1_result = parse_generic_info(result)
    pos2_continue, p2_result = parse_search_info(result, pos1_continue)
    pos3_continue, p3_result = parse_criteria(result, pos2_continue)
    pos4_continue, p4_result = parse_relationship(result, pos3_continue + 1)
    pos5_continue, p5_result = parse_entries(result, pos4_continue + 2)
    pos6_continue, p6_result = parse_link_nodes(result, pos5_continue + 1)

    p1_result.update(p2_result)
    p1_result.update(p3_result)
    p1_result.update(p4_result)
    p1_result.update(p5_result)
    p1_result.update(p6_result)

    return p1_result