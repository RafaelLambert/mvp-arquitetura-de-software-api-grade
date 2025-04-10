from pydantic import BaseModel
from typing import  List
from model.grade import Grade

class GradeSchema(BaseModel):
    """
    Define como um novo Grade a ser inserido, deve ser representado
    """
    student_id:int = 1

class RollbackGradeSchema(BaseModel):
    """
    Define como um novo Grade a ser inserido, deve ser representado
    """
    student_id:int = 1
    grade_1: float = 0 
    grade_2: float = 0 
    grade_3: float = 0 
    grade_4: float = 0 
    final_average: float = 0 

class GradeSearchSchema(BaseModel):
    """
    define como deve ser a estrutura que representa a busca que será
    feita apenas com base no nome do produto    
    """
    student_id:int = 1

class GradeUpdateSchema(BaseModel):
    """
    Define o schema para atualizar as notas de um estudante.
    """
    grade_1: float
    grade_2: float
    grade_3: float
    grade_4: float

class GradeViewSchema(BaseModel):
    """ Define como um Grade será retornado
    """
    id: int = 1
    id_student:int = 1
    grade_level:str = "1st grade"
    grade_1:float = "0"
    grade_2:float = "0"
    grade_3:float = "0"
    grade_4:float = "0"
    final_average:float = "0"

class GradeDelSchema(BaseModel):
    """
    Define como deve ser a estrutura do dado retornado após uma requisição
    de remoção.
    """

    message: str
    name: str

def show_grade(grade:Grade):
    """
    Retorna uma representação do estudante seguindo o schema definido em
    GradeViewSchema.        
    """
    return {
        "id": grade.id,
        "student_id":grade.student_id,
        "grade_1":grade.grade_1,
        "grade_2":grade.grade_2,
        "grade_3":grade.grade_3,
        "grade_4":grade.grade_4,
        "final_average":grade.final_average
    }
