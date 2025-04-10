from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union
from  model import Base

import re

class Grade(Base):
    __tablename__= 'grade'

    id = Column("pk_produto",Integer, primary_key=True)
    student_id = Column(Integer, nullable=False)  # Não é ForeignKey intencionalmente
    grade_1 = Column(Float, default = 0)
    grade_2 = Column(Float, default = 0)
    grade_3 = Column(Float, default = 0)
    grade_4 = Column(Float, default = 0)
    final_average = Column(Float, default = 0)

    def __init__(self,student_id:int, grade_1:float = 0, grade_2:float = 0, grade_3:float = 0, grade_4:float = 0, final_average:float = 0):
        self.student_id = student_id
        self.grade_1 = grade_1
        self.grade_2 = grade_2
        self.grade_3 = grade_3
        self.grade_4 = grade_4
        self.final_average = final_average

    @classmethod
    def empty(cls, student_id: int):
        """Cria uma Grade com todas as notas zeradas."""
        print()
        print("TO NO CURTO")
        print()
        return cls(student_id)

    @classmethod
    def full(cls, student_id: int, grade_1: float, grade_2: float, grade_3: float, grade_4: float):
        """Cria uma Grade com as notas preenchidas e média calculada automaticamente."""
        return cls(student_id, grade_1, grade_2, grade_3, grade_4)        

    def calculate_final_average(self):
        self.final_average = (self.grade_1 + self.grade_2 + self.grade_3 + self.grade_4) / 4

