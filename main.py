import random
import datetime
from graph import Graph
from person import Person

# Initializing Person objects and the social media graph
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

# Establishing initial connections
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
    """Displays the main menu options for the social media application with improved aesthetics."""
    print("\n**********************************************")
    print("      --- Social Media App Menu ---")
    print("**********************************************")
    print("Mandatory Features:")
    print("  1) Display all users' names")
    print("  2) View a person's profile in detail (Ignore privacy)")
    print("  3) View followed accounts of a person")
    print("  4) View followers of a person")
    print("\nAdvanced Features:")
    print("  5) Add a new user profile")
    print("  6) View a person's profile (with privacy settings)")
    print("  7) Allow a user to follow another user")
    print("  8) Allow a user to unfollow another user")
    print("\n  x) Exit")
    print("==============================================")

def get_person_choice(prompt="Select a person:"):
    """
    Displays a numbered list of all available users and prompts the user
    to select a person by number. Returns the selected person's name or None.
    Enhanced for better visual appeal.
    """
    
    print(f"==============================================")
    print(f"      --- {prompt} ---")
    print(f"==============================================")
    user_names = list(people_profiles.keys())
    
    if not user_names:
        print("No users available to select.")
        return None

    for i, name in enumerate(user_names):
        print(f"{i+1}.) {name}")
    print("----------------------------------------------")
    
    while True:
        try:
            choice_num_str = input(f"Select whose profile to view (1 - {len(user_names)}): ").strip()
            if not choice_num_str.isdigit():
                print("Invalid input. Please enter a number.")
                continue

            choice_num = int(choice_num_str)
            if 1 <= choice_num <= len(user_names):
                return user_names[choice_num - 1]
            else:
                print(f"Invalid number. Please enter a number between 1 and {len(user_names)}.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None


def view_followers(graph, target_vertex):
    """
    Finds and displays all users who follow the target_vertex with improved aesthetics.
    """
    followers = []
    # Iterate through all vertices to find who has an outgoing edge to target_vertex
    for vertex, outgoing_edges in graph.vertices.items():
        if target_vertex in outgoing_edges:
            followers.append(vertex)

    print(f"\n==============================================")
    print(f"      --- Followers of {target_vertex} ---")
    print(f"==============================================")
    if followers:
        for follower in followers:
            print(f"- {follower}")
    else:
        print(f"    {target_vertex} has no followers.")
    print("----------------------------------------------")

def press_any_key_to_continue():
    """Pauses execution and waits for user input before continuing."""
    input("\n< < < Press Enter to return to the main menu... > > >")

def main():
    """Main function to run the social media application with improved aesthetics."""
    while True:
        display_menu()
        choice = input("Enter your choice: ").lower()

        if choice == '1':
            print(f"\n==============================================")
            print("         --- All Users ---")
            print(f"==============================================")
            if not people_profiles:
                print("No users in the system.")
            else:
                for name, person_obj in people_profiles.items():
                    privacy_status = "Private" if person_obj.is_private else "Public"
                    print(f"- {name} ({privacy_status})")
            print("-------------------------------------")
            press_any_key_to_continue()

        elif choice == '2':
            person_name = get_person_choice("View Details for Any Profile:")
            if person_name:
                # Assuming display_profile method in Person class also has improved formatting
                people_profiles[person_name].display_profile(ignore_privacy=True)
            press_any_key_to_continue()

        elif choice == '3':
            person_name = get_person_choice("View Followed Accounts:")
            if person_name:
                followed_accounts = social_media_graph.listOutgoingAdjacentVertex(person_name)
                print(f"\n==============================================")
                print(f"    --- Accounts followed by {person_name} ---")
                print(f"==============================================")
                if followed_accounts:
                    for account in followed_accounts:
                        print(f"- {account}")
                else:
                    print(f"    {person_name} is not following anyone.")
                print("---------------------------------------")
            press_any_key_to_continue()

        elif choice == '4':
            person_name = get_person_choice("View Followers:")
            if person_name:
                view_followers(social_media_graph, person_name)
            press_any_key_to_continue()

        elif choice == '5':
            print(f"\n==============================================")
            print("     --- Add New User Profile ---")
            print(f"==============================================")
            name = input("Enter new user's name: ").strip()
            if not name:
                print("User name cannot be empty.")
                press_any_key_to_continue()
                continue
            if name in people_profiles:
                print(f"A user with the name '{name}' already exists. Please choose a different name.")
                press_any_key_to_continue()
                continue
            gender = input("Enter new user's gender: ").strip()
            biography = input("Enter new user's biography: ").strip()
            is_private_input = input("Is this profile private? (yes/no): ").strip().lower()
            is_private = True if is_private_input == 'yes' else False

            new_person = Person(name, gender, biography, is_private)
            people_profiles[name] = new_person
            social_media_graph.addVertex(name) # This will print "Vertex added" from graph.py
            print(f"User '{name}' added successfully!")
            print("-------------------------------------")
            press_any_key_to_continue()

        elif choice == '6':
            person_name = get_person_choice("View Profile with Privacy Settings:")
            if person_name:
                people_profiles[person_name].display_profile(ignore_privacy=False)
            press_any_key_to_continue()

        elif choice == '7':
            follower_name = get_person_choice("Select the user who wants to follow:")
            if follower_name:
                followed_name = get_person_choice("Select the user to be followed:")
                if followed_name:
                    if follower_name == followed_name:
                        print("\n! ! ! A user cannot follow themselves. ! ! !")
                    else:
                        social_media_graph.addEdge(follower_name, followed_name) # This will print "Edge added" or "already following"
            press_any_key_to_continue()

        elif choice == '8':
            unfollower_name = get_person_choice("Select the user who wants to unfollow:")
            if unfollower_name:
                unfollowed_name = get_person_choice("Select the user to be unfollowed:")
                if unfollowed_name:
                    social_media_graph.removeEdge(unfollower_name, unfollowed_name) # This will print "Edge removed" or "not following"
            press_any_key_to_continue()

        elif choice == 'x':
            print("\n**********************************************")
            print("    Exiting Social Media App. Goodbye!")
            print("**********************************************")
            break

        else:
            print("\n! ! ! Invalid choice. Please try again. ! ! !")
            press_any_key_to_continue()

if __name__ == "__main__":
    main()
