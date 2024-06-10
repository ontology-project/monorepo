from SPARQLWrapper import SPARQLWrapper, JSON
from utils.constants import GRAPHDB_GET, GRAPHDB_POST, OWL, PREFIX, RDF, OBE
from utils.utils import clean_cell
import pandas as pd

def import_excel(excel_file):
    error_dict = {}
    print("Sheet 1")
    error_dict['StudyProgram_Curriculum'] = import_SP_curriculum(excel_file)
    print("Sheet 2")
    error_dict['Curriculum_PEO'] = import_curriculum_PEO(excel_file)
    print("Sheet 3")
    error_dict['Curriculum_PLO'] = import_curriculum_PLO(excel_file)
    print("Sheet 4")
    error_dict['PEO_PLO'] = import_PEO_PLO(excel_file)
    print("Sheet 5")
    error_dict['PLO_SubPLO'] = import_PLO_SubPLO(excel_file)
    print("Sheet 6")
    error_dict['PLO_CLO'] = import_PLO_CLO(excel_file)
    print("Sheet 7")
    error_dict['CLO_ULO'] = import_CLO_ULO(excel_file)
    print("Sheet 8")
    error_dict['ULO_Criteria (OPTIONAL)'] = import_ULO_criteria(excel_file)
    print("Sheet 9")
    error_dict['Curriculum_Course'] = import_curriculum_course(excel_file)
    print("Sheet 10")
    error_dict['Course_CLO'] = import_course_CLO(excel_file)
    print("Sheet 11")
    error_dict['Course_PLO'] = import_course_PLO(excel_file)
    print("Sheet 12")
    error_dict['Course_Content'] = import_course_content(excel_file)

    return error_dict

def import_SP_curriculum(excel_file):
    error_list = []

    # Transform data to dataframe pandas
    df = pd.read_excel(excel_file,sheet_name='StudyProgram_Curriculum') # sheet_name = Sheet seq. number on excel/Sheet name

    for index, row in df.iterrows():
        study_program = str(row['Study Program']) if str(row['Study Program']) != "nan" else ""
        curriculum = str(row['Curriculum']) if str(row['Curriculum']) != "nan" else ""
        curriculum_desc = str(row['Curriculum Description']) if str(row['Curriculum Description']) != "nan" else ""

        if not all([study_program, curriculum, curriculum_desc]):
            error_list.append(index+2)
            continue
        
        study_program = clean_cell(study_program)
        curriculum = clean_cell(curriculum)
        curriculum_desc = clean_cell(curriculum_desc)

        print(study_program, curriculum, curriculum_desc)

        query_string = f"""
            PREFIX : <{PREFIX}>
            PREFIX owl: <{OWL}>
            PREFIX rdf: <{RDF}>

            INSERT {{
                :{study_program} a :StudyProgram .
            }}
            WHERE {{
                FILTER NOT EXISTS {{
                    :{study_program} a :StudyProgram
                }}
            }};

            DELETE {{
                :{curriculum}   a :Curriculum ;
                                :curriculumName ?oldCurrName .
            }}
            INSERT {{
                :{curriculum}   a :Curriculum ;
                                :curriculumName "{curriculum_desc}"
            }}  
            WHERE {{
                OPTIONAL{{ :{curriculum} :curriculumName ?oldCurrName }}
            }};

            INSERT {{
                :{study_program} :hasCurriculum :{curriculum}
            }}
            WHERE {{
                FILTER NOT EXISTS {{
                    :{study_program} :hasCurriculum :{curriculum}
                }}
            }};
            """
        
        sparql = SPARQLWrapper(GRAPHDB_POST) 
        sparql.setQuery(query_string)
        sparql.setReturnFormat(JSON)
        sparql.setMethod("POST")

        print("sparqql", query_string)

        try: 
            sparql.queryAndConvert()
        except:
            print("ERROR")
        print("ACHIEVED")

    return error_list

