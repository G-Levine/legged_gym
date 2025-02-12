# SPDX-FileCopyrightText: Copyright (c) 2021 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# Copyright (c) 2021 ETH Zurich, Nikita Rudin

from legged_gym.envs.base.legged_robot_config import LeggedRobotCfg, LeggedRobotCfgPPO

LEG_KP = 40.0
LEG_KD = 4.0
WHEEL_KD = 0.5

class RheaRoughCfg( LeggedRobotCfg ):
    class env:
        num_envs = 4096
        num_observations = 30
        num_privileged_obs = None # if not None a priviledge_obs_buf will be returned by step() (critic obs for assymetric training). None is returned otherwise 
        num_actions = 6
        env_spacing = 3.  # not used with heightfields/trimeshes 
        send_timeouts = True # send time out information to the algorithm
        episode_length_s = 20 # episode length in seconds
    class init_state( LeggedRobotCfg.init_state ):
        pos = [0.0, 0.0, 0.5] # x,y,z [m]
        default_joint_angles = { # = target angles [rad] when action = 0.0
            'left_hip': 0.75,
            'left_knee': -1.5,
            'left_wheel': 0.0,  # [rad]
            'right_hip': -0.75,
            'right_knee': 1.5,
            'right_wheel': 0.0,  # [rad]
        }

    class terrain( LeggedRobotCfg.terrain ):
        # mesh_type = 'plane'
        mesh_type = 'trimesh'
        curriculum = True
        # horizontal_scale = 0.05 # [m]
        # vertical_scale = 0.0025 # [m]
        # max_init_terrain_level = 0
        # measure_heights = True
        # measured_points_x = []
        # measured_points_y = []
        # terrain types: [smooth slope, rough slope, stairs up, stairs down, discrete]
        # terrain_proportions = [0.5, 0.5, 0, 0, 0]
        # terrain_proportions = [0, 1.0, 0, 0, 0]
        # terrain_proportions = [1.0, 0, 0, 0, 0]
        # terrain_proportions = [0.3, 0.3, 0, 0, 0.4]
        terrain_proportions = [0, 0, 0, 0, 1.0]
        # terrain_length = 4.
        # terrain_width = 4.
        slope_treshold = 100.0
        # Intentionally set friction to 0 so it only uses the wheel friction
        static_friction = 0.0
        dynamic_friction = 0.0

    class control( LeggedRobotCfg.control ):
        # PD Drive parameters:
        control_type = 'V'
        stiffness = {
            'left_hip': LEG_KP,
            'left_knee': LEG_KP,
            'left_wheel': WHEEL_KD,
            'right_hip': LEG_KP, 
            'right_knee': LEG_KP, 
            'right_wheel': WHEEL_KD,
        } # [N*m/rad]
        damping = {
            'left_hip': LEG_KD,
            'left_knee': LEG_KD,
            'left_wheel': 0.0,
            'right_hip': LEG_KD, 
            'right_knee': LEG_KD, 
            'right_wheel': 0.0,
        }     # [N*m*s/rad]
        # action scale: target angle = actionScale * action + defaultAngle
        action_scale = 1.0
        # decimation: Number of control action updates @ sim DT per policy DT
        decimation = 4
        # delay_range: Range for randomly sampling number of sim DT delay steps for policy actions
        delay_range = [1, 2]
        joint_control_types = {
            'left_hip': 'P', 
            'left_knee': 'P', 
            'left_wheel': 'V',
            'right_hip': 'P', 
            'right_knee': 'P', 
            'right_wheel': 'V',
        }
        action_scales = {
            'left_hip': 1.0,
            'left_knee': 1.0,
            'left_wheel': 10.0,
            'right_hip': 1.0,
            'right_knee': 1.0,
            'right_wheel': 10.0,
        }
        joint_friction = 0.1

    class asset( LeggedRobotCfg.asset ):
        file = '{LEGGED_GYM_ROOT_DIR}/resources/robots/rhea/urdf/rhea.urdf'
        name = "rhea"
        foot_name = "wheel"
        penalize_contacts_on = ["left_hip", "left_knee", "right_hip", "right_knee"]
        terminate_after_contacts_on = ["base_link"]
        # self_collisions = 1 # 1 to disable, 0 to enable...bitwise filter
        replace_cylinder_with_capsule = False
  
    class rewards( LeggedRobotCfg.rewards ):
    #     # soft_dof_pos_limit = 0.9
        # only_positive_rewards = False
        # base_height_target = 0.5
    #     only_positive_rewards = True # if true negative total rewards are clipped at zero (avoids early termination problems)
        class scales( LeggedRobotCfg.rewards.scales ):
            # no_fly = 0.1
            # stand_still = -1.0
            # alive = 1.0
            # termination = -200.
            # tracking_lin_vel = 1.0
            # tracking_ang_vel = 0.5
            # torques = -1.e-3
    #         dof_acc = -2.e-7
            # lin_vel_z = -0.1
            feet_air_time = 0.
            # orientation = -1.0
            # action_rate = -0.01
            # base_height = -1.0
            symmetry = -0.1
    #         # dof_pos_limits = -1.
    #         dof_vel = -2.e-6
    #         # ang_vel_xy = -0.0
    #         # feet_contact_forces = -0.
    #         # action_rate = -0.01

    class commands( LeggedRobotCfg.commands ):
        num_commands = 4# default: lin_vel_x, lin_vel_y, ang_vel_yaw, heading (in heading mode ang_vel_yaw is recomputed from heading error)
        resampling_time = 10. # time before command are changed[s]
        heading_command = True
        deadband = 0.1
        class ranges:
            # lin_vel_x = [-1.0, 1.0] # min max [m/s]
            lin_vel_x = [-0.5, 0.5] # min max [m/s]
            # lin_vel_x = [0.0, 0.0] # min max [m/s]
            lin_vel_y = [0.0, 0.0]   # min max [m/s]
            # ang_vel_yaw  = [-0.5, 0.5]    # min max [rad/s]
            ang_vel_yaw  =[1.0, 1.0]    # min max [rad/s]
            heading = [-3.14, 3.14]

    class noise:
        add_noise = True
        noise_level = 1.0 # scales other values
        class noise_scales:
            dof_pos = 0.01
            dof_vel = 0.1
            lin_vel = 0.1
            ang_vel = 0.2
            gravity = 0.05
            height_measurements = 0.1

    class domain_rand( LeggedRobotCfg.domain_rand ):
        randomize_friction = True
        friction_range = [0.75, 1.25]
        randomize_base_mass = True
        added_mass_range = [-0.25, 0.25]
        randomize_base_com = True
        added_com_range_x = [-0.01, 0.01]
        added_com_range_y = [-0.01, 0.01]
        added_com_range_z = [-0.01, 0.01]
        randomize_gripper_mass = False
        push_robots = False
        push_interval_s = 15
        max_push_vel_xy = 0.1

    # class sim:
    #     dt =  0.005
        # substeps = 1
        # gravity = [0., 0. ,-9.81]  # [m/s^2]
        # up_axis = 1  # 0 is y, 1 is z

        # class physx:
        #     num_threads = 10
        #     solver_type = 1  # 0: pgs, 1: tgs
        #     num_position_iterations = 4
        #     num_velocity_iterations = 0
        #     contact_offset = 0.01  # [m]
        #     rest_offset = 0.0   # [m]
        #     bounce_threshold_velocity = 0.5 #0.5 [m/s]
        #     max_depenetration_velocity = 1.0
        #     max_gpu_contact_pairs = 2**23 #2**24 -> needed for 8000 envs and more
        #     default_buffer_size_multiplier = 5
        #     contact_collection = 2 # 0: never, 1: last sub-step, 2: all sub-steps (default=2)

class RheaRoughCfgPPO( LeggedRobotCfgPPO ):
    class policy( LeggedRobotCfgPPO.policy ):
        # actor_hidden_dims = [256, 128]
        # critic_hidden_dims = [256, 128]
        rnn_type = 'lstm'
        rnn_hidden_size = 512
        rnn_num_layers = 1
    class algorithm( LeggedRobotCfgPPO.algorithm ):
        entropy_coef = 0.01
    class runner( LeggedRobotCfgPPO.runner ):
        policy_class_name = 'ActorCriticRecurrent'
        run_name = ''
        experiment_name = 'rough_rhea'