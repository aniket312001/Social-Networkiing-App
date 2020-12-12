class Person:
    """
    Represent a person , Hold Name, Address, Client
    """

    def __init__(self,addr,client):
        self.addr = addr
        self.client = client
        self.name = None

    def set_name(self,name):
        """
        Set the person name 
        param name: str
        return : None 
        """
        self.name = name

    def __repr__(self):
        return f'Person({self.addr}, {self.name})'
        