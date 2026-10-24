"""
URL configuration for epi project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from . import views

from django.views.generic import RedirectView
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('', RedirectView.as_view(url='colaborators')),

    path('colaborators', views.home, name='nucleo-inicial'),
    path('colaborator/criar', views.tela_criar, name='nucleo-criar'),
    path('colaborator/salvar', views.salvar, name='nucleo-salvar'),
    path('colaborator/editar/<int:id>', views.editar, name='nucleo-editar'),
    path('colaborator/excluir/<int:id>', views.excluir, name='nucleo-excluir'),

    path('equipamentos', views.equipamentos, name='equipamentos-inicial'),
    path('equipamentos/criar', views.criar_equipamento, name='equipamentos-criar'),
    path('equipamentos/salvar', views.salvar_equipamento, name='equipamentos-salvar'),
    path('equipamentos/editar/<int:id>', views.editar_equipamento, name='equipamentos-editar'),
    path('equipamentos/excluir/<int:id>', views.excluir_equipamento, name='equipamentos-excluir'),
    
    path('equipamentos/registros/<int:id>', views.equipamentos_registros, name='equipamentos-registros-inicial'),
    path('equipamentos/registros/criar/<int:id>', views.criar_equipamento_registro, name='equipamentos-registros-criar'),
    path('equipamentos/registros/salvar/<int:id>', views.salvar_equipamento_registro, name='equipamentos-registros-salvar'),
    path('equipamentos/registros/editar/<int:id>', views.editar_equipamento_registro, name='equipamentos-registros-editar'),
    path('equipamentos/registros/excluir/<int:id>', views.excluir_equipamento_registro, name='equipamentos-registros-excluir'),

    path('emprestimos', views.emprestimos, name='emprestimo-inicial'),
    path('emprestimo/criar', views.criar_emprestimo, name='emprestimo-criar'),
    path('emprestimo/salvar', views.salvar_emprestimo, name='emprestimo-salvar'),
    path('emprestimos/editar/<int:id>', views.editar_emprestimo, name='emprestimo-editar'),
]
