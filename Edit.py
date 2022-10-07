import os
import cv2 as cv
from moviepy.editor import vfx, AudioFileClip, CompositeAudioClip, VideoFileClip
import numpy as np
from zipfile import ZipFile
from uuid import uuid4

media_path = os.environ["MEDIA_PATH"]
music_path = os.environ["PROD_ROOT"] + '/music'

class ImageEdit:
    
    def __init__(self, image, number):
        self.image = cv.imread(image)
        self.number = number
        self.file_name = uuid4()
        self.path = f"{media_path}/{self.file_name}"
        self.extention = image.split(".")[-1:][0]
        self.exp_value = 10
        self.con_value = 1.2
        self.top = 5
        self.bottom = 5
        self.left = 5
        self.right = 5
        self.border_color = [255,255,255]
        self.flip_axis = 90
        self.angle = 1
        self.edit_list = ["exposure", "contrast", "border", "rotate"]
        self.noise_list = ["gaussian", "poisson"]
        
    def random_files(self):
        for _ in range(self.number):
            self.get_random()
        self.fileZip()
    
    def get_random(self):
        edit = {"exposure": self.exposure(), "contrast": self.contrast(), "border": self.border(), "rotate": self.rotate()}
        get_edit = np.random.choice(self.edit_list)
        get_noise = np.random.choice(self.noise_list)
        return self.noise(edit[get_edit], get_noise)
        
    def dimentions(self):
        height = self.image.shape[0]
        width = self.image.shape[1]
        return height >=250 and width >= 250
            
    def exposure(self):
        exp = np.random.choice(["bright", "dark"])
        mat = np.ones(self.image.shape,dtype = 'uint8')*self.exp_value
        if exp == "bright":
            image = cv.add(self.image,mat)
        image = cv.subtract(self.image,mat)
        return image

    def contrast(self):
        image_new = self.image * self.con_value
        return image_new

    def border(self):
        if self.dimentions():
            image = cv.copyMakeBorder(self.image, self.top, self.bottom, self.left, self.right, cv.BORDER_CONSTANT, None , value=self.border_color)
            return image

    # def flip(self):
    #     image = cv.flip(self.image, self.flip_axis)
    #     return image

    def rotate(self):
        image_center = tuple(np.array(self.image.shape[1::-1]) / 2)
        rot_mat = cv.getRotationMatrix2D(image_center, self.angle, 1.0)
        result = cv.warpAffine(self.image, rot_mat, self.image.shape[1::-1], flags=cv.INTER_LINEAR)
        return result

    def noise(self, image, noise_type):
        if noise_type == "gaussian":
            row,col,ch= image.shape
            mean = 0
            var = 0.1
            sigma = var**0.5
            gauss = np.random.normal(mean,sigma,(row,col,ch))
            gauss = gauss.reshape(row,col,ch)
            noisy = image + gauss
            return self.save(noisy)
        elif noise_type == "poisson":
            vals = len(np.unique(image))
            vals = 2 ** np.ceil(np.log2(vals))
            noisy = np.random.poisson(image * vals) / float(vals)
            return self.save(noisy)
        # elif noise_type =="speckle":              #Visual difference is noticable
        #     row,col,ch = image.shape
        #     gauss = np.random.normal(0,1,image.size)
        #     gauss = gauss.reshape(row, col, ch).astype('uint8')
        #     noisy = image + gauss
        #     return self.save(noisy)

    def save(self, image):
        if not os.path.isdir(f"{self.path}"):
            os.system(f"mkdir {self.path}")
        path = f"{self.path}/{uuid4()}.{self.extention}"
        cv.imwrite(path, image)

#     def metadata(self):
#         os.system(f"exiftool -all= {self.path}")
#         os.system(f"exiftool {self.path}")

    def fileZip(self):
        for root, dirs, files in os.walk(f"{self.path}"):
            write_file = [write_file for write_file in files if write_file.split(".")[1] != f"{self.extention}_original"]
            with ZipFile(f"{media_path}/{self.file_name}.zip", "w") as zip:
                for file in write_file:
                    zip.write(f"{root}/{file}", arcname=f"{self.file_name}/{file}")
        
    # def hash(self):
    #     with open(f"{self.path}", "rb") as f:
    #         hash = hashlib.sha256(f.read()).hexdigest()
    #         print(hash)

    def __del__(self):
        print("I am being destroyed")


class VideoEdit:
    
    def __init__(self, video, number):
        self.clip = VideoFileClip(video)
        self.number= number
        self.file_name = uuid4()
        self.path = f"{media_path}/{self.file_name}"
        self.extention = video.split(".")[-1:][0]
        self.exp_value = 1.1
        self.speed_value = 1.1
        # self.video_height = 480
        self.resize_value = 0.9
        self.margin_width = 3
        self.color = (255,255,255)
        self.luminosity = 0
        self.contrast_value = 0.1
        self.contrast_thr = 20
        self.edit_list = ["exposure", "speed", "margin", "contrast", "FPS", "crop"]                    #Add new edits to this list
        self.music_list = ["music_1", "music_2", "music_3", "music_4", "music_5", "music_6"]


    def random_files(self):
        for _ in range(self.number):
            self.get_random()
        self.fileZip()

    def get_random(self):
        edit = {"exposure": "self.exposure()", "speed": "self.speed()", "margin": "self.margin()", "contrast": "self.contrast()", "FPS":"self.fps()", "crop":"self.crop()"}
        apply = np.random.choice(self.edit_list)
        eval(edit[apply])
        return self.audio(self.clip)

    def exposure(self):
        self.clip = self.clip.fx(vfx.colorx, self.exp_value)
        return "Exposure"

    def speed(self):
        self.clip = self.clip.fx(vfx.speedx, self.speed_value)
        return "Speed"

    def margin(self):
        self.clip = self.clip.margin(self.margin_width, color=self.color)
        return "Border"
        
    def contrast(self):
        self.clip = self.clip.fx(vfx.lum_contrast, self.luminosity, self.contrast_value, self.contrast_thr)
        return "Contrast"

    def fps(self):
        fps = self.clip.fps
        self.clip = self.clip.set_fps(fps+1)
        return "FPS"

#     def resize(self):                             # causes error for some videos
#         self.clip = self.clip.resize(height = self.resize_value)
#         return "resize"

    def crop(self):
        size=self.clip.size
        [width, height] = size
        self.clip = self.clip.crop(width=width-5, height=height-5)
        return "crop"

    # def invert_green_blue(image):
    #     self.clip = image[:,:,[0,2,1]]

    def audio(self, edit):
        music = np.random.choice(self.music_list)
        video = edit.without_audio()
        audio = AudioFileClip(f"{music_path}/{music}.mp4").subclip(0, video.duration)

        new_audio = CompositeAudioClip([audio])
        video.audio = new_audio
        self.save(video)
    
    def save(self, video):
        if not os.path.isdir(f"{self.path}"):
            os.system(f"mkdir {self.path}")
        path = f"{self.path}/{uuid4()}.{self.extention}"
        video.write_videofile(path)
        
    def fileZip(self):
        for root, dirs, files in os.walk(f"{self.path}"):
            write_file = [write_file for write_file in files if write_file.split(".")[1] != f"{self.extention}_original"]
            with ZipFile(f"{media_path}/{self.file_name}.zip", "w") as zip:
                for file in write_file:
                    zip.write(f"{root}/{file}", arcname=f"{self.file_name}/{file}")

#     def metadata(self):
#         os.system("exiftool -all= " + self.path)
#         os.system("exiftool " + self.path)
        #return "Success!!"

    def __del__(self):
        print("I am being destroyed")
