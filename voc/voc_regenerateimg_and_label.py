import os
import sys
import operator

image_dir = '/home/gy/Database/Done/grape/voc/JPEGImages'
anno_dir = '/home/gy/Database/Done/grape/voc/Annotations'

images = os.listdir(image_dir)
annos = os.listdir(anno_dir)

images_names = [os.path.splitext(image)[0] for image in images]
annos_names = [os.path.splitext(anno)[0] for anno in annos]

if operator.eq(images_names, annos_names):
    print('image and anno not match images {} annos {}'.format(len(images_names), len(annos_names)))
    exit()

# images.sort()
# annos.sort()

check = True
for index, name in enumerate(images):
    source_image_name = os.path.join(image_dir, name)
    source_anno_name = os.path.join(anno_dir, os.path.splitext(name)[0] + '.xml')

    if not os.path.exists(source_anno_name) or not os.path.exists(source_image_name):
        print('{} or {} not exist'.format(source_anno_name, source_image_name))
        check = False
    # os.rename(source_image_name,dst_image_name)
    # os.rename(source_anno_name,dst_anno_name)
    # print(index,name)

if not check:
    print('check failed')
    exit()

for index, name in enumerate(images):
    source_image_name = os.path.join(image_dir, name)
    dst_image_name = os.path.join(image_dir, 'rename' + str(index) + os.path.splitext(name)[1])

    source_anno_name = os.path.join(anno_dir, os.path.splitext(name)[0] + '.xml')
    dst_anno_name = os.path.join(anno_dir, 'rename' + str(index) + '.xml')

    os.rename(source_image_name, dst_image_name)
    os.rename(source_anno_name, dst_anno_name)
