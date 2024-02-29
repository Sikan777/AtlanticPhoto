from pydantic import BaseModel, validator
from datetime import datetime
from enum import Enum


# added enum classes to have options for the main scheme
class CropEnum(str, Enum):
    fill = "fill"
    fit = "fit"
    crop = "crop"
    limit = "limit"
    thumb = "thumb"
    scale = "scale"


class EffectEnum(str, Enum):
    grayscale = "grayscale"
    sepia = "sepia"
    invert = "invert"
    cartoonify = "cartoonify"
    blur = "blur"
    brightness = "brightness"
    contrast = "contrast"
    saturation = "saturation"
    sharpen = "sharpen"


class BorderEnum(str, Enum):
    solid_black = "1px_solid_black"
    solid_red = "1px_solid_red"
    dashed_blue = "2px_dashed_blue"


class TransSchema(BaseModel):
    width: int = 500
    height: int = 300
    crop: CropEnum = CropEnum.crop
    effect: EffectEnum = EffectEnum.grayscale
    border: BorderEnum = BorderEnum.dashed_blue
    angle: int = 15

    # here and then we validate width, height and angle
    @validator("width")
    def check_width(cls, v):
        if not 100 < v <= 1920:
            raise ValueError("Width must be between 1 and 1920")
        return v

    @validator("height")
    def check_height(cls, v):
        if not 100 < v <= 1080:
            raise ValueError("Height must be between 1 and 1080")
        return v

    @validator("angle")
    def check_angle(cls, v):
        if not 0 <= v <= 360:
            raise ValueError("Angle must be between 0 and 360 degrees")
        return v


class TransResponse(BaseModel):
    id: int
    original_pic_id: int
    url: str
    user_id: int
    created_at: datetime
