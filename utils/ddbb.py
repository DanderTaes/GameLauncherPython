import os
import json

class DDBBParent:
    def __init__(self):
        self.path = ""
        self.data_list = []
    
    def get_list_from_ddbb(self):
        if not os.path.exists(self.path) or os.path.getsize(self.path) == 0:
            os.makedirs(os.path.dirname(self.path), exist_ok=True)
            with open(self.path, "w") as file:
                json.dump([], file)
            return []

        with open(self.path, "r") as file:
            self.data_list = json.load(file)
        return self.data_list
    
    def save_list_to_ddbb(self):
        with open(self.path, "w") as file:
            json.dump(self.data_list, file, indent=4)

    def add_item(self, item):
        self.data_list.append(item)
        self.save_list_to_ddbb()
    def remove_item(self, item):
        if item not in self.data_list:
            raise ValueError("Item not found in the list.")
        self.data_list.remove(item)
        self.save_list_to_ddbb()

    def modify_item(self, old_item, new_item):
        if old_item not in self.data_list:
            raise ValueError("Old item not found in the list.")
        index = self.data_list.index(old_item)
        self.data_list[index] = new_item
        self.save_list_to_ddbb()
        
    def get_items(self):
        return self.data_list