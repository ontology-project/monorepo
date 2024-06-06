"""server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import include
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
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
    path('admin/', admin.site.urls),
    # Auth endpoints
    url(r'^auth/', include('djoser.urls')),
    url(r'^auth/', include('djoser.urls.jwt')),
    url('user/', include('users.urls')),
    # Review endpoints
    url('review/', include('review.urls')),
    # Neo4j endpoints
    url('api/get-message', GetMessageView.as_view()),
    url('api/create-node', CreateNodeView.as_view()),
    url('api/create-relationship', CreateNodeWithRelationshipView.as_view()),
    url('api/get-relationship', GetNodeWithRelationshipView.as_view()),
    url('api/get-node', GetNodeView.as_view()),
    url('api/update-node', UpdateNodeView.as_view()),
    url('api/update-relationship', UpdateNodeWithRelationshipView.as_view()),
    url('api/delete-node', DeleteNodeView.as_view()),
    url('api/delete-relationship', DeleteRelationshipView.as_view()),
    url('api/delete-field', DeleteFieldView.as_view()),
    # GraphDB endpoints
    url('api/graphdb/create-node', GraphDBCreateNodeView.as_view()),
    url('api/graphdb/create-relationship', GraphDBCreateNodeWithRelationshipView.as_view()),
    url('api/graphdb/get-classes', GraphDBGetClassesView.as_view()),
    url('api/graphdb/get-object-properties', GraphDBGetObjectPropertiesView.as_view()),
    url('api/graphdb/get-node', GraphDBGetNodeView.as_view()),
    url('api/graphdb/get-relationship', GraphDBGetNodeWithRelationshipView.as_view()),
    url('api/graphdb/get-curriculums', GraphDBGetCurriculumsView.as_view()),
    url('api/graphdb/update-node', GraphDBUpdateNodeView.as_view()),
    url('api/graphdb/update-relationship', GraphDBUpdateNodeWithRelationshipView.as_view()),
    url('api/graphdb/delete-node', GraphDBDeleteNodeView.as_view()),
    # Import Excel endpoint(s)
    url('api/import-excel', ImportExcelAPIView.as_view()),
    # GraphDB query
    url('api/get-plo', GetPLOByCurriculumAPIView.as_view()),
    url('api/get-sndikti', GetPLOByCurriculumSNDiktiAPIView.as_view()),
    url('api/get-kkni', GetPLOByCurriculumKKNIAPIView.as_view()),
    url('api/get-knowledge-cat', GetPLOByCurriculumKnowledgeCategoryAPIView.as_view()),
    url('api/get-peo-map', GetPEOMapToPLOAPIView.as_view()),
    url('api/get-curriculum-structure', GetCurriculumStructure.as_view()),
    url('api/get-course-plo-map', GetCoursePLOMapAPIView.as_view()),
    url('api/get-course-plo-clo-map', GetCoursePLOCLOMapAPIView.as_view()),
    url('api/get-peo', GetPEOByCurriculumAPIView.as_view())
]