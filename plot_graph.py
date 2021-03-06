from matplotlib import pyplot as plt
import numpy as np
from kivy.garden.matplotlib import FigureCanvasKivyAgg
from sqlite_database import SQL_Database
import datetime


class MatPlot:
    def __init__(self):
        self.x=[]
        self.y=[]

    def graph_internal(self, elements):
            database = SQL_Database('test.db')

            data_int = database.get("sensors_int", ("temp_int, date_int"))
            #print (data_int[0])
            for data in data_int:
                #print (data)
                xx = datetime.datetime.fromtimestamp(data[1])
                #xx = xx.strftime('%Y-%m-%d %H:%M:%S')
                xx = xx.strftime('%H:%M')
                if (data[0] != -1000):
                    self.x.append(xx)
                    self.y.append(data[0])
            
            plt.figure().clear()
            plt.ylim(20,31)
            plt.title("Aquarium Temperature °C")
            for xy in zip(self.x[-elements:], self.y[-elements:]):
                #plt.annotate('(%s, %s)' % xy, xy=xy, textcoords='data')
                plt.annotate('%s' % round(xy[1],1), xy=xy, textcoords='data')
                

            #print(self.x[-elements:])  
            #print(self.y[-elements:]) 
            # this will plot the signal on graph
            plt.plot(self.x[-elements:], self.y[-elements:])
            
            canvas = FigureCanvasKivyAgg(plt.gcf())
            return canvas
    def graph_external(self, elements):
            database = SQL_Database('test.db')

            data_ext = database.get("sensors_ext", ("temp_ext, date_ext"))
            #print (data_int[0])
            for data in data_ext:
                #print (data)
                xx = datetime.datetime.fromtimestamp(data[1])
                #xx = xx.strftime('%Y-%m-%d %H:%M:%S')
                xx = xx.strftime('%H:%M')
                if (data[0] != -1000):
                    self.x.append(xx)
                    self.y.append(data[0])
            
            plt.figure().clear()
            plt.ylim(10,40)
            plt.title("Room Temperature °C")
            for xy in zip(self.x[-elements:], self.y[-elements:]):
                #plt.annotate('(%s, %s)' % xy, xy=xy, textcoords='data')
                plt.annotate('%s' % round(xy[1],1), xy=xy, textcoords='data')
                

            #print(self.x[-elements:])  
            #print(self.y[-elements:]) 
            # this will plot the signal on graph
            plt.plot(self.x[-elements:], self.y[-elements:])
            
            canvas = FigureCanvasKivyAgg(plt.gcf())
            return canvas
    def graph_external_hum(self, elements):
            database = SQL_Database('test.db')

            data_ext = database.get("sensors_ext", ("hum_ext, date_ext"))
            #print (data_int[0])
            for data in data_ext:
                #print (data)
                xx = datetime.datetime.fromtimestamp(data[1])
                #xx = xx.strftime('%Y-%m-%d %H:%M:%S')
                xx = xx.strftime('%H:%M')
                if (data[0] != -1000):
                    self.x.append(xx)
                    self.y.append(data[0])
            
            plt.figure().clear()
            plt.ylim(30,70)
            plt.title("Room Humidity %")
            for xy in zip(self.x[-elements:], self.y[-elements:]):
                #plt.annotate('(%s, %s)' % xy, xy=xy, textcoords='data')
                plt.annotate('%s' % round(xy[1],1), xy=xy, textcoords='data')
                

            #print(self.x[-elements:])  
            #print(self.y[-elements:]) 
            # this will plot the signal on graph
            plt.plot(self.x[-elements:], self.y[-elements:])
            
            canvas = FigureCanvasKivyAgg(plt.gcf())
            return canvas