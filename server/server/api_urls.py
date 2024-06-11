from django.conf.urls import include, url
from django.urls import path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from server.views import *

schema_view = get_schema_view(
   openapi.Info(
      title="Server API",
      default_version='v1',
      description="API Explorer for Server",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="google@google.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
   url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

urlpatterns += [
    # Admin endpoint
   #  path('admin/', admin.site.urls),
    # Auth endpoints
    url(r'^auth/', include('djoser.urls')),
    url(r'^auth/', include('djoser.urls.jwt')),
    url('user/', include('users.urls')),
    # Review endpoints
    url('review/', include('review.urls')),
    # Neo4j endpoints
    url('get-message', GetMessageView.as_view()),
    url('create-node', CreateNodeView.as_view()),
    url('create-relationship', CreateNodeWithRelationshipView.as_view()),
    url('get-relationship', GetNodeWithRelationshipView.as_view()),
    url('get-node', GetNodeView.as_view()),
    url('update-node', UpdateNodeView.as_view()),
    url('update-relationship', UpdateNodeWithRelationshipView.as_view()),
    url('delete-node', DeleteNodeView.as_view()),
    url('delete-relationship', DeleteRelationshipView.as_view()),
    url('delete-field', DeleteFieldView.as_view()),
    # GraphDB endpoints
    url('graphdb/create-node', GraphDBCreateNodeView.as_view()),
    url('graphdb/create-relationship', GraphDBCreateNodeWithRelationshipView.as_view()),
    url('graphdb/get-classes', GraphDBGetClassesView.as_view()),
    url('graphdb/get-object-properties', GraphDBGetObjectPropertiesView.as_view()),
    url('graphdb/get-node', GraphDBGetNodeView.as_view()),
    url('graphdb/get-relationship', GraphDBGetNodeWithRelationshipView.as_view()),
    url('graphdb/get-curriculums', GraphDBGetCurriculumsView.as_view()),
    url('graphdb/update-node', GraphDBUpdateNodeView.as_view()),
    url('graphdb/update-relationship', GraphDBUpdateNodeWithRelationshipView.as_view()),
    url('graphdb/delete-node', GraphDBDeleteNodeView.as_view()),
    # Import Excel endpoint(s)
    url('import-excel', ImportExcelAPIView.as_view()),
    # GraphDB query
    url('get-plo', GetPLOByCurriculumAPIView.as_view()),
    url('get-sndikti', GetPLOByCurriculumSNDiktiAPIView.as_view()),
    url('get-kkni', GetPLOByCurriculumKKNIAPIView.as_view()),
    url('get-knowledge-cat', GetPLOByCurriculumKnowledgeCategoryAPIView.as_view()),
    url('get-peo-map', GetPEOMapToPLOAPIView.as_view()),
    url('get-curriculum-structure', GetCurriculumStructure.as_view()),
    url('get-course-plo-map', GetCoursePLOMapAPIView.as_view()),
    url('get-course-plo-clo-map', GetCoursePLOCLOMapAPIView.as_view()),
    url('get-peo', GetPEOByCurriculumAPIView.as_view())
]