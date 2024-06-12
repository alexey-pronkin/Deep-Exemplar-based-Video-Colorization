#!/bin/bash

for n in {1..300};
do
python test.py --clip_path ./sample_videos7/clips/$n \
               --ref_path ./sample_videos7/ref/$n \
               --output_path ./sample_videos7/output \
               --image_size [768,1024] \
               --image_format jpg \
               --quality 1.0 \
               --make_video false
done