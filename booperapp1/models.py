from django.db import models

'''
This is the model for the BoopBoard. It contains a name, the number of columns, and the number of rows it has.
It also contains a list of Boops, which are the individual buttons on the BoopBoard.
I use SQLite3 as the database for this project, so the BoopBoard and Boop models are stored in the database.
'''
class BoopBoard(models.Model):
    name = models.CharField(max_length=100, default="Nameless BoopBoard")
    columns = models.IntegerField(default=4)
    rows = models.IntegerField(default=4)

    def __str__(self):
        return f"BoopBoard named {self.name} with {self.columns} columns and {self.rows} rows."


'''
This is the model for the Boop. It contains a reference to the BoopBoard it is on,
the column and row it is in, and a boolean for whether it is booped or not.
'''
class Boop(models.Model):
    boopboard = models.ForeignKey(BoopBoard, on_delete=models.CASCADE) # This connects the Boops to the BoopBoard
    thisID = models.IntegerField(default=0)
    column = models.IntegerField()
    row = models.IntegerField()
    booped = models.BooleanField(default=False)


    # This function toggles the booped boolean
    def toggle_booped(self):
        self.booped = not self.booped
        self.save()

    # This function returns the ID (1-16) of the booped boolean
    def getThisID(self):
        return self.thisID

    
    def __str__(self):
        return f"The Boop at {self.column} {self.row} is {'Booped' if self.booped else 'Not Booped'}"


