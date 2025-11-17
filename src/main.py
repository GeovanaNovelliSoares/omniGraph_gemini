import time
from db_manager import Neo4jService
from data_gen import DataGenerator
from ai_service import GeminiService


CYPHER_SETUP = [
    "CREATE CONSTRAINT IF NOT EXISTS FOR (u:User) REQUIRE u.id IS UNIQUE",
    "CREATE INDEX IF NOT EXISTS FOR (t:Transaction) ON (t.id)"
]

CYPHER_IMPORT_USERS = """
UNWIND $batch AS row
MERGE (u:User {id: row.id})
SET u.name = row.name, u.risk_score = row.risk_score
"""

CYPHER_IMPORT_TX = """
UNWIND $batch AS row
MATCH (u:User {id: row.user_id})
MERGE (d:Device {id: row.device_id})
CREATE (t:Transaction {id: row.tx_id, amount: row.amount, date: datetime()})
MERGE (u)-[:PERFORMED]->(t)
MERGE (t)-[:USED_DEVICE]->(d)
MERGE (t)-[:AT_MERCHANT]->(m:Merchant {name: row.merchant})
"""

CYPHER_FRAUD_DETECTION = """
MATCH (u1:User)-[:PERFORMED]->(:Transaction)-[:USED_DEVICE]->(d:Device)<-[:USED_DEVICE]-(:Transaction)<-[:PERFORMED]-(u2:User)
WHERE u1.id <> u2.id
RETURN d.id as SharedDevice, collect(distinct u1.name) as SuspiciousUsers, count(distinct u1) as UserCount
ORDER BY UserCount DESC LIMIT 1
"""

def main():
    print("🚀 Iniciando OmniGraph Senior...")
    db = Neo4jService()
    gen = DataGenerator()
    ai = GeminiService()

    try:
        print("⚙️  Configurando Banco de Dados...")
        for q in CYPHER_SETUP:
            db.run_query(q)

        users, transactions = gen.generate_synthetic_data(num_users=50, num_tx=1000)
        
        print(f"📥 Inserindo {len(users)} usuários...")
        db.run_batch(CYPHER_IMPORT_USERS, users)
        
        print(f"📥 Inserindo {len(transactions)} transações...")
        db.run_batch(CYPHER_IMPORT_TX, transactions)

        print("\n🕵️  Executando Algoritmo de Detecção de Fraude...")
        fraud_result = db.run_query(CYPHER_FRAUD_DETECTION)
        
        if fraud_result:
            top_case = fraud_result[0]
            device = top_case['SharedDevice']
            count = top_case['UserCount']
            names = top_case['SuspiciousUsers']
            
            print(f"   🚨 ALERTA CRÍTICO: Dispositivo {device} compartilhado por {count} usuários.")

            print("\n🤖 [Gemini AI] Gerando relatório de inteligência...")
            analise = ai.analyze_fraud_risk(device, names, count)
            
            print("\n" + "="*50)
            print(analise)
            print("="*50)
            
        else:
            print("✅ Nenhuma anomalia grave detectada nos dados atuais.")

    except Exception as e:
        print(f"❌ Erro Fatal: {e}")
    finally:
        db.close()
        print("\n🏁 Conexão encerrada.")

if __name__ == "__main__":
    main()