import cv2
import numpy as np
from numpy import random


class Compose(object):
    """Composes several augmentations together.
    Args:
        transforms (List[Transform]): list of transforms to compose.
    Example:
        >>> augmentations.Compose([
        >>>     transforms.CenterCrop(10),
        >>>     transforms.ToTensor(),
        >>> ])
    """

    def __init__(self, transforms):
        self.transforms = transforms

    def __call__(self, img):
        for t in self.transforms:
            img = t(img)
        return img


class ConvertFromInts(object):
    def __call__(self, image):
        return image.astype(np.float32)
        
    
class Resize(object):
    def __init__(self, size=(300, 300)):
        self.size = size

    def __call__(self, image):
        image = cv2.resize(image, (self.size[0],
                                   self.size[1]))
        return image


class RandomResize(object):
    def __init__(self, min_size = 50, max_size=200):
        self.min_size = min_size
        self.max_size = max_size

    def __call__(self, image):
        h, w = image.shape[:2]
        new_h = random.randint(self.min_size, self.max_size)
        new_w = int(w / h * new_h)
        print(h,w,new_h,new_w)
        image = cv2.resize(image, (new_w,
                                   new_h))
        return image


class RandomCut(object):
    def __init__(self, cut_size = 10):
        self.cut_size = cut_size

    def __call__(self, image):
        h, w = image.shape[:2]
        if random.randint(2):
            cut = random.randint(self.cut_size)
            image = image[0:h-cut, 0:w]
        if random.randint(2):
            cut = random.randint(self.cut_size)
            image = image[0:h, 0:w-cut]
        return image


class RandomBox(object):
    def __init__(self, box_size = 30):
        self.box_size = box_size

    def __call__(self, image):
        h, w = image.shape[:2]
        if random.randint(2):
            b_x = random.randint(w)
            b_y = random.randint(h)
            size = random.randint(self.box_size)
            image[b_y:b_y+size, b_x:b_x+size] = random.randint(255)
        return image


class RandomSpNoise(object):
    def __init__(self, prob = .2):
        self.prob = prob

    def __call__(self, image):
        for i in range(0, image.shape[0], 3):
            for j in range(0, image.shape[1], 3):
                rdn = random.random()
                if rdn < self.prob:
                    image[i][j] = random.randint(255)

        return image


class RandomSaturation(object):
    def __init__(self, lower=0.5, upper=1.5):
        self.lower = lower
        self.upper = upper
        assert self.upper >= self.lower, "contrast upper must be >= lower."
        assert self.lower >= 0, "contrast lower must be non-negative."

    def __call__(self, image):
        if random.randint(2):
            image[:, :, 1] *= random.uniform(self.lower, self.upper)

        return image


class RandomHue(object):
    def __init__(self, delta=18.0):
        assert delta >= 0.0 and delta <= 360.0
        self.delta = delta

    def __call__(self, image):
        if random.randint(2):
            image[:, :, 0] += random.uniform(-self.delta, self.delta)
            image[:, :, 0][image[:, :, 0] > 360.0] -= 360.0
            image[:, :, 0][image[:, :, 0] < 0.0] += 360.0
        return image


class RandomLightingNoise(object):
    def __init__(self):
        self.perms = ((0, 1, 2), (0, 2, 1),
                      (1, 0, 2), (1, 2, 0),
                      (2, 0, 1), (2, 1, 0))

    def __call__(self, image):
        if random.randint(2):
            swap = self.perms[random.randint(len(self.perms))]
            shuffle = SwapChannels(swap)  # shuffle channels
            image = shuffle(image)
        return image


class ConvertColor(object):
    def __init__(self, current, transform):
        self.transform = transform
        self.current = current

    def __call__(self, image):
        if self.current == 'BGR' and self.transform == 'HSV':
            image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        elif self.current == 'RGB' and self.transform == 'HSV':
            image = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
        elif self.current == 'BGR' and self.transform == 'RGB':
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        elif self.current == 'HSV' and self.transform == 'BGR':
            image = cv2.cvtColor(image, cv2.COLOR_HSV2BGR)
        elif self.current == 'HSV' and self.transform == "RGB":
            image = cv2.cvtColor(image, cv2.COLOR_HSV2RGB)
        else:
            raise NotImplementedError
        return image


