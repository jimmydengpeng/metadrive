import json
import numpy as np
from scipy.spatial.transform import Rotation as R

from metadrive.component.vehicle_module.base_camera import BaseCamera
from metadrive.constants import CamMask
from metadrive.engine.engine_utils import engine_initialized, get_global_config
from direct.filter.CommonFilters import CommonFilters


class RGBCamera(BaseCamera):
    # shape(dim_1, dim_2)
    BUFFER_W = 84  # dim 1
    BUFFER_H = 84  # dim 2
    CAM_MASK = CamMask.RgbCam
    PBR_ADAPT = False

    def __init__(self):
        assert engine_initialized(), "You should initialize engine before adding camera to vehicle"
        config = get_global_config()["vehicle_config"]["rgb_camera_config"]
        cuda = True if get_global_config()["vehicle_config"]["image_source"] == "rgb_camera" else False
        if type(config) == tuple:   # compatible with the original config format
            self.BUFFER_W, self.BUFFER_H = config[0], config[1]
            super(RGBCamera, self).__init__(True, cuda)
            cam = self.get_cam()
            lens = self.get_lens()
            cam.lookAt(2.4, 0, 0.0)
            lens.setFov(60)
            lens.setAspectRatio(config[0]/config[1])
        elif type(config)==str:
            with open(config, "r") as f:
                config = json.load(f)
            H, W, F = config["height"], config["width"], config["focal_length"]
            self.BUFFER_W, self.BUFFER_H = W, H
            super(RGBCamera, self).__init__(True, cuda)
            cam = self.get_cam()
            lens = self.get_lens()
            type(self)._singleton.origin.setPos(config["x"], config["y"], config["z"])
            roll, pitch, yaw = map(np.rad2deg, [config["roll"], config["pitch"], config["yaw"]])
            yaw = yaw - 90 # since the default viewing direction for cameras is the y-axis in Panda3D 
            cam.setHpr(yaw, pitch, roll)
            fov = np.rad2deg(2*np.arctan2(W, 2*F))
            lens.setFov(fov)
            lens.setAspectRatio(W/H)
        else:
            raise TypeError("rgb_camera config type is not defined")
