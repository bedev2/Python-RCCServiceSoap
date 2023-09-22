# Copyright 2023 LA

from Models.Job import Job
from Models.ScriptExecution import ScriptExecution
from Models.LuaValue import LuaValue

@staticmethod
def _create_job_request(job: Job):
    return {
        'job': {
            'id': job.id,
            'expirationInSeconds': job.expirationInSeconds,
            'category': job.category,
            'cores': job.cores
        }
    }

@staticmethod
def _create_lua_value(arg: LuaValue):
    return {
        'type': arg.type.value,
        'value': str(arg.value),
        'table': [_create_lua_value(t) for t in arg.table] if arg.table else []
    }

@staticmethod
def _create_script_request(script: ScriptExecution):
    return {
        'script': {
            'name': script.name,
            'script': script.script,
            'arguments': { # https://github.com/mvantellingen/python-zeep/issues/145#issuecomment-299317970 this was a PAIN
                'LuaValue': [
                    _create_lua_value(arg) for arg in script.arguments
                ]
            }
        }
    }
