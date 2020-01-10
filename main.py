from common.parser import Parser
from double_way_rrt.double_rrt import DoubleRRT
from trajectory_builder import TrajectoryBuilder

if __name__ == "__main__":
    data = Parser('data/cheese.json')
    # scheduler = APFScheduler(data, 1., 30., 3, 10000, 0.002)
    # scheduler.fit()
    scheduler = DoubleRRT(data, 10)
    scheduler.build_path()

    smooth = TrajectoryBuilder(data, scheduler.path)
    smooth.reduction()
