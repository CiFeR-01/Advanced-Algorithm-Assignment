class Person:
    def __init__(self, name, gender, biography, is_private=False):
        self.name = name
        self.gender = gender
        self.biography = biography
        self.is_private = is_private

    def display_profile(self, ignore_privacy=True):
        print(f"\n--- Profile of {self.name} ---")
        print(f"Name: {self.name}")
        if not self.is_private or ignore_privacy:
            print(f"Gender: {self.gender}")
            print(f"Biography: {self.biography}")
        else:
            print("This profile is private. Details are hidden.")
        print(f"Profile Status: {'Private' if self.is_private else 'Public'}")
        print("--------------------------")

    def __str__(self):
        return self.name

"""
# --- Test Section for Person ---
if __name__ == "__main__":
    print("--- Testing Person Class ---")

    # Create some person objects
    p1 = Person("John Doe", "Male", "Software Developer, loves coding.", is_private=False)
    p2 = Person("Jane Smith", "Female", "Artist and Traveler, passionate about nature.", is_private=True)
    p3 = Person("Mike Johnson", "Non-binary", "Gamer and Streamer.", is_private=False)

    print("\nDisplaying public profile (ignoring privacy):")
    p1.display_profile(ignore_privacy=True)

    print("\nDisplaying private profile (ignoring privacy):")
    p2.display_profile(ignore_privacy=True)

    print("\nDisplaying public profile (respecting privacy):")
    p3.display_profile(ignore_privacy=False)

    print("\nDisplaying private profile (respecting privacy):")
    p2.display_profile(ignore_privacy=False)

    print("\nTesting __str__ method:")
    print(f"String representation of p1: {p1}") # Expected: John Doe
    print(f"String representation of p2: {p2}") # Expected: Jane Smith

    print("--- Person Class Testing Complete ---")
"""