from neo4j_cypher.chain import chain

if __name__ == "__main__":
    original_query = "Beschluss zu Stadtentwässerung"
    print(chain.invoke({"question": original_query}))
