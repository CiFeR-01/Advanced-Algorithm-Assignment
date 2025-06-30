class Person:
    def __init__(self, name, gender, biography, is_private=False):
        self.name = name
        self.gender = gender
        self.biography = biography
        self.is_private = is_private

    def display_profile(self, ignore_privacy=True):
        print(f"\n------- Profile of {self.name} -------")
        print(f"Name: {self.name}")
        if not self.is_private or ignore_privacy:
            print(f"Gender: {self.gender}")
            print(f"Biography: {self.biography}")
        else:
            print("This profile is private. Details are hidden.")
        print(f"Profile Status: {'Private' if self.is_private else 'Public'}")
        print("-------------------------------------------\n")

    def __str__(self):
        return self.name
