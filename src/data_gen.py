from faker import Faker
import random

fake = Faker()

class DataGenerator:
    def generate_synthetic_data(self, num_users=100, num_tx=500):
        print("🏗️  Gerando dados sintéticos...")
        
        users = [{"id": f"u_{i}", "name": fake.name(), "risk_score": 0.0} for i in range(num_users)]
        
        devices = [{"id": f"dev_{random.randint(0, 20)}", "model": "Smartphone"} for _ in range(num_users)]
        
        transactions = []
        for _ in range(num_tx):
            u_id = f"u_{random.randint(0, num_users-1)}"
            tx_data = {
                "user_id": u_id,
                "tx_id": fake.uuid4(),
                "amount": round(random.uniform(10.0, 5000.0), 2),
                "device_id": f"dev_{random.randint(0, 20)}",
                "merchant": random.choice(["Amazon", "Walmart", "Netflix", "Uber", "MercadoLivre"])
            }
            transactions.append(tx_data)
            
        return users, transactions