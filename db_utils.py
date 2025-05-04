import pyodbc
import config

def get_connection():
    conn_str = (
        f"DRIVER={config.DB_DRIVER};"
        f"SERVER={config.DB_SERVER};"
        f"DATABASE={config.DB_DATABASE};"
        f"UID={config.DB_USER};"
        f"PWD={config.DB_PASSWORD};"
    )
    return pyodbc.connect(conn_str)

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
    cursor.execute("SELECT descricao FROM tipos_documento")
    tipos = [row[0].lower() for row in cursor.fetchall()]
    conn.close()
    return tipos

def get_fornecedores():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT nome, nif FROM fornecedores")
    fornecedores = [{"nome": row[0], "nif": str(row[1])} for row in cursor.fetchall()]
    conn.close()
    return fornecedores

if __name__ == "__main__":
    test_connection()