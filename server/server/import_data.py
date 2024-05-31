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
    error_dict['PEO_PLO'] = import_PEO_PLO(excel_file)
    print("Sheet 4")
    error_dict['PLO_CLO'] = import_PLO_CLO(excel_file)
    print("Sheet 5")
    error_dict['CLO_ULO'] = import_CLO_ULO(excel_file)
    print("Sheet 6")
    error_dict['ULO_Criteria (OPTIONAL)'] = import_ULO_criteria(excel_file)
    print("Sheet 7")
    error_dict['Curriculum_Course'] = import_curriculum_course(excel_file)
    print("Sheet 8")
    error_dict['Course_CLO'] = import_course_CLO(excel_file)
    print("Sheet 9")
    error_dict['Course_PLO'] = import_course_PLO(excel_file)
    print("Sheet 10")
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
        nqf_auth_resp = str(row['KKNI wewenang dan tanggung jawab']) if str(row['KKNI wewenang dan tanggung jawab']) != "nan" else ""
        description = str(row['Description']) if str(row['Description']) != "nan" else ""
        domain = str(row['Domain']) if str(row['Domain']) != "nan" else ""
        nqf_knowledge = str(row['KKNI pengetahuan']) if str(row['KKNI pengetahuan']) != "nan" else ""
        nqf_working_skill = str(row['KKNI keterampilan kerja']) if str(row['KKNI keterampilan kerja']) != "nan" else ""
        ns_attitude = str(row['SNDIKTI sikap']) if str(row['SNDIKTI sikap']) != "nan" else ""
        ns_knowledge = str(row['SNDIKTI pengetahuan']) if str(row['SNDIKTI pengetahuan']) != "nan" else ""
        ns_generic_skill = str(row['SNDIKTI keterampilan umum']) if str(row['SNDIKTI keterampilan umum']) != "nan" else ""
        ns_specific_skill = str(row['SNDIKTI keterampilan khusus']) if str(row['SNDIKTI keterampilan khusus']) != "nan" else ""

        if not all([curriculum, peo, description, domain]):
            error_list.append(index+2)
            continue
        
        print("HALOGAN")
        curriculum = clean_cell(curriculum)
        peo = clean_cell(peo)
        domain = clean_cell(domain)
        description = clean_cell(description)
        nqf_auth_resp = clean_cell(nqf_auth_resp)
        nqf_knowledge = clean_cell(nqf_knowledge)
        nqf_working_skill = clean_cell(nqf_working_skill)
        ns_attitude = clean_cell(ns_attitude)
        ns_knowledge = clean_cell(ns_knowledge)
        ns_generic_skill = clean_cell(ns_generic_skill)
        ns_specific_skill = clean_cell(ns_specific_skill)

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
                :{peo}  a :ProgramEducationalObjective ;
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
                :{peo}  a :ProgramEducationalObjective ;
                        :label "{description}" ;
                        :hasDomain :{domain} ;
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
                    :{peo}  a :ProgramEducationalObjective ;
                            :label ?oldPEOLabel ;
                            :hasDomain ?oldDomain . 
                    }}
            }}; 
            """
        
        query_string += f"""
            INSERT {{
                    :{curriculum} :hasPEO :{peo} .
                }}
                WHERE {{
                    FILTER NOT EXISTS {{
                        :{curriculum} :hasPEO :{peo} .
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

def import_PEO_PLO(excel_file):
    error_list = []

    # Transform data to dataframe pandas
    df = pd.read_excel(excel_file,sheet_name='PEO_PLO') # sheet_name = Sheet seq. number on excel/Sheet name

    for index, row in df.iterrows():
        peo = str(row['PEO']) if str(row['PEO']) != "nan" else ""
        plo = str(row['PLO']) if str(row['PLO']) != "nan" else ""
        sub_plo = str(row['Sub PLO']) if str(row['Sub PLO']) != "nan" else "EMPTY"
        rel = str(row['Relation To PEO']) if str(row['Relation To PEO']) != "nan" else ""
        learning_domain = str(row['Learning Domain']) if str(row['Learning Domain']) != "nan" else ""
        knowledge_cat = str(row['Knowledge Category']) if str(row['Knowledge Category']) != "nan" else ""
        course_code = str(row['Course Code']) if str(row['Course Code']) != "nan" else ""
        description = str(row['Description']) if str(row['Description']) != "nan" else ""
        nqf_authority_responsibility = str(row['KKNI wewenang dan tanggung jawab']) if str(row['KKNI wewenang dan tanggung jawab']) != "nan" else ""
        nqf_knowledge = str(row['KKNI pengetahuan']) if str(row['KKNI pengetahuan']) != "nan" else ""
        nqf_working_skill = str(row['KKNI keterampilan kerja']) if str(row['KKNI keterampilan kerja']) != "nan" else ""
        ns_attitude = str(row['SNDIKTI sikap']) if str(row['SNDIKTI sikap']) != "nan" else ""
        ns_knowledge = str(row['SNDIKTI pengetahuan']) if str(row['SNDIKTI pengetahuan']) != "nan" else ""
        ns_generic_skill = str(row['SNDIKTI keterampilan umum']) if str(row['SNDIKTI keterampilan umum']) != "nan" else ""
        ns_specific_skill = str(row['SNDIKTI keterampilan khusus']) if str(row['SNDIKTI keterampilan khusus']) != "nan" else ""

        

        if not all([peo, plo, sub_plo, rel, learning_domain, knowledge_cat, course_code, description, nqf_authority_responsibility, nqf_knowledge,
                    nqf_working_skill, ns_attitude, ns_generic_skill, ns_specific_skill]):
            error_list.append(index+2)
            continue
        
        peo = clean_cell(peo)
        plo = clean_cell(plo)
        sub_plo = clean_cell(sub_plo)
        rel = clean_cell(rel)
        

        query_string = f"""
            PREFIX : <{PREFIX}>
            PREFIX owl: <{OWL}>
            PREFIX rdf: <{RDF}>

            INSERT {{
                :{peo} a :ProgramEducationalObjective .
            }} 
            WHERE {{
                FILTER NOT EXISTS {{
                    :{peo} a :ProgramEducationalObjective .
                }}
            }};
            
            DELETE {{
                :{plo}  a :ProgramLearningOutcome ;
                        :partOf ?oldPLOLabel ;
                        :label ?oldLabel ;
                        :nqfAuthorityResponsibility ?oldNQFAuthorityResp ;
                        :nqfKnowledge ?oldNQFKnowledge ;
                        :nqfWorkingSkill ?oldNQFWorkingSkill ;
                        :nsAttitude ?oldNSAttitude ;
                        :nsKnowledge ?oldNSKnowledge ;
                        :nsGenericSkill ?oldNSGenericSkill ;
                        :nsSpecificSkill ?oldNSSpecificSkill ;
                        :hasDomain ?oldDomain .
            }}
            INSERT {{
                :{plo}  a :ProgramLearningOutcome ;
                        :partOf :{peo} ;
                        :label "{description}" ;
                        :nqfAuthorityResponsibility "{nqf_authority_responsibility}";
                        :nqfKnowledge "{nqf_knowledge}";
                        :nqfWorkingSkill "{nqf_working_skill}" ;
                        :nsAttitude "{ns_attitude}" ;
                        :nsKnowledge "{knowledge_cat}" ;
                        :nsGenericSkill "{ns_generic_skill}" ;
                        :nsSpecificSkill "{ns_specific_skill}" ;
                        :hasDomain :{learning_domain} .
            }}
            WHERE {{
                OPTIONAL {{ 
                    :{plo}  a :ProgramLearningOutcome ;  
                            :label ?oldPEOLabel ;
                            :hasDomain ?oldDomain .
                    }}
            }};
            """
        
        if (sub_plo != "EMPTY"):
            query_string += f"""
            DELETE {{
                :{sub_plo}  a :SubProgramLearningOutcome ;
                            :partOf ?oldPLO ;
                            :nsKnowledge ?oldNSKnowledge ;
                            :hasDomain ?oldDomain .
            }}
            INSERT {{
                :{sub_plo}  a :SubProgramLearningOutcome ;
                            :partOf :{plo} ;
                            :label "{description}" ;
                            :nsKnowledge "{knowledge_cat}" ;
                            :hasDomain :{learning_domain} .
            }}
            WHERE {{
                :{sub_plo}  a :SubProgramLearningOutcome ;
                            :partOf ?oldPLO ;
                            :hasDomain ?oldDomain .
            }};
            """
            if (rel == "yes"):
                query_string += f"""
                INSERT {{
                    :{sub_plo} :partOf :{peo}
                }}
                WHERE {{
                FILTER EXISTS {{
                    :{sub_plo} a :SubProgramLearningOutcome .
                    }}
                }}
                """
            else:
                query_string += f"""
                INSERT {{
                    :{plo} :partOf :{peo}
                }}
                WHERE {{
                FILTER EXISTS {{
                    :{plo} a :ProgramLearningOutcome .
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
        learning_domain = str(row['Learning Domain']) if str(row['Learning Domain']) != "nan" else ""
        knowledge_cat = str(row['Knowledge Category']) if str(row['Knowledge Category']) != "nan" else ""

        if not all([plo, clo, learning_domain, knowledge_cat]):
            error_list.append(index+2)
            continue
        
        plo = clean_cell(plo)
        clo = clean_cell(clo)
        

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
                        :hasDomain :{learning_domain} ;
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
        description = str(row['Description']) if str(row['Description']) != "nan" else ""
        learning_domain = str(row['Learning Domain']) if str(row['Learning Domain']) != "nan" else ""
        knowledge_cat = str(row['Knowledge Category']) if str(row['Knowledge Category']) != "nan" else ""

        if not all([clo, ulo, learning_domain, knowledge_cat]):
            error_list.append(index+2)
            continue
        
        clo = clean_cell(clo)
        ulo = clean_cell(ulo)
        

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
                        :label "{description}" ;
                        :hasDomain :{learning_domain} ;
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