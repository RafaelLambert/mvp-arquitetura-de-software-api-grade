from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect,Flask
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Grade
from logger import logger
from schemas import GradeSchema,RollbackGradeSchema, GradeUpdateSchema, GradeSearchSchema, GradeViewSchema, GradeDelSchema,\
                            show_grade
from schemas.error import ErrorSchema
from flask_cors import CORS



info = Info(title="api-grade", version="0.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

if __name__ == '__main__':
    # Configuração da rede (host e porta)
    app.run(host='0.0.0.0', port=5002)

#definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
grade_tag = Tag(name="Grade", description="Tela de cadastro, visualização e consulta das Notas")

@app.get('/', tags=[home_tag])
def home():
    """"Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')

@app.post('/grade', tags=[grade_tag],
          responses={"200":GradeViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_grade(form: GradeSchema):
    """Adiciona um conjunto de Notas a um Aluno à base de dados

    Retorna uma representação das notas.

    """
    print()
    print("/**//**/")
    print(form)
    logger.info(form)

    grade = Grade.empty(
        student_id = form.student_id
    )
    logger.info(f"Recebido: name={form.student_id}")

    logger.warning(f"Adicionando nota ao estudante: '{grade.student_id}'")

    try:
        # criando conexão com a base
        session = Session()
        logger.warning(session)
        # adicionando grade
        session.add(grade)
        logger.warning(grade)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.warning(f"Adicionado estudante de nome: '{grade.student_id}'")
        return show_grade(grade), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Conujunto de notas já adicionado a este aluno :/"
        logger.warning(f"Erro ao adicionar estudante '{grade.student_id}', {error_msg}")
        return {"message": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo Conjunto de notas :/"
        logger.warning(f"Erro ao adicionar estudante '{grade.student_id}', {error_msg}")
        return {"message": error_msg}, 400

@app.post('/grade/rollback', tags=[grade_tag],
          responses={"200":GradeViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def rollback_add_grade(form: RollbackGradeSchema):
    """Readiciona um conjunto de Notas a um Aluno à base de dados, quando algum outro micro serviço falha nma sequência de delete

    Retorna uma representação das notas.
    """

    logger.info(form)

    grade = Grade.full(
        student_id = form.student_id,
        grade_1 = form.grade_1,
        grade_2 = form.grade_2,
        grade_3 = form.grade_3,
        grade_4 = form.grade_4,
        final_average = form.final_average
    )
    logger.info(f"Recebido: name={form.student_id}")

    logger.warning(f"Adicionando nota ao estudante: '{grade.student_id}'")

    try:
        # criando conexão com a base
        session = Session()
        logger.warning(session)
        # adicionando grade
        session.add(grade)
        logger.warning(grade)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.warning(f"Adicionado estudante de nome: '{grade.student_id}'")
        return show_grade(grade), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Conujunto de notas já adicionado a este aluno :/"
        logger.warning(f"Erro ao adicionar estudante '{grade.student_id}', {error_msg}")
        return {"message": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo Conjunto de notas :/"
        logger.warning(f"Erro ao adicionar estudante '{grade.student_id}', {error_msg}")
        return {"message": error_msg}, 400

@app.get('/grade', tags=[grade_tag],
         responses={"200": GradeViewSchema, "404": ErrorSchema})
def get_grade(query: GradeSearchSchema):
    """Faz a busca por um Grade a partir do id do grade

    Retorna uma representação dos Grades e comentários associados.
    """
    student_id = query.student_id
    logger.debug(f"Coletando dados sobre grade #{student_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    grade = session.query(Grade).filter(Grade.student_id == student_id).first()

    if not grade:
        # se o grade não foi encontrado
        error_msg = "Grade não encontrado na base :/"
        logger.warning(f"Erro ao buscar grade '{student_id}', {error_msg}")
        return {"message": error_msg}, 404
    else:
        logger.debug(f"Grade econtrado: '{grade.student_id}'")
        # retorna a representação de grade
        return show_grade(grade), 200
    
@app.delete('/grade', tags=[grade_tag],
            responses={"200": GradeViewSchema,"404": ErrorSchema})    
def del_grade(query: GradeSearchSchema):
    """Deleta uma nota de um estudante a partir do id do aluno informado

    Retorna uma mensagem de confirmação da remoção.
    """
    grade_student_id = query.student_id
    print(grade_student_id)
    logger.debug(f"Deletando dados sobre grade #{grade_student_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Grade).filter(Grade.student_id == grade_student_id).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado grade #{grade_student_id}")
        return {"message": "grade removido", "grade student_id": grade_student_id}
    else:
        # se o produto não foi encontrado
        error_msg = "Student não encontrado na base :/"
        logger.warning(f"Erro ao deletar grade #'{grade_student_id}', {error_msg}")
        return {"message": error_msg}, 404

@app.put('/grade', tags=[grade_tag],
         responses={"200": GradeViewSchema, "404": ErrorSchema, "400": ErrorSchema})
def update_grade(query: GradeSearchSchema, form: GradeUpdateSchema):
    """Atualiza as informações da nota de um estudante existente na base de dados

    Retorna a representação da nota atualizado.
    """
    logger.info("")
    logger.info(query)
    logger.info(form)
    logger.info("")
    student_id = query.student_id
    logger.debug(f"Atualizando dados do student #{student_id}")
    
    # criando conexão com a base
    session = Session()
    try:

        # buscando o estudante pelo nome
        grade = session.query(Grade).filter(Grade.student_id == student_id).first()
        
        if not grade:
            # se o estudante não for encontrado
            error_msg = "Grade student_id não encontrado na base :/"
            logger.warning(f"Erro ao atualizar grade '{student_id}', {error_msg}")
            return {"message": error_msg}, 404
        

        # atualizando os campos
        grade.grade_1 = form.grade_1
        grade.grade_2 = form.grade_2
        grade.grade_3 = form.grade_3
        grade.grade_4 = form.grade_4
        grade.calculate_final_average()
        
        # confirmando as alterações no banco
        session.commit()
        logger.debug(f"Grade student_id atualizado: '{grade.student_id}'")
        
        # retorna a representação da nota do estudante atualizado
        return show_grade(grade), 200
    
    except Exception as e:
        # caso ocorra um erro inesperado
        error_msg = "Não foi possível atualizar a nota :/"
        logger.error(f"Erro ao atualizar student's grade '{student_id}', {error_msg}: {str(e)}")
        return {"message": error_msg}, 400
    finally:
        # encerrando a sessão
        session.close()

