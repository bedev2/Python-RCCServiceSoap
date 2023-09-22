from RCCServiceSoap import * # [WARNING] Importing everything is important!
from GridServiceUtils import GridServiceUtils
from Lua import *

def print_result(msg, result):
    print(f"{msg}: {result}")

def create_job(job_id, expiration, category, cores):
    """Creates a new Job"""
    return Job(job_id, expiration, category, cores)

def create_lua_script(name, code, *args):
    """Creates a new Lua script"""
    return Lua.NewScript(name, code, Lua.new_args(*args))

# NOTE: Lua.GetValues Will return an Python array which contains the LuaValue(s) returned from the script. You don't need to parse them like this you can just store the result to a variable and do result[0] for the first value returned
def parse_job_response(result: ArrayOfLuaValue):
    for i, arg_value in enumerate(Lua.GetValues(result), 1): 
        print_result(f"Argument{i}", arg_value)
    
client = GridServiceUtils.GetService("127.0.0.1", 64000, 50)

# Example #1: Hello World
hello_world_response = client.HelloWorld()
print_result("Hello World Result", hello_world_response.HelloWorldResult)

# Example #2: RCC Version
get_version_response = client.GetVersion()
print_result("RCC Version", get_version_response.GetVersionResult)

# Example #3: Job creation and Lua script creation with arguments
job = create_job("this-is-my-job-id", 20, 0, 0)
lua_script = create_lua_script("HelloWorldScriptName", '''
local argument1, argument2, argument3 = ...

print("Hello from example.py", argument1, argument2, argument3)

-- return the arguments we passed to script
return argument1, argument2, argument3
''', "hello world", False, 123)

# Example #4: Open Job & Parse value(s) returned
open_job = client.OpenJob(job, lua_script)
parse_job_response(open_job.OpenJobExResult)

# Example #5: Batch Job & Parse value(s) returned
# batch_job = client.BatchJob(job, lua_script)
# parse_job_response(batch_job.BatchJobExResult) # Literally just Open Job but Batch Job is meant for Job(s) which have a short lifetime

# ^^ commented out to stop job already existing error but it's just like open_job and will work fine as long as a job with the id doesnt already exist.

# Example #6: Renew Lease
renew_lease = client.RenewLease(job.id, job.expirationInSeconds + 5) # add 5 seconds onto the current expiration
print_result("New Job Expiration Is", renew_lease.RenewLeaseResult) # whatttttt it returns 0.0 maybe im wrong i swear this was the new expiration maybe it is different on certain rcc(s) either way this does still change expiration fine!

# Example #7: Execute
execute = client.Execute(job.id, create_lua_script("some-new-script", "print('hello again job')")) # Similar to Batch Job & Open Job but this is meant for Job(s) that are currently running
if execute.ExecuteExResult is not None:
    parse_job_response(execute.ExecuteExResult) # When we do something like print we don't need to parse the job result as it is None so if you have a script which does a lot of things it is safe to do this check before attempting to parse it

# Example #8: Get Expiration
get_expiration = client.GetExpiration(job.id)
print_result("Job Expiration Is", get_expiration.GetExpirationResult)

# Example #9: Diag; Diag is obvious by the name if you don't already know what it is it's used for diagnostics!
diag = client.Diag(0, job.id) # Diag takes an int argument called 'Type': 0 = Diagnostics Data, 1 = Leak Dump, 2 = Attempts to allocate 500k and returns True if successful else False, 4 = DataModel dutyCycles
parse_job_response(diag.DiagExResult) # yes diag is an array of lua values, NOTE: some of the tables in diag are nested if you even ever use diag i suggest you take this into note

# This is about it everything else should be easy


client.CloseAllJobs()