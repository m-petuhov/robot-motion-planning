from common.parser import Parser
from double_way_rrt.double_rrt import DoubleRRT
from trajectory_builder import TrajectoryBuilder


def write_answer(name, forces):
    with open('answers/' + str(name) + '.txt', 'w') as file:
        for force in forces[:-1]:
            file.write(str(force[0]) + ',' + str(force[1]) + '\n')

        file.write(str(forces[-1][0]) + ',' + str(forces[-1][1]))


def check_answer(dt, forces):
    coordinates = [0, 0]
    speed = [0, 0]

    for force in forces:
        coordinates[0] += dt * speed[0]
        coordinates[1] += dt * speed[1]
        speed[0] += dt * force[0]
        speed[1] += dt * force[1]

    return coordinates


if __name__ == "__main__":
    data = Parser('data/cheese.json')
    scheduler = DoubleRRT(data, 10)

    scheduler.build_path()

    builder = TrajectoryBuilder(data, scheduler.path)

    builder.reduction()
    forces = builder.simple_robot_motion()

    # print(check_answer(data.dt, forces))
    write_answer(data.name, forces)