class RandomContrast(object):
    def __init__(self, lower=0.5, upper=1.5):
        self.lower = lower
        self.upper = upper
        assert self.upper >= self.lower, "contrast upper must be >= lower."
        assert self.lower >= 0, "contrast lower must be non-negative."

    # expects float image
    def __call__(self, image):
        if random.randint(2):
            alpha = random.uniform(self.lower, self.upper)
            image *= alpha
        return image


class RandomBrightness(object):
    def __init__(self, delta=32):
        assert delta >= 0.0
        assert delta <= 255.0
        self.delta = delta

    def __call__(self, image):
        if random.randint(2):
            delta = random.uniform(-self.delta, self.delta)
            image += delta
        return image


class RandomMirror(object):
    def __call__(self, image):
        _, width, _ = image.shape
        if random.randint(2):
            image = image[:, ::-1]
        return image


class SwapChannels(object):
    """Transforms a tensorized image by swapping the channels in the order
     specified in the swap tuple.
    Args:
        swaps (int triple): final order of channels
            eg: (2, 1, 0)
    """

    def __init__(self, swaps):
        self.swaps = swaps

    def __call__(self, image):
        """
        Args:
            image (Tensor): image tensor to be transformed
        Return:
            a tensor with channels swapped according to swap
        """
        # if torch.is_tensor(image):
        #     image = image.data.cpu().numpy()
        # else:
        #     image = np.array(image)
        image = image[:, :, self.swaps]
        return image


class PhotometricDistort(object):
    def __init__(self):
        self.pd = [
            RandomContrast(),  # RGB
            ConvertColor(current="RGB", transform='HSV'),  # HSV
            RandomSaturation(),  # HSV
            RandomHue(),  # HSV
            ConvertColor(current='HSV', transform='RGB'),  # RGB
            RandomContrast()  # RGB
        ]
        self.rand_brightness = RandomBrightness()
        self.rand_light_noise = RandomLightingNoise()

    def __call__(self, image):
        im = image.copy()
        im = self.rand_brightness(im)
        if random.randint(2):
            distort = Compose(self.pd[:-1])
        else:
            distort = Compose(self.pd[1:])
        im = distort(im)
        return self.rand_light_noise(im)

    
class PhotometricDistortV2(object):
    def __init__(self):
        self.pd = [
            RandomMirror(),
            RandomCut(),
            RandomResize(50, 200),
            RandomBox(),
            RandomContrast(0.6, 1.4),  # RGB
            ConvertColor(current="RGB", transform='HSV'),  # HSV
            RandomSaturation(0.8, 1.2),  # HSV
            RandomHue(12),  # HSV
            ConvertColor(current='HSV', transform='RGB'),  # RGB
            RandomContrast(0.6, 1.4),  # RGB
            RandomSpNoise()
        ]
        self.rand_brightness = RandomBrightness(32)
        self.rand_light_noise = RandomLightingNoise()

    def __call__(self, image):
        im = image.copy()
        im = self.rand_brightness(im)
        if random.randint(2):
            distort = Compose(self.pd[:-1])
        else:
            distort = Compose(self.pd[1:])
        im = distort(im)
        return self.rand_light_noise(im)
        
        
        
import os

root = 'guider/'
jpgs = os.listdir(root)
os.makedirs('aug_' + root, exist_ok=True)

auger = PhotometricDistortV2()

for f in jpgs:
    img = cv2.imread(root + f)
    if img is not None:
        img = ConvertFromInts()(img)
        img_aug = auger(img)
        cv2.imwrite('aug_' + root + 'aug_' + f, img_aug)


