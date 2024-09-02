from neo4j_advanced_rag.chain import chain
import sys


def main():
    while True:
        user_input = input("Enter your question (or 'exit' to quit): ")
        if user_input.lower() == "exit":
            sys.exit(0)

        response = chain.invoke(
            {"question": user_input},
            {"configurable": {"strategy": "parent_strategy"}},
        )
        print("\nAnswer:")
        print(response)
        print("\n" + "-" * 50 + "\n")


if __name__ == "__main__":
    print("Welcome to the Dune Q&A CLI!")
    print("You can ask questions about Dune, and I'll try to answer them.")
    print("Type 'exit' to quit the program.\n")
    main()
