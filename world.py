import copy
from collections import namedtuple

from game import *
from map_ import *
from usv import *
from plane_test import *
from CircleObstacle import *
import numpy as np

from collections.abc import Iterable

class NpaMyUSV(MyUSV):

    def __init__(self, uid, x, y, env):
        super().__init__(uid, x, y, env)
        self.last_action = None
        self.radius = 3

    def decision_algorithm(self):
        return self.last_action


class _MyContinueDynamicsUSV(MyContinueDynamicsUSV3):

    def __init__(self, uid, x, y, env, envDisturb, FTListValue=[]):
        super().__init__(uid, x, y, env, envDisturb, FTListValue=FTListValue)
        self.last_action = None

    def decision_algorithm(self):
        return self.last_action

class World(object):
    def __init__(self, Policy):
        self.policy_agents = []
        self.policy = Policy(self)

    def step(self, action_n):
        raise NotImplementedError()

    def reset(self):
        # reset world
        raise NotImplementedError()

    # render environment
    def render(self):
        raise NotImplementedError()

    def observe(self):
        return copy.copy(self.observation_space)

class TestWorld(World):
    def __init__(self, Policy):
        super().__init__(Policy)

        self.policy_agents = ["Npa"]

        # configure spaces
        self.action_space = ["Left", "Right", "Up", "Down"]
        self.observation_space = ["Left", "Right", "Up", "Down"]

    def decide(self):
        return [self.policy.action(obs) for obs in self.observation_space]

    def step(self, action_n):
        action = action_n[0] # as there is only one agent
        return [copy.copy(self.observation_space)], [0], [False], ["Nothing"]

    def reset(self):
        # reset world
        self.agents = ["Npa"]

        # configure spaces
        self.action_space = ["Left", "Right", "Up", "Down"]
        self.observation_space = ["Left", "Right", "Up", "Down"]

    # render environment
    def render(self):
        print("render!")

