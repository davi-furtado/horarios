from sqlalchemy import Column, Integer, String, Enum, ForeignKey, Time, Table, UniqueConstraint, CheckConstraint, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

professor_materia_table = Table(
    'professor_materia',
    Base.metadata,
    Column('professor_id', Integer, ForeignKey('professores.id', ondelete='CASCADE'), primary_key=True),
    Column('materia_id', Integer, ForeignKey('materias.id', ondelete='CASCADE'), primary_key=True)
)

aula_professor_table = Table(
    'aula_professor',
    Base.metadata,
    Column('aula_id', Integer, ForeignKey('aulas.id', ondelete='CASCADE'), primary_key=True),
    Column('professor_id', Integer, ForeignKey('professores.id', ondelete='CASCADE'), primary_key=True),
    Index('idx_ap_professor', 'professor_id')
)


class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(150), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    tipo = Column(Enum('admin', 'professor'), nullable=False, default='professor')

    professor = relationship('Professor', back_populates='usuario', uselist=False)


class Professor(Base):
    __tablename__ = 'professores'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    usuario_id = Column(Integer, ForeignKey('usuarios.id', ondelete='SET NULL'), unique=True)

    usuario = relationship('Usuario', back_populates='professor')
    materias = relationship('Materia', secondary=professor_materia_table, back_populates='professores')
    aulas = relationship('Aula', secondary=aula_professor_table, back_populates='professores')
    restricoes = relationship('RestricaoProfessor', back_populates='professor', cascade='all, delete-orphan')

    __table_args__ = (
        Index('idx_prof_nome', 'nome'),
    )


class Materia(Base):
    __tablename__ = 'materias'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), unique=True, nullable=False)

    professores = relationship('Professor', secondary=professor_materia_table, back_populates='materias')
    aulas = relationship('Aula', back_populates='materia')


class Curso(Base):
    __tablename__ = 'cursos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), unique=True, nullable=False)

    turmas = relationship('Turma', back_populates='curso', cascade='all, delete-orphan')
    restricoes = relationship('RestricaoCurso', back_populates='curso', cascade='all, delete-orphan')


class Sala(Base):
    __tablename__ = 'salas'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), unique=True, nullable=False)
    tipo = Column(Enum('sala', 'lab', 'quadra', 'outro'), default='sala', nullable=False)

    turmas = relationship('Turma', back_populates='sala')
    aulas = relationship('Aula', back_populates='sala')

    __table_args__ = (
        Index('idx_salas_tipo', 'tipo'),
    )


class Turma(Base):
    __tablename__ = 'turmas'

    id = Column(Integer, primary_key=True, autoincrement=True)
    serie = Column(Integer)
    curso_id = Column(Integer, ForeignKey('cursos.id', ondelete='CASCADE'), nullable=False)
    letra = Column(String(1))
    sala_id = Column(Integer, ForeignKey('salas.id', ondelete='SET NULL'))

    curso = relationship('Curso', back_populates='turmas')
    sala = relationship('Sala', back_populates='turmas')
    aulas = relationship('Aula', back_populates='turma', cascade='all, delete-orphan')

    __table_args__ = (
        UniqueConstraint('serie', 'curso_id', 'letra', name='uq_turma_serie_curso_letra'),
        CheckConstraint('serie IS NULL OR serie >= 1'),
        Index('idx_turma_curso', 'curso_id'),
        Index('idx_turma_serie', 'serie'),
    )


class Aula(Base):
    __tablename__ = 'aulas'

    id = Column(Integer, primary_key=True, autoincrement=True)
    turma_id = Column(Integer, ForeignKey('turmas.id', ondelete='CASCADE'), nullable=False)
    materia_id = Column(Integer, ForeignKey('materias.id', ondelete='CASCADE'), nullable=False)
    dia_semana = Column(Integer, nullable=False)
    hora_inicio = Column(Time, nullable=False)
    hora_fim = Column(Time, nullable=False)
    subturma = Column(String(1))
    sala_id = Column(Integer, ForeignKey('salas.id', ondelete='CASCADE'), nullable=False)

    turma = relationship('Turma', back_populates='aulas')
    materia = relationship('Materia', back_populates='aulas')
    sala = relationship('Sala', back_populates='aulas')
    professores = relationship('Professor', secondary=aula_professor_table, back_populates='aulas')

    __table_args__ = (
        CheckConstraint('dia_semana BETWEEN 1 AND 5'),
        CheckConstraint('hora_inicio < hora_fim'),
        Index('idx_aulas_turma', 'turma_id'),
        Index('idx_aulas_dia', 'dia_semana'),
        Index('idx_aulas_horario', 'hora_inicio', 'hora_fim'),
    )


class RestricaoCurso(Base):
    __tablename__ = 'restricoes_curso'

    id = Column(Integer, primary_key=True)
    curso_id = Column(Integer, ForeignKey('cursos.id', ondelete='CASCADE'), nullable=False)
    dia_semana = Column(Integer, nullable=False)
    hora_inicio = Column(Time, nullable=False)
    hora_fim = Column(Time, nullable=False)

    curso = relationship('Curso', back_populates='restricoes')

    __table_args__ = (
        CheckConstraint('dia_semana BETWEEN 1 AND 5'),
        CheckConstraint('hora_inicio < hora_fim'),
        Index('idx_rc_curso', 'curso_id'),
        Index('idx_rc_dia', 'dia_semana'),
    )


class RestricaoProfessor(Base):
    __tablename__ = 'restricoes_professor'

    id = Column(Integer, primary_key=True)
    professor_id = Column(Integer, ForeignKey('professores.id', ondelete='CASCADE'), nullable=False)
    dia_semana = Column(Integer, nullable=False)
    hora_inicio = Column(Time, nullable=False)
    hora_fim = Column(Time, nullable=False)

    professor = relationship('Professor', back_populates='restricoes')

    __table_args__ = (
        CheckConstraint('dia_semana BETWEEN 1 AND 5'),
        CheckConstraint('hora_inicio < hora_fim'),
        Index('idx_rp_prof', 'professor_id'),
        Index('idx_rp_dia', 'dia_semana'),
    )