# Copyright (c) 2022-2024, NVIDIA CORPORATION. All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto. Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.
#


class ScenarioTemplate:
    def __init__(self):
        pass

    def setup_scenario(self):
        pass

    def teardown_scenario(self):
        pass

    def update_scenario(self):
        pass


import numpy as np
from .ik_solver.lims_ex_ik_solver import LIMSExKinematicsSolver
from .global_variables import *


class ExampleScenario(ScenarioTemplate):
    def __init__(self):
        self._articulation = None

        self._running_scenario = False

        self._time = 0.0  # s

        self._joint_index = 0
        self._max_joint_speed = 4  # rad/sec
        self._lower_joint_limits = None
        self._upper_joint_limits = None

        self._joint_time = 0
        self._path_duration = 0


    def setup_scenario(self, articulation, object_prim):
        self._articulation = articulation
        self.lims_ex_ik_solver = LIMSExKinematicsSolver(self._articulation)

        self._running_scenario = True

    def teardown_scenario(self):
        self._time = 0.0
        self._articulation = None
        self._running_scenario = False

        self._joint_index = 0
        self._lower_joint_limits = None
        self._upper_joint_limits = None

        self._joint_time = 0
        self._path_duration = 0


    def update_scenario(self, step: float):
        if not self._running_scenario:
            return

        self._time += step


