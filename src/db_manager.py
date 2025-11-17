import os
import time
from neo4j import GraphDatabase, exceptions
from dotenv import load_dotenv

load_dotenv()

class Neo4jService:
    def __init__(self):
        uri = os.getenv("NEO4J_URI")
        user = os.getenv("NEO4J_USERNAME")
        password = os.getenv("NEO4J_PASSWORD")
        
        if not uri or not user or not password:
            raise ValueError("Verifique o arquivo .env - Credenciais ausentes.")
            
        self.driver = None
        max_retries = 10
        for attempt in range(max_retries):
            try:
                self.driver = GraphDatabase.driver(uri, auth=(user, password))
                self.driver.verify_connectivity()
                print(f"✅ Conexão com Neo4j estabelecida com sucesso!")
                return 
            except (exceptions.ServiceUnavailable, exceptions.AuthError) as e:
                print(f"⏳ Tentativa {attempt+1}/{max_retries}: Banco ainda indisponível... aguardando 5s.")
                time.sleep(5)
                if attempt == max_retries - 1:
                    raise ConnectionError(f"❌ Não foi possível conectar ao Neo4j após {max_retries} tentativas. Verifique o Docker.") from e

    def close(self):
        if self.driver:
            self.driver.close()

    def run_query(self, query, parameters=None):
        with self.driver.session() as session:
            result = session.run(query, parameters)
            return [record.data() for record in result]

    def run_batch(self, query, data_list, batch_size=1000):
        total = len(data_list)
        with self.driver.session() as session:
            for i in range(0, total, batch_size):
                batch = data_list[i : i + batch_size]
                session.run(query, {"batch": batch})
                print(f"   Processado: {min(i + len(batch), total)} / {total}")