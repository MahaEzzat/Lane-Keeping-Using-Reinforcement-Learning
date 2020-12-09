import numpy
import pandas 
import Qtable
import re
import carState
import GetState2

table = Qtable.maketable()
table.to_csv("../input_path/Qtable.csv",index=False)
print(table.loc[79][1])


