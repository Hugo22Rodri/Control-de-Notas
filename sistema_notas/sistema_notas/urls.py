"""
URL configuration for sistema_notas project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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


from django.contrib import admin
from django.urls import path
from notas.views import dashboard
from notas.views import reporte_individual, reporte_general
from estudiantes.views import lista_estudiantes

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', dashboard, name='dashboard'),
    path('reporte-individual/', reporte_individual, name='reporte_individual'),
    path('reporte-general/', reporte_general, name='reporte_general'),
    path('estudiantes/', lista_estudiantes, name='estudiantes'),
]