"""
    Instancia formularios flask para a aplicacao principal
"""

from flask_wtf import FlaskForm
from wtforms import SubmitField, RadioField, HiddenField
from ..models import Questao

class QuestaoJogoForm(FlaskForm):
    cod_questao = HiddenField(Questao.cod_questao)
    questao = RadioField(
        Questao.questao,
        choices=[
            ('alternativa1', Questao.alternativa1),
            ('alternativa2', Questao.alternativa2),
            ('alternativa3', Questao.alternativa3),
            ('alternativa4', Questao.alternativa4),
            ('alternativa5', Questao.alternativa5)
        ]
    )
    enviar = SubmitField('Confirmar')