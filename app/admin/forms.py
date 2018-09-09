"""
    Instancia formularios flask para a aplicacao de administracao
"""

from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, SelectField
from wtforms.validators import DataRequired

class InserirQuestaoForm(FlaskForm):
    questao = StringField('Informe a questão:', validators=[DataRequired()])
    alternativa1 = StringField('A) Primeira alternativa:', validators=[DataRequired()])
    alternativa2 = StringField('B) Segunda alternativa:', validators=[DataRequired()])
    alternativa3 = StringField('C) Terceira alternativa:', validators=[DataRequired()])
    alternativa4 = StringField('D) Quarta alternativa:', validators=[DataRequired()])
    alternativa5 = StringField('E) Quinta alternativa (opcional):')
    alternativa_correta = SelectField(
        'Selecione a alternativa correta:',
        choices=[
            (0, '--'),
            ('alternativa1', 'A'),
            ('alternativa2', 'B'),
            ('alternativa3', 'C'),
            ('alternativa4', 'D'),
            ('alternativa5', 'E')
        ],
        validators=[DataRequired()]
    )
    cod_categoria = SelectField(
        'Selecione a categoria da questão:',
        choices=[
            (0, '--'),
            (1, 'Matemática'),
            (2, 'Geografia')
        ],
        validators=[DataRequired()],
        coerce=int
    )
    enviar = SubmitField('Inserir Questão')

class InserirCategoriaForm(FlaskForm):
    categoria_nome = StringField('Informe o nome da nova categoria:', validators=[DataRequired()])
    enviar = SubmitField('Inserir Categoria')