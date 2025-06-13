# Servidor MCP por Reynaldo Vieira

Este repositório contém uma implementação de um servidor de Protocolo de Contexto de Modelo (MCP) para fins educacionais e de demonstração, criado por Reynaldo Vieira. Este código demonstra como construir um servidor MCP funcional que pode se integrar a vários clientes LLM.


### Principais Benefícios

- Uma lista crescente de integrações pré-construídas que seu LLM pode conectar diretamente
- Flexibilidade para alternar entre provedores e fornecedores de LLM
- Melhores práticas para proteger seus dados em sua infraestrutura

## Visão Geral da Arquitetura

O MCP segue uma arquitetura cliente-servidor, onde uma aplicação hospedeira pode se conectar a vários servidores:

- **Hospedeiros MCP**: Programas como Claude Desktop, IDEs ou ferramentas de IA que desejam acessar dados através do MCP
- **Clientes MCP**: Clientes de protocolo que mantêm conexões 1:1 com os servidores
- **Servidores MCP**: Programas leves que expõem capacidades específicas através do Protocolo de Contexto de Modelo padronizado
- **Fontes de Dados**: Serviços locais (arquivos, bancos de dados) e remotos (APIs) que os servidores MCP podem acessar

## Conceitos Centrais do MCP

Os servidores MCP podem fornecer três tipos principais de capacidades:

- **Recursos**: Dados semelhantes a arquivos que podem ser lidos por clientes (como respostas de API ou conteúdo de arquivos)
- **Ferramentas**: Funções que podem ser chamadas pelo LLM (com a aprovação do usuário)
- **Prompts**: Modelos pré-escritos que ajudam os usuários a realizar tarefas específicas

## Requisitos do Sistema

- Python 3.10 ou superior
- MCP SDK 1.2.0 ou superior
- Gerenciador de pacotes `uv`

## Começando

### Instalando o gerenciador de pacotes uv

No MacOS/Linux:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Certifique-se de reiniciar seu terminal para garantir que o comando `uv` seja reconhecido.

### Configuração do Projeto

1. Crie e inicialize o projeto:
```bash
# Crie um novo diretório para o nosso projeto
uv init mcp-server
cd mcp-server

# Crie e ative o ambiente virtual
uv venv
source .venv/bin/activate  # No Windows, use: .venv\Scripts\activate

# Instale as dependências
uv add "mcp[cli]" httpx
```

2. Crie o arquivo de implementação do servidor:
```bash
touch main.py
```

### Executando o Servidor

1. Inicie o servidor MCP:
```bash
uv run main.py
```

2. O servidor será iniciado e estará pronto para aceitar conexões.

## Conectando ao Claude Desktop

1. Instale o Claude Desktop a partir do site oficial.
2. Configure o Claude Desktop para usar seu servidor MCP:

Edite `~/Library/Application Support/Claude/claude_desktop_config.json`:
```json
{
    "mcpServers": {
        "mcp-server-reynaldo": {
            "command": "uv",  # É melhor usar o caminho absoluto para o comando uv
            "args": [
                "--directory",
                "/CAMINHO/ABSOLUTO/PARA/SEU/mcp-server",
                "run",
                "main.py"
            ]
        }
    }
}
```

3. Reinicie o Claude Desktop.

## Solução de Problemas

Se o seu servidor não estiver sendo reconhecido pelo Claude Desktop:

1. Verifique o caminho e as permissões do arquivo de configuração.
2. Verifique se o caminho absoluto na configuração está correto.
3. Certifique-se de que o `uv` está instalado corretamente e acessível.
4. Verifique os logs do Claude Desktop para mensagens de erro.

## Licença

Este projeto está licenciado sob a Licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
