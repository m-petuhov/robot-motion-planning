from common.parser import Parser
from rrt.rrt_scheduler import RRTScheduler
from apf.apf_scheduler import APFScheduler

if __name__ == "__main__":
    data = Parser('data/cheese.json')
    # scheduler = RRTScheduler(data, 50000, 10)
    scheduler = APFScheduler(data, 1., 10., 3, 10000, 0.002)
    scheduler.fit()
    # scheduler.build_shortest_path()
