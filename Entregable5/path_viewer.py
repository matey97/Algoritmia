'''
Created on Dec 5, 2014

@author: David Llorens (dllorens@uji.es)
'''
from easycanvas import EasyCanvas
from algoritmia.datastructures.digraphs import UndirectedGraph
import sys

class PathViewer(EasyCanvas):
    def __init__(self, heights, scores, path, window_size=(600,400)):
        EasyCanvas.__init__(self)
        self.heights = heights
        self.scores = scores
        self.path = path

        self.window_size = window_size

    def main(self):
        ix = (1000/self.window_size[1]*self.window_size[0])/(len(heights)-1)
        m = (1000/self.window_size[1]*self.window_size[0])*0.03
        r = (1000/self.window_size[1]*self.window_size[0])*0.008
        self.easycanvas_configure(title = '2D Graph Viewer',
                                  background = 'white',
                                  size = self.window_size, 
                                  coordinates = (0-m, 0-m, 1000/self.window_size[1]*self.window_size[0]+m, 999+m))
                
        self.create_line(0, 0, 1000/self.window_size[1]*self.window_size[0], 0, "black")
        self.create_line(0, 0, 0, 1000, "black")
        for i in range(len(self.heights)):
            self.create_filled_circle(i*ix, self.heights[i], r, relleno='palegreen')

        pre = self.path[0]-1
        for i in range(1,len(self.path)):
            c = self.path[i]-1
            self.create_line(pre*ix, self.heights[pre], (c)*ix, self.heights[c], "blue")
            pre = c

        # Wait for a key   
        self.readkey(True)
        
if __name__ == '__main__':
    if len(sys.argv) == 3:
        problem_file = sys.argv[1]
        solution_file = sys.argv[2]
        heights = []
        scores = []
        for lin in open(problem_file):
            h, s = (int(x) for x in lin.strip().split())
            heights.append(h)
            scores.append(s)
        #print(scores)
        f = open(solution_file)
        f.readline()
        path = [int(x) for x in f.readline().split()]
        f.close()
        
        viewer = PathViewer(heights, scores, path, window_size=(800, 600))
        viewer.run()
    else:
        print("Use:")
        print("  python3 path_viewer.py <problem.txt> <solution.txt>")