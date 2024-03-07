import re

from utils.constants import OWL, RDF, PREFIX

def clean_response(response: str) -> str:
    response = response.replace(PREFIX, "")
    response = response.replace(RDF, "")
    response = response.replace(OWL, "")
    response = response.replace('\\n', ' ') 
    response = response.replace('b\'', '')
    response = re.sub(r"\s+", " ", response)  
    response = re.sub(r"\s{2,}", " ", response)

    return response