def import_curriculum_PEO(excel_file):
    error_list = []

    # Transform data to dataframe pandas
    df = pd.read_excel(excel_file,sheet_name='Curriculum_PEO') # sheet_name = Sheet seq. number on excel/Sheet name

    for index, row in df.iterrows():
        curriculum = str(row['Curriculum']) if str(row['Curriculum']) != "nan" else ""
        peo = str(row['PEO']) if str(row['PEO']) != "nan" else ""
        description = str(row['PEO_Description']) if str(row['PEO_Description']) != "nan" else ""
        domain = str(row['Domain']) if str(row['Domain']) != "nan" else ""
        nqf_auth_resp = 'Y' if str(row['KKNI kewenangan & tanggung jawab']) != "nan" else "N"
        nqf_knowledge = 'Y' if str(row['KKNI pengetahuan']) != "nan" else "N"
        nqf_working_skill = 'Y' if str(row['KKNI Kemampuan bidang kerja']) != "nan" else "N"
        ns_attitude = 'Y' if str(row['SNDIKTI sikap']) != "nan" else "N"
        ns_knowledge = 'Y' if str(row['SNDIKTI pengetahuan']) != "nan" else "N"
        ns_generic_skill = 'Y' if str(row['SNDIKTI keterampilan umum']) != "nan" else "N"
        ns_specific_skill = 'Y' if str(row['SNDIKTI keterampilan khusus']) != "nan" else "N"

        # print("curr: ", curriculum)
        # print("peo: ", peo)
        # print("desc: ", description)
        # print("domain: ", domain)
        # print("===============================================")


        if not all([curriculum, peo, description]): # return the domain var
            error_list.append(index+2)
            continue
        
        print("HALOGAN")
        curriculum = clean_cell(curriculum)
        peo = clean_cell(peo)
        
        domain_lst = domain.split(", ")
        
        # domain list processing query
        domain_query = "\n".join(f":hasDomain :{item} ;" for item in domain_lst)

        query_string = f"""
            PREFIX : <{PREFIX}>
            PREFIX owl: <{OWL}>
            PREFIX rdf: <{RDF}>

            INSERT {{
                :{curriculum} a :Curriculum .
            }} 
            WHERE {{
                FILTER NOT EXISTS {{
                    :{curriculum} a :Curriculum .
                }}
            }};

            DELETE {{
                :{curriculum}-{peo}  a :ProgramEducationalObjective ;
                        :label ?oldPEOLabel ;
                        :hasDomain ?oldDomain ;
                        :nqfAuthorityResponsibility ?oldNQFAuthorityResp ;
                        :nqfKnowledge ?oldNQFKnowledge ;
                        :nqfWorkingSkill ?oldNQFWorkingSkill ;
                        :nsAttitude ?oldNSAttitude ;
                        :nsKnowledge ?oldNSKnowledge ;
                        :nsGenericSkill ?oldNSGenericSkill ;
                        :nsSpecificSkill ?oldNSSpecificSkill .
            }}
            INSERT {{
                :{curriculum}-{peo}  a :ProgramEducationalObjective ;
                        :label "{description}" ;
                        {domain_query}
                        {f':nqfAuthorityResponsibility "{nqf_auth_resp}" ;'   if nqf_auth_resp != "" else ""}
                        {f':nqfKnowledge "{nqf_knowledge}" ;'                 if nqf_knowledge != "" else ""}
                        {f':nqfWorkingSkill "{nqf_working_skill}" ;'          if nqf_working_skill != "" else ""}
                        {f':nsAttitude "{ns_attitude}" ;'                     if ns_attitude != "" else ""}
                        {f':nsKnowledge "{ns_knowledge}" ;'                   if ns_knowledge != "" else ""}
                        {f':nsGenericSkill "{ns_generic_skill}" ;'            if ns_generic_skill != "" else ""}
                        {f':nsSpecificSkill "{ns_specific_skill}" ;'          if ns_specific_skill != "" else ""}
            }}
            WHERE {{
                OPTIONAL {{ 
                    :{curriculum}-{peo}  a :ProgramEducationalObjective ;
                            :label ?oldPEOLabel ;
                            :hasDomain ?oldDomain ;
                    }}
            }}; 
            """
        
        query_string += f"""
            INSERT {{
                    :{curriculum} :hasPEO :{curriculum}-{peo} .
                }}
                WHERE {{
                    FILTER NOT EXISTS {{
                        :{curriculum} :hasPEO :{curriculum}-{peo} .
                    }}
                }}
            """

        sparql = SPARQLWrapper(GRAPHDB_POST) 
        sparql.setQuery(query_string)
        sparql.setReturnFormat(JSON)
        sparql.setMethod("POST")

        print("sparqql", query_string)

        sparql.queryAndConvert()

    return error_list

