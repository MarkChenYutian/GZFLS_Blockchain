from ShelveManager import ShelveManager

agent = ShelveManager("./storage/Ledger.db")
for item in agent.getAll(): print(item)