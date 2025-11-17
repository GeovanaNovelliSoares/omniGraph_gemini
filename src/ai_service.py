import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

class GeminiService:
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            print("⚠️ AVISO: GOOGLE_API_KEY não encontrada no .env. A IA não funcionará.")
            self.llm = None
        else:
            self.llm = ChatGoogleGenerativeAI(
                model="gemini-2.5-flash", 
                temperature=0.3,
                google_api_key=api_key
            )

    def analyze_fraud_risk(self, device_id, suspicious_users, user_count):
        if not self.llm:
            return "Erro: Chave de API do Google não configurada."

        template = """
        Você é um Analista Sênior de Fraude Financeira.
        Analise os dados abaixo extraídos de uma análise de grafos (Neo4j):
        
        - ID do Dispositivo Suspeito: {device_id}
        - Número de Contas usando este dispositivo: {user_count}
        - Nomes dos Usuários envolvidos: {suspicious_users}
        
        Contexto: O sistema detectou um padrão de "Device Sharing" anômalo.
        
        Tarefa:
        1. Gere um breve relatório explicando o risco de identidade sintética ou invasão de conta.
        2. Sugira 2 ações de mitigação técnica.
        3. Escreva um rascunho de e-mail para o gerente de segurança (assunto e corpo).
        
        Responda em Português do Brasil.
        """
        
        prompt = PromptTemplate(
            input_variables=["device_id", "suspicious_users", "user_count"],
            template=template
        )
        
        chain = prompt | self.llm
        
        try:
            response = chain.invoke({
                "device_id": device_id,
                "suspicious_users": ", ".join(suspicious_users),
                "user_count": user_count
            })
            return response.content
        except Exception as e:
            return f"Erro ao chamar Gemini: {str(e)}"