def import_curriculum_PLO(excel_file):
    error_list = []

    # Transform data to dataframe pandas
    df = pd.read_excel(excel_file,sheet_name='Curriculum_PLO') # sheet_name = Sheet seq. number on excel/Sheet name

    for index, row in df.iterrows():
        curriculum = str(row['Curriculum']) if str(row['Curriculum']) != "nan" else ""
        plo = str(row['PLO']) if str(row['PLO']) != "nan" else ""
        description = str(row['PLO_Description']) if str(row['PLO_Description']) != "nan" else ""
        domain = str(row['Domain']) if str(row['Domain']) != "nan" else ""
        nqf_auth_resp = 'Y' if str(row['KKNI kewenangan & tanggung jawab']) != "nan" else "N"
        nqf_knowledge = 'Y' if str(row['KKNI pengetahuan']) != "nan" else "N"
        nqf_working_skill = 'Y' if str(row['KKNI Kemampuan bidang kerja']) != "nan" else "N"
        ns_attitude = 'Y' if str(row['SNDIKTI sikap']) != "nan" else "N"
        ns_knowledge = 'Y' if str(row['SNDIKTI pengetahuan']) != "nan" else "N"
        ns_generic_skill = 'Y' if str(row['SNDIKTI keterampilan umum']) != "nan" else "N"
        ns_specific_skill = 'Y' if str(row['SNDIKTI keterampilan khusus']) != "nan" else "N"

        if not all([curriculum, plo, description]): # return the domain var
            error_list.append(index+2)
            continue
        
        print("HALOGAN")
        curriculum = clean_cell(curriculum)
        plo = clean_cell(plo)
        
        domain_lst = domain.split(", ")
        
        # domain list processing query
        domain_query = "\n".join(f":hasDomain :{item} ;" for item in domain_lst)

        query_string = f"""
            PREFIX : <{PREFIX}>
            PREFIX owl: <{OWL}>
            PREFIX rdf: <{RDF}>

            DELETE {{
                :{curriculum}-{plo}  a :ProgramLearningOutcome ;
                        :label ?oldPLOLabel ;
                        :hasDomain ?oldDomain ;
                        :nqfAuthorityResponsibility ?oldNQFAuthorityResp ;
                        :nqfKnowledge ?oldNQFKnowledge ;
                        :nqfWorkingSkill ?oldNQFWorkingSkill ;
                        :nsAttitude ?oldNSAttitude ;
                        :nsKnowledge ?oldNSKnowledge ;
                        :nsGenericSkill ?oldNSGenericSkill ;
                        :nsSpecificSkill ?oldNSSpecificSkill .
            }}
            INSERT {{
                :{curriculum}-{plo}  a :ProgramLearningOutcome ;
                        :label "{description}" ;
                        {domain_query}
                        {f':nqfAuthorityResponsibility "{nqf_auth_resp}" ;'   if nqf_auth_resp != "" else ""}
                        {f':nqfKnowledge "{nqf_knowledge}" ;'                 if nqf_knowledge != "" else ""}
                        {f':nqfWorkingSkill "{nqf_working_skill}" ;'          if nqf_working_skill != "" else ""}
                        {f':nsAttitude "{ns_attitude}" ;'                     if ns_attitude != "" else ""}
                        {f':nsKnowledge "{ns_knowledge}" ;'                   if ns_knowledge != "" else ""}
                        {f':nsGenericSkill "{ns_generic_skill}" ;'            if ns_generic_skill != "" else ""}
                        {f':nsSpecificSkill "{ns_specific_skill}" ;'          if ns_specific_skill != "" else ""}
            }}
            WHERE {{
                OPTIONAL {{ 
                    :{curriculum}-{plo}  a :ProgramLearningOutcome ;
                            :label ?oldPLOLabel ;
                            :hasDomain ?oldDomain ;
                    }}
            }}; 
            """

        sparql = SPARQLWrapper(GRAPHDB_POST) 
        sparql.setQuery(query_string)
        sparql.setReturnFormat(JSON)
        sparql.setMethod("POST")

        print("sparqql", query_string)

        sparql.queryAndConvert()
        
    return error_list