class OneStepWorld(World):
    def __init__(self, Policy):
        super().__init__(Policy)

        self.game = self.init_game()

        self.policy_agents = self.game.map.friendly_ships

        self.action_class = namedtuple(
            "action", ['stay', 'clockwise', 'angular_speed'])
        Action = self.action_class

        l = Action(False, True, 0)
        u = Action(False, True, 90)
        r = Action(False, True, 180)
        d = Action(False, True, 270)

        # configure spaces
        self._action_space = [l, u, r, d]

        self.path_len = 0

    @property
    def action_space(self):
        return self._action_space

    @property
    def observation_space(self):
        return self.game.map.env_matrix()

    def init_game(self):
        test_map = BasicMap(10, 10)
        test_map.set_target(9, 9)

        test_friendly_ship = NpaMyUSV(uid=0, x=0, y=0, env=test_map)  # USV友艇起始点
        test_friendly_ship.set_as_friendly()
        test_map.add_ship(test_friendly_ship)

        test_enemy_ship1 = MyUSV(uid=1, x=2, y=2, env=test_map)
        test_enemy_ship1.set_as_enemy()
        test_map.add_ship(test_enemy_ship1)
        test_enemy_ship2 = MyUSV(uid=2, x=3, y=2, env=test_map)
        test_enemy_ship2.set_as_enemy()
        test_map.add_ship(test_enemy_ship2)
        test_enemy_ship3 = MyUSV(uid=3, x=4, y=2, env=test_map)
        test_enemy_ship3.set_as_enemy()
        test_map.add_ship(test_enemy_ship3)
        test_enemy_ship4 = MyUSV(uid=4, x=2, y=5, env=test_map)
        test_enemy_ship4.set_as_enemy()
        test_map.add_ship(test_enemy_ship4)
        test_enemy_ship5 = MyUSV(uid=5, x=2, y=6, env=test_map)
        test_enemy_ship5.set_as_enemy()
        test_map.add_ship(test_enemy_ship5)

        test_enemy_ship6 = MyUSV(uid=6, x=2, y=7, env=test_map)
        test_enemy_ship6.set_as_enemy()
        test_map.add_ship(test_enemy_ship6)
        test_enemy_ship7 = MyUSV(uid=7, x=3, y=5, env=test_map)
        test_enemy_ship7.set_as_enemy()
        test_map.add_ship(test_enemy_ship7)
        test_enemy_ship8 = MyUSV(uid=8, x=3, y=6, env=test_map)
        test_enemy_ship8.set_as_enemy()
        test_map.add_ship(test_enemy_ship8)
        test_enemy_ship9 = MyUSV(uid=9, x=4, y=3, env=test_map)
        test_enemy_ship9.set_as_enemy()
        test_map.add_ship(test_enemy_ship9)
        test_enemy_ship10 = MyUSV(uid=10, x=5, y=6, env=test_map)
        test_enemy_ship10.set_as_enemy()
        test_map.add_ship(test_enemy_ship10)

        test_enemy_ship11 = MyUSV(uid=11, x=6, y=5, env=test_map)
        test_enemy_ship11.set_as_enemy()
        test_map.add_ship(test_enemy_ship11)
        test_enemy_ship12 = MyUSV(uid=12, x=7, y=5, env=test_map)
        test_enemy_ship12.set_as_enemy()
        test_map.add_ship(test_enemy_ship12)
        test_enemy_ship13 = MyUSV(uid=13, x=7, y=6, env=test_map)
        test_enemy_ship13.set_as_enemy()
        test_map.add_ship(test_enemy_ship13)
        test_enemy_ship14 = MyUSV(uid=14, x=7, y=7, env=test_map)
        test_enemy_ship14.set_as_enemy()
        test_map.add_ship(test_enemy_ship14)
        test_enemy_ship15 = MyUSV(uid=15, x=8, y=5, env=test_map)
        test_enemy_ship15.set_as_enemy()
        test_map.add_ship(test_enemy_ship15)

        game = MyGame()
        game.set_map(test_map)

        return game

    def step(self, action_n, time):
        self.path_len += 1

        if isinstance(action_n, Iterable):
            action_i = action_n[0]  # as there is only one agent
        else:
            action_i = action_n
        actor = self.policy_agents[0]
        actor.last_action = self.action_space[action_i]
        self.game.update()

        x, y = actor.coordinate()
        # distance_reward = 30 - (abs(self.game.map.target_coordinate()[0] - x) + abs(self.game.map.target_coordinate()[1] - y))
        distance_reward = 0

        if x < 0 or y < 0 or x > self.game.map.target_coordinate()[0] or y > self.game.map.target_coordinate()[1]:
            if x < 0:
                x = 0
            if x > self.game.map.target_coordinate()[0]:
                x = self.game.map.target_coordinate()[0]
            if y < 0:
                y = 0
            if y > self.game.map.target_coordinate()[1]:
                y = self.game.map.target_coordinate()[1]
            actor.x = x
            actor.y = y
            return [self.game.map.env_matrix()], [-150], [True], []

        if self.game.arriveTarget:
            return [self.game.map.env_matrix()], [300 - self.path_len], [True], []

        if self.game.arriveObstacle:
            return [self.game.map.env_matrix()], [-300], [True], []

        return [self.game.map.env_matrix()], [distance_reward], [False], []

    def reset(self):
        # reset world
        self.game = self.init_game()
        self.policy_agents = self.game.map.friendly_ships
        self.path_len = 0
        return self.game.map.env_matrix()

    # render environment
    def render(self):
        # print("render!")
        raise NotImplementedError()

