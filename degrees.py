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


from alive_progress import alive_bar
import time

def shortest_path(source, target):
    print("Starting the shortest path search...")

    bfs_frontier = QueueFrontier()
    dfs_frontier = StackFrontier()
    
    start = Node(state=source, parent=None, action=None)
    bfs_frontier.add(start)
    dfs_frontier.add(start)
    
    bfs_explored = set()
    dfs_explored = set()
    
    bfs_nodes_explored = 0
    dfs_nodes_explored = 0
    bfs_path = None
    dfs_path = None

    start_time = time.time()

    with alive_bar(title="Searching for path", unknown="waves2", spinner="dots_waves2") as bar:
        while (not bfs_frontier.empty() or not dfs_frontier.empty()) and (bfs_path is None and dfs_path is None):
            # BFS step
            if not bfs_frontier.empty():
                bfs_node = bfs_frontier.remove()
                bfs_nodes_explored += 1
                
                if bfs_node.state == target:
                    bfs_path = reconstruct_path(bfs_node)
                    break
                
                bfs_explored.add(bfs_node.state)
                
                for movie_id, person_id in neighbors_for_person(bfs_node.state):
                    if person_id not in bfs_explored and not bfs_frontier.contains_state(person_id):
                        child = Node(state=person_id, parent=bfs_node, action=(movie_id, person_id))
                        bfs_frontier.add(child)
            
            # DFS step
            if not dfs_frontier.empty():
                dfs_node = dfs_frontier.remove()
                dfs_nodes_explored += 1
                
                if dfs_node.state == target:
                    dfs_path = reconstruct_path(dfs_node)
                    break
                
                dfs_explored.add(dfs_node.state)
                
                for movie_id, person_id in neighbors_for_person(dfs_node.state):
                    if person_id not in dfs_explored and not dfs_frontier.contains_state(person_id):
                        child = Node(state=person_id, parent=dfs_node, action=(movie_id, person_id))
                        dfs_frontier.add(child)
            
            bar.text = f'BFS: {bfs_nodes_explored} nodes, DFS: {dfs_nodes_explored} nodes'
            bar()

    end_time = time.time()
    time_taken = end_time - start_time

    if bfs_path:
        print(f"\nPath found using BFS. Nodes explored by BFS: {bfs_nodes_explored}")
        print(f"Time taken: {time_taken:.2f} seconds")
        print(f"\nDFS progress:")
        print(f"DFS had explored {dfs_nodes_explored} nodes when BFS found the solution, but hadn't found the path yet.")
        return bfs_path
    elif dfs_path:
        print(f"\nPath found using DFS. Nodes explored by DFS: {dfs_nodes_explored}")
        print(f"Time taken: {time_taken:.2f} seconds")
        print(f"\nBFS progress:")
        print(f"BFS had explored {bfs_nodes_explored} nodes when DFS found the solution, but hadn't found the path yet.")
        return dfs_path
    else:
        print(f"\nNo path found. BFS nodes explored: {bfs_nodes_explored}, DFS nodes explored: {dfs_nodes_explored}")
        print(f"Time taken: {time_taken:.2f} seconds")
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
    resolving ambiguities automatically when possible.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Multiple persons found with name '{name}':")
        candidates = []
        for person_id in person_ids:
            person = people[person_id]
            print(f"ID: {person_id}, Name: {person['name']}, Birth: {person['birth']}")
            candidates.append((person_id, person['name'], person['birth']))
        
        # Automatically choose the person with the most information (i.e., birth year)
        chosen = max(candidates, key=lambda x: len(x[2]))
        print(f"\nAutomatically chosen: ID: {chosen[0]}, Name: {chosen[1]}, Birth: {chosen[2]}")
        return chosen[0]
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
