from matplotlib import pyplot as plt
import numpy as np
from kivy.garden.matplotlib import FigureCanvasKivyAgg
from sqlite_database import SQL_Database


class MatPlot:
    def __init__(self):
        x=[]
        y=[]

        database = SQL_Database('test.db')

        data_int = database.get("sensors_int", ("temp_int, date_int"))
        print (data_int[0])
        for data in data_int:
            #print (data)
            x.append(data[1])
            y.append(data[0])

        signal = [7, 89.6, 45.-56.34]
    
        signal = np.array(signal)
        print(x)  
        print(y) 
        # this will plot the signal on graph
        plt.plot(signal)
          
        canvas = FigureCanvasKivyAgg(plt.gcf())

c = MatPlot()