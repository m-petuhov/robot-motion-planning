from common.parser import Parser
from rrt.rrt_scheduler import RRTScheduler

if __name__ == "__main__":
    data = Parser('data/cheese.json')
    scheduler = RRTScheduler(data, 50000, 10)
    scheduler.fit()
    scheduler.build_shortest_path()
