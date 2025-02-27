from metadrive.envs.metadrive_env import MetaDriveEnv
from metadrive.policy.idm_policy import IDMPolicy
from metadrive.utils import setup_logger

if __name__ == "__main__":
    setup_logger(True)
    env = MetaDriveEnv(
        {
            "num_scenarios": 1,
            "traffic_density": 0,
            "traffic_mode": "trigger",
            "start_seed": 22,
            # "_disable_detector_mask":True,
            # "debug_physics_world": True,
            "global_light": True,
            # "debug_static_world":True,
            "cull_scene": False,
            # "image_observation": True,
            # "controller": "joystick",
            # "manual_control": True,
            "use_render": False,
            "render_mode": "top_down",
            "decision_repeat": 5,
            "need_inverse_traffic": True,
            "rgb_clip": True,
            "debug": False,
            "map": "yBY",
            # "agent_policy": IDMPolicy,
            "random_traffic": False,
            "random_lane_width": True,
            # "random_agent_model": True,
            "driving_reward": 1.0,
            "force_destroy": False,
            "vehicle_config": {
                "enable_reverse": False,
                # "image_source": "depth_camera",
                # "random_color": True
                # "show_lidar": True,
                # "spawn_lane_index":("1r1_0_", "1r1_1_", 0),
                # "destination":"2R1_3_",
                # "show_side_detector": True,
                # "show_lane_line_detector": True,
                # "side_detector": dict(num_lasers=2, distance=50),
                # "lane_line_detector": dict(num_lasers=2, distance=50),
                # # "show_line_to_dest": True,
                # "show_dest_mark": True
            },
        }
    )
    import time
    # [9.95036221 0.99503618]
    start = time.time()
    o, _ = env.reset()
    env.vehicle.set_velocity([1, 0.1], 10)
    # print(env.vehicle.speed)

    for s in range(1, 10000):
        o, r, tm, tc, info = env.step([1, 0.5])
        # print("heading: {} forward_direction: {}".format(env.vehicle.heading, env.vehicle.velocity_direction))

        # env.vehicle.set_velocity([1, 10], 10)
        # # print(env.vehicle.velocity)

        # if s % 100 == 0:
        #     env.close()
        #     env.reset()
        # info["fuel"] = env.vehicle.energy_consumption
        env.render(track_target_vehicle=True)