def import_PEO_PLO(excel_file):
    error_list = []

    # Transform data to dataframe pandas
    df = pd.read_excel(excel_file,sheet_name='PEO_PLO') # sheet_name = Sheet seq. number on excel/Sheet name

    for index, row in df.iterrows():
        curr = str(row['Curriculum']) if str(row['Curriculum']) != "nan" else ""
        peo = str(row['PEO']) if str(row['PEO']) != "nan" else ""
        plo = str(row['PLO']) if str(row['PLO']) != "nan" else ""

        if not all([peo, plo, curr]):
            error_list.append(index+2)
            continue
        
        curr = clean_cell(curr)
        peo = clean_cell(peo)
        plo = clean_cell(plo)
        

        query_string = f"""
            PREFIX : <{PREFIX}>
            PREFIX owl: <{OWL}>
            PREFIX rdf: <{RDF}>

            INSERT {{
                :{curr}-{peo} a :ProgramEducationalObjective .
            }} 
            WHERE {{
                FILTER NOT EXISTS {{
                    :{curr}-{peo} a :ProgramEducationalObjective .
                }}
            }};

            INSERT {{
                :{curr}-{plo} a :ProgramLearningOutcome .
            }} 
            WHERE {{
                FILTER NOT EXISTS {{
                    :{curr}-{plo} a :ProgramLearningOutcome .
                }}
            }};

            INSERT {{
                    :{curr}-{plo} :partOf :{curr}-{peo}
                }}
            WHERE {{
                FILTER EXISTS {{
                    :{curr}-{plo} a :ProgramLearningOutcome .
                    :{curr}-{peo} a :ProgramEducationalObjective .
                }}
            }}
            """

        sparql = SPARQLWrapper(GRAPHDB_POST) 
        sparql.setQuery(query_string)
        sparql.setReturnFormat(JSON)
        sparql.setMethod("POST")

        print("sparqql", query_string)

        sparql.queryAndConvert()
        
    return error_list

def import_PLO_SubPLO(excel_file):
    error_list = []

    # Transform data to dataframe pandas
    df = pd.read_excel(excel_file,sheet_name='PLO_SubPLO') # sheet_name = Sheet seq. number on excel/Sheet name

    for index, row in df.iterrows():
        curriculum = str(row['Curriculum']) if str(row['Curriculum']) != "nan" else ""
        peo = str(row['PEO']) if str(row['PEO']) != "nan" else ""
        plo = str(row['PLO']) if str(row['PLO']) != "nan" else ""
        sub_plo = str(row['SubPLO']) if str(row['SubPLO']) != "nan" else ""
        sub_plo_description = str(row['SubPLO_Description']) if str(row['SubPLO_Description']) != "nan" else ""
        domain = str(row['Learning Domain']) if str(row['Learning Domain']) != "nan" else ""
        know_cat = str(row['Knowledge Category']) if str(row['Knowledge Category']) != "nan" else ""
        nqf_auth_resp = 'Y' if str(row['KKNI wewenang & tanggung jawab']) != "nan" else "N"
        nqf_knowledge = 'Y' if str(row['KKNI pengetahuan']) != "nan" else "N"
        nqf_working_skill = 'Y' if str(row['KKNI Kemampuan bidang kerja']) != "nan" else "N"
        ns_attitude = 'Y' if str(row['SNDIKTI sikap']) != "nan" else "N"
        ns_knowledge = 'Y' if str(row['SNDIKTI pengetahuan']) != "nan" else "N"
        ns_generic_skill = 'Y' if str(row['SNDIKTI keterampilan umum']) != "nan" else "N"
        ns_specific_skill = 'Y' if str(row['SNDIKTI keterampilan khusus']) != "nan" else "N"

        if not all([curriculum, peo, plo, sub_plo, sub_plo_description]):
            error_list.append(index+2)
            continue
        
        print("HALOGAN")
        curriculum = clean_cell(curriculum)
        peo = clean_cell(peo)
        plo = clean_cell(plo)
        sub_plo = clean_cell(sub_plo)

        domain_lst = domain.split(", ")
        
        # domain list processing query
        domain_query = "\n".join(f":hasDomain :{item} ;" for item in domain_lst)

        query_string = f"""
            PREFIX : <{PREFIX}>
            PREFIX owl: <{OWL}>
            PREFIX rdf: <{RDF}>

            INSERT {{
                :{curriculum}-{plo} a :ProgramLearningOutcome .
            }} 
            WHERE {{
                FILTER NOT EXISTS {{
                    :{curriculum}-{plo} a :ProgramLearningOutcome .
                }}
            }};

            DELETE {{
                :{curriculum}-{sub_plo}  a :SubProgramLearningOutcome ;
                        :label ?oldPLOLabel ;
                        :hasDomain ?oldDomain ;
                        :nqfAuthorityResponsibility ?oldNQFAuthorityResp ;
                        :nqfKnowledge ?oldNQFKnowledge ;
                        :nqfWorkingSkill ?oldNQFWorkingSkill ;
                        :nsAttitude ?oldNSAttitude ;
                        :nsKnowledge ?oldNSKnowledge ;
                        :nsGenericSkill ?oldNSGenericSkill ;
                        :nsSpecificSkill ?oldNSSpecificSkill .
            }}
            INSERT {{
                :{curriculum}-{sub_plo}  a :SubProgramLearningOutcome ;
                        :label "{sub_plo_description}" ;
                        {domain_query}
                        {f':nqfAuthorityResponsibility "{nqf_auth_resp}" ;'   if nqf_auth_resp != "" else ""}
                        {f':nqfKnowledge "{nqf_knowledge}" ;'                 if nqf_knowledge != "" else ""}
                        {f':nqfWorkingSkill "{nqf_working_skill}" ;'          if nqf_working_skill != "" else ""}
                        {f':nsAttitude "{ns_attitude}" ;'                     if ns_attitude != "" else ""}
                        {f':nsKnowledge "{ns_knowledge}" ;'                   if ns_knowledge != "" else ""}
                        {f':nsGenericSkill "{ns_generic_skill}" ;'            if ns_generic_skill != "" else ""}
                        {f':nsSpecificSkill "{ns_specific_skill}" ;'          if ns_specific_skill != "" else ""}
            }}
            WHERE {{
                OPTIONAL {{ 
                    :{curriculum}-{sub_plo}  a :SubProgramLearningOutcome ;
                            :label ?oldPLOLabel .
                    }}
            }};

            INSERT {{
                    :{curriculum}-{sub_plo} :partOf :{curriculum}-{plo}
                }}
            WHERE {{
                FILTER EXISTS {{
                    :{curriculum}-{plo} a :ProgramLearningOutcome .
                    :{curriculum}-{sub_plo} a :SubProgramLearningOutcome .
                }}
            }}
            """

        sparql = SPARQLWrapper(GRAPHDB_POST) 
        sparql.setQuery(query_string)
        sparql.setReturnFormat(JSON)
        sparql.setMethod("POST")

        print("sparqql", query_string)

        sparql.queryAndConvert()
        
    return error_list

def import_PLO_CLO(excel_file):
    error_list = []

    # Transform data to dataframe pandas
    df = pd.read_excel(excel_file,sheet_name='PLO_CLO') # sheet_name = Sheet seq. number on excel/Sheet name

    for index, row in df.iterrows():
        plo = str(row['PLO']) if str(row['PLO']) != "nan" else ""
        clo = str(row['CLO']) if str(row['CLO']) != "nan" else ""
        description = str(row['Description']) if str(row['Description']) != "nan" else ""
        domain = str(row['Learning Domain']) if str(row['Learning Domain']) != "nan" else ""
        knowledge_cat = str(row['Knowledge Category']) if str(row['Knowledge Category']) != "nan" else ""

        if not all([plo, clo, domain, knowledge_cat]):
            error_list.append(index+2)
            continue
        
        plo = clean_cell(plo)
        clo = clean_cell(clo)

        domain_lst = domain.split(", ")
        
        # domain list processing query
        domain_query = "\n".join(f":hasDomain :{item} ;" for item in domain_lst)
        
        query_string = f"""
            PREFIX : <{PREFIX}>
            PREFIX owl: <{OWL}>
            PREFIX rdf: <{RDF}>

            INSERT {{
                :{plo} a :ProgramLearningOutcome .
            }} 
            WHERE {{
                FILTER NOT EXISTS {{
                    :{plo} a :ProgramLearningOutcome .
                }}
            }};

            DELETE {{
                :{clo}  a :CourseLearningOutcome ;
                        :label ?oldDescription ;
                        :partOf ?oldPLO ;
                        :hasDomain ?oldDomain ;
                        :nsKnowledge ?oldNSKnowledge .
            }}
            INSERT {{
                :{clo}  a :CourseLearningOutcome ;
                        :label "{description}" ;
                        :partOf :{plo} ;
                        {domain_query}
                        :nsKnowledge "{knowledge_cat}" .
            }}
            WHERE {{
                OPTIONAL {{
                    :{clo}  a :CourseLearningOutcome ;
                            :partOf ?oldPLO ;
                            :hasDomain ?oldDomain .
                }}
            }}
            """

        sparql = SPARQLWrapper(GRAPHDB_POST) 
        sparql.setQuery(query_string)
        sparql.setReturnFormat(JSON)
        sparql.setMethod("POST")

        print("sparqql", query_string)

        sparql.queryAndConvert()
        
    return error_list

