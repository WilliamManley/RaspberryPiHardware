# focal_stack: capture a focal stack using a Raspberry Pi
# Copyright (C) 2015 Matthew Wincott
# University of Oxford, Oxford, United Kingdom
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#*******************************************************************************
import picamera
import picamera.array
import time
import os
from datetime import datetime

class Camera(picamera.PiCamera):
    """ Custom PiCamera class """
    
    def __init__(self,*args,**kwargs):
        picamera.PiCamera.__init__(self,*args,**kwargs)
        self.setup_camera()
        
        self._start_preview = self.start_preview
    
        
    def setup_camera(self):
        self.resolution = (1024,768)
        
        self.preview_fullscreen = False
        self.preview_window = (0,0,600,400)
        
        self.framerate = 30
        
        time.sleep(2)

    def start_preview(self):
        self.preview_fullscreen = False
        self.preview_window = (0,0,1024,768)
        super(Camera,self).start_preview()
          
    def toggle_preview(self):
        if self.previewing:
            self.stop_preview()
        else:
            self.start_preview()       

    def capture(self,output=None,greyscale=False,**kwargs):
        if not output:
            output = picamera.array.PiRGBArray(self)
            super(Camera,self).capture(output,'rgb')
            array = output.array
            if greyscale:
                array = 0.299*array[:,:,0] + 0.587*array[:,:,1] + 0.114*array[:,:,2]

            return array

        else:
            super(Camera,self).capture(output,**kwargs)

    def timelapse(self,n=10):
        print("Real Timelapse with {} frames".format(n))

        image_dir = os.path.join(os.getcwd(),datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
        os.makedirs(image_dir)
        start = time.time()
        for i in xrange(0,n):
            self.capture(image_dir+"/image-{:03d}.jpg".format(i),use_video_port=True)
        end = time.time()
        dt_real = (end-start)/(n-1)
        print("End timelapse ({:.3f}s = {:.1f}fps )".format(dt_real,1/dt_real))
            

class DummyCamera(picamera.PiCamera):
    """ Custom PiCamera class """
    
    def __init__(self,*args,**kwargs):
        pass
        
    def capture(self,filename):
        print("capture to {}".format(filename))

    def timelapse(self,n=10):
        print("Timelapse with {} frames".format(n))
        start = time.time()
        for i in xrange(0,n):
            self.capture("image-{:03d}.jpg".format(i))
        end = time.time()
        
        print("End timelapse ({}s per image)".format((end-start)/(n-1)))
        
_camera_instance = False
def get_camera():
    try:
        _camera_instance = Camera()
        return _camera_instance
            
    except:
        print("Failed to load camera, creating dummy camera")
        cam = DummyCamera()
        return cam
