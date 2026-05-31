from setuptools import find_packages, setup

package_name = 'px4_console'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='iskra',
    maintainer_email='iskra42@proton.me',
    description='PX4 command line interface for drone control via ROS 2',
    license='MIT',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'console = px4_console.console:main',
        ],
    },
)
