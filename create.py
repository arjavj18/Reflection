import yaml
from py2neo import Graph
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
neo4j_password = os.getenv('NEO4J_PASSWORD')

# Load YAML data from file
with open('agents.yaml', 'r') as file:
    data = yaml.safe_load(file)

# Connect to the Neo4j database
graph = Graph("bolt://localhost:7687", auth=("neo4j", neo4j_password))

# Clear existing data (optional, be cautious with this)
graph.run("MATCH (n) DETACH DELETE n")

# Create nodes and relationships based on the YAML file
for node, properties in data.items():
    name = properties['Name']
    desc = properties['Desc']
    parents = properties['parent']

    # Create the node
    query = f"CREATE (n:{name} {{Name: '{name}', Desc: '{desc}'}})"
    graph.run(query)

    # Handle parent relationships
    if parents and parents != []:
        for parent in parents:
            # Create relationships with parent
            parent_query = f"MATCH (p:{parent}), (c:{name}) CREATE (p)-[:PARENT_OF]->(c)"
            graph.run(parent_query)
            child_query = f"MATCH (p:{parent}), (c:{name}) CREATE (c)-[:CHILD_OF]->(p)"
            graph.run(child_query)

print("Data imported successfully.")