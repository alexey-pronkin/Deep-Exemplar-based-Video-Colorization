from timeit import Timer

import numpy as np;
import cv2, png
import argparse
bits_to_n = {"uint8": 255, "uint16":65_535}

def png_save(filename:str, arr:np.array):
    assert len(arr.shape) in [2, 3], "image should be 2d or 3d numpy array" 
    if len(arr.shape) == 2:
        gs = True
    elif len(arr.shape) == 3:
        gs = False
    else:
        raise Exception("image should be 2d or 3d numpy array")
    assert arr.dtype in ["uint8", "uint16"], "numpy array shuold be uint8 or uint16 for png image type"
    if arr.dtype == "uint16":
        bits = 16
    elif arr.dtype == "uint8":
        bits = 8
    with open(filename, 'wb') as f:
        writer = png.Writer(width=arr.shape[1], height=arr.shape[0], bitdepth=bits,
                            greyscale=gs)
        arr2list = arr.reshape(-1, arr.shape[1]*arr.shape[2]).tolist()
        writer.write(f, arr2list)
    return 1

def png_read(filename:str, bits:int=16) -> np.array:
    with open(filename, 'rb') as f:
        reader = png.Reader(file=f, greyscale=False)
        w, h, pixels, metadata = reader.read_flat()

        arr = reader.read()
    return np.vstack([np.getattr("uint"+str(bits))(row) for row in arr])

# for bits in [("uint8", 8), ("uint16", 16)]:

#     t = Timer(stmt = "cv2.imwrite" + f"('cv2_img{bits[1]}.png', image.astype({bits[0]}))", setup="import cv2")
#     try:
#         print(t.timeit(10))
#     except Exception:
#         t.print_exc()
#     t = Timer(stmt = "png_save" + f"('png_img{bits[1]}.png', image.astype({bits[0]}))")
#     try:
#         print(t.timeit(10))
#     except Exception:
#         t.print_exc()
if __name__ == "__main__":
    import timeit
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--frame_propagate", default=False, type=bool, help="propagation mode, , please check the paper"
    )
    parser.add_argument("--png_bits", type=str, default="uint8", help="uint8, uint16 - png 8/16")
    
    parser.add_argument("--image_size", type=str, default=[216 * 2, 384 * 2], help="the image size, eg. [216,384]")
    opt = parser.parse_args()
    def pypng():
        png_save(filename="pypng_img.png", arr=image.astype(opt.png_bits))
    def opencv():
        cv2.imwrite("pypng_img.png", image.astype(opt.png_bits))
    img_size = eval(opt.image_size)
    image = np.random.randint(low=0, high= 2**16-1, size=(2048, 2048, 3), dtype="uint16")

    print("pypng save time: ", timeit.Timer(pypng).timeit(number=1))
    print("opencv save time: ", timeit.Timer(opencv).timeit(number=1))

    