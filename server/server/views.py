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

class GetNodeWithRelationshipView(APIView):
    def get(self, request):
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
                    MATCH (otherNode:{other_node_type} {{label: '{other_node_name}'}})
                    MATCH (node:{node_type} {{label: '{node_name}'}})
                    MATCH (node) -[r:{relationship_type}]-> (otherNode) 
                    RETURN node, r, otherNode
                    """
            
            print("query ")
            print(query)

            try:
                result = session.run(query)
                data = result.data()[0]
                print(data)
            except ClientError as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST) 
            
        return Response({'data': data}, status=status.HTTP_200_OK)
    
class GetNodeView(APIView):
    def get(self, request):
        node_name = request.data.get('name')
        node_type = request.data.get('type')

        if not all([node_name]):
            return Response(
                {'error': 'Some error'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

        with driver.session() as session:
            query = f"""
                    MATCH (node:{node_type} {{label: '{node_name}'}})
                    RETURN node
                    """
            
            print("query ")
            print(query)

            try:
                result = session.run(query)
                data = result.data()
                print(data)
            except ClientError as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST) 
            
        return Response({'data': data}, status=status.HTTP_200_OK)

class UpdateNodeView(APIView):
    def patch(self, request):
        node_name = request.data.get('name')
        node_type = request.data.get('type')
        node_field = request.data.get('field')
        node_prop = request.data.get('prop')

        print(node_name, node_type, node_field, node_prop)

        if not all([node_name, node_type, node_field, node_prop]):
            return Response(
                {'error': 'Some error'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
        with driver.session() as session:
            query = f"""
                    MATCH (node:{node_type} {{label: '{node_name}'}})
                    SET node.{node_field} = '{node_prop}' 
                    RETURN node
                    """
            
            print("query ")
            print(query)

            try:
                result = session.run(query)
                data = result.data()
                print(data)
            except ClientError as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST) 
            
        return Response({'data': data}, status=status.HTTP_200_OK)

class UpdateNodeWithRelationshipView(APIView):
    def patch(self, request):
        node_name = request.data.get('name')
        node_type = request.data.get('type')
        other_node_name = request.data.get('otherName')
        other_node_type = request.data.get('otherType')
        relationship_type = request.data.get('relationshipType')
        relationship_field = request.data.get('field')
        relationship_prop = request.data.get('prop')

        print(node_name, node_type, other_node_name, other_node_type, relationship_type, relationship_field, relationship_prop)

        if not all([node_name, node_type, other_node_name, other_node_type, relationship_type, relationship_field, relationship_prop]):
            return Response(
                {'error': 'Some error'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
        with driver.session() as session:
            query = f"""
                    MATCH (node:{node_type} {{label: '{node_name}'}}) -[r:{relationship_type}]-> (otherNode:{other_node_type} {{label: '{other_node_name}'}})
                    SET r.{relationship_field} = '{relationship_prop}'
                    RETURN node, r, otherNode
                    """
            
            print("query ")
            print(query)

            try:
                result = session.run(query)
                data = result.data()
                print(data)
            except ClientError as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST) 
            
        return Response({'data': data}, status=status.HTTP_200_OK)

class DeleteNodeView(APIView):
    # For the 'mode': <empty> for normal, DETACH for cascade delete relationships, NODETACH for no cascade delete relationships
    def delete(self, request):
        node_name = request.data.get('name')
        node_type = request.data.get('type')
        mode = request.data.get('mode') if request.data.get('mode') else ''

        

        if not all([node_name, node_type]):
            return Response(
                {'error': 'Some error'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

        with driver.session() as session:
            query = f"""
                    MATCH (node:{node_type} {{label: '{node_name}'}})
                    {mode} DELETE node
                    """
            
            print("query ")
            print(query)

            try:
                result = session.run(query)
                data = result.data()
                print(data)
            except ClientError as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST) 
            
        return Response({'data': data}, status=status.HTTP_200_OK)

class DeleteRelationshipView(APIView):
    def delete(self, request):
        node_name = request.data.get('name')
        node_type = request.data.get('type')
        is_delete_all = request.data.get('isDeleteAll')
        other_node_name = request.data.get('otherName')
        other_node_type = request.data.get('otherType')
        relationship_type = request.data.get('relationshipType')

        if not all([node_name, node_type]):
            return Response(
                {'error': 'Some error'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        query = ""

        if (is_delete_all == 'true'):
            query = f"""
                    MATCH (node:{node_type} {{label: '{node_name}'}}) -[r]-> (o)
                    DELETE r
                    """
        elif (other_node_name != None or other_node_type != None):
            query = f"""
                    MATCH (node:{node_type} {{label: '{node_name}'}}) -[r:{relationship_type}]-> (otherNode:'{other_node_type}' {{label: '{other_node_name}'}})
                    DELETE r
                    """
        else:
            query = f"""
                    MATCH (node:{node_type} {{label: '{node_name}'}}) -[r:{relationship_type}]-> (otherNode)
                    DELETE r
                    """

        driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

        with driver.session() as session:            
            print("query ")
            print(query)

            try:
                result = session.run(query)
                data = result.data()
                print(data)
            except ClientError as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST) 
            
        return Response({'data': data}, status=status.HTTP_200_OK)

class DeleteFieldView(APIView):
    def delete(self, request):
        node_name = request.data.get('name')
        node_type = request.data.get('type')
        node_field = request.data.get('field')

        if not all([node_name, node_type]):
            return Response(
                {'error': 'Some error'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        query = f"""
                MATCH (node:{node_type} {{label: '{node_name}'}})
                REMOVE node.{node_field}
                """
        driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

        with driver.session() as session:            
            print("query ")
            print(query)

            try:
                result = session.run(query)
                data = result.data()
                print(data)
            except ClientError as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST) 
            
        return Response({'data': data}, status=status.HTTP_200_OK)       
    