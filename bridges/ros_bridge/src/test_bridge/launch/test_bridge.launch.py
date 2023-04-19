from launch import LaunchDescription
from launch_ros.actions import Node
 
def generate_launch_description():
    ld = LaunchDescription()
    camera_node = Node(
        package="test_bridge",
        executable="camera_bridge",
        name='camera_bridge'
    )
    ld.add_action(camera_node)
    lidar_node = Node(
        package="test_bridge",
        executable="lidar_bridge",
        name='lidar_bridge'
    )
    ld.add_action(lidar_node)

    rviz_node = Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2'
    )
    ld.add_action(rviz_node)
    return ld


if __name__ == '__main__':
    generate_launch_description()
