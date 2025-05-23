# Sistema de Gestão de Calibração

Sistema para gestão de calibração e cálculos de certificado de calibração com erro de medição e incerteza, similar aos sistemas Metroex e Isoplan.

## Características

- Cadastro e gestão de instrumentos de medição
- Cadastro e gestão de padrões de calibração
- Registro e acompanhamento de calibrações
- Cálculos metrológicos de erro e incerteza conforme normas técnicas
- Geração de certificados de calibração
- Interface web responsiva e intuitiva

## Estrutura do Projeto

```
sistema_calibracao/
├── requirements.txt      # Dependências do projeto
├── Procfile             # Configuração para deploy no Railway
├── runtime.txt          # Versão do Python para o Railway
└── src/                 # Código-fonte do sistema
    ├── app.py           # Aplicação principal Flask
    ├── database/        # Scripts e arquivos de banco de dados
    │   ├── calibracao.db        # Banco de dados SQLite (local)
    │   └── schema_sqlite.sql    # Schema para SQLite
    ├── models/          # Modelos e lógica de negócio
    │   └── calculo_metrologico.py  # Implementação dos cálculos
    ├── static/          # Arquivos estáticos (CSS, JS, imagens)
    │   ├── css/
    │   ├── js/
    │   └── img/
    ├── templates/       # Templates HTML
    │   └── certificado_exemplo.html  # Modelo de certificado
    ├── tests/           # Testes e validações
    │   └── validacao_calculos.py     # Validação dos cálculos
    └── utils/           # Utilitários e ferramentas
        └── gerar_graficos.py         # Geração de gráficos
```

## Requisitos

- Python 3.11 ou superior
- Flask e dependências (ver requirements.txt)
- PostgreSQL (para produção) ou SQLite (para desenvolvimento)

## Instalação e Execução Local

1. Clone este repositório:
```bash
git clone https://github.com/seu-usuario/sistema-calibracao.git
cd sistema-calibracao
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Execute a aplicação:
```bash
cd src
python app.py
```

4. Acesse a aplicação em http://localhost:5000

## Deploy no Railway

1. Faça fork deste repositório para sua conta GitHub

2. No Railway:
   - Crie uma nova conta ou faça login em https://railway.app/
   - Clique em "New Project"
   - Selecione "Deploy from GitHub repo"
   - Conecte sua conta GitHub e selecione o repositório
   - Railway detectará automaticamente as configurações

3. Adicione um banco de dados PostgreSQL:
   - No projeto Railway, clique em "New"
   - Selecione "Database" e depois "PostgreSQL"
   - Railway conectará automaticamente o banco ao seu projeto

4. Verifique as variáveis de ambiente:
   - No projeto Railway, clique em "Variables"
   - Verifique se as variáveis de conexão com o banco estão presentes
   - Se necessário, adicione `PORT=5000`

5. Acesse sua aplicação através da URL fornecida pelo Railway

## Funcionalidades Implementadas

- Cálculos de erro de medição
- Cálculos de incerteza Tipo A (estatística)
- Cálculos de incerteza Tipo B (outras fontes)
- Cálculos de incerteza combinada e expandida
- Avaliação de conformidade
- Geração de certificados de calibração
- Visualização gráfica de erros e contribuições de incerteza

## Próximos Passos

- Implementar autenticação de usuários
- Adicionar relatórios e dashboards
- Implementar notificações de calibrações vencidas
- Adicionar suporte para calibrações em campo
- Integrar com outros sistemas (ERP, MES, etc.)

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo LICENSE para detalhes.

## Contato

Para suporte ou dúvidas, entre em contato através do GitHub.
