CREATE DATABASE document_reader;
GO
USE document_reader;
GO

CREATE TABLE fornecedores (
    id INT IDENTITY(1,1) PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    nif VARCHAR(20) NOT NULL UNIQUE -- Para permitir referência externa
);

CREATE TABLE equipas (
    id INT IDENTITY(1,1) PRIMARY KEY,
    nome VARCHAR(255) NOT NULL
);

CREATE TABLE clientes (
    id INT IDENTITY(1,1) PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    nif VARCHAR(20) NOT NULL UNIQUE
);

CREATE TABLE processos (
    ref VARCHAR(12) NOT NULL PRIMARY KEY,
    id_cliente INT NOT NULL,
    descricao VARCHAR(60),
    FOREIGN KEY (id_cliente) REFERENCES clientes(id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE tipos_documento (
    id INT IDENTITY(1,1) PRIMARY KEY,
    nome VARCHAR(56),
    abrev VARCHAR(5),
    arquivamento VARCHAR(20) CHECK (arquivamento IN ('fornecedor', 'equipa', 'processo')) NOT NULL
);

CREATE TABLE documentos (
    id INT IDENTITY(1,1) PRIMARY KEY,
    id_tipo_doc INT NOT NULL,
    numero VARCHAR(20),
    data DATETIME,
    ano CHAR(4),
    total DECIMAL(10,3),
    ficheiro_pdf VARBINARY(MAX),

    -- Ligações possíveis
    nif_fornecedor VARCHAR(20) NULL,
    id_equipa INT NULL,
    id_processo VARCHAR(12) NULL,

    FOREIGN KEY (id_tipo_doc) REFERENCES tipos_documento(id),
    FOREIGN KEY (nif_fornecedor) REFERENCES fornecedores(nif),
    FOREIGN KEY (id_equipa) REFERENCES equipas(id),
    FOREIGN KEY (id_processo) REFERENCES processos(ref)
);
