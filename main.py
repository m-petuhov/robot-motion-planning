from common.parser import Parser
from double_way_rrt.double_rrt import DoubleRRT

if __name__ == "__main__":
    data = Parser('data/cheese.json')
    scheduler = DoubleRRT(data, 10)
    scheduler.build_path()
