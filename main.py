from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import httpx
import json
import os
from bs4 import BeautifulSoup
load_dotenv()

reynaldo_mcp_server = FastMCP("reynaldo-docs")

USER_AGENT_REYNALDO = "reynaldo-docs-app/1.0"
SERPER_URL="https://google.serper.dev/search"

urls_documentacao_reynaldo = {
    "langchain": "python.langchain.com/docs",
    "llama-index": "docs.llamaindex.ai/en/stable",
    "openai": "platform.openai.com/docs",
}

async def buscar_na_web_reynaldo(query: str) -> dict | None:
    payload = json.dumps({"q": query, "num": 2})

    headers = {
        "X-API-KEY": os.getenv("SERPER_API_KEY"),
        "Content-Type": "application/json",
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                SERPER_URL, headers=headers, data=payload, timeout=30.0
            )
            response.raise_for_status()
            return response.json()
        except httpx.TimeoutException:
            return {"organic": []}
  
async def obter_conteudo_url_reynaldo(url: str):
  async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=30.0)
            soup = BeautifulSoup(response.text, "html.parser")
            text = soup.get_text()
            return text
        except httpx.TimeoutException:
            return "Timeout error"

@reynaldo_mcp_server.tool()  
async def obter_documentacao_reynaldo(query: str, library: str):
  """
  Busca a documentação mais recente para uma determinada consulta e biblioteca.
  Suporta langchain, openai e llama-index.

  Args:
    query: A consulta a ser pesquisada (por exemplo, "Chroma DB")
    library: A biblioteca para pesquisar (por exemplo, "langchain")

  Returns:
    Texto da documentação
  """
  if library not in urls_documentacao_reynaldo:
    raise ValueError(f"Biblioteca {library} não suportada por esta ferramenta")
  
  query = f"site:{urls_documentacao_reynaldo[library]} {query}"
  results = await buscar_na_web_reynaldo(query)
  if len(results["organic"]) == 0:
    return "Nenhum resultado encontrado"
  
  text = ""
  for result in results["organic"]:
    text += await obter_conteudo_url_reynaldo(result["link"])
  return text


if __name__ == "__main__":
    reynaldo_mcp_server.run(transport="stdio")
