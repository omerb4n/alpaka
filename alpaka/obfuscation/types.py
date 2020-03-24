import abc
from typing import List


class ScoreSystem(abc.ABC):
    MAXIMUM_SCORE = 1.0
    MINIMUM_SCORE = 0.0

    @abc.abstractmethod
    def _calc_score(self, obj):
        raise NotImplementedError()

    def calc_score(self, obj):
        return max(self.MINIMUM_SCORE, min(self.MAXIMUM_SCORE, self._calc_score(obj)))


class ScoreWeight(ScoreSystem):
    MAXIMUM_WEIGHT = 1.0
    MINIMUM_WEIGHT = 0.0

    def __init__(self, score_system: ScoreSystem, weight: float):
        super(ScoreWeight, self).__init__()
        self._validate_weight(weight)
        self.weight = weight
        self._score_system = score_system

    def _calc_score(self, obj):
        score = self._score_system.calc_score(obj)
        return score * self.weight

    def _validate_weight(self, weight):
        if weight > self.MAXIMUM_WEIGHT or weight < self.MINIMUM_WEIGHT:
            raise ValueError(f"Given weight {weight} is not valid")


class GradeSystem(ScoreSystem):
    def __init__(self, score_weights: List[ScoreWeight] = None, pass_grade: float = ScoreSystem.MINIMUM_SCORE):
        super(GradeSystem, self).__init__()
        if score_weights is None:
            score_weights = []
        else:
            self._validate_score_weights(score_weights)
        self._score_weights = score_weights
        self._pass_grade = pass_grade

    def _calc_score(self, obj):
        total_score = ScoreSystem.MINIMUM_SCORE
        for score_weight in self._score_weights:
            score = score_weight.calc_score(obj)
            total_score += score
        return total_score

    @staticmethod
    def _validate_score_weights(score_weights: List[ScoreWeight]):
        weights = [score_weight.weight for score_weight in score_weights]
        GradeSystem._validate_weights(weights)

    @staticmethod
    def _validate_weights(weights):
        if not sum(weights) == ScoreWeight.MAXIMUM_WEIGHT:
            raise ValueError(f"Given weights {weights} are not valid")

    def did_pass(self, obj):
        return self.calc_score(obj) >= self._pass_grade


class ObfuscationDetector(abc.ABC):
    def is_obfuscated(self, obj) -> bool:
        raise NotImplementedError()
