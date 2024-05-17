import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status 
from rest_framework.parsers import MultiPartParser, FormParser
from neo4j import GraphDatabase
from neo4j.exceptions import ClientError
from SPARQLWrapper import SPARQLWrapper, JSON

from utils.constants import GRAPHDB_GET, GRAPHDB_POST, OWL, PREFIX, RDF
from utils.utils import clean_response
from .serializers import ImportSerializer
from .import_data import import_excel
import pandas as pd


# GraphDB APIs
class GraphDBCreateNodeView(APIView):
    def post(self, request):
        left_name = request.data.get('name')
        left_type = request.data.get('type')

        if not left_name or not left_type:
            return Response({'error': 'Not all values are inputted'}, status=status.HTTP_400_BAD_REQUEST)
        
        query_string = f"""
        PREFIX : <{PREFIX}> 
        INSERT DATA {{
            :{left_name} a :{left_type} .
        }}
        """

        # Invalid query example
        # query_string = f"""
        # PREFIX : <{PREFIX}> 
        # INSERT DATA {{
        #     :Whiskers a :Cat .
        #     :Whiskers a :Dog .
        # }}
        # """

        sparql = SPARQLWrapper(GRAPHDB_POST)
        sparql.setQuery(query_string)
        sparql.setReturnFormat(JSON) 
        sparql.setMethod("POST")

        try:
            results = sparql.queryAndConvert()
            return Response({'success': True, 'results': results}) 
        except Exception as e:
            error_str = clean_response(str(e))
            return Response({'success': False, 'error': error_str}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class GraphDBCreateNodeWithRelationshipView(APIView):
    def post(self, request):
        left_name = request.data.get('name')
        left_type = request.data.get('type')
        right_name = request.data.get('rightName')
        right_type = request.data.get('rightType')
        relationship_type = request.data.get('relationshipType')

        if not all([left_name, left_type, right_name, right_type, relationship_type]):
            return Response({'error': 'Name, type, and relationship type are required'}, 
                                status=status.HTTP_400_BAD_REQUEST) 

        query_string = f"""
        PREFIX : <{PREFIX}> 
        INSERT DATA {{
            :{left_name} a :{left_type} .   
            :{right_name} a :{right_type} .
            :{left_name} :{relationship_type} :{right_name} .
        }}
        """

        sparql = SPARQLWrapper(GRAPHDB_POST)
        sparql.setQuery(query_string)
        sparql.setReturnFormat(JSON) 
        sparql.setMethod("POST")

        try:
            results = sparql.queryAndConvert()
            return Response({'success': True, 'results': results}) 
        except Exception as e:
            error_str = clean_response(str(e)) 
            return Response({'success': False, 'error': error_str}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GraphDBGetClassesView(APIView):
    def get(self, request):
        print("lol")
        query_string = f"""
        PREFIX : <{PREFIX}> 
        PREFIX owl: <{OWL}>

        SELECT ?class
        WHERE {{
          ?class a owl:Class .
        }}
        """

        sparql = SPARQLWrapper(GRAPHDB_GET) 
        sparql.setQuery(query_string)
        sparql.setReturnFormat(JSON)
        sparql.setMethod("POST")


        try:
            results = sparql.queryAndConvert()
            classes = [clean_response(result["class"]["value"]) for result in results["results"]["bindings"]]
            return Response({'classes': classes})

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GraphDBGetObjectPropertiesView(APIView):
    def get(self, request):
        query_string = f"""
        PREFIX : <{PREFIX}> 
        PREFIX owl: <{OWL}>

        SELECT ?obj
        WHERE {{
          ?obj a owl:ObjectProperty .
        }}
        """

        sparql = SPARQLWrapper(GRAPHDB_GET) 
        sparql.setQuery(query_string)
        sparql.setReturnFormat(JSON)
        sparql.setMethod("POST")

        print("sparqql", sparql)

        try:
            results = sparql.queryAndConvert()
            properties = [clean_response(result["obj"]["value"]) for result in results["results"]["bindings"]]
            return Response({'properties': properties})

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GraphDBGetNodeView(APIView):
    def get(self, request):
        name = request.data.get('name')
        type = request.data.get('type')

        query_string = f"""
        PREFIX : <{PREFIX}> 
        PREFIX owl: <{OWL}>

        SELECT ?rel ?obj
        WHERE {{
          :{name} a :{type} ;
                ?rel ?obj .
        }}
        """
        sparql = SPARQLWrapper(GRAPHDB_GET) 
        sparql.setQuery(query_string)
        sparql.setReturnFormat(JSON)
        sparql.setMethod("GET")

        print("sparqql", query_string)

        try:
            results = sparql.queryAndConvert()
            properties = {clean_response(result["rel"]["value"]):clean_response(result["obj"]["value"]) for result in results["results"]["bindings"]}
            return Response({'properties': properties})

        except Exception as e:
            print(e)
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GraphDBGetNodeWithRelationshipView(APIView):
    def get(self, request):
        name = request.data.get('name')
        type = request.data.get('type')
        prefix = request.data.get('prefix') if request.data.get('prefix') else ''
        relationship_type = request.data.get('relationshipType')

        if not all([name, type, relationship_type]):
            return Response({'error': 'Name, type, and relationship type are required'}, 
                                status=status.HTTP_400_BAD_REQUEST) 

        query_string = f"""
        PREFIX : <{PREFIX}> 
        PREFIX rdf: <{RDF}>
        PREFIX owl: <{OWL}>

        SELECT ?obj
        WHERE {{
          :{name} a :{type} ;
                {prefix}:{relationship_type} ?obj .
        }}
        """

        sparql = SPARQLWrapper(GRAPHDB_GET) 
        sparql.setQuery(query_string)
        sparql.setReturnFormat(JSON)
        sparql.setMethod("POST")

        print("sparqql", query_string)

        try:
            results = sparql.queryAndConvert()
            properties = [clean_response(result["obj"]["value"]) for result in results["results"]["bindings"]]
            return Response({'properties': properties})

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GraphDBUpdateNodeView(APIView):
    def patch(self, request):
        name = request.data.get('name')
        type = request.data.get('type')
        node_field = request.data.get('field')
        node_prop = request.data.get('prop')

        if not all([name, type, node_field, node_prop]):
            return Response({'error': 'Name, type, field, and property are required'}, 
                                status=status.HTTP_400_BAD_REQUEST)
        
        query_string = f"""
        PREFIX : <{PREFIX}> 
        PREFIX rdf: <{RDF}>
        PREFIX owl: <{OWL}>

        DELETE {{
            :{name} a :{type} ;
                    :{node_field} ?oldProp .
        }}
        INSERT {{
            :{name} a :{type} ;
                    :{node_field} :{node_prop} .
        }}
        WHERE {{
            :{name} a :{type} ;
            OPTIONAL {{
                :{name} :{node_field} ?oldProp
            }}
        }}
        """
        sparql = SPARQLWrapper(GRAPHDB_POST) 
        sparql.setQuery(query_string)
        sparql.setReturnFormat(JSON)
        sparql.setMethod("POST")

        print("sparqql", query_string)

        try:
            sparql.queryAndConvert()

            return Response({'success': 'Update Success!'})

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class GraphDBUpdateNodeWithRelationshipView(APIView):
    def patch(self, request):
        left_name = request.data.get('name')
        left_type = request.data.get('type')
        right_name = request.data.get('rightName')
        right_type = request.data.get('rightType')
        rel_type = request.data.get('relType')
        rel_field = request.data.get('relField')
        rel_prop = request.data.get('relProp')

        if not all([left_name, left_type, right_name, right_type, rel_type, rel_field, rel_prop]):
            return Response({'error': 'Name, type, field, and property are required'}, 
                                status=status.HTTP_400_BAD_REQUEST)
        
        query_string = f"""
        PREFIX : <{PREFIX}> 
        PREFIX rdf: <{RDF}>
        PREFIX owl: <{OWL}>

        DELETE {{
            :{left_name} a :{left_type} .
            :{right_name} a :{right_type} .
            :{left_name} :{rel_type} :{right_name} .
            :{rel_type} :{rel_field} ?oldProp .
        }}
        INSERT {{
            :{left_name} a :{left_type} .
            :{right_name} a :{right_type} .
            :{left_name} :{rel_type} :{right_name} .
            :{rel_type} :{rel_field} :{rel_prop} .
            
        }}
        WHERE {{
            :{left_name} a :{left_type} .
            :{right_name} a :{right_type} .
            :{left_name} :{rel_type} :{right_name} .
            OPTIONAL {{
                :{rel_type} :{rel_field} ?oldProp
            }}
        }}
        """
        sparql = SPARQLWrapper(GRAPHDB_POST) 
        sparql.setQuery(query_string)
        sparql.setReturnFormat(JSON)
        sparql.setMethod("POST")

        print("sparqql", query_string)

        try:
            sparql.queryAndConvert()

            return Response({'success': 'Update Success!'})

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class GraphDBDeleteNodeView(APIView):
    def delete(self, request):
        left_name = request.data.get('name')
        left_type = request.data.get('type')

        if not all([left_name, left_type]):
            return Response({'error': 'Name, type, field, and property are required'}, 
                                status=status.HTTP_400_BAD_REQUEST)
        query_string = f"""
        PREFIX : <{PREFIX}> 
        PREFIX rdf: <{RDF}>
        PREFIX owl: <{OWL}>

        DELETE {{
            :{left_name} a :{left_type} .
            :{left_name} ?rel ?obj .
            ?rel ?field ?oldProp .
        }}
        WHERE {{
            :{left_name} a :{left_type} .
            :{left_name} ?rel ?obj .
            ?rel ?field ?oldProp .
            FILTER (STRSTARTS(STR(?rel), "{PREFIX}"))
        }}
        """

        sparql = SPARQLWrapper(GRAPHDB_POST) 
        sparql.setQuery(query_string)
        sparql.setReturnFormat(JSON)
        sparql.setMethod("POST")

        print("sparqql", query_string)

        try:
            sparql.queryAndConvert()

            return Response({'success': 'Delete Success!'})

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 
# Excel APIs
class ImportExcelAPIView(APIView):
    serializers_class = ImportSerializer
    parser_classes = [MultiPartParser, FormParser]
    
    def post(self, request):
        try:
            error_dict = {}
            data = request.FILES
            serializer = self.serializers_class(data=data)
            if not serializer.is_valid():
                return Response({
                    'status': False,
                    'message': 'Provide a valid file'
                }, status-status.HTTP_400_BAD_REQUEST)
            excel_file = data.get('file')
            print("HELLO")
            error_dict = import_excel(excel_file)
            print("OUI")   

            return Response({'success': 'Import success', 'unimported': error_dict}, status=200)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Neo4J APIs
NEO4J_URI = os.environ.get("NEO4J_URI")
NEO4J_USER = os.environ.get("NEO4J_USERNAME")
NEO4J_PASSWORD = os.environ.get("NEO4J_PASSWORD")

class GetMessageView(APIView):
    def get(self, request):
        message = f"Hello from the server! {NEO4J_URI} {NEO4J_USER} {NEO4J_PASSWORD}"
        return Response({'message': message})
    
        
class CreateNodeView(APIView):
    def post(self, request):
        left_name = request.data.get('name')
        left_type = request.data.get('type')

        if not left_name or not left_type:
            return Response({'error': 'Some error'}, status=status.HTTP_400_BAD_REQUEST)

        driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

        query = f"MERGE (n:{left_type} {{label: '{left_name}'}}) RETURN n"

        with driver.session() as session:
            session.run(query)

        return Response({'name': left_name, 'type': left_type}, status=status.HTTP_201_CREATED)


class CreateNodeWithRelationshipView(APIView):
    def post(self, request):
        left_name = request.data.get('name')
        left_type = request.data.get('type')
        right_name = request.data.get('rightName')
        right_type = request.data.get('rightType')
        relationship_type = request.data.get('relationshipType')

        print(left_name, left_type, right_name, right_type, relationship_type)

        if not all([left_name, right_name, relationship_type]):
            return Response(
                {'error': 'Some error'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

        with driver.session() as session:
            query = f"""
                    MERGE (otherNode:{right_type} {{label: '{right_name}'}})
                    MERGE (node:{left_type} {{label: '{left_name}'}})
                    MERGE (node) -[r:{relationship_type}]-> (otherNode) 
                    RETURN node
                    """
            
            print("query ")
            print(query)

            try:
                session.run(query)
            except ClientError as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST) 
            
        return Response({'name': left_name, 'other_name': right_name, 'relationship': relationship_type}, status=status.HTTP_201_CREATED)


class GetNodeWithRelationshipView(APIView):
    def get(self, request):
        left_name = request.data.get('name')
        left_type = request.data.get('type')
        right_name = request.data.get('rightName')
        right_type = request.data.get('rightType')
        relationship_type = request.data.get('relationshipType')

        print(left_name, left_type, right_name, right_type, relationship_type)

        if not all([left_name, right_name, relationship_type]):
            return Response(
                {'error': 'Some error'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

        with driver.session() as session:
            query = f"""
                    MATCH (otherNode:{right_type} {{label: '{right_name}'}})
                    MATCH (node:{left_type} {{label: '{left_name}'}})
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
        left_name = request.data.get('name')
        left_type = request.data.get('type')

        if not all([left_name]):
            return Response(
                {'error': 'Some error'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

        with driver.session() as session:
            query = f"""
                    MATCH (node:{left_type} {{label: '{left_name}'}})
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
        left_name = request.data.get('name')
        left_type = request.data.get('type')
        node_field = request.data.get('field')
        node_prop = request.data.get('prop')

        print(left_name, left_type, node_field, node_prop)

        if not all([left_name, left_type, node_field, node_prop]):
            return Response(
                {'error': 'Some error'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
        with driver.session() as session:
            query = f"""
                    MATCH (node:{left_type} {{label: '{left_name}'}})
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
        left_name = request.data.get('name')
        left_type = request.data.get('type')
        right_name = request.data.get('rightName')
        right_type = request.data.get('rightType')
        relationship_type = request.data.get('relationshipType')
        relationship_field = request.data.get('field')
        relationship_prop = request.data.get('prop')

        print(left_name, left_type, right_name, right_type, relationship_type, relationship_field, relationship_prop)

        if not all([left_name, left_type, right_name, right_type, relationship_type, relationship_field, relationship_prop]):
            return Response(
                {'error': 'Some error'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
        with driver.session() as session:
            query = f"""
                    MATCH (node:{left_type} {{label: '{left_name}'}}) -[r:{relationship_type}]-> (otherNode:{right_type} {{label: '{right_name}'}})
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
        left_name = request.data.get('name')
        left_type = request.data.get('type')
        mode = request.data.get('mode') if request.data.get('mode') else ''

        

        if not all([left_name, left_type]):
            return Response(
                {'error': 'Some error'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

        with driver.session() as session:
            query = f"""
                    MATCH (node:{left_type} {{label: '{left_name}'}})
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
        left_name = request.data.get('name')
        left_type = request.data.get('type')
        is_delete_all = request.data.get('isDeleteAll')
        right_name = request.data.get('rightName')
        right_type = request.data.get('rightType')
        relationship_type = request.data.get('relationshipType')

        if not all([left_name, left_type]):
            return Response(
                {'error': 'Some error'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        query = ""

        if (is_delete_all == 'true'):
            query = f"""
                    MATCH (node:{left_type} {{label: '{left_name}'}}) -[r]-> (o)
                    DELETE r
                    """
        elif (right_name != None or right_type != None):
            query = f"""
                    MATCH (node:{left_type} {{label: '{left_name}'}}) -[r:{relationship_type}]-> (otherNode:'{right_type}' {{label: '{right_name}'}})
                    DELETE r
                    """
        else:
            query = f"""
                    MATCH (node:{left_type} {{label: '{left_name}'}}) -[r:{relationship_type}]-> (otherNode)
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
        left_name = request.data.get('name')
        left_type = request.data.get('type')
        node_field = request.data.get('field')

        if not all([left_name, left_type]):
            return Response(
                {'error': 'Some error'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        query = f"""
                MATCH (node:{left_type} {{label: '{left_name}'}})
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
    