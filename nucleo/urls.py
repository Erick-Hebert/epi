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

from django.contrib.auth.decorators import login_required
from django.views.generic import RedirectView
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('', login_required(RedirectView.as_view(url='colaborators')), name='home'),

    path('colaborators', login_required(views.home), name='nucleo-inicial'),
    path('colaborator/criar', login_required(views.tela_criar), name='nucleo-criar'),
    path('colaborator/salvar', login_required(views.salvar), name='nucleo-salvar'),
    path('colaborator/editar/<int:id>', login_required(views.editar), name='nucleo-editar'),
    path('colaborator/excluir/<int:id>', login_required(views.excluir), name='nucleo-excluir'),

    path('equipamentos', login_required(views.equipamentos), name='equipamentos-inicial'),
    path('equipamentos/criar', login_required(views.criar_equipamento), name='equipamentos-criar'),
    path('equipamentos/salvar', login_required(views.salvar_equipamento), name='equipamentos-salvar'),
    path('equipamentos/editar/<int:id>', login_required(views.editar_equipamento), name='equipamentos-editar'),
    path('equipamentos/excluir/<int:id>', login_required(views.excluir_equipamento), name='equipamentos-excluir'),
    
    path('equipamentos/registros/<int:id>', login_required(views.equipamentos_registros), name='equipamentos-registros-inicial'),
    path('equipamentos/registros/criar/<int:id>', login_required(views.criar_equipamento_registro), name='equipamentos-registros-criar'),
    path('equipamentos/registros/salvar/<int:id>', login_required(views.salvar_equipamento_registro), name='equipamentos-registros-salvar'),
    path('equipamentos/registros/editar/<int:id>', login_required(views.editar_equipamento_registro), name='equipamentos-registros-editar'),
    path('equipamentos/registros/excluir/<int:id>', login_required(views.excluir_equipamento_registro), name='equipamentos-registros-excluir'),

    path('emprestimos', login_required(views.emprestimos), name='emprestimo-inicial'),
    path('emprestimo/criar', login_required(views.criar_emprestimo), name='emprestimo-criar'),
    path('emprestimo/salvar', login_required(views.salvar_emprestimo), name='emprestimo-salvar'),
    path('emprestimos/editar/<int:id>', login_required(views.editar_emprestimo), name='emprestimo-editar'),
]
