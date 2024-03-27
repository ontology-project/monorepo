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

            INSERT {{
                :{curriculum} a :Curriculum ;
                    :curriculumName "{curriculum_desc}"
            }}
            WHERE {{
                FILTER NOT EXISTS {{
                    :{curriculum} a :Curriculum
                }}
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

        sparql.queryAndConvert()
        print("ACHIEVED")

    return error_list

def import_curriculum_PEO(excel_file):
    error_list = []

    # Transform data to dataframe pandas
    df = pd.read_excel(excel_file,sheet_name='Curriculum_PEO') # sheet_name = Sheet seq. number on excel/Sheet name

    for index, row in df.iterrows():
        curriculum = str(row['Curriculum']) if str(row['Curriculum']) != "nan" else ""
        peo = str(row['PEO']) if str(row['PEO']) != "nan" else ""
        nqf_auth_resp = str(row['nqfAuthorityResponsibility']) if str(row['nqfAuthorityResponsibility']) != "nan" else ""
        description = str(row['Description']) if str(row['Description']) != "nan" else ""
        ns_attitude = str(row['Attitude']) if str(row['Attitude']) != "nan" else ""
        domain = str(row['Domain']) if str(row['Domain']) != "nan" else ""

        if not all([curriculum, peo, nqf_auth_resp, description, ns_attitude, domain]):
            error_list.append(index+2)
            continue
        
        curriculum = clean_cell(curriculum)
        peo = clean_cell(peo)
        domain = clean_cell(domain)

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
                :{peo}  a :ProgramEducationalObjective ;
                        :label "{description}" ;
                        :nqfAuthorityResponsibility "{nqf_auth_resp}" ;
                        :nsAttitude "{ns_attitude}" ;
                        :hasDomain :{domain} .
            }}
            WHERE {{
                FILTER NOT EXISTS {{
                    :{peo} a :ProgramEducationalObjective .
                }}
            }};

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
        label = str(row['Description']) if str(row['Description']) != "nan" else ""

        if not all([peo, plo, sub_plo, rel, learning_domain, knowledge_cat, course_code, label]):
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

            INSERT {{
                :{plo}  a :ProgramLearningOutcome ;
                        :partOf :{peo} ;
                        :label "{label}" ;
                        :nsKnowledge "{knowledge_cat}" .
                        :hasDomain :{learning_domain} ;
            }}
            WHERE {{
                FILTER NOT EXISTS {{
                    :{plo} a :ProgramLearningOutcome .
                }}
            }}
            """
        
        if (sub_plo != "EMPTY"):
            query_string += f"""
            INSERT {{
                :{sub_plo}  a :SubProgramLearningOutcome ;
                            :partOf :{plo} ;
                            :nsKnowledge "{knowledge_cat}" .
                            :hasDomain :{learning_domain} ;
            }}
            WHERE {{
                FILTER NOT EXISTS {{
                    :{sub_plo} a :SubProgramLearningOutcome .
                }}
            }}
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

            INSERT {{
                :{clo}  a :CourseLearningOutcome ;
                        :partOf :{plo} ;
                        :hasDomain :{learning_domain} ;
                        :nsKnowledge "{knowledge_cat}" .
            }}
            WHERE {{
                FILTER NOT EXISTS {{
                    :{clo} a :CourseLearningOutcome .
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

            INSERT {{
                :{ulo}  a :UnitLearningOutcome ;
                        :partOf :{clo} ;
                        :hasDomain :{learning_domain} ;
                        :nsKnowledge "{knowledge_cat}" .
            }}
            WHERE {{
                FILTER NOT EXISTS {{
                    :{ulo} a :CourseLearningOutcome .
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
    df = pd.read_excel(excel_file,sheet_name='Course_CLO') # sheet_name = Sheet seq. number on excel/Sheet name

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