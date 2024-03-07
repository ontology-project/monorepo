import re

from utils.constants import PREFIX

def clean_response(response: str) -> str:
    response = response.replace(PREFIX, "")
    response = response.replace("http://www.w3.org/1999/02/22-rdf-syntax-ns#", "")
    response = response.replace("http://www.w3.org/2002/07/owl", "")
    response = response.replace('\\n', ' ') 
    response = response.replace('b\'', '')
    response = re.sub(r"\s+", " ", response)  
    response = re.sub(r"\s{2,}", " ", response)

    return response
