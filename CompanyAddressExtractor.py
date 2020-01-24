import re


def get_company_address_info(document):
    pl_diacritics = "ąćęłńóśźż"
    
    # Substrings of regex
    postal_code_regex_str = "[0-9]{2}-[0-9]{3}"
    city_name_regex_str = "[A-z%s][a-z%s]+" % (pl_diacritics.upper(), pl_diacritics)
    street_name_regex_str = "([A-Z%s][a-z%s]+ )+"  % (pl_diacritics.upper(), pl_diacritics)
    street_no_regex_str = "[0-9]+\w?"
    
    # Compiling regex searchers
    r_pc_cn = re.compile(postal_code_regex_str + " " + city_name_regex_str)
    r_pc = re.compile("[0-9]{2}-[0-9]{3}")
    r_cn = re.compile("[Ss]iedzib\w:? (w )?" + city_name_regex_str)
    r_sn_sn = re.compile("([A-z]l\.)? " + street_name_regex_str + street_no_regex_str)
    
    # Initializing variables to avoid getting an error in case given thing is not found
    postal_code = None
    postal_code2 = None
    city_name = None
    city_name2 = None
    street_name = None
    street_no = None
    
    is_done = {"pc_cn": False, "pc": False, "cn": False, "sn_sn": False}
    for page in document:
        for row in page:
            # Postal code and city name
            if not is_done["pc_cn"] and r_pc_cn.search(row) is not None:
                res_pc_cn = r_pc_cn.search(row).group()
                postal_code = re.search(postal_code_regex_str, res_pc_cn).group()
                city_name = re.search(city_name_regex_str, res_pc_cn).group()
                is_done["pc_cn"] = True
                
            # Postal code
            if not is_done["pc"] and r_pc.search(row) is not None:
                postal_code2 = r_pc.search(row).group()
                is_done["pc"] = True
            
            # City name 
            if not is_done["cn"] and r_cn.search(row) is not None:
                res_cn = r_cn.search(row).group()
                city_name2 = re.search(city_name_regex_str + "$", res_cn).group()
                is_done["cn"] = True
                
            # Street name and number
            if not is_done["sn_sn"] and r_sn_sn.search(row) is not None:
                res_sn_sn = r_sn_sn.search(row).group()
                street_name = re.search(street_name_regex_str, res_sn_sn).group()[:-1]
                street_no = re.search(street_no_regex_str + "$", res_sn_sn).group()
                is_done["sn_sn"] = True
        
            if all(is_done.values()):
                break
                
        if all(is_done.values()):
            break
    
    if postal_code is None:
        postal_code = postal_code2
        
    if city_name is None:
        city_name = city_name2
        
    return postal_code, city_name, street_name, street_no