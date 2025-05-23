-- Schema para o Sistema de Gestão de Calibração (SQLite)

-- Tabela de Usuários
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    senha TEXT NOT NULL,
    cargo TEXT,
    departamento TEXT,
    nivel_acesso INTEGER NOT NULL DEFAULT 1,
    ativo INTEGER NOT NULL DEFAULT 1,
    data_criacao TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP
);

-- Tabela de Setores/Departamentos
CREATE TABLE IF NOT EXISTS setores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    descricao TEXT,
    responsavel TEXT,
    ativo INTEGER NOT NULL DEFAULT 1,
    data_criacao TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP
);

-- Tabela de Tipos de Instrumentos
CREATE TABLE IF NOT EXISTS tipos_instrumentos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    descricao TEXT,
    unidade_padrao TEXT,
    ativo INTEGER NOT NULL DEFAULT 1,
    data_criacao TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP
);

-- Tabela de Fabricantes
CREATE TABLE IF NOT EXISTS fabricantes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    contato TEXT,
    telefone TEXT,
    email TEXT,
    website TEXT,
    ativo INTEGER NOT NULL DEFAULT 1,
    data_criacao TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP
);

-- Tabela de Instrumentos
CREATE TABLE IF NOT EXISTS instrumentos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo TEXT UNIQUE NOT NULL,
    descricao TEXT NOT NULL,
    tipo_id INTEGER,
    fabricante TEXT,
    modelo TEXT,
    numero_serie TEXT,
    resolucao REAL,
    faixa_minima REAL,
    faixa_maxima REAL,
    unidade TEXT,
    localizacao TEXT,
    setor_id INTEGER,
    status TEXT NOT NULL DEFAULT 'ativo',
    criticidade TEXT,
    periodicidade_calibracao INTEGER,
    data_ultima_calibracao DATE,
    data_proxima_calibracao DATE,
    observacoes TEXT,
    ativo INTEGER NOT NULL DEFAULT 1,
    data_criacao TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP,
    FOREIGN KEY (tipo_id) REFERENCES tipos_instrumentos(id),
    FOREIGN KEY (setor_id) REFERENCES setores(id)
);

-- Tabela de Padrões
CREATE TABLE IF NOT EXISTS padroes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo TEXT UNIQUE NOT NULL,
    descricao TEXT NOT NULL,
    tipo_id INTEGER,
    fabricante TEXT,
    modelo TEXT,
    numero_serie TEXT,
    resolucao REAL,
    faixa_minima REAL,
    faixa_maxima REAL,
    unidade TEXT,
    incerteza_padrao REAL,
    fator_k REAL,
    certificado_numero TEXT,
    certificado_validade DATE,
    rastreabilidade TEXT,
    status TEXT NOT NULL DEFAULT 'ativo',
    observacoes TEXT,
    ativo INTEGER NOT NULL DEFAULT 1,
    data_criacao TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP,
    FOREIGN KEY (tipo_id) REFERENCES tipos_instrumentos(id)
);

-- Tabela de Procedimentos de Calibração
CREATE TABLE IF NOT EXISTS procedimentos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo TEXT UNIQUE NOT NULL,
    nome TEXT NOT NULL,
    descricao TEXT,
    versao TEXT,
    data_aprovacao DATE,
    aprovado_por TEXT,
    tipo_instrumento_id INTEGER,
    pontos_calibracao TEXT,
    condicoes_ambientais TEXT,
    equipamentos_necessarios TEXT,
    instrucoes TEXT,
    criterios_aceitacao TEXT,
    ativo INTEGER NOT NULL DEFAULT 1,
    data_criacao TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP,
    FOREIGN KEY (tipo_instrumento_id) REFERENCES tipos_instrumentos(id)
);

-- Tabela de Calibrações
CREATE TABLE IF NOT EXISTS calibracoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    numero TEXT UNIQUE NOT NULL,
    instrumento_id INTEGER,
    procedimento_id INTEGER,
    responsavel TEXT,
    data_inicio TIMESTAMP NOT NULL,
    data_fim TIMESTAMP,
    temperatura REAL,
    umidade REAL,
    pressao REAL,
    status TEXT NOT NULL DEFAULT 'em_andamento',
    resultado TEXT,
    observacoes TEXT,
    data_criacao TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP,
    FOREIGN KEY (instrumento_id) REFERENCES instrumentos(id),
    FOREIGN KEY (procedimento_id) REFERENCES procedimentos(id)
);

