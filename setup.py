from setuptools import setup, find_packages


def readme() -> str:
    with open('./README.md') as f:
        return f.read()


setup(
    name='aiokemon',
    packages=find_packages(),
    version='1.0.1',
    description='An asynchronous Python wrapper for making PokéAPI requests',
    long_description=readme(),
    author='Birthday Boy',
    url='https://github.com/bday-boy/aiokemon',
    keywords=['pokemon', 'wrapper', 'RESTAPI'],
    install_requires=[
        'aiohttp',
        'aiohttp-client-cache',
        'aiosqlite'
    ],
    license='MIT License'
)
