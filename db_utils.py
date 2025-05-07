import config


def get_connection():
    if config.DB_ENGINE == "sqlserver":
        import pyodbc
        conn_str = (
            f"DRIVER={config.DB_DRIVER};"
            f"SERVER={config.DB_SERVER};"
            f"DATABASE={config.DB_DATABASE};"
            f"UID={config.DB_USER};"
            f"PWD={config.DB_PASSWORD};"
        )
        return pyodbc.connect(conn_str)

    elif config.DB_ENGINE == "postgresql":
        import psycopg2
        conn = psycopg2.connect(
            host=config.PG_HOST,
            dbname=config.PG_DATABASE,
            user=config.PG_USER,
            password=config.PG_PASSWORD
        )
        return conn

    else:
        raise ValueError("DB_ENGINE inválido. Use 'sqlserver' ou 'postgresql'.")


def test_connection():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT GETDATE()")
        row = cursor.fetchone()
        print(f"Conexão bem-sucedida! Data atual do SQL Server: {row[0]}")
        conn.close()
    except Exception as e:
        print(f"Erro na conexão: {e}")

def get_tipos_documento():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT RTRIM(nome) FROM tipos_documento")
    tipos = [row[0].lower() for row in cursor.fetchall()]
    conn.close()
    return tipos

def get_fornecedores():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT RTRIM(nome), RTRIM(nif) FROM fornecedores")
    fornecedores = [{"nome": row[0], "nif": str(row[1])} for row in cursor.fetchall()]
    conn.close()
    return fornecedores

def get_clientes():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, RTRIM(nome), RTRIM(nif) FROM clientes")
    clientes = [{"id": row[0], "nome": row[1], "nif": str(row[2])} for row in cursor.fetchall()]
    conn.close()
    return clientes


def get_processos():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.ref, p.id_cliente, p.descricao, c.nome
        FROM processos p
        JOIN clientes c ON p.id_cliente = c.id
    """)
    processos = []
    for row in cursor.fetchall():
        processos.append({
            "ref": row[0],
            "id_cliente": row[1],
            "descricao": row[2],
            "cliente_nome": row[3]
        })
    conn.close()
    conn.close()
    return processos


def get_equipas():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, RTRIM(nome) FROM equipas")
    equipas = [{"id": row[0], "nome": row[1]} for row in cursor.fetchall()]
    conn.close()
    return equipas

def inserir_processo_se_nao_existir(ref, id_cliente, descricao=None):
    conn = get_connection()
    cursor = conn.cursor()

    # Verifica se já existe
    cursor.execute("SELECT RTRIM(ref) FROM processos WHERE ref = ?", (ref,))
    existente = cursor.fetchone()

    if not existente:
        cursor.execute("""
            INSERT INTO processos (ref, id_cliente, descricao)
            VALUES (?, ?, ?)
        """, (ref, id_cliente, descricao))
        conn.commit()
        print(f"✅ Processo '{ref}' criado.")
    else:
        print(f"ℹ️ Processo '{ref}' já existe.")

    conn.close()

def inserir_documento(id_tipo_doc, numero, data, total, caminho_pdf,
                      nif_fornecedor=None, id_equipa=None, id_processo=None):
    conn = get_connection()
    cursor = conn.cursor()

    ano = str(data.year) if data else None

    with open(caminho_pdf, "rb") as f:
        pdf_data = f.read()

    query = """
        INSERT INTO documentos (
            id_tipo_doc, numero, data, ano, total, ficheiro_pdf,
            nif_fornecedor, id_equipa, id_processo
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """

    params = (
        id_tipo_doc, numero, data, ano, total, pdf_data,
        nif_fornecedor, id_equipa, id_processo
    )

    cursor.execute(query, params)
    conn.commit()
    conn.close()
    print(f"✅ Documento '{numero}' inserido com sucesso.")

def get_tipo_doc_id_por_nome(nome):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM tipos_documento WHERE LOWER(nome) = ?", (nome.lower(),))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None


if __name__ == "__main__":
    test_connection()