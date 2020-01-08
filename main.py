from apf.apf_scheduler import APFScheduler
from common.parser import Parser
from double_way_rrt.double_rrt import DoubleRRT
from smooth import Smooth

if __name__ == "__main__":
    data = Parser('data/cheese.json')
    # scheduler = APFScheduler(data, 1., 30., 3, 10000, 0.002)
    # scheduler.fit()
    scheduler = DoubleRRT(data, 10)
    scheduler.build_path()

    smooth = Smooth(data, scheduler.path)
    smooth.reduction()
