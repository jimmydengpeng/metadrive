import random

import matplotlib.pyplot as plt
from metadrive.obs.top_down_renderer import draw_top_down_map
from metadrive.envs.scenario_env import ScenarioEnv

if __name__ == '__main__':
    fig, axs = plt.subplots(1, 3, figsize=(10, 10), dpi=1000)
    count = 0
    env = ScenarioEnv(dict(start_scenario_index=0, num_scenarios=3))
    for j in range(3):
        count += 1
        env.reset(force_seed=j)

        # You can access the reference line after the env.reset() is called (specifically, map_manager.reset())
        reference_line = env.engine.map_manager.current_sdc_route
        m = draw_top_down_map(env.current_map, reference_line=reference_line, reference_line_width=4, resolution=(2048, 2048))

        ax = axs[j]
        ax.imshow(m, cmap="bone")
        ax.set_xticks([])
        ax.set_yticks([])
        print("Drawing {}-th map!".format(count))
    # fig.suptitle("Top-down view of generated maps")
    plt.show()
    env.close()
