class Inventory:
    """
    Manages the player's inventory.
    """
    def __init__(self):
        self.items = []
        self.capacity = 20

    def add_item(self, item):
        """
        Add an item to the inventory.
        """
        if len(self.items) < self.capacity:
            self.items.append(item)
            print(f"Picked up: {item}")
            return True
        else:
            print("Inventory is full!")
            return False

    def remove_item(self, item):
        """
        Remove an item from the inventory.
        """
        if item in self.items:
            self.items.remove(item)
            return True
        return False
