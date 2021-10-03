import os

broker_url = os.environ['REDIS_URL']
result_backend = os.environ['REDIS_URL']

broker_transport_options = {
   'max_connections': 20
}

task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']

task_routes = {
    # 'mozio.apps.app-name.tasks.*': {'queue': 'mozio'}
}
