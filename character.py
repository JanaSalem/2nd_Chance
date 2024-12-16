class Character():

    def __init__(self, name:str, description:str, current_room, msg:list):
        self.name = name
        self.description = description
        self.current_room = current_room
        self.msg = msg

    def __str__(self):
        return str(self.name) + " : " +  str(self.description)
    

