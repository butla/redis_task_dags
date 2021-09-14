# redis_task_dags
A simple runner for task DAGs based on Redis.

Currently, a very early work in progress :) I'm just fiddling with the idea.
Maybe it'll go into `rq`, maybe it'll be a separate project.

I want to leverage as much of the built-in Redis functionality, to have as little as possible Python code.
Maybe that way, this can be a base for task DAGs implementation in many languages.

I have different issues with the current task runners for Python:

- rq: doesn't support DAGs of tasks
- celery: buggy, convoluted
- Airflow - really unflexible (why can't I just define and run DAGs from code?), needlessly heavyweight
