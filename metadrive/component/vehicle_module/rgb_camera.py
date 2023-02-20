from metadrive.component.vehicle_module.base_camera import BaseCamera
from metadrive.constants import CamMask
from metadrive.engine.engine_utils import engine_initialized, get_global_config


class RGBCamera(BaseCamera):
    # shape(dim_1, dim_2)
    BUFFER_W = 84  # dim 1
    BUFFER_H = 84  # dim 2
    CAM_MASK = CamMask.RgbCam

    def __init__(self):
        assert engine_initialized(), "You should initialize engine before adding camera to vehicle"
        config = get_global_config()["vehicle_config"]["rgb_camera"]
        self.BUFFER_W, self.BUFFER_H = config[0], config[1]
        super(RGBCamera, self).__init__()
        cam = self.get_cam()
        lens = self.get_lens()
        cam.lookAt(0, 2.4, 1.3)
        cam.setHpr(0, 0.8, 0)
        lens.setFov(160)
        lens.setAspectRatio(1.15)
