from typing import Tuple, Sequence
from panda3d.core import LVector3
from metadrive.base_class.base_object import BaseObject

LaneIndex = Tuple[str, str, int]


class BaseTrafficParticipant(BaseObject):
    NAME = None
    COLLISION_GROUP = None

    def __init__(self, position: Sequence[float], heading_theta: float = 0., random_seed=None):
        super(BaseTrafficParticipant, self).__init__(random_seed=random_seed)
        self.set_position(position, self.HEIGHT / 2 if hasattr(self, "HEIGHT") else 0)
        self.set_heading_theta(heading_theta)
        assert self.MASS is not None, "No mass for {}".format(self.class_name)
        assert self.NAME is not None, "No name for {}".format(self.class_name)
        assert self.COLLISION_GROUP is not None, "No collision group for {}".format(self.class_name)

    def top_down_color(self):
        raise NotImplementedError(
            "Implement this func for rendering class {} in top down renderer".format(self.class_name)
        )

    def set_roll(self, roll):
        self.origin.setP(roll)

    def set_pitch(self, pitch):
        self.origin.setR(pitch)

    @property
    def roll(self):
        return self.origin.getP()

    @property
    def pitch(self):
        return self.origin.getR()

    def add_body(self, physics_body):
        super(BaseTrafficParticipant, self).add_body(physics_body)
        self._body.set_friction(0.)
        self._body.set_anisotropic_friction(LVector3(0., 0., 0.))