-- Tabela de Padrões utilizados na Calibração
CREATE TABLE IF NOT EXISTS calibracao_padroes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    calibracao_id INTEGER,
    padrao_id INTEGER,
    data_criacao TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (calibracao_id) REFERENCES calibracoes(id),
    FOREIGN KEY (padrao_id) REFERENCES padroes(id)
);

-- Tabela de Pontos de Calibração
CREATE TABLE IF NOT EXISTS pontos_calibracao (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    calibracao_id INTEGER,
    sequencia INTEGER NOT NULL,
    valor_referencia REAL NOT NULL,
    valor_lido REAL NOT NULL,
    erro REAL,
    incerteza_padrao REAL,
    incerteza_expandida REAL,
    fator_k REAL,
    conforme INTEGER,
    observacoes TEXT,
    data_criacao TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP,
    FOREIGN KEY (calibracao_id) REFERENCES calibracoes(id)
);

-- Tabela de Fontes de Incerteza
CREATE TABLE IF NOT EXISTS fontes_incerteza (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ponto_calibracao_id INTEGER,
    descricao TEXT NOT NULL,
    tipo TEXT NOT NULL,
    distribuicao TEXT,
    valor REAL NOT NULL,
    divisor REAL,
    graus_liberdade INTEGER,
    coeficiente_sensibilidade REAL,
    contribuicao REAL,
    data_criacao TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP,
    FOREIGN KEY (ponto_calibracao_id) REFERENCES pontos_calibracao(id)
);

-- Tabela de Certificados
CREATE TABLE IF NOT EXISTS certificados (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    numero TEXT UNIQUE NOT NULL,
    calibracao_id INTEGER,
    data_emissao TIMESTAMP NOT NULL,
    emitido_por TEXT,
    aprovado_por TEXT,
    status TEXT NOT NULL DEFAULT 'emitido',
    observacoes TEXT,
    caminho_arquivo TEXT,
    data_criacao TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP,
    FOREIGN KEY (calibracao_id) REFERENCES calibracoes(id)
);

-- Tabela de Histórico de Instrumentos
CREATE TABLE IF NOT EXISTS historico_instrumentos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    instrumento_id INTEGER,
    tipo_evento TEXT NOT NULL,
    data_evento TIMESTAMP NOT NULL,
    descricao TEXT,
    usuario TEXT,
    referencia_id INTEGER,
    data_criacao TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (instrumento_id) REFERENCES instrumentos(id)
);

-- Tabela de Configurações do Sistema
CREATE TABLE IF NOT EXISTS configuracoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chave TEXT UNIQUE NOT NULL,
    valor TEXT,
    descricao TEXT,
    data_atualizacao TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Inserir configurações iniciais
INSERT INTO configuracoes (chave, valor, descricao) VALUES
('nome_empresa', 'Empresa de Calibração', 'Nome da empresa'),
('logo_empresa', 'logo.png', 'Caminho para o logo da empresa'),
('endereco_empresa', 'Rua Exemplo, 123', 'Endereço da empresa'),
('telefone_empresa', '(11) 1234-5678', 'Telefone da empresa'),
('email_empresa', 'contato@empresa.com', 'Email de contato da empresa'),
('nivel_confianca_padrao', '95', 'Nível de confiança padrão para cálculos de incerteza (%)'),
('formato_certificado', 'padrao', 'Formato padrão para certificados');

-- Inserir tipos de instrumentos comuns
INSERT INTO tipos_instrumentos (nome, descricao, unidade_padrao) VALUES
('Paquímetro', 'Instrumento de medição de comprimento', 'mm'),
('Micrômetro', 'Instrumento de medição de precisão para dimensões externas', 'mm'),
('Termômetro', 'Instrumento de medição de temperatura', '°C'),
('Manômetro', 'Instrumento de medição de pressão', 'bar'),
('Balança', 'Instrumento de medição de massa', 'g'),
('Multímetro', 'Instrumento de medição de grandezas elétricas', 'V');
