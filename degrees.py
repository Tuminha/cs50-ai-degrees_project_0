import csv
import sys
from alive_progress import alive_bar
import time

from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target)

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")


def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """
    print("Starting the shortest path search...")

    # Initialize both BFS and DFS frontiers
    bfs_frontier = QueueFrontier()
    dfs_frontier = StackFrontier()
    
    start = Node(state=source, parent=None, action=None)
    bfs_frontier.add(start)
    dfs_frontier.add(start)
    
    # Keep track of explored nodes for both algorithms
    bfs_explored = set()
    dfs_explored = set()
    
    nodes_explored = 0
    start_time = time.time()

    while not bfs_frontier.empty() and not dfs_frontier.empty():
        # BFS step
        if not bfs_frontier.empty():
            bfs_node = bfs_frontier.remove()
            nodes_explored += 1
            
            if bfs_node.state == target:
                end_time = time.time()
                print(f"Path found using BFS. Nodes explored: {nodes_explored}")
                print(f"Time taken: {end_time - start_time:.2f} seconds")
                return reconstruct_path(bfs_node)
            
            bfs_explored.add(bfs_node.state)
            
            for movie_id, person_id in neighbors_for_person(bfs_node.state):
                if person_id not in bfs_explored and not bfs_frontier.contains_state(person_id):
                                       child = Node(state=person_id, parent=bfs_node, action=(movie_id, person_id))
                                       bfs_frontier.add(child)
        
        # DFS step
        if not dfs_frontier.empty():
            dfs_node = dfs_frontier.remove()
            nodes_explored += 1
            
            if dfs_node.state == target:
                end_time = time.time()
                print(f"Path found using DFS. Nodes explored: {nodes_explored}")
                print(f"Time taken: {end_time - start_time:.2f} seconds")
                return reconstruct_path(dfs_node)
            
            dfs_explored.add(dfs_node.state)
            
            for movie_id, person_id in neighbors_for_person(dfs_node.state):
                if person_id not in dfs_explored and not dfs_frontier.contains_state(person_id):
                    child = Node(state=person_id, parent=dfs_node, action=(movie_id, person_id))
                    dfs_frontier.add(child)
    
    # If we've exhausted both frontiers without finding a path
    end_time = time.time()
    print(f"No path found. Nodes explored: {nodes_explored}")
    print(f"Time taken: {end_time - start_time:.2f} seconds")
    return None

def reconstruct_path(node):
    path = []
    while node.parent is not None:
        path.append(node.action)
        node = node.parent
    path.reverse()
    return path


def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


if __name__ == "__main__":
    main()
