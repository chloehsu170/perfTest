# import time
# from locust import HttpUser, task, between


# class QuickstartUser(HttpUser):
#     wait_time = between(1, 5)

#     @task
#     def hello_world(self):
#         self.client.get("/")
#         # self.client.get("/world")

#     @task(3)
#     def view_items(self):
#         for item_id in range(10):
#             self.client.get(f"/item?id={item_id}", name="/item")
#             time.sleep(1)

#     def on_start(self):
#         self.client.post("/login", json={"username": "foo", "password": "bar"})


import math

from locust import HttpUser, task, constant
from locust import LoadTestShape


class UserA(HttpUser):
    wait_time = constant(600)

    # host = "https://example.com"

    @task
    def get_root(self):
        self.client.get("/", name="UserA")
        # self.client.post("/login", {"username": "test", "password": "1234"})


class UserB(HttpUser):
    wait_time = constant(600)

    # host = "https://example.com"

    @task
    def get_root(self):
        self.client.get("/", name="UserB")


class UserC(HttpUser):
    wait_time = constant(600)

    # host = "https://example.com"

    @task
    def get_root(self):
        self.client.get("/", name="UserC")


# class StepLoadShape(LoadTestShape):
#     step_time = 30
#     step_load = 10
#     spawn_rate = 1
#     time_limit = 300
#
#     def tick(self):
#         run_time = self.get_run_time()
#
#         if run_time > self.time_limit:
#             return None
#
#         current_step = math.floor(run_time / self.step_time) + 1
#         return current_step * self.step_load, self.spawn_rate


class RampUpThenDownLoadShape(LoadTestShape):
    stages = [
        # {"duration": 5, "users": 1, "spawn_rate": 1},
        # {"duration": 35, "users": 30, "spawn_rate": 1},
        # {"duration": 35, "users": 1, "spawn_rate": 1},
        {"duration": 35, "users": 73, "spawn_rate": 16},
        {"duration": 35, "users": 301, "spawn_rate": 16},
        {"duration": 35, "users": 2530, "spawn_rate": 37},
        # {"duration": 10, "users": 145, "spawn_rate": 1},
        # {"duration": 60, "users": 130, "spawn_rate": 0.25},
        {"duration": 15, "users": 50, "spawn_rate": 25},
        {"duration": 20, "users": 1, "spawn_rate": 5},
    ]

    for previous_stage, stage in zip(stages[:-1], stages[1:]):
        stage["duration"] += previous_stage["duration"]

    for previous_stage, stage in zip(stages[:-1], stages[1:]):
        assert stage["duration"] > previous_stage["duration"]

    def tick(self):
        run_time = self.get_run_time()

        for stage in self.stages:
            if run_time < stage["duration"]:
                tick_data = (stage["users"], stage["spawn_rate"])
                return tick_data

        return None
