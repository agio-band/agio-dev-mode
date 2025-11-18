import logging
import os

from agio.core.plugins.base_service import ServicePlugin, make_action
from agio.tools import launching
from agio.core import api

logger = logging.getLogger(__name__)


class SimplePublisherService(ServicePlugin):
    name = 'dev'

    def execute(self, **kwargs):
        pass

    @make_action(menu_name='task.launcher', app_name='front')
    def open_publisher_dialog(self, *args, task_id: str, **kwargs):
        project_info = self.get_workspace_id(task_id)

        if not project_info['ws_id']:
            raise ValueError(f'Workspace not set for project {project_info["project"]["name"]}')
        cmd_args = [
            'pub',
            *args,
            '--task-id', task_id,
            '--ui',
        ]
        launching.exec_agio_command(
            args=cmd_args,
            workspace=project_info['ws_id'],
            detached=os.name != 'nt',   # fix for windows
            non_blocking=os.name == 'nt',
            new_console=True
        )

    def get_workspace_id(self, task_id: str):
        task = api.track.get_entity(task_id)
        pr = api.track.get_project(task['projectId'])
        return {
            'project': pr,
            'ws_id': pr.get('workspace', {}).get('id') or pr.get('workspaceRevision', {}).get('id')
        }