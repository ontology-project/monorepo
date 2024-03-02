import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status 
from neo4j import GraphDatabase
from neo4j.exceptions import ClientError

NEO4J_URI = os.environ.get("NEO4J_URI")
NEO4J_USER = os.environ.get("NEO4J_USERNAME")
NEO4J_PASSWORD = os.environ.get("NEO4J_PASSWORD")

class GetMessageView(APIView):
    def get(self, request):
        message = f"Hello from the server! {NEO4J_URI} {NEO4J_USER} {NEO4J_PASSWORD}"
        return Response({'message': message})

class CreateNodeView(APIView):
    def post(self, request):
        node_name = request.data.get('name')
        node_type = request.data.get('type')

        if not node_name or not node_type:
            return Response({'error': 'Some error'}, status=status.HTTP_400_BAD_REQUEST)

        driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

        query = f"MERGE (n:{node_type} {{label: '{node_name}'}}) RETURN n"

        #  CREATE (charlie:Person:Actor {name: 'Charlie Sheen'}), (oliver:Person:Director {name: 'Oliver Stone'})
        with driver.session() as session:
            session.run(query)

        return Response({'name': node_name, 'type': node_type}, status=status.HTTP_201_CREATED)
    
class CreateNodeWithRelationshipView(APIView):
    def post(self, request):
        node_name = request.data.get('name')
        node_type = request.data.get('type')
        other_node_name = request.data.get('otherName')
        other_node_type = request.data.get('otherType')
        relationship_type = request.data.get('relationshipType')

        print(node_name, node_type, other_node_name, other_node_type, relationship_type)

        if not all([node_name, other_node_name, relationship_type]):
            return Response(
                {'error': 'Some error'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

        with driver.session() as session:
            query = f"""
                    MERGE (otherNode:{other_node_type} {{label: '{other_node_name}'}})
                    MERGE (node:{node_type} {{label: '{node_name}'}})
                    MERGE (node) -[r:{relationship_type}]-> (otherNode) 
                    RETURN node
                    """
            
            print("query ")
            print(query)

            try:
                session.run(query)
            except ClientError as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST) 
            
        return Response({'name': node_name, 'other_name': other_node_name, 'relationship': relationship_type}, status=status.HTTP_201_CREATED) 
    


# Neo4j gone wrong

# def add_study_program(driver, name):
#     driver.execute_query(
#         "MERGE (a:StudyProgram {curriculumName: $name}) ",
#         name=name, database_=USER,
#     )
#     return f"Study Program {name} has added successfully"

# def add_curriculum(driver, sp_name, curr_name):
#     driver.execute_query(
#         "MERGE (sp:StudyProgram {name: $sp}) "
#         "MERGE (c:Curriculum {curriculumName: $curr}) "
#         "MERGE (c)<-[:belongsToSP]-(sp) ",
#         sp=sp_name, curr=curr_name, database_=USER,
#     )
#     return f"Study Program {sp_name} has added successfully"

# def add_course(driver, course_name, curr_name):
#     driver.execute_query(
#         "MERGE (co:Course {name: $co}) "
#         "MERGE (c:Curriculum {name: $curr}) "
#         "MERGE (c)-[:hasCourse]->(co) ",
#         co=course_name, curr=curr_name, database_=USER,
#     )
#     return f"Course {course_name} has added successfully"

# def add_peo(driver, peo_name, curr_name):
#     driver.execute_query(
#         "MERGE (peo:PEO {name: $peo}) "
#         "MERGE (c:Curriculum {name: $curr}) "
#         "MERGE (c)-[:PEO]->(peo) ",
#         peo=peo_name, curr=curr_name, database_=USER,
#     )
#     return f"PEO {peo_name} has added successfully to {curr_name}"