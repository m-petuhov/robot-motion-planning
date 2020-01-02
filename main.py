from common.parser import Parser
from rrt.rrt_scheduler import RRTScheduler

if __name__ == "__main__":
    trivial = Parser('data/gigant.json')
    scheduler = RRTScheduler(trivial, 5000, 100)
    scheduler.fit()
