'''
Create and solve graph using g2o library
Adopted from https://github.com/miquelmassot/g2o-python-examples/blob/main/g2o%20covariance%20retrieval.ipynb
'''

import g2o
import numpy as np

class GraphSLAM2D:
    def __init__(self, verbose=False) -> None:
        '''
        GraphSLAM in 2D with G2O
        '''
        self.optimizer = g2o.SparseOptimizer()
        self.solver = g2o.BlockSolverX(g2o.LinearSolverDenseX())
        self.algorithm = g2o.OptimizationAlgorithmLevenberg(self.solver)
        self.optimizer.set_algorithm(self.algorithm)

        self.vertex_count = 0
        self.edge_count = 0
        self.verbose = verbose

    def vertex_pose(self, id):
        '''
        Get position of vertex by id
        '''
        return self.optimizer.vertex(id).estimate()

    def vertex(self, id):
        '''
        Get vertex by id
        '''
        return self.optimizer.vertex(id)

    def edge(self, id):
        '''
        Get edge by id
        '''
        return self.optimizer.edge(id)

    def add_fixed_pose(self, pose, vertex_id=None):
        '''
        Add fixed pose to the graph
        '''
        v_se2 = g2o.VertexSE2()
        if vertex_id is None:
            vertex_id = self.vertex_count
        v_se2.set_id(vertex_id)
        if self.verbose:
            print("Adding fixed pose vertex with ID", vertex_id)
        v_se2.set_estimate(pose)
        v_se2.set_fixed(True)
        self.optimizer.add_vertex(v_se2)
        self.vertex_count += 1

    def add_odometry(self, northings, eastings, heading, information):	#Modify this to use lat/lon?
        '''
        Add odometry to the graph
        '''
        # Find the last pose vertex id
        vertices = self.optimizer.vertices()
        if len(vertices) > 0:
            last_id = [v for v in vertices if type(vertices[v]) == g2o.VertexSE2][0]
            print("Last id is", last_id)
        else:
            raise ValueError("There is no previous pose, have you forgot to add a fixed initial pose?")
        v_se2 = g2o.VertexSE2()
        if self.verbose:
            print("Adding pose vertex", self.vertex_count)
        v_se2.set_id(self.vertex_count)
        pose = g2o.SE2(northings, eastings, heading)
        v_se2.set_estimate(pose)
        self.optimizer.add_vertex(v_se2)
        # add edge
        e_se2 = g2o.EdgeSE2()
        e_se2.set_vertex(0, self.vertex(last_id))
        e_se2.set_vertex(1, self.vertex(self.vertex_count))
        e_se2.set_measurement(pose)
        e_se2.set_information(information)
        self.optimizer.add_edge(e_se2)
        self.vertex_count += 1
        self.edge_count += 1
        if self.verbose:
            print("Adding SE2 edge between", last_id, self.vertex_count-1)

    def add_landmark(self, x, y, information, pose_id, landmark_id=None):
        '''
        Add landmark to the graph
        '''
        relative_measurement = np.array([x, y])
        
        # Check that the pose_id is of type VertexSE2
        if type(self.optimizer.vertex(pose_id)) != g2o.VertexSE2:
            raise ValueError("The pose_id that you have provided does not correspond to a VertexSE2")
        
        trans0 = self.optimizer.vertex(pose_id).estimate()
        measurement = trans0 * relative_measurement
        
        print(relative_measurement, measurement)
        
        if landmark_id is None:
            landmark_id = self.vertex_count
            v_pointxy = g2o.VertexPointXY()
            v_pointxy.set_estimate(measurement)
            v_pointxy.set_id(landmark_id)
            if self.verbose:
                print("Adding landmark vertex", landmark_id)
            self.optimizer.add_vertex(v_pointxy)
            self.vertex_count += 1
        # add edge
        e_pointxy = g2o.EdgeSE2PointXY()
        e_pointxy.set_vertex(0, self.vertex(pose_id))
        e_pointxy.set_vertex(1, self.vertex(landmark_id))
        self.edge_count += 1
        e_pointxy.set_measurement(relative_measurement)
        e_pointxy.set_information(information)
        self.optimizer.add_edge(e_pointxy)
        if self.verbose:
            print("Adding landmark edge between", pose_id, landmark_id)

    def optimize(self, iterations=10, verbose=None):
        '''
        Optimize the graph
        '''
        self.optimizer.initialize_optimization()
        if verbose is None:
            verbose = self.verbose
        self.optimizer.set_verbose(verbose)
        self.optimizer.optimize(iterations)
        return self.optimizer.chi2()



# graph_slam = GraphSLAM2D(verbose=True)

# # Add fixed pose ID #0
# graph_slam.add_fixed_pose(g2o.SE2())

# # Add a landmark #1
# landmark_x = 0
# landmark_y = 1
# graph_slam.add_landmark(landmark_x, landmark_y, np.eye(2), pose_id=0)

# # Add odometry #2
# graph_slam.add_odometry(1, 0, 0, 0.1*np.eye(3))
 
# # Add a landmark #3
# landmark_x = 0
# landmark_y = 1
# graph_slam.add_landmark(landmark_x, landmark_y, np.eye(2), pose_id=2)

# # Add another odometry #4
# graph_slam.add_odometry(2, 0, 0, 0.1*np.eye(3))

# # Add a new landmark #5
# landmark_x = 0
# landmark_y = 1
# graph_slam.add_landmark(landmark_x, landmark_y, np.eye(2), pose_id=4)

# # Add a new landmark relationship between ID #2 and ID #5
# landmark_x = 1
# landmark_y = 1
# graph_slam.add_landmark(landmark_x, landmark_y, np.eye(2), pose_id=2, landmark_id=5)

# # Optimize
# graph_slam.optimize(10, verbose=True)




