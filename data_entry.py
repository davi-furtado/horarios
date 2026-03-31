from mysql.connector import connect
from csv import DictReader, DictWriter

DATA_DIR = 'dados/'

def ler_ordenar(path, lambda_key):
    arquivo = f'{DATA_DIR}{path}.csv'

    with open(arquivo, 'r', encoding='utf-8') as f:
        reader = DictReader(f)
        fieldnames = reader.fieldnames
        dados = sorted(reader, key=lambda_key)

    with open(arquivo, 'w', encoding='utf-8', newline='') as f:
        writer = DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(dados)

    return dados


def inserir(tabela, dados):
    if not dados: return

    colunas = list(dados[0].keys())
    placeholders = ', '.join(['%s'] * len(colunas))
    colunas_sql = ', '.join(colunas)

    sql = f'INSERT INTO {tabela} ({colunas_sql}) VALUES ({placeholders})'

    valores = [
        tuple(linha[col] if linha[col] != '' else None for col in colunas)
        for linha in dados
    ]

    cursor.executemany(sql, valores)


def truncate(table):
    cursor.execute(f'TRUNCATE TABLE {table}')

escolas = ler_ordenar('escolas', lambda x: x['nome'])
usuarios = ler_ordenar('usuarios', lambda x: (x['escola_id'], x['username']))
professores = ler_ordenar('professores', lambda x: (x['escola_id'], x['nome']))
materias = ler_ordenar('materias', lambda x: (x['escola_id'], x['nome']))
cursos = ler_ordenar('cursos', lambda x: (x['escola_id'], x['nome']))
salas = ler_ordenar('salas', lambda x: (x['escola_id'], x['nome']))
turmas = ler_ordenar('turmas', lambda x: (x['escola_id'], x['curso_id']))
aulas = ler_ordenar(
    'aulas',
    lambda x: (
        x['escola_id'],
        x['turma_id'],
        x['dia_semana'],
        x['hora_inicio'],
        x['subturma'] or ''
    )
)
aula_professor = ler_escrever('aula_professor', lambda x: (x['escola_id'], x['aula_id']))

connection = connect(
    host='localhost',
    user='root',
    password='',
    database='horarios',
    charset='utf8mb4'
)
cursor = connection.cursor(dictionary=True)

inserir('escolas', escolas)
inserir('usuarios', usuarios)
inserir('professores', professores)
inserir('materias', materias)
inserir('cursos', cursos)
inserir('salas', salas)
inserir('turmas', turmas)
inserir('aulas', aulas)
inserir('aula_professor', aula_professor)

connection.commit()

cursor.close()
connection.close()