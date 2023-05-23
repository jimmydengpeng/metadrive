from tqdm import tqdm

from metadrive.engine.asset_loader import AssetLoader
from metadrive.envs.real_data_envs.nuscenes_env import NuScenesEnv
from metadrive.policy.replay_policy import ReplayEgoCarPolicy


def _test_level(level=1, render=False):
    env = NuScenesEnv(
        {
            "use_render": render,
            "agent_policy": ReplayEgoCarPolicy,
            "sequential_seed": True,
            "reactive_traffic": False,
            "window_size": (1600, 900),
            "num_scenarios": 10,
            "horizon": 1000,
            "curriculum_level": level,
            "no_static_vehicles": True,
            "data_directory": AssetLoader.file_path("nuscenes", return_raw_style=False),
        }
    )
    try:
        scenario_id = set()
        for i in tqdm(range(10), desc=str(level)):
            env.reset(force_seed=i)
            for i in range(10):
                o, r, d, _ = env.step([0, 0])
                if d:
                    break

            scenario_id.add(env.engine.data_manager.current_scenario_summary["id"])
        assert len(scenario_id) == int(10 / level)
    finally:
        env.close()


def test_curriculum_seed():
    _test_level(level=5)
    _test_level(level=1)
    _test_level(level=2)
    _test_level(level=3)


def test_curriculum_up_1_level(render=False, level=5):
    env = NuScenesEnv(
        {
            "use_render": render,
            "agent_policy": ReplayEgoCarPolicy,
            "sequential_seed": True,
            "reactive_traffic": False,
            "window_size": (1600, 900),
            "num_scenarios": 10,
            "episodes_to_evaluate_curriculum": 2,
            "horizon": 1000,
            "curriculum_level": level,
            "no_static_vehicles": True,
            "data_directory": AssetLoader.file_path("nuscenes", return_raw_style=False),
        }
    )
    try:
        scenario_id = []
        for i in tqdm(range(10), desc=str(level)):
            env.reset(force_seed=i)
            for i in range(10):
                o, r, d, _ = env.step([0, 0])
            scenario_id.append(env.engine.data_manager.current_scenario_summary["id"])
        assert len(set(scenario_id)) == 4
        ids = [env.engine.data_manager.summary_dict[f]["id"] for f in env.engine.data_manager.summary_lookup]
        assert set(scenario_id) == set(ids[:4])
    finally:
        env.close()


def test_curriculum_level_up(render=False, level=5):
    env = NuScenesEnv(
        {
            "use_render": render,
            "agent_policy": ReplayEgoCarPolicy,
            "sequential_seed": True,
            "reactive_traffic": False,
            "window_size": (1600, 900),
            "num_scenarios": 10,
            "episodes_to_evaluate_curriculum": 2,
            "horizon": 1000,
            "curriculum_level": int(10 / level),
            "no_static_vehicles": True,
            "data_directory": AssetLoader.file_path("nuscenes", return_raw_style=False),
        }
    )
    try:
        scenario_id = []
        for i in tqdm(range(20), desc=str(level)):
            env.reset()
            for i in range(250):
                o, r, d, _ = env.step([0, 0])
            scenario_id.append(env.engine.data_manager.current_scenario_summary["id"])
        assert len(set(scenario_id)) == 10
        ids = [env.engine.data_manager.summary_dict[f]["id"] for f in env.engine.data_manager.summary_lookup]
        assert scenario_id[:10] == ids
        assert scenario_id[-2:] == ids[-2:] == scenario_id[-4:-2]
    finally:
        env.close()


def _worker_env(render, worker_index, level_up=False):
    assert worker_index in [0, 1]
    level = 2
    env = NuScenesEnv(
        {
            "use_render": render,
            "agent_policy": ReplayEgoCarPolicy,
            "sequential_seed": True,
            "reactive_traffic": False,
            "window_size": (1600, 900),
            "num_scenarios": 8,
            "episodes_to_evaluate_curriculum": 4,
            "curriculum_level": level,
            "no_static_vehicles": True,
            "data_directory": AssetLoader.file_path("nuscenes", return_raw_style=False),
            "worker_index": worker_index,
            "num_workers": 2,
        }
    )
    try:
        env.reset()
        if level_up:
            env.engine.curriculum_manager._level_up()
            env.reset()
        scenario_id = []
        for i in range(20):
            env.reset()
            for i in range(10):
                o, r, d, _ = env.step([0, 0])
            scenario_id.append(env.engine.data_manager.current_scenario_summary["id"])
            print(env.current_seed)
        all_scenario = [env.engine.data_manager.summary_dict[f]["id"] for f in env.engine.data_manager.summary_lookup]
        assert len(set(scenario_id)) == 2
        assert env.engine.data_manager.data_coverage == 0.6 if level_up else 0.4
    finally:
        env.close()
    return scenario_id, all_scenario


def test_curriculum_multi_worker(render=False):
    # 1
    all_scenario_id = []
    all_scenario_id.extend(_worker_env(render, 1, level_up=True)[0])
    set_1, all_scenario = _worker_env(render, 0, level_up=True)
    all_scenario_id.extend(set_1)

    ids = all_scenario
    assert set(all_scenario_id) == set(ids[-6:-2])
    # 2
    all_scenario_id = []
    set_1, all_scenario = _worker_env(render, 0)
    all_scenario_id.extend(set_1)
    all_scenario_id.extend(_worker_env(render, 1)[0])

    ids = all_scenario
    assert set(all_scenario_id) == set(ids[:4])


if __name__ == '__main__':
    test_curriculum_multi_worker()
    # test_curriculum_seed()
    # test_curriculum_level_up()
