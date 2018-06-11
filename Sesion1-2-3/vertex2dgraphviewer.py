'''
Created on 02/10/2013

@author: david
'''
from easycanvas import EasyCanvas
from algoritmia.datastructures.digraphs import UndirectedGraph

class Vertex2dGraphViewer(EasyCanvas):
    def __init__(self, g, window_size=(400,400)):
        EasyCanvas.__init__(self)
        
        # check 'g' type
        if not isinstance(g, UndirectedGraph) or \
           any([type(p)!=type((1,1)) or len(p)!=2 or type(p[0])!=type(1) or type(p[1])!=type(1) for p in g.V]):
            raise TypeError("The labyrinth must be an UnirectedGraph of two integer tuples")
        
        self.g = g
        self.max_col = max(p[1] for p in self.g.V)
        self.max_row = max(p[0] for p in self.g.V)
        self.min_col = min(p[1] for p in self.g.V)
        self.min_row = min(p[0] for p in self.g.V)
        self.window_size = window_size

    def main(self):
        rows = self.max_row-self.min_row+1
        cols = self.max_col-self.min_col+1
        self.cell_size = min(self.window_size[0]/cols, self.window_size[1]/rows)
        m = ((self.window_size[0]-self.cell_size*cols)/2 - self.min_col*self.cell_size, 
             (self.window_size[1]-self.cell_size*rows)/2 - self.min_row*self.cell_size)
        self.easycanvas_configure(title = '2D Graph Viewer',
                                  background = 'white',
                                  size = self.window_size, 
                                  coordinates = (0, 0, self.window_size[0]-1,self.window_size[1]-1))
                
        for u,v in self.g.E:
            self.create_line((u[1]+0.5)*self.cell_size+m[0], (u[0]+0.5)*self.cell_size+m[1], (v[1]+0.5)*self.cell_size+m[0], (v[0]+0.5)*self.cell_size+m[1])
         
        for u in self.g.V:
            self.create_filled_circle((u[1]+0.5)*self.cell_size+m[0], (u[0]+0.5)*self.cell_size+m[1], self.cell_size/8, relleno='palegreen')
        # Wait for a key   
        self.readkey(True)
        
if __name__ == '__main__':
    viewer = Vertex2dGraphViewer(UndirectedGraph(E=[((-3,-2), (0,0)), ((0,0),(1,1))]), window_size=(400, 200))
    viewer.run()