import argparse
import random

from metadrive.constants import HELP_MESSAGE
from metadrive.engine.asset_loader import AssetLoader
from metadrive.envs.real_data_envs.waymo_env import WaymoEnv

import os
import openai

openai.organization = "org-lCw9sPRNt7Cdd1ses124VCsI"
openai.api_key = os.getenv("OPENAI_API_KEY")
l = openai.Model.list()

MODEL = "gpt-3.5-turbo"

# response = openai.ChatCompletion.create(
#     model=MODEL,
#     messages=[
#         {"role": "system", "content": "You are a helpful, pattern-following assistant that translates corporate jargon into plain English."},
#         {"role": "system", "name":"example_user", "content": "New synergies will help drive top-line growth."},
#         {"role": "system", "name": "example_assistant", "content": "Things working well together will increase revenue."},
#         {"role": "system", "name":"example_user", "content": "Let's circle back when we have more bandwidth to touch base on opportunities for increased leverage."},
#         {"role": "system", "name": "example_assistant", "content": "Let's talk later when we're less busy about how to do better."},
#         {"role": "user", "content": "This late pivot means we don't have time to boil the ocean for the client deliverable."},
#     ],
#     temperature=0,
# )
#
# print(response["choices"][0]["message"]["role"])
# print(response["choices"][0]["message"]["content"])
from metadrive.scenario.utils import read_scenario_data

if __name__ == "__main__":
    scenario = read_scenario_data(AssetLoader.file_path(
        "waymo/sd_training.tfrecord-00000-of-01000_2a1e44d405a6833f.pkl", return_raw_style=False
    ))

    scenario2 = read_scenario_data(AssetLoader.file_path(
        "waymo/sd_training.tfrecord-00000-of-01000_8a346109094cd5aa.pkl", return_raw_style=False
    ))


    def get_input_dict(scenario):

        input_dict = {}
        for count, (k, v) in enumerate(scenario["tracks"].items()):
            if count >= 20:
                break

            input_dict[k] = {}

            input_dict[k]["type"] = v["type"]
            input_dict[k]["state"] = {}
            input_dict[k]["state"]["position"] = v["state"]["position"][0].tolist()
            input_dict[k]["state"]["heading"] = v["state"]["heading"][0].tolist()
            input_dict[k]["state"]["velocity"] = v["state"]["velocity"][0].tolist()

        # input_dict = {"tracks": input_dict}

        answer = {
            atype: sum(s["type"] == atype for s in input_dict.values())
            for atype in ['VEHICLE', 'PEDESTRIAN', 'CYCLIST']
        }

        question = ["start"] + ["{}\n{}".format(k, v) for k, v in input_dict.items()] + ["end"]

        return question, answer


    q1, a1 = get_input_dict(scenario)
    q2, a2 = get_input_dict(scenario2)

    promt = "You are a helpful assistant that is capable to read and understand MetaDrive Scenario Description, a nested Python dict object that describe everything in a driving scenario, including the HD map and the states of actors and traffic lights at each time steps. A scenario (an instance of MetaDrive Scenario Description) is a dict whose keys are the name of actors and whose values are a dict describing the state of an actor. The state dict of an actor has two keys: 'type' and 'state'. The 'type' is a string describing the type of the actor in one of those choices: ['VEHICLE', 'PEDESTRIAN', 'CYCLIST']. The `state` is a dict describing the states of the actor with these keys: ['position', 'heading', 'velocity'], where 'position' is a 3-dimensional list describing the x, y, z coordinate of the actor, 'heading' is a radian describing the heading direction of the actor, and the velocity is a 2-dimensional list describing the velocity of the actor projected into x, y coordinates. Due to the token limits, the user will feed the information of each actor to you via separate messages. Each message has two lines, the first line tell you the name of the actor and the second line is the state dict of the actor. You will receive two special messages 'start' and 'end' telling you the user begins to or has finished the input. You need to return a Python dict whose keys are three types of actor and the values are the count of the actor of that type."

    messages = [
                   {
                       "role": "system",
                       "content": promt
                   },
                   {
                       "role": "system",
                       "name": "example_user",
                       "content": promt
                   }
               ] + [
                   {
                       "role": "system",
                       "name": "example_user",
                       "content": str(astate)
                   } for astate in q1
               ] + [
                   {
                       "role": "system",
                       "name": "example_assistant",
                       "content": str(a1)
                   },
                    {
                        "role": "user",
                        "content": promt
                    }
               ] + [
                   {
                       "role": "user",
                       "content": str(astate)
                   } for astate in q2
               ]

    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=messages,
        temperature=0,
    )

    print("===============================================")
    print("PZH: The answer is:", str(a2))
    print("===============================================")
    print(response["choices"][0]["message"]["role"])
    print(response["choices"][0]["message"]["content"])
    print("===============================================")
