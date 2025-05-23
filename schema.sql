-- Schema para o Sistema de Gestão de Calibração

-- Tabela de Usuários
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL,
    cargo VARCHAR(50),
    departamento VARCHAR(50),
    nivel_acesso INTEGER NOT NULL DEFAULT 1,
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    data_criacao TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP
);

-- Tabela de Setores/Departamentos
CREATE TABLE setores (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT,
    responsavel VARCHAR(100),
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    data_criacao TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP
);

-- Tabela de Tipos de Instrumentos
CREATE TABLE tipos_instrumentos (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT,
    unidade_padrao VARCHAR(20),
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    data_criacao TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP
);

-- Tabela de Fabricantes
CREATE TABLE fabricantes (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    contato VARCHAR(100),
    telefone VARCHAR(20),
    email VARCHAR(100),
    website VARCHAR(255),
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    data_criacao TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP
);

-- Tabela de Instrumentos
CREATE TABLE instrumentos (
    id SERIAL PRIMARY KEY,
    codigo VARCHAR(50) UNIQUE NOT NULL,
    descricao VARCHAR(255) NOT NULL,
    tipo_id INTEGER REFERENCES tipos_instrumentos(id),
    fabricante_id INTEGER REFERENCES fabricantes(id),
    modelo VARCHAR(100),
    numero_serie VARCHAR(100),
    resolucao DECIMAL(20, 10),
    faixa_minima DECIMAL(20, 10),
    faixa_maxima DECIMAL(20, 10),
    unidade VARCHAR(20),
    localizacao VARCHAR(100),
    setor_id INTEGER REFERENCES setores(id),
    status VARCHAR(20) NOT NULL DEFAULT 'ativo', -- ativo, inativo, em_calibracao, em_manutencao
    criticidade VARCHAR(20), -- baixa, media, alta
    periodicidade_calibracao INTEGER, -- em dias
    data_ultima_calibracao DATE,
    data_proxima_calibracao DATE,
    observacoes TEXT,
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    data_criacao TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP
);

-- Tabela de Padrões
CREATE TABLE padroes (
    id SERIAL PRIMARY KEY,
    codigo VARCHAR(50) UNIQUE NOT NULL,
    descricao VARCHAR(255) NOT NULL,
    tipo_id INTEGER REFERENCES tipos_instrumentos(id),
    fabricante_id INTEGER REFERENCES fabricantes(id),
    modelo VARCHAR(100),
    numero_serie VARCHAR(100),
    resolucao DECIMAL(20, 10),
    faixa_minima DECIMAL(20, 10),
    faixa_maxima DECIMAL(20, 10),
    unidade VARCHAR(20),
    incerteza_padrao DECIMAL(20, 10),
    fator_k DECIMAL(5, 2),
    certificado_numero VARCHAR(100),
    certificado_validade DATE,
    rastreabilidade TEXT,
    status VARCHAR(20) NOT NULL DEFAULT 'ativo', -- ativo, inativo, em_calibracao, vencido
    observacoes TEXT,
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    data_criacao TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP
);

-- Tabela de Procedimentos de Calibração
CREATE TABLE procedimentos (
    id SERIAL PRIMARY KEY,
    codigo VARCHAR(50) UNIQUE NOT NULL,
    nome VARCHAR(255) NOT NULL,
    descricao TEXT,
    versao VARCHAR(20),
    data_aprovacao DATE,
    aprovado_por VARCHAR(100),
    tipo_instrumento_id INTEGER REFERENCES tipos_instrumentos(id),
    pontos_calibracao TEXT, -- Pode ser JSON ou texto formatado com pontos de calibração padrão
    condicoes_ambientais TEXT,
    equipamentos_necessarios TEXT,
    instrucoes TEXT,
    criterios_aceitacao TEXT,
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    data_criacao TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP
);

-- Tabela de Calibrações
CREATE TABLE calibracoes (
    id SERIAL PRIMARY KEY,
    numero VARCHAR(50) UNIQUE NOT NULL,
    instrumento_id INTEGER REFERENCES instrumentos(id),
    procedimento_id INTEGER REFERENCES procedimentos(id),
    responsavel_id INTEGER REFERENCES usuarios(id),
    data_inicio TIMESTAMP NOT NULL,
    data_fim TIMESTAMP,
    temperatura DECIMAL(5, 2),
    umidade DECIMAL(5, 2),
    pressao DECIMAL(8, 2),
    status VARCHAR(20) NOT NULL DEFAULT 'em_andamento', -- em_andamento, concluida, aprovada, reprovada, cancelada
    resultado VARCHAR(20), -- conforme, nao_conforme
    observacoes TEXT,
    data_criacao TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP
);

-- Tabela de Padrões utilizados na Calibração
CREATE TABLE calibracao_padroes (
    id SERIAL PRIMARY KEY,
    calibracao_id INTEGER REFERENCES calibracoes(id),
    padrao_id INTEGER REFERENCES padroes(id),
    data_criacao TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Pontos de Calibração
CREATE TABLE pontos_calibracao (
    id SERIAL PRIMARY KEY,
    calibracao_id INTEGER REFERENCES calibracoes(id),
    sequencia INTEGER NOT NULL,
    valor_referencia DECIMAL(20, 10) NOT NULL,
    valor_lido DECIMAL(20, 10) NOT NULL,
    erro DECIMAL(20, 10),
    incerteza_padrao DECIMAL(20, 10),
    incerteza_expandida DECIMAL(20, 10),
    fator_k DECIMAL(5, 2),
    conforme BOOLEAN,
    observacoes TEXT,
    data_criacao TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP
);

-- Tabela de Fontes de Incerteza
CREATE TABLE fontes_incerteza (
    id SERIAL PRIMARY KEY,
    ponto_calibracao_id INTEGER REFERENCES pontos_calibracao(id),
    descricao VARCHAR(255) NOT NULL,
    tipo VARCHAR(10) NOT NULL, -- tipo_a, tipo_b
    distribuicao VARCHAR(20), -- normal, retangular, triangular
    valor DECIMAL(20, 10) NOT NULL,
    divisor DECIMAL(10, 5),
    graus_liberdade INTEGER,
    coeficiente_sensibilidade DECIMAL(10, 5),
    contribuicao DECIMAL(20, 10),
    data_criacao TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP
);

-- Tabela de Certificados
CREATE TABLE certificados (
    id SERIAL PRIMARY KEY,
    numero VARCHAR(50) UNIQUE NOT NULL,
    calibracao_id INTEGER REFERENCES calibracoes(id),
    data_emissao TIMESTAMP NOT NULL,
    emitido_por INTEGER REFERENCES usuarios(id),
    aprovado_por INTEGER REFERENCES usuarios(id),
    status VARCHAR(20) NOT NULL DEFAULT 'emitido', -- emitido, aprovado, cancelado
    observacoes TEXT,
    caminho_arquivo VARCHAR(255),
    data_criacao TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP
);

-- Tabela de Histórico de Instrumentos
CREATE TABLE historico_instrumentos (
    id SERIAL PRIMARY KEY,
    instrumento_id INTEGER REFERENCES instrumentos(id),
    tipo_evento VARCHAR(50) NOT NULL, -- calibracao, manutencao, verificacao, ajuste
    data_evento TIMESTAMP NOT NULL,
    descricao TEXT,
    usuario_id INTEGER REFERENCES usuarios(id),
    referencia_id INTEGER, -- ID da calibração, manutenção, etc.
    data_criacao TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Configurações do Sistema
CREATE TABLE configuracoes (
    id SERIAL PRIMARY KEY,
    chave VARCHAR(50) UNIQUE NOT NULL,
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
