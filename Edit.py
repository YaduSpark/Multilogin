import os
import cv2 as cv
from moviepy.editor import vfx, AudioFileClip, CompositeAudioClip, VideoFileClip
import numpy as np
from zipfile import ZipFile
from uuid import uuid4
from dotenv import load_dotenv

load_dotenv()
media_path = os.environ["MEDIA_PATH"]
music_path = os.environ["PROD_ROOT"] + 'music'


class ImageEdit:

    exp_value = 10
    con_value = 1.2
    top = 5
    bottom = 5
    left = 5
    right = 5
    border_color = [255,255,255]
    flip_axis = 90
    angle = 1
    edit_list = ["exposure", "contrast", "border", "rotate"]
    noise_list = ["gaussian", "poisson"]
    
    def __init__(self, image):
        self.image_path = image
        self.file_name = uuid4()
        self.path = f"{media_path}/{self.file_name}"
        self.extension = image.split(".")[-1:][0]
        
    # def random_files(self):
    #     # for _ in range(self.number):
    #     self.get_random()
    #     return self.path

    @property
    def image(self):
        return cv.imread(self.image_path)
    
    def get_random(self):
        edit = {"exposure": self.exposure(), "contrast": self.contrast(), "border": self.border(), "rotate": self.rotate()}
        get_edit = np.random.choice(self.edit_list)
        get_noise = np.random.choice(self.noise_list)
        print('get_edit: ', get_edit)
        print('get_noise: ', get_noise)
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
        path = f"{self.path}/{uuid4()}.{self.extension}"
        cv.imwrite(path, image)
        self.metadata()

    def metadata(self):
        os.system(f"exiftool -all= {self.path}")
        # os.system(f"exiftool {self.path}")
        return 'Success'

    # def fileZip(self):
    #     for root, dirs, files in os.walk(f"{self.path}"):
    #         write_file = [write_file for write_file in files if write_file.split(".")[1] != f"{self.extension}_original"]
    #         with ZipFile(f"{media_path}/{self.file_name}.zip", "w") as zip:
    #             for file in write_file:
    #                 zip.write(f"{root}/{file}", arcname=f"{self.file_name}/{file}")
        
    # def hash(self):
    #     with open(f"{self.path}", "rb") as f:
    #         hash = hashlib.sha256(f.read()).hexdigest()
    #         print(hash)

    # def __del__(self):
    #     os.system(f"rm -r {self.path}")
    #     print("I am being destroyed")
    #     os.system(f"rm -rf {self.path}")


class VideoEdit:

    exp_value = 1.1
    speed_value = 1.1
    # video_height = 480
    resize_value = 0.9
    margin_width = 3
    color = (255,255,255)
    luminosity = 0
    contrast_value = 0.1
    contrast_thr = 20
    
    edit_list = ["exposure", "speed", "margin", "contrast", "FPS", "crop"]                    #Add new edits to this list
    music_list = ["music_1", "music_2", "music_3", "music_4", "music_5", "music_6"]
    
    def __init__(self, video):
        self.video = video
        self.file_name = uuid4()
        self.path = f"{media_path}/{self.file_name}"
        self.extension = video.split(".")[-1:][0]


    # def random_files(self):
    #     for _ in range(self.number):
    #         self.get_random()
    #     return self.path

    @property
    def clip(self):
        return VideoFileClip(self.video)

    def get_random(self):
        edit = {"exposure": "self.exposure()", "speed": "self.speed()", "margin": "self.margin()", "contrast": "self.contrast()", "FPS":"self.fps()", "crop":"self.crop()"}
        apply = np.random.choice(self.edit_list)
        return self.audio(eval(edit[apply]))

    def exposure(self):
        video = self.clip.fx(vfx.colorx, self.exp_value)
        return video

    def speed(self):
        video = self.clip.fx(vfx.speedx, self.speed_value)
        return video

    def margin(self):
        video = self.clip.margin(self.margin_width, color=self.color)
        return video
        
    def contrast(self):
        video = self.clip.fx(vfx.lum_contrast, self.luminosity, self.contrast_value, self.contrast_thr)
        return video

    def fps(self):
        fps = self.clip.fps
        video = self.clip.set_fps(fps+1)
        return video

#     def resize(self):                             # causes error for some videos
#         video = self.clip.resize(height = self.resize_value)
#         return video

    def crop(self):
        size=self.clip.size
        [width, height] = size
        video = self.clip.crop(width=width-5, height=height-5)
        return video

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
        path = f"{self.path}/{uuid4()}.{self.extension}"
        temp_filepath = f"{media_path}/temp/{uuid4()}.mp3"
        print(temp_filepath)
        os.system(f'touch {temp_filepath}')
        video.write_videofile(path, temp_audiofile=temp_filepath)
        self.metadata()
        
    def metadata(self):
        os.system("exiftool -all= " + self.path)
        # os.system("exiftool " + self.path)
        return "Success!!"


class FileZip:

    def __init__(self, path, file_name, extension):
        self.path = path
        self.file_name = file_name
        self.extension = extension

    def file_zip(self):
        for root, dirs, files in os.walk(f"{self.path}"):
            write_file = [write_file for write_file in files if write_file.split(".")[1] != f"{self.extension}_original"]
            with ZipFile(f"{media_path}/{self.file_name}.zip", "w") as zip:
                for file in write_file:
                    zip.write(f"{root}/{file}", arcname=f"{self.file_name}/{file}")


    def __del__(self):
        os.system(f"rm -rf {self.path}")
        print("I am being destroyed")
