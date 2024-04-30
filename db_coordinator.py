from utils import UTILS

class DB_COOORDINATOR(UTILS):
    def __init__(self) -> None:
        super().__init__() 

    def db_writer(self, set_item):
        print("dbb_coordinator")
        if set_item:
            print(set_item)
            return True 
        return False