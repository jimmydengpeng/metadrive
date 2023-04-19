from setuptools import setup
from glob import glob

package_name = 'test_bridge'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, glob('launch/*.launch.py'))
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='liuzhi',
    maintainer_email='candyboear@gmail.com',
    description='ros2 bridge for metadrive',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'camera_bridge = test_bridge.camera_bridge:main',
            'lidar_bridge = test_bridge.lidar_bridge:main'
        ],
    },
)