def import_CLO_ULO(excel_file):
    error_list = []

    # Transform data to dataframe pandas
    df = pd.read_excel(excel_file,sheet_name='CLO_ULO') # sheet_name = Sheet seq. number on excel/Sheet name

    for index, row in df.iterrows():
        clo = str(row['CLO']) if str(row['CLO']) != "nan" else ""
        ulo = str(row['ULO']) if str(row['ULO']) != "nan" else ""
        # description = str(row['Description']) if str(row['Description']) != "nan" else ""
        domain = str(row['Learning Domain']) if str(row['Learning Domain']) != "nan" else ""
        knowledge_cat = str(row['Knowledge Category']) if str(row['Knowledge Category']) != "nan" else ""

        if not all([clo, ulo, domain, knowledge_cat]):
            error_list.append(index+2)
            continue
        
        clo = clean_cell(clo)
        ulo = clean_cell(ulo)

        domain_lst = domain.split(", ")
        
        # domain list processing query
        domain_query = "\n".join(f":hasDomain :{item} ;" for item in domain_lst)
        
        query_string = f"""
            PREFIX : <{PREFIX}>
            PREFIX owl: <{OWL}>
            PREFIX rdf: <{RDF}>

            INSERT {{
                :{clo} a :CourseLearningOutcome .
            }} 
            WHERE {{
                FILTER NOT EXISTS {{
                    :{clo} a :CourseLearningOutcome .
                }}
            }};

            DELETE {{
                :{ulo}  a :UnitLearningOutcome ;
                        :partOf ?oldCLO ;
                        :label ?oldDescription ;
                        :hasDomain ?oldDomain ;
                        :nsKnowledge ?oldNSKnowledge .
            }}
            INSERT {{
                :{ulo}  a :UnitLearningOutcome ;
                        :partOf :{clo} ;

                        {domain_query}
                        :nsKnowledge "{knowledge_cat}" .
            }}
            WHERE {{
                OPTIONAL {{
                    :{ulo}  a :UnitLearningOutcome ;
                            :partOf ?oldCLO ;
                            :hasDomain ?oldDomain ;
                            :nsKnowledge ?oldNSKnowledge .
                }}
            }}
            """

        sparql = SPARQLWrapper(GRAPHDB_POST) 
        sparql.setQuery(query_string)
        sparql.setReturnFormat(JSON)
        sparql.setMethod("POST")

        print("sparqql", query_string)

        sparql.queryAndConvert()
        
    return error_list

def import_ULO_criteria(excel_file):
    error_list = []

    # Transform data to dataframe pandas
    df = pd.read_excel(excel_file,sheet_name='ULO_Criteria (OPTIONAL)') # sheet_name = Sheet seq. number on excel/Sheet name

    for index, row in df.iterrows():
        ulo = str(row['ULO']) if str(row['ULO']) != "nan" else ""
        criteria = str(row['Criteria']) if str(row['Criteria']) != "nan" else ""

        if not all([ulo, criteria]):
            error_list.append(index+2)
            continue
        
        ulo = clean_cell(ulo)
        criteria = clean_cell(criteria)
        

        query_string = f"""
            PREFIX : <{PREFIX}>
            PREFIX owl: <{OWL}>
            PREFIX rdf: <{RDF}>

            INSERT {{
                :{ulo} a :UnitLearningOutcome .
            }} 
            WHERE {{
                FILTER NOT EXISTS {{
                    :{ulo} a :UnitLearningOutcome .
                }}
            }};

            INSERT {{
                :{criteria}  a :Criteria .
            }}
            WHERE {{
                FILTER NOT EXISTS {{
                    :{criteria} a :Criteria .
                }}
            }};

            INSERT {{
                :{ulo} :hasCriteria :{criteria} .
            }}
            WHERE {{
                FILTER NOT EXISTS {{
                    :{ulo} :hasCriteria :{criteria} .
                }}
            }}
            """

        sparql = SPARQLWrapper(GRAPHDB_POST) 
        sparql.setQuery(query_string)
        sparql.setReturnFormat(JSON)
        sparql.setMethod("POST")

        print("sparqql", query_string)

        sparql.queryAndConvert()
        
    return error_list

