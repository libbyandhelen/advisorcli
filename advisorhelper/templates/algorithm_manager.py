import json

import numpy as np
import requests


def deal_with_discrete(feasible_values, current_value):
    diff = np.subtract(feasible_values, current_value)
    diff = np.absolute(diff)
    return feasible_values[np.argmin(diff)]


def deal_with_categorical(feasible_values, one_hot_values):
    index = np.argmax(one_hot_values)
    return feasible_values[index]


class AlgorithmManager:
    def __init__(self, study_id, study_config, X_train, y_train, host, port, url):
        self._study_id = study_id
        self._study_config = json.loads(study_config)

        self._goal = self._study_config["goal"]
        self._max_trails = self._study_config["max_trails"]
        self._dim = 0
        self._lowerbound = []
        self._upperbound = []
        self._types = []
        self._names = []
        # record all the feasible values of discrete type variables
        self._discrete_info = []
        self._categorical_info = []

        self._parse_config()

        self._X_train = json.loads(X_train)
        if len(self._X_train) == 0:
            self._X_train = None
        self._y_train = json.loads(y_train)
        self._parse_metric()

        self._host = host
        self._port = port
        self._url = url
        print(self._X_train)
        print(self._y_train)

    @property
    def study_id(self):
        return self._study_id

    @property
    def study_config(self):
        return self._study_config

    @property
    def goal(self):
        return self._goal

    @property
    def max_trails(self):
        return self._max_trails

    @property
    def dim(self):
        return self._dim

    @property
    def lower_bound(self):
        return self._lowerbound

    @property
    def upper_bound(self):
        return self._upperbound

    @property
    def types(self):
        return self._types

    @property
    def names(self):
        return self._names

    @property
    def discrete_info(self):
        return self._discrete_info

    @property
    def categorical_info(self):
        return self._categorical_info

    @property
    def X_train(self):
        return self._X_train

    @property
    def y_train(self):
        return self._y_train

    def _parse_config(self):
        for param in self._study_config["params"]:
            self._types.append(param["type"])
            self._names.append(param["name"])

            if param["type"] == "DOUBLE" or param["type"] == "INTEGER":
                self._dim = self._dim + 1
                self._lowerbound.append(param["min_value"])
                self._upperbound.append(param["max_value"])
            elif param["type"] == "DISCRETE":
                self._dim = self._dim + 1
                min_value = min(param["discrete_values"])
                max_value = max(param["discrete_values"])
                self._lowerbound.append(min_value)
                self._upperbound.append(max_value)
                self._discrete_info.append(dict({
                    "name": param["name"],
                    "values": param["discrete_values"]
                }))
            # one hot encoding for categorical type
            elif param["type"] == "CATEGORICAL":
                num_feasible = len(param["categorical_values"])
                for i in range(num_feasible):
                    self._lowerbound.append(0)
                    self._upperbound.append(1)
                self._categorical_info.append(dict({
                    "name": param["name"],
                    "values": param["categorical_values"],
                    "number": num_feasible,
                }))
                self._dim = self._dim + num_feasible

                # self.lowerbound = np.array(self.lowerbound)
                # self.upperbound = np.array(self.upperbound)

                # return goal, max_trails, dim, lowerbound, upperbound, types, names, discrete_info, categorical_info

    def _parse_metric(self):
        if len(self._y_train) == 0:
            return None
        y = []
        for metric in self._y_train:
            y.append(metric["value"])

        self._y_train = np.array(y)

    def _parse_x_next(self, x_next):
        counter = 0
        result = []
        for i in range(len(self._types)):
            if self._types[i] == "INTEGER":
                result.append(int(round(x_next[counter], 0)))
                counter = counter + 1
            elif self._types[i] == "DISCRETE":
                for param in self._discrete_info:
                    if param["name"] == self._names[i]:
                        result.append(
                            deal_with_discrete(param["values"], x_next[counter])
                        )
                        counter = counter + 1
                        break
            elif self._types[i] == "CATEGORICAL":
                for param in self._categorical_info:
                    if param["name"] == self._names[i]:
                        result.append(deal_with_categorical(
                            feasible_values=param["values"],
                            one_hot_values=x_next[counter:counter + param["number"]],
                        ))
                        counter = counter + param["number"]
                        break
            elif self._types[i] == "DOUBLE":
                print(counter)
                result.append(x_next[counter])
                counter = counter + 1
        return result

    def _convert_to_dict(self, x_next):
        result = []
        for i in range(len(x_next)):
            tmp = dict({
                "name": self._names[i],
                "value": x_next[i],
            })
            result.append(tmp)
        return result

    def send_result(self, x_next):
        trail = self._parse_x_next(x_next)
        trail = self._convert_to_dict(trail)
        print(x_next)
        print(trail)
        r = requests.post(
            url='http://' + self._host + ':' + str(self._port) + self._url,
            json={
                'study_id': self._study_id,
                'trail': trail,
                'raw_trail': list(x_next),
            }
        )
