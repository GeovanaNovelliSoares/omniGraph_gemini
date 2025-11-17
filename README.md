# 🛡️ OmniGraph: Sistema de Inteligência Conectada para Detecção de Fraude (Neo4j + Gemini AI)

## Visão Geral do Projeto

O **OmniGraph** implementa uma plataforma resiliente para **detecção de padrões invisíveis e geração de inteligência acionável** usando bancos de dados de grafos.

Este projeto aborda o desafio de transformar vastos conjuntos de dados de transações em um **Grafo de Conhecimento** (`Knowledge Graph`), aplicando algoritmos de fraude e utilizando **Inteligência Artificial Generativa (GraphRAG)** para criar relatórios executivos instantâneos.

---

## 🎯 Objetivos Principais

1.  **Dominar o Neo4j:** Modelar e consultar relações complexas usando Cypher com alta performance.
2.  **Escalabilidade (ETL):** Implementar ingestão de dados em lote (`Batching`) via Python para milhões de conexões.
3.  **Graph Data Science:** Aplicar lógica de grafos para descobrir anéis de fraude (conexões anômalas de dispositivos).
4.  **IA Generativa:** Conectar dados estruturados (Grafos) com o LLM **Gemini** para análise conversacional (GraphRAG), elevando a inteligência do sistema.

---

## 🏗️ Arquitetura e Stack Tecnológico

| Componente | Tecnologia | Responsabilidade Sênior |
| :--- | :--- | :--- |
| **Banco de Dados** | Neo4j 5.x (Docker) | Modelagem, Cypher otimizado, GDS Plugins. |
| **Backend Core** | Python 3.10+ | Lógica de Ingestão e Orquestração. |
| **Conectividade** | `neo4j-driver` | Implementação de **Lógica de Retry** para resiliência de conexão. |
| **Inteligência** | Gemini (via LangChain) | **GraphRAG** para análise de risco em linguagem natural. |
| **Configuração** | Docker Compose / `.env` | Infraestrutura como Código e Gerenciamento de Segredos. |

---

## ⚙️ Configuração e Instalação

Siga os passos para configurar o ambiente de forma replicável no seu Visual Studio Code.

### Pré-requisitos

1.  **Docker Desktop** (para rodar o Neo4j).
2.  **Python 3.9+**.
3.  **Chave de API do Google Gemini** (para o `ai_service.py`).

## Instale as dependências Python
Configure o .env para os dados do banco;

1. pip install -r requirements.txt

2. Suba o banco: docker-compose up -d.

3. Rode o app: python src/main.py.
