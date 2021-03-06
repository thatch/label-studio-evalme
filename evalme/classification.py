from evalme.eval_item import EvalItem


class ClassificationEvalItem(EvalItem):

    SHAPE_KEY = 'undefined'

    def exact_match(self, item, label_weights=None):
        label_weights = label_weights or {}
        if self.empty and item.empty:
            return 1
        if self.empty ^ item.empty:
            return 0
        if len(self) != len(item):
            return 0
        total_weight, n = 0, 0
        for x, y in zip(self.get_values_iter(), item.get_values_iter()):
            if x[self._shape_key] != y[self._shape_key]:
                return 0
            weight = sum(label_weights.get(l, 1) for l in x[self._shape_key])
            total_weight += weight
            n += len(x[self._shape_key])
        if n == 0:
            return 0
        return total_weight / n


class ChoicesEvalItem(ClassificationEvalItem):
    SHAPE_KEY = 'choices'


class PairwiseEvalItem(ClassificationEvalItem):
    SHAPE_KEY = 'pairwise'


def _as_choices(item):
    if not isinstance(item, ChoicesEvalItem):
        return ChoicesEvalItem(item)
    return item


def _as_pairwise(item):
    if not isinstance(item, PairwiseEvalItem):
        return PairwiseEvalItem(item)
    return item


def exact_matching_choices(item_gt, item_pred, label_weights=None):
    return _as_choices(item_gt).exact_match(_as_choices(item_pred), label_weights)


def exact_matching_pairwise(item_gt, item_pred, label_weights=None):
    return _as_pairwise(item_gt).exact_match(_as_pairwise(item_pred), label_weights)