def import_curriculum_course(excel_file):
    error_list = []

    # Transform data to dataframe pandas
    df = pd.read_excel(excel_file,sheet_name='Curriculum_Course') # sheet_name = Sheet seq. number on excel/Sheet name

    for index, row in df.iterrows():
        curriculum = str(row['Curriculum']) if str(row['Curriculum']) != "nan" else ""
        course = str(row['Course']) if str(row['Course']) != "nan" else ""

        if not all([curriculum, course]):
            error_list.append(index+2)
            continue
        
        curriculum = clean_cell(curriculum)
        course = clean_cell(course)
        

        query_string = f"""
            PREFIX : <{PREFIX}>
            PREFIX owl: <{OWL}>
            PREFIX rdf: <{RDF}>

            INSERT {{
                :{curriculum} a :Curriculum .
            }} 
            WHERE {{
                FILTER NOT EXISTS {{
                    :{curriculum} a :Curriculum .
                }}
            }};

            INSERT {{
                :{course}  a :Course .
            }}
            WHERE {{
                FILTER NOT EXISTS {{
                    :{course} a :Course .
                }}
            }};

            INSERT {{
                :{curriculum} :hasCriteria :{course} .
            }}
            WHERE {{
                FILTER NOT EXISTS {{
                    :{curriculum} :hasCriteria :{course} .
                }}
            }}
            """

        sparql = SPARQLWrapper(GRAPHDB_POST) 
        sparql.setQuery(query_string)
        sparql.setReturnFormat(JSON)
        sparql.setMethod("POST")

        print("sparqql", query_string)

        sparql.queryAndConvert()
        
    return error_list

def import_course_CLO(excel_file):
    error_list = []

    # Transform data to dataframe pandas
    df = pd.read_excel(excel_file,sheet_name='Course_CLO') # sheet_name = Sheet seq. number on excel/Sheet name

    for index, row in df.iterrows():
        course = str(row['Course']) if str(row['Course']) != "nan" else ""
        clo = str(row['CLO']) if str(row['CLO']) != "nan" else ""


        if not all([course, clo]):
            error_list.append(index+2)
            continue
        
        course = clean_cell(course)
        clo = clean_cell(clo)
        

        query_string = f"""
            PREFIX : <{PREFIX}>
            PREFIX owl: <{OWL}>
            PREFIX rdf: <{RDF}>

            INSERT {{
                :{course} a :Course .
            }} 
            WHERE {{
                FILTER NOT EXISTS {{
                    :{course} a :Course .
                }}
            }};

            INSERT {{
                :{clo}  a :CLO .
            }}
            WHERE {{
                FILTER NOT EXISTS {{
                    :{clo} a :CLO .
                }}
            }};

            INSERT {{
                :{course} :hasCLO :{clo} .
            }}
            WHERE {{
                FILTER NOT EXISTS {{
                    :{course} :hasCLO :{clo} .
                }}
            }}
            """

        sparql = SPARQLWrapper(GRAPHDB_POST) 
        sparql.setQuery(query_string)
        sparql.setReturnFormat(JSON)
        sparql.setMethod("POST")

        print("sparqql", query_string)

        sparql.queryAndConvert()
        
    return error_list

