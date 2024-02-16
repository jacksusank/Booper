import os
from django.conf import settings


 
from django.db import models

# Testing
# Create your models here.
# models.py

print("models.py")


# # Manually configure Django settings
# if __name__ == "__main__":
#     os.environ.setdefault("DJANGO_SETTINGS_MODULE", "booper1.settings")
#     settings.configure()


class BoopBoard(models.Model):
    name = models.CharField(max_length=100, default="Nameless BoopBoard")
    columns = models.IntegerField(default=4)
    rows = models.IntegerField(default=4)


    # def __init__(self, columns, rows):
    #     self.columns = columns
    #     self.rows = rows
    #     self.myBoops = []
    #     i = 1
    #     for thatColumn in range(self.columns):
    #         for thatRow in range(self.rows):
    #             i += 1
    #             self.myBoops.append(Boop(column=thatColumn, row=thatRow, thisID=i))

    def getMyBoops(self):
        return self.myBoops

    def __str__(self):
        return f"BoopBoard with {self.columns} columns and {self.rows} rows"
    

class Boop(models.Model):
    boopboard = models.ForeignKey(BoopBoard, on_delete=models.CASCADE)
    thisID = models.IntegerField(default=0)
    column = models.IntegerField()
    row = models.IntegerField()
    booped = models.BooleanField(default=False)

    # def __init__(self, column, row, thisID):
    #     self.column = column
    #     self.row = row
    #     self.booped = False
    #     self.thisID = thisID

    def toggle_booped(self):
        self.booped = not self.booped
        self.save()


    def getThisID(self):
        return self.thisID

    def __str__(self):
        return f"The Boop at {self.column} {self.row} is {'Booped' if self.booped else 'Not Booped'}"


# Initializing the Boops and boopboard:
    
# thisBoopBoard = BoopBoard(collumns=4, rows=4)









"""
class ButtonState(models.Model):
    name = models.CharField(max_length=100)
    state = models.BooleanField(default=False)


    def __str__(self):
        return self.name
"""


"""
class Boop:
    def __init__(self, collumn, row):
        self.collumn = collumn
        self.row = row
        self.booped = False
    
    def __str__(self):
        return f"The Boop at {self.collumn} {self.row} is {self.booped}"
    
    def __isBooped__(self):
        return self.booped
    
    def __boop__(self):
        if self.booped == True:
            self.booped = False
        else:    
            self.booped = True
        print("I have been booped!")

class BoopBoard:
    def __init__(self, collumns, rows):
        self.collumns = collumns
        self.rows = rows
        self.boops = []
        for collumn in range(self.collumns):
            self.boops.append([])
            for row in range(self.rows):
                self.boops[collumn].append(Boop(collumn, row))
    
    def __boop__(self, collumn, row):
        self.boops[collumn][row].__boop__()

    def __isBooped__(self, collumn, row):
        return self.boops[collumn][row].__isBooped__()

    def __str__(self):
        string = ""
        for row in range(self.rows):
            for collumn in range(self.collumns):
                if self.boops[collumn][row].booped == True:
                    string += "1 "
                else:
                    string += "0 "
            string += "\n"
        return string
"""
"""
    # return a string that looks like a collumn x row grid of boops (1 means booped, 0 means not booped).
    def __str__(self):
        string = ""
        for collumn in self.boops:
            for row in collumn:
                if row.booped == True:
                    string += "1 "
                else:
                    string += "0 "
            string += "\n"
        return string
"""
        


"""
    def __str__(self):
        for collumn in self.boops:
            for row in collumn:
                print(row)

        return "BoopBoard:\n"
    
    def __boop__(self, collumn, row):
        self.boops[collumn][row].__boop__()
"""

"""
def main():
    boopboard = BoopBoard(4, 4)
    print(boopboard)
    boopboard.__boop__(0, 1)
    print(boopboard)
    boopboard.__boop__(2, 1)
    print(boopboard)
    boopboard.__boop__(3, 3)
    print(boopboard)
    boopboard.__boop__(3, 3)
    print(boopboard)


    print(boopboard.__isBooped__(1, 0))





if __name__ == "__main__":
    main()
"""