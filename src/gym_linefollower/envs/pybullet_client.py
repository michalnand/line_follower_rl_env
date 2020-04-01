import functools
import inspect
import pybullet
import time

class PybulletClient():
    """A wrapper for pybullet to manage different clients."""

    def __init__(self, connection_mode=pybullet.DIRECT):
        
        time.sleep(0.5)
        self._client = pybullet.connect(connection_mode)
        time.sleep(0.5)
        self._shapes = {}

      


    def __del__(self):
        """Clean up connection if not already done."""
        try:
            pybullet.disconnect(physicsClientId=self._client)
        except pybullet.error:
            pass

    def __getattr__(self, name):
        """Inject the client id into Bullet functions."""
        attribute = getattr(pybullet, name)
        if inspect.isbuiltin(attribute):
            attribute = functools.partial(attribute, physicsClientId=self._client)
        return attribute
