from isaacsim.robot_motion.motion_generation import ArticulationKinematicsSolver, LulaKinematicsSolver
from isaacsim.core.prims import Articulation
from typing import Optional
from ..global_variables import LIMS_EX_IK_DESCRIPTOR_PATH, LIMS_EX_URDF_PATH

class LIMSExKinematicsSolver(ArticulationKinematicsSolver):
    def __init__(self, robot_articulation: Articulation, end_effector_frame_name: Optional[str] = None) -> None:
        # TODO: change the config path
        # print("초기화 성공 #########################################################")
        self._kinematics = LulaKinematicsSolver(robot_description_path=LIMS_EX_IK_DESCRIPTOR_PATH,
                                                urdf_path=LIMS_EX_URDF_PATH)
        if end_effector_frame_name is None:
            end_effector_frame_name = "gripper"
        ArticulationKinematicsSolver.__init__(self, robot_articulation, self._kinematics, end_effector_frame_name)
        return