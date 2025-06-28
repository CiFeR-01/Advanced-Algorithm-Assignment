from graph import Graph
from person import Person

person1 = Person("Alice Wonderland", "Female", "Loves adventures and tea parties.", False)
person2 = Person("Bob TheBuilder", "Male", "Can we fix it? Yes we can!", False)
person3 = Person("Charlie Chaplin", "Male", "Silent film actor and comedian.", True)
person4 = Person("Diana Prince", "Female", "Warrior princess and ambassador of peace.", False)
person5 = Person("Eve Harrington", "Female", "Aspiring actress with a mysterious past.", True)
person6 = Person("Frankenstein Monster", "Male", "Misunderstood creation seeking acceptance.", False)
person7 = Person("Grace Hopper", "Female", "Pioneering computer scientist and naval admiral.", False)

people_profiles = {
    person1.name: person1,
    person2.name: person2,
    person3.name: person3,
    person4.name: person4,
    person5.name: person5,
    person6.name: person6,
    person7.name: person7
}

social_media_graph = Graph()

for person_name in people_profiles:
    social_media_graph.addVertex(person_name)

social_media_graph.addEdge("Alice Wonderland", "Bob TheBuilder")
social_media_graph.addEdge("Alice Wonderland", "Charlie Chaplin")
social_media_graph.addEdge("Alice Wonderland", "Diana Prince")

social_media_graph.addEdge("Bob TheBuilder", "Alice Wonderland")
social_media_graph.addEdge("Bob TheBuilder", "Eve Harrington")

social_media_graph.addEdge("Charlie Chaplin", "Alice Wonderland")

social_media_graph.addEdge("Diana Prince", "Bob TheBuilder")
social_media_graph.addEdge("Diana Prince", "Frankenstein Monster")

social_media_graph.addEdge("Frankenstein Monster", "Grace Hopper")

social_media_graph.addEdge("Grace Hopper", "Alice Wonderland")


def display_menu():
    print("\n--- Social Media App Menu ---")
    print("Mandatory Features:")
    print("  a) Display all users' names")
    print("  b) View a person's profile in detail (Ignore privacy)")
    print("  c) View followed accounts of a person")
    print("  d) View followers of a person")
    print("Advanced Features:")
    print("  e) Add a new user profile")
    print("  f) View a person's profile (with privacy settings)")
    print("  g) Allow a user to follow another user")
    print("  h) Allow a user to unfollow another user")
    print("  x) Exit")
    print("-----------------------------")

def get_person_choice(prompt="Enter the name of the person:"):
    person_name = input(prompt).strip()
    if person_name in people_profiles:
        return person_name
    else:
        print(f"Error: User '{person_name}' not found.")
        return None

def view_followers(graph, target_vertex):
    followers = []
    for vertex, outgoing_edges in graph.vertices.items():
        if target_vertex in outgoing_edges:
            followers.append(vertex)

    if followers:
        print(f"\n--- Followers of {target_vertex} ---")
        for follower in followers:
            print(f"- {follower}")
        print("-----------------------------")
    else:
        print(f"\n{target_vertex} has no followers.")

def main():
    while True:
        display_menu()
        choice = input("Enter your choice: ").lower()

        if choice == 'a':
            print("\n--- All Users ---")
            if not people_profiles:
                print("No users in the system.")
            else:
                for name in people_profiles.keys():
                    print(f"- {name}")
            print("-----------------")

        elif choice == 'b':
            person_name = get_person_choice()
            if person_name:
                people_profiles[person_name].display_profile(ignore_privacy=True)

        elif choice == 'c':
            person_name = get_person_choice()
            if person_name:
                followed_accounts = social_media_graph.listOutgoingAdjacentVertex(person_name)
                if followed_accounts:
                    print(f"\n--- Accounts followed by {person_name} ---")
                    for account in followed_accounts:
                        print(f"- {account}")
                    print("---------------------------------------")
                else:
                    print(f"\n{person_name} is not following anyone.")

        elif choice == 'd':
            person_name = get_person_choice()
            if person_name:
                view_followers(social_media_graph, person_name)

        elif choice == 'e':
            print("\n--- Add New User Profile ---")
            name = input("Enter new user's name: ").strip()
            if not name:
                print("User name cannot be empty.")
                continue
            if name in people_profiles:
                print(f"A user with the name '{name}' already exists. Please choose a different name.")
                continue
            gender = input("Enter new user's gender: ").strip()
            biography = input("Enter new user's biography: ").strip()
            is_private_input = input("Is this profile private? (yes/no): ").strip().lower()
            is_private = True if is_private_input == 'yes' else False

            new_person = Person(name, gender, biography, is_private)
            people_profiles[name] = new_person
            social_media_graph.addVertex(name)
            print(f"User '{name}' added successfully!")

        elif choice == 'f':
            person_name = get_person_choice()
            if person_name:
                people_profiles[person_name].display_profile(ignore_privacy=False)

        elif choice == 'g':
            follower_name = get_person_choice("Enter the name of the user who wants to follow: ")
            if follower_name:
                followed_name = get_person_choice("Enter the name of the user to be followed: ")
                if followed_name:
                    if follower_name == followed_name:
                        print("A user cannot follow themselves.")
                    elif followed_name in social_media_graph.listOutgoingAdjacentVertex(follower_name):
                        print(f"{follower_name} is already following {followed_name}.")
                    else:
                        social_media_graph.addEdge(follower_name, followed_name)

        elif choice == 'h':
            unfollower_name = get_person_choice("Enter the name of the user who wants to unfollow: ")
            if unfollower_name:
                unfollowed_name = get_person_choice("Enter the name of the user to be unfollowed: ")
                if unfollowed_name:
                    if unfollowed_name not in social_media_graph.listOutgoingAdjacentVertex(unfollower_name):
                        print(f"{unfollower_name} is not following {unfollowed_name}.")
                    else:
                        social_media_graph.removeEdge(unfollower_name, unfollowed_name)

        elif choice == 'x':
            print("Exiting Social Media App. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()