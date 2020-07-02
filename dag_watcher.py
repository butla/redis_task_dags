import asyncio
import contextvars
import string

import aioredis


redis_client: contextvars.ContextVar[aioredis.Redis] = contextvars.ContextVar('redis')

A, B, C, D, E, F, G, H = string.ascii_uppercase[:8]
nodes = [A, B, C, D, E, F, G, H]


async def create_dag():
    redis = redis_client.get()

    async def write_dependencies():
        dependency_sets = {
            A: set(),
            B: {A},
            C: {A},
            D: {B, C},
            E: {D},
            F: {D},
            G: {D},
            H: {F, G},
        }

        for node, dependencies in dependency_sets.items():
            for dependent_node in dependencies:
                await redis.rpush(_dependencies_list_name(node), dependent_node)
        print("Written graph dependencies")

    async def write_successors():
        succesor_sets = {
            A: {B, C},
            B: {D},
            C: {D},
            D: {E, F, G},
            E: set(),
            F: {H},
            G: {H},
        }

        for node, successors in succesor_sets.items():
            for successor in successors:
                await redis.rpush(_successors_list_name(node), successor)
        print("Written graph succesors")

    await write_dependencies()
    await write_successors()


def _dependencies_list_name(node_name: str) -> str:
    return f'dependencies-{node_name}'


def _successors_list_name(node_name: str) -> str:
    return f'successors-{node_name}'


async def dump_dag():
    # TODO would be nice to view this in D3 JS
    redis = redis_client.get()

    node_lists = [
        ('Dependencies', _dependencies_list_name),
        ('Successors', _successors_list_name),
    ]

    for list_name, list_name_for_node in node_lists:
        print(f'\n{list_name}')
        print('============')
        for node in nodes:
            connected_nodes_encoded = await redis.lrange(list_name_for_node(node), 0, -1)
            connected_nodes = (dep.decode() for dep in connected_nodes_encoded)
            print(node, ':', ' '.join(connected_nodes))


async def iterate_dag():
    print()
    print('TODO run the next task without dependencies - do that with lua through a redis queue, or a log')
    print('TODO update dependencies list - remove executed tasks, remove dependencies for successors')


async def main():
    await setup()

    await create_dag()
    await dump_dag()
    await iterate_dag()

    await teardown()


async def setup():
    redis = await aioredis.create_redis_pool('redis://localhost')
    await redis.flushall()
    redis_client.set(redis)


async def teardown():
    redis_client.get().close()
    await redis_client.get().wait_closed()

if __name__ == '__main__':
    asyncio.run(main())
