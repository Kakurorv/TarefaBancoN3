from neo4j import GraphDatabase
from py2neo import Node

def connect_to_neo4j():
    return GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "Paulo@123654"))


def add_person(name, age, location):
    person = Node("Person")
    person["name"] = name
    person["age"] = age
    person["location"] = location
    person.set("ID", uuid.uuid4())
    return person

def print_person(person):
    if "ID" in person:
        print(f"Pessoa adicionada - ID: {person['ID']}, Nome: {person['name']}")
    else:
        print(f"Pessoa adicionada - Nome: {person['name']}")

def create_relationship(id_a, id_b):
    session = connect_to_neo4j().session()
    session.run("MATCH (a:Person {id: $id_a}), (b:Person {id: $id_b}) CREATE (a)-[r:FRIENDS]->(b)", {"id_a": id_a, "id_b": id_b})
    session.close()

def list_people():
    session = connect_to_neo4j().session()
    results = session.run("MATCH (p:Person) RETURN p LIMIT $limit")
    people = results.result()
    session.close()

    for person in people:
        node = person["p"]
        properties = node._properties
        print(
            f"Element ID: {node._id}, Name: {properties.get('name')}, Age: {properties.get('age')}, Location: {properties.get('location')}"
        )


if __name__ == "__main__":
    list_people(limit=None)

def show_friendships():
    session = connect_to_neo4j().session()
    results = session.run("MATCH (a:Person)-[r:FRIENDS]->(b:Person) RETURN a, b, r")

    for result in results:
        print(
            f"{result['a']['name']} é amigo de {result['b']['name']} - {result['r']['id']}"
        )
    session.close()

def remove_person(id):
    session = connect_to_neo4j().session()
    session.run(f"MATCH (p:Person {id}) DETACH DELETE p")
    session.close()

people = []

while True:
    print("1. Adicionar pessoa")
    print("2. Criar relação de amizade")
    print("3. Listar pessoas")
    print("4. Mostrar rede de amizades")
    print("5. Remover pessoa")
    print("6. Sair")

    choice = input("Escolha uma opção: ")

    if choice == "1":
        name = input("Nome da pessoa: ")
        age = input("Idade da pessoa: ")
        location = input("Localização da pessoa: ")
        person = add_person(name, age, location)
        people.append(person)
        print(f"Pessoa adicionada - ID: {person['ID']}, Nome: {person['name']}")

    elif choice == "2":
        id_a = input("ID da primeira pessoa: ")
        id_b = input("ID da segunda pessoa: ")
        create_relationship(id_a, id_b)

    elif choice == "3":
        list_people()

    elif choice == "4":
        show_friendships()

    elif choice == "5":
        id = input("ID da pessoa a ser removida: ")
        remove_person(id)

    elif choice == "6":
        break

    else:
        print("Opção inválida.")
