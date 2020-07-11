import abc
import copy


class Mutator():
    @abc.abstractmethod
    def id(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def mutate(self, param_map: dict, obj: object):
        raise NotImplementedError()


class Tester():
    @abc.abstractmethod
    def id(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def test(self, param_map: dict, obj: object):
        raise NotImplementedError()


class MutatorInfo():
    mutator: Mutator
    param_map: dict


class TesterInfo():
    tester: Tester
    param_map: dict


class Node():
    mutator_info: MutatorInfo
    tester_info_list: list[TesterInfo]
    children: list

    def consume(self, obj: object):
        # do mutation
        mutator = self.mutator_info.mutator
        mutator_param_map = self.mutator_info.param_map
        mutated_obj = mutator.mutate(mutator_param_map, obj)

        # run tests
        for tester_info in self.tester_info_list:
            obj_copy = copy.deepcopy(mutated_obj)
            tester = tester_info.tester
            tester_param_map = tester_info.param_map
            tester.test(tester_param_map, obj_copy)

        # run child nodes
        for child_node in self.children:
            child_node: Node
            obj_copy = copy.deepcopy(mutated_obj)
            child_node.consume(obj_copy)
