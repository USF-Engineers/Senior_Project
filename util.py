import json
import time
from twilio.rest import Client

# read account's configuration file
def load_conf_file (acc_name = "Botty"):
	with open ("config.json", "r") as file:
		account = json.load (file)[acc_name]
	return account["account_sid"], account["auth_token"], account["assistant_sid"]

# load account's assistant 
def get_assistant (acc_name = "Botty"):
	account_sid, auth_token, assistant_sid = load_conf_file (acc_name)
	assistant = Client (account_sid, auth_token).autopilot.assistants (assistant_sid)
	return assistant

# read assistant's tasks and samples, and returns a dictionary
def get_tasks (assistant):
	print ("Reading assistant's tasks : " + assistant.fetch ().unique_name)
	tasks = []
	for task in assistant.tasks.list ():
		unique_name = task.unique_name
		samples = [sample.tagged_text for sample in task.samples.list ()]
		if len (samples) > 0:
			tasks.append ({"task_name" : unique_name, "samples" : samples})
	return tasks

# delete all queries 
def clear_queries (assistant):
	print ("Deleting all queries")
	for query in assistant.queries.list ():
		query.delete ()

# delete all models
def clear_models (assistant):
	print ("Deleting all models")
	for model in assistant.model_builds.list ():
		model.delete ()

# create new model
def create_model (assistant, unique_name = "model_v1.0"):
	print (f"Creating new model : {unique_name}")
	model = assistant.model_builds.create (unique_name = unique_name)
	time.sleep (5)
	return model

# load json object
def load_json (filename):
	with open (filename, "r") as file:
		return json.load (file)

# save json object
def save_json (json_obj, filename):
	print ("Saving " + filename)
	with open (filename, "w") as file:
		json.dump (json_obj, file, indent = 4)

# remove duplicates samples in each task
def remove_duplicates (assistant):
	print ("Eliminating duplicate samples")
	for task in assistant.tasks.list ():
		samples = []
		for sample in task.samples.list ():
			tagged_text = sample.tagged_text.lower ()
			if tagged_text in samples:
				print ("deleting duplicate sample " + tagged_text)
				sample.delete ()
			else:
				samples.append (tagged_text)

# check the number of samples of each task >= 10
def check_tasks (assistant):
	print ("Checking tasks samples")
	for task in assistant.tasks.list ():
		samples = task.samples.list ()
		if len (samples) < 10:
			print (f"Task {task.unique_name} has only {len(samples)} samples")

# upload and reset assistant's tasks
def upload_tasks (assistant, tasks):
	# clear all tasks first
	print ("Deleting all tasks")
	for task in assistant.tasks.list ():
		for sample in task.samples.list ():
			sample.delete ()
		task.delete ()
	print ("Uploading tasks")
	for t in tasks:
		task = assistant.tasks.create (unique_name = t["task_name"])
		for s in t["samples"]:
			task.samples.create (language="en-US", tagged_text=s)

# create new query
def send_query (assistant, query):
	return assistant.queries.create (language = "en-US", query = query)

# test samples
def test (assistant, tasks):
	print ("Testing")
	miss = []
	for task in tasks:
		task_name = task["task_name"]
		samples = task["samples"]
		for sample in samples:
			query = send_query (assistant, sample)
			routed_task_name  = query.results["task"]
			if routed_task_name != task_name:
				miss.append ({"sample" : sample, "task_name" : task_name, "routed_task_name" : routed_task_name})
			else:
				query.delete ()		
	return miss