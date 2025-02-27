from metadrive.component.map.base_map import BaseMap
from metadrive.component.map.pg_map import MapGenerateMethod
from metadrive.envs.metadrive_env import MetaDriveEnv

if __name__ == "__main__":
    env = MetaDriveEnv(
        {
            "num_scenarios": 1,
            "traffic_density": 0.1,
            "start_seed": 4,
            "manual_control": True,
            "use_render": True,
            "image_observation": True,
            "rgb_clip": True,
            "vehicle_config": dict(depth_camera=(200, 88, False), image_source="depth_camera"),
            "map_config": {
                BaseMap.GENERATE_TYPE: MapGenerateMethod.BIG_BLOCK_NUM,
                BaseMap.GENERATE_CONFIG: 12,
                BaseMap.LANE_WIDTH: 3.5,
                BaseMap.LANE_NUM: 3,
            }
        }
    )
    env.reset()
    env.engine.accept("m", env.vehicle.get_camera("depth_camera").save_image, extraArgs=[env.vehicle, "debug.jpg"])

    for i in range(1, 100000):
        o, r, tm, tc, info = env.step([0, 1])
        assert env.observation_space.contains(o)
        if env.config["use_render"]:
            # for i in range(ImageObservation.STACK_SIZE):
            #     ObservationType.show_gray_scale_array(o["image"][:, :, i])
            env.render(text={"can you see me": i})
        if tm or tc:
            env.vehicle.get_camera("rgb_camera").save_image(env.vehicle)
            # print("Reset")
            env.reset()
    env.close()
