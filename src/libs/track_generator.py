import numpy
import matplotlib.pyplot as plt
import os

class TrackGenerator:


    def __init__(self, base_points_count = 1024, width = 15.0):

        self.base_points_count = base_points_count
        self.width = width

        points = []

        self.pi = 3.141591654

        p_curve_change = 0.2 #0.01 .. 0.2
        dr_max         = 0.02


        dphi         = 2.0*self.pi/self.base_points_count
        if numpy.random.randint(2) == 1:
            dphi = -dphi
 
        line_curve_mode = "right"

        r_max       = 4.0
        r_initial   = r_max/2
        r           = r_initial
        dr          = 0.0
        dr_smooth   = 0.0
        
        phi = 0.0
        k = 0.05

        for i in range(self.base_points_count):
            
            t = numpy.exp(10*(i/self.base_points_count - 1.0))
            rw = t*r_initial + (1.0 - t)*r

            x = rw*numpy.sin(phi)
            y = rw*numpy.cos(phi)


            if numpy.random.rand() < p_curve_change:
                rnd = numpy.random.randint(2)
                if rnd == 0:
                    line_curve_mode = "right"
                    dr = numpy.random.rand()*dr_max + 0.001
                elif rnd == 1:
                    line_curve_mode = "left"
                    dr = -(numpy.random.rand()*dr_max + 0.001)
                else:
                    line_curve_mode = "sraight"
                    dr = self._calc_dr_for_straight(r, dphi, dphi)

                    

            dr_smooth = (1.0 - k)*dr_smooth + k*dr
            r = numpy.clip(r + dr_smooth, 0.1*r_max, r_max)
            

            phi+= dphi

            points.append([x, y])

        self.points = numpy.asarray(points)

    def get_length(self):
        return len(self.points)

    def get_start(self, idx = 4):
        dx = self.points[idx][0] - self.points[idx-1][0]
        dy = self.points[idx][1] - self.points[idx-1][1]

        yaw = numpy.arctan2(dy, dx)

        point       = [self.points[idx][0], self.points[idx][1], 0.05]
        orientation = [yaw + self.pi, 0.0, 0.0]
        return [point, orientation]

    def get_start_random(self):
        idx = numpy.random.randint(self.get_length()//2) + 4
        return self.get_start(idx)

    def get_closest(self, x, y):
        position = [x, y]

        dif = self.points - position
        distances = (numpy.sum((dif**2), axis = 1))**0.5

        closest_idx         = numpy.argmin(distances)
        closest_distance    = distances[closest_idx]

        return closest_idx, closest_distance

       
    def save(self, file_name):

        f = open(file_name,"w") 

        idx_current = 1

        for i in range(self.base_points_count-2):
            
            points_now   = self._get_points(self.width, self.points[i + 0], self.points[i + 1])
            points_next  = self._get_points(self.width, self.points[i + 1], self.points[i + 2])


            points = []
            points.append(points_now[0])
            points.append(points_next[1])
            
            points_str, idx_current = self._get_obj(points, idx_current)

            f.write(points_str)
        
        f.flush()
        os.fsync(f)
        f.close()

    def _get_points(self, width, start_point, end_point):

        x0 = start_point[0]
        y0 = start_point[1]

        x1 = end_point[0]
        y1 = end_point[1]
        
        #vector
        vx = x1 - x0
        vy = y1 - y0

        #perpindicular vector
        vxp = vy
        vyp = -vx

        #normalise vector
        length = (vxp**2 + vyp**2)**0.5

        vxp = vxp / length
        vyp = vyp / length

        points = []

        points.append([x0 + vxp*0.5*width, y0 + vyp*0.5*width])
        points.append([x0 - vxp*0.5*width, y0 - vyp*0.5*width])
        points.append([x1 + vxp*0.5*width, y1 + vyp*0.5*width])
        points.append([x1 - vxp*0.5*width, y1 - vyp*0.5*width])

        return points

    def _get_obj(self, points, idx_start = 1):

        idx_end = len(points) + idx_start
        
        result = ""

        for i in range(len(points)):
            result+= "v " + str(points[i][0]) + " " + str(points[i][1]) + " " + str(0.0) + "\n"

          
        result+= "f " + str(idx_start + 0) + " " + str(idx_start + 2) + " " + str(idx_start + 1) + "\n"
        result+= "f " + str(idx_start + 2) + " " + str(idx_start + 3) + " " + str(idx_start + 1) + "\n"


        return result, idx_end

    def _calc_dr_for_straight(self, r, dphi1, dphi2):

        alpha = self.pi/2.0 + 0.5*dphi1
        beta  = self.pi - (dphi2 + alpha)

        arg = (alpha/beta)*numpy.sin(r)
        result = numpy.arcsin(arg) - r

        return result

    def show(self):
        
        tmp = numpy.transpose(self.points)
        plt.plot(tmp[0], tmp[1])
        plt.show()



if __name__ == '__main__':
    line = TrackGenerator(1024, 0.015)

    line.show()
    #line.save("line.obj")


'''
v  0.0      0.0  0.0
v  0.025    0.0  0.0
v  0.025    0.1  0.0
v  0.0      0.1  0.0

f  1  2  3
f  1  3  4
'''