class ContinuousWorld(World):
    class _MyContinueUSV(MyContinueUSV):

        def __init__(self, uid, x, y, env):
            super().__init__(uid, x, y, env)
            self.last_action = None

        def decision_algorithm(self):
            return self.last_action

    def __init__(self, Policy, obsticle_moving):
        super().__init__(Policy)

        self.obsticle_moving = obsticle_moving

        self.game = self.init_game(obsticle_moving)

        self.policy_agents = self.game.map.friendly_ships

        self.action_class = namedtuple(
            "action", ['stay', 'clockwise', 'angular_speed', "speed"])

        self.time = 0

    def init_game(self, obsticle_moving):
        test_map = MyContinueObsMap(100, 100)
        test_map.set_target(2.0, 48.0)  # 目标终点,(注：初始点的设定要合法--即在map缩小ship.radius的范围)

        # USV友艇起始点,(注：初始点的设定要合法--即在map缩小ship.radius的范围)
        test_friendly_ship = self._MyContinueUSV(uid=0, x=12.0, y=50.0, env=test_map)
        test_friendly_ship.set_as_friendly()
        test_map.add_ship(test_friendly_ship)

        # 静态矩形障碍物区域（注：初始位置的设定要合法，即在map缩小obs.radius的范围）
        obs1 = CircleObstacle(uid=0, x=10.0, y=10.0, radius=10, env=test_map)
        test_map.addobs(obs1)
        obs2 = CircleObstacle(uid=1, x=40.0, y=40.0, radius=10, env=test_map)
        test_map.addobs(obs2)
        obs3 = CircleObstacle(uid=2, x=70.0, y=60.0, radius=10, env=test_map)
        test_map.addobs(obs3)

        # False表示障碍物不随机移动; True表示障碍物随机移动
        game = MyContinueGame(obsticle_moving)
        game.set_map(test_map)

        return game

    def step(self, action_n, time):
        self.time += 1

        if isinstance(action_n, Iterable):
            action = action_n[0]  # as there is only one agent
        else:
            action = action_n
        actor = self.policy_agents[0]
        actor.last_action = self.action_class(False, True, action * 360, 1)
        self.game.update()

        x, y = actor.coordinate()
        # distance_reward = 30 - (abs(self.game.map.target_coordinate()[0] - x) + abs(self.game.map.target_coordinate()[1] - y))
        distance_reward = 0

        if x < 0 or y < 0 or x >= self.game.map.width or y >= self.game.map.height:
            if x < 0:
                x = 0
            if x >= self.game.map.width:
                x = self.game.map.width - 1
            if y < 0:
                y = 0
            if y >= self.game.map.height:
                y = self.game.map.height - 1
            actor.x = x
            actor.y = y
            return [self.game.map.env_matrix()], [-150], [True], []

        if self.game.arriveTarget:
            return [self.game.map.env_matrix()], [300 - self.time / 5], [True], []

        if self.game.arriveObstacle:
            return [self.game.map.env_matrix()], [-300], [True], []

        return [self.game.map.env_matrix()], [distance_reward], [False], []

    def reset(self):
        # reset world
        self.game = self.init_game(self.obsticle_moving)
        self.policy_agents = self.game.map.friendly_ships
        self.time = 0
        return self.game.map.env_matrix()


class _MyContinueUSV_SmallMap(MyContinueUSV_SmallMap):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.last_action = None
    
    def decision_algorithm(self):
        Action = self.action_class
        angular_speed_value = self.last_action.F * self.angular_speed_max
        speed_value = self.last_action.T * self.speed_max
        act = Action(False, False, angular_speed_value, speed_value)
        # print(act)
        return act

class ContinuousDynamicWorld(ContinuousWorld):
    def __init__(self, Policy, obsticle_moving):
        super().__init__(Policy, obsticle_moving)

        self.obsticle_moving = obsticle_moving

        self.game = self.init_game(obsticle_moving)

        self.policy_agents = self.game.map.friendly_ships

        self.action_class = namedtuple("action", ['F', 'T'])

        self.time = 0

        self.last_feature = np.array([0, 0, 0, 0, 0, 0])

    def init_game(self, obsticle_moving):

        test_map = MyContinueObsMap(3.0, 3.0)
        # 目标终点,(注：初始点的设定要合法--即在map缩小ship.radius的范围)
        test_map.set_target(0.50, 2.50)
        test_map.set_target_radius(0.1)

        # USV友艇起始点,(注：初始点的设定要合法--即在map缩小ship.radius的范围)
        test_friendly_ship = _MyContinueUSV_SmallMap(
            uid=0, x=2.50, y=0.5, env=test_map)
        test_friendly_ship.set_as_friendly()
        test_map.add_ship(test_friendly_ship)
        test_friendly_ship.set_usv_radius(0.1)
        test_friendly_ship.set_usv_speed(0.1)

        # 静态矩形障碍物区域（注：初始位置的设定要合法，即在map缩小obs.radius的范围）
        obs1 = CircleObstacle(uid=0, x=0.85, y=1.00, radius=0.1, env=test_map)
        test_map.addobs(obs1)
        # obs2 = CircleObstacle(uid=1, x=1.50, y=0.50, radius=0.1, env=test_map)
        # test_map.addobs(obs2)
        obs3 = CircleObstacle(uid=2, x=1.60, y=1.40, radius=0.1, env=test_map)
        test_map.addobs(obs3)
        obs4 = CircleObstacle(uid=3, x=1.10, y=1.80, radius=0.1, env=test_map)
        test_map.addobs(obs4)
        obs5 = CircleObstacle(uid=3, x=0.30, y=1.60, radius=0.2, env=test_map)
        test_map.addobs(obs5)

        obs6 = CircleObstacle(uid=4, x=2.00, y=1.00, radius=0.1, env=test_map)
        test_map.addobs(obs6)
        # obs7 = CircleObstacle(uid=5, x=2.30, y=1.80, radius=0.2, env=test_map);test_map.addobs(obs7)
        obs8 = CircleObstacle(uid=6, x=1.80, y=2.40, radius=0.2, env=test_map)
        test_map.addobs(obs8)
        obs9 = CircleObstacle(uid=6, x=1.20, y=2.60, radius=0.1, env=test_map)
        test_map.addobs(obs9)

        #是否可视化
        # game = CoutinuePyGame(False)  # False表示障碍物不随机移动; True表示障碍物随机移动
        game = CoutinueNoPyGame(False)

        game.set_map(test_map)

        return game

    @property
    def obs(self):
        # board = self.game.map.env_matrix()
        # board = np.array(board)
        # board = np.reshape(board, (1, ) + board.shape)

        # game = self.game
        # u = game.get_uvr_u() / 5
        # v = game.get_uvr_v() / 5
        # r = game.get_uvr_r() / 10
        # h = (game.get_xyh_heading() - 180) / 180

        actor = self.policy_agents[0]
        x, y = actor.coordinate()
        # print(x, y)
        x, y = (x - 50) / 50, (y - 50) / 50
        dis = actor.getDistanceUSVTarget()

        # u_board = np.zeros(board.shape) + u
        # v_board = np.zeros(board.shape) + v
        # r_board = np.zeros(board.shape) + r
        # h_board = np.zeros(board.shape) + h

        # data = (board, u_board, v_board, r_board, h_board)
        # feature = np.concatenate(data, axis=0)
        # feature = np.array([x, y, u, v, r, h])
        feature = np.array([x, y, dis])
        self.last_feature = feature
        # print(feature.shape, feature)
        # exit()
        feature = np.concatenate((feature, self.last_feature), axis=0)
        # print("\n\n\n\n\n\n\n\n\n\n")
        # print(feature)
        # exit()
        # print(feature)
        return feature

    @property
    def observation_space(self):
        return self.obs

    def step(self, action_n, time):
        actor = self.policy_agents[0]

        distance_punish_rate = 1000

        if self.time > 2000:
            return [self.obs], [-150 - actor.getDistanceUSVTarget() * distance_punish_rate], [True], []

        self.time += 1
        # print(action_n)
        # note that there is only one actor currently
        action = np.reshape(action_n, (2, ))
        F, T = action[0], action[1]

        
        # print("in world:", actor)
        actor.last_action = self.action_class(F, T)
        self.game.update()

        x, y = actor.coordinate()
        # distance_reward = 30 - (abs(self.game.map.target_coordinate()[0] - x) + abs(self.game.map.target_coordinate()[1] - y))
        distance_reward = 0

        if x < 0 or y < 0 or x >= self.game.map.width or y >= self.game.map.height:
            if x < 0:
                x = 0
            if x >= self.game.map.width:
                x = self.game.map.width - 1
            if y < 0:
                y = 0
            if y >= self.game.map.height:
                y = self.game.map.height - 1
            actor.x = x
            actor.y = y
            return [self.obs], [-150 - actor.getDistanceUSVTarget() * distance_punish_rate], [True], []

        if self.game.arriveTarget:
            # return [self.obs], [10000 - self.time], [True], []
            return [self.obs], [10000], [True], []

        if self.game.arriveObstacle:
            return [self.obs], [-300 - actor.getDistanceUSVTarget() * distance_punish_rate], [True], []

        return [self.obs], [distance_reward], [False], []

    def reset(self):
        # reset world
        self.game = self.init_game(self.obsticle_moving)
        self.policy_agents = self.game.map.friendly_ships
        self.time = 0
        return self.obs
