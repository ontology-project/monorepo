import os
from neo4j import GraphDatabase, RoutingControl

URI = os.environ.get("URI")
USER = os.environ.get("USER")
PASSWORD = os.environ.get("PASSWORD")

AUTH = (USER, PASSWORD)


def add_study_program(driver, name):
    driver.execute_query(
        "MERGE (a:StudyProgram {curriculumName: $name}) ",
        name=name, database_=USER,
    )
    return f"Study Program {name} has added successfully"

def add_curriculum(driver, sp_name, curr_name):
    driver.execute_query(
        "MERGE (sp:StudyProgram {name: $sp}) "
        "MERGE (c:Curriculum {curriculumName: $curr}) "
        "MERGE (c)<-[:belongsToSP]-(sp) ",
        sp=sp_name, curr=curr_name, database_=USER,
    )
    return f"Study Program {sp_name} has added successfully"

def add_course(driver, course_name, curr_name):
    driver.execute_query(
        "MERGE (co:Course {name: $co}) "
        "MERGE (c:Curriculum {name: $curr}) "
        "MERGE (c)-[:hasCourse]->(co) ",
        co=course_name, curr=curr_name, database_=USER,
    )
    return f"Course {course_name} has added successfully"

def add_peo(driver, peo_name, curr_name):
    driver.execute_query(
        "MERGE (peo:PEO {name: $peo}) "
        "MERGE (c:Curriculum {name: $curr}) "
        "MERGE (c)-[:PEO]->(peo) ",
        peo=peo_name, curr=curr_name, database_=USER,
    )
    return f"PEO {peo_name} has added successfully to {curr_name}"



with GraphDatabase.driver(URI, auth=AUTH) as driver:
    pass