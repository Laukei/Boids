
def sign(x):
    '''
    Returns the sign of x (+1 or -1)
    :param x: value
    :return: {-1,+1}
    '''
    if x >= 0:
        return +1
    elif x < 0:
        return -1
    else:
        raise ValueError(x)


class BaseLogic:
    def __init__(self):
        pass


class Priority(BaseLogic):
    def __init__(self,allowed_change):
        self.allowed_change = allowed_change

    def from_recommendations(self,recommendations):
        change = 0
        allowed_change_remaining = self.allowed_change
        recommendations = sorted(recommendations, key=lambda l: l[0], reverse=True)
        for severity, recommendation in recommendations:
            if recommendation != 0 and allowed_change_remaining > 0:
                if abs(recommendation) > allowed_change_remaining:
                    change += sign(recommendation) * allowed_change_remaining
                    break
                else:
                    change += recommendation
                    allowed_change_remaining -= abs(recommendation)
        return change