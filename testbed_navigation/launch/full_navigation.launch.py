from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():

    bringup_dir = get_package_share_directory('testbed_bringup')
    gazebo_dir = get_package_share_directory('testbed_gazebo')
    description_dir = get_package_share_directory('testbed_description')

    nav_dir = get_package_share_directory('testbed_navigation')

    map_file = os.path.join(
        bringup_dir,
        'maps',
        'testbed_world.yaml'
    )

    nav_params = os.path.join(
        nav_dir,
        'config',
        'nav2_params.yaml'
    )

    amcl_params = os.path.join(
        nav_dir,
        'config',
        'amcl_params.yaml'
    )

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                gazebo_dir,
                'launch',
                'spawn_playground.launch.py'
            )
        )
    )

    robot = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                description_dir,
                'launch',
                'robot_description.launch.py'
            )
        )
    )

    map_server = Node(
        package='nav2_map_server',
        executable='map_server',
        name='map_server',
        output='screen',
        parameters=[{
            'yaml_filename': map_file,
            'use_sim_time': True
        }]
    )

    map_lifecycle = Node(
        package='nav2_lifecycle_manager',
        executable='lifecycle_manager',
        name='lifecycle_manager_map',
        output='screen',
        parameters=[{
            'use_sim_time': True,
            'autostart': True,
            'node_names': ['map_server']
        }]
    )

    amcl = Node(
        package='nav2_amcl',
        executable='amcl',
        name='amcl',
        output='screen',
        parameters=[amcl_params]
    )

    localization_lifecycle = Node(
        package='nav2_lifecycle_manager',
        executable='lifecycle_manager',
        name='lifecycle_manager_localization',
        output='screen',
        parameters=[{
            'use_sim_time': True,
            'autostart': True,
            'node_names': ['amcl']
        }]
    )

    planner = Node(
        package='nav2_planner',
        executable='planner_server',
        name='planner_server',
        output='screen',
        parameters=[nav_params]
    )

    controller = Node(
        package='nav2_controller',
        executable='controller_server',
        name='controller_server',
        output='screen',
        parameters=[nav_params]
    )

    bt_navigator = Node(
        package='nav2_bt_navigator',
        executable='bt_navigator',
        name='bt_navigator',
        output='screen',
        parameters=[nav_params]
    )

    behavior = Node(
        package='nav2_behaviors',
        executable='behavior_server',
        name='behavior_server',
        output='screen',
        parameters=[nav_params]
    )

    navigation_lifecycle = Node(
        package='nav2_lifecycle_manager',
        executable='lifecycle_manager',
        name='lifecycle_manager_navigation',
        output='screen',
        parameters=[{
            'use_sim_time': True,
            'autostart': True,
            'node_names': [
                'planner_server',
                'controller_server',
                'bt_navigator',
                'behavior_server'
            ]
        }]
    )

    return LaunchDescription([
        gazebo,
        robot,

        map_server,
        map_lifecycle,

        amcl,
        localization_lifecycle,

        planner,
        controller,
        bt_navigator,
        behavior,
        navigation_lifecycle,
    ])
