import csv
import sys

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
    # Check for correct number of command-line arguments
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    # Get the source actor's ID
    source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found.")
    
    # Get the target actor's ID
    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")

    # Find the shortest path between the source and target actors
    path = shortest_path(source, target)

    # Print the result
    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        for i in range(degrees):
            person1 = people[source]["name"]
            person2 = people[path[i][1]]["name"]
            movie = movies[path[i][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")


def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """
    # Initialize the frontier to just the starting position
    start = Node(state=source, parent=None, action=None)
    frontier = QueueFrontier()
    frontier.add(start)

    # Initialize an empty explored set
    explored = set()

    # Keep looping until solution found
    while not frontier.empty():
        # Choose a node from the frontier
        node = frontier.remove()

        # If node is the goal, then we have a solution
        if node.state == target:
            path = []
            while node.parent is not None:
                path.append(node.action)
                node = node.parent
            path.reverse()
            return path

        # Mark node as explored
        explored.add(node.state)

        # Add neighbors to frontier
        for movie_id, person_id in neighbors_for_person(node.state):
            if not frontier.contains_state(person_id) and person_id not in explored:
                child = Node(state=person_id, parent=node, action=(movie_id, person_id))
                frontier.add(child)
    
    # If we exhaust the frontier, then no path was found
    return None


def reconstruct_path(node):
    """
    Reconstructs the path from the source to the target node.
    """
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