def import_course_PLO(excel_file):
    error_list = []

    # Transform data to dataframe pandas
    df = pd.read_excel(excel_file,sheet_name='Course_PLO') # sheet_name = Sheet seq. number on excel/Sheet name

    for index, row in df.iterrows():
        course = str(row['Course']) if str(row['Course']) != "nan" else ""
        plo = str(row['PLO']) if str(row['PLO']) != "nan" else ""


        if not all([course, plo]):
            error_list.append(index+2)
            continue
        
        course = clean_cell(course)
        plo = clean_cell(plo)
        

        query_string = f"""
            PREFIX : <{PREFIX}>
            PREFIX owl: <{OWL}>
            PREFIX rdf: <{RDF}>

            INSERT {{
                :{course} a :Course .
            }} 
            WHERE {{
                FILTER NOT EXISTS {{
                    :{course} a :Course .
                }}
            }};

            INSERT {{
                :{plo}  a :PLO .
            }}
            WHERE {{
                FILTER NOT EXISTS {{
                    :{plo} a :PLO .
                }}
            }};

            INSERT {{
                :{plo} :ploHasCourse :{course} .
            }}
            WHERE {{
                FILTER NOT EXISTS {{
                    :{plo} :ploHasCourse :{course} .
                }}
            }}
            """

        sparql = SPARQLWrapper(GRAPHDB_POST) 
        sparql.setQuery(query_string)
        sparql.setReturnFormat(JSON)
        sparql.setMethod("POST")

        print("sparqql", query_string)

        sparql.queryAndConvert()
        
    return error_list

def import_course_content(excel_file):
    error_list = []

    # Transform data to dataframe pandas
    df = pd.read_excel(excel_file,sheet_name='Course_Content') # sheet_name = Sheet seq. number on excel/Sheet name

    for index, row in df.iterrows():
        course = str(row['Course']) if str(row['Course']) != "nan" else ""
        content = str(row['Content']) if str(row['Content']) != "nan" else ""


        if not all([course, content]):
            error_list.append(index+2)
            continue
        
        course = clean_cell(course)
        content = clean_cell(content)
        

        query_string = f"""
            PREFIX : <{PREFIX}>
            PREFIX owl: <{OWL}>
            PREFIX rdf: <{RDF}>

            INSERT {{
                :{course} a :Course .
            }} 
            WHERE {{
                FILTER NOT EXISTS {{
                    :{course} a :Course .
                }}
            }};

            INSERT {{
                :{content}  a :Content .
            }}
            WHERE {{
                FILTER NOT EXISTS {{
                    :{content} a :Content .
                }}
            }};

            INSERT {{
                :{course} :coversContent :{content} .
            }}
            WHERE {{
                FILTER NOT EXISTS {{
                    :{course} :coversContent :{content} .
                }}
            }}
            """

        sparql = SPARQLWrapper(GRAPHDB_POST) 
        sparql.setQuery(query_string)
        sparql.setReturnFormat(JSON)
        sparql.setMethod("POST")

        print("sparqql", query_string)

        sparql.queryAndConvert()
        
    return error_list

def import_content_knowledgecat(excel_file):
    error_list = []

    # Transform data to dataframe pandas
    df = pd.read_excel(excel_file,sheet_name='Content_KnowledgeCat') # sheet_name = Sheet seq. number on excel/Sheet name

    for index, row in df.iterrows():
        content = str(row['Content']) if str(row['Content']) != "nan" else ""
        know_cat = str(row['Knowledge Category']) if str(row['Knowledge Category']) != "nan" else ""


        if not all([content, know_cat]):
            error_list.append(index+2)
            continue
        
        content = clean_cell(content)
        know_cat = clean_cell(know_cat)
        

        query_string = f"""
            PREFIX : <{PREFIX}>
            PREFIX owl: <{OWL}>
            PREFIX rdf: <{RDF}>

            INSERT {{
                :{content} a :Content .
            }} 
            WHERE {{
                FILTER NOT EXISTS {{
                    :{content} a :Content .
                }}
            }};

            INSERT {{
                :{know_cat}  a :KnowledgeCategory .
            }}
            WHERE {{
                FILTER NOT EXISTS {{
                    :{know_cat} a :KnowledgeCategory .
                }}
            }};

            INSERT {{
                :{content} :hasKnowCat :{know_cat} .
            }}
            WHERE {{
                FILTER NOT EXISTS {{
                    :{content} :hasKnowCat :{know_cat} .
                }}
            }}
            """

        sparql = SPARQLWrapper(GRAPHDB_POST) 
        sparql.setQuery(query_string)
        sparql.setReturnFormat(JSON)
        sparql.setMethod("POST")

        print("sparqql", query_string)

        sparql.queryAndConvert()
        
    return error_list