from pg_drive.scene_creator.blocks.curve import Curve
from pg_drive.scene_creator.blocks.first_block import FirstBlock
from pg_drive.scene_creator.blocks.intersection import InterSection
from pg_drive.scene_creator.road.road_network import RoadNetwork
from pg_drive.tests.block_test.test_block_base import TestBlock

if __name__ == "__main__":
    test = TestBlock()
    from pg_drive.utils.visualization_loader import VisLoader
    VisLoader.init_loader(test.loader, test.asset_path)

    global_network = RoadNetwork()
    first = FirstBlock(global_network, 3.0, 2, test.render, test.world, 1)

    intersection = InterSection(3, first.get_socket(0), global_network, 1)
    print(intersection.construct_block_in_world(test.render, test.world))

    id = 4
    for socket_idx in range(intersection.SOCKET_NUM):
        block = Curve(id, intersection.get_socket(socket_idx), global_network, id)
        block.construct_block_in_world(test.render, test.world)
        id += 1
    # test.run()
