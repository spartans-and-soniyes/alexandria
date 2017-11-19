# -*- coding: utf-8 -*-
"""
Created on Wed Dec  9 14:55:43 2015

This script is to convert the txt annotation files to appropriate format needed by YOLO 

@author: Guanghan Ning
Email: gnxr9@mail.missouri.edu
"""

import os
from os import walk, getcwd
from PIL import Image

classes = ["exitsign"]

def upscale(from_size, to_size, box):
    # upscale box to size of picture
    
    new_box = []

    fw = from_size[0]
    fh = from_size[1]
    tw = to_size[0]
    th = to_size[1]

    xmin = box[0]
    ymin = box[1]
    xmax = box[2]
    ymax = box[3]

    new_box.append( xmin * (tw / fw) )
    new_box.append( ymin * (th / fh) )
    new_box.append( xmax * (tw / fw) )
    new_box.append( ymax * (th / fh) )

    return new_box


def convert(size, box):
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)
    
    
"""-------------------------------------------------------------------""" 

""" Configure Paths"""   
in_path = "/run/media/sean/SEANHDD/HackWIT/Labels/"
out_path = "/run/media/sean/SEANHDD/HackWIT/ConvertedLabels/"
img_base_path = "/run/media/sean/SEANHDD/HackWIT/Images/"

cls = "exitsign"
if cls not in classes:
    exit(0)
cls_id = classes.index(cls)

wd = getcwd()
list_file = open('%s/%s_list.txt'%(wd, cls), 'w+')

""" Get input text file list """
txt_name_list = []
for (dirpath, dirnames, filenames) in walk(in_path):
    txt_name_list.extend(filenames)
    break
# print(txt_name_list)

""" Process """
for txt_name in txt_name_list:
    
    """ Open input text files """
    txt_path = in_path + txt_name
    print("Input:" + txt_path)
    txt_file = open(txt_path, "r")
    lines = txt_file.read().split('\n') # for ubuntu, use "\r\n" instead of "\n"
    
    """ Open output text files """
    txt_out_path = out_path + txt_name
    print("Output:" + txt_out_path)
    txt_outfile = open(txt_out_path, "w+")
    
    """ Convert the data to YOLO format """
    ct = 0
    for line in lines:
        if(len(line) >= 2):
            ct = ct + 1
            print(line)
            elems = line.split(' ')
            print(elems)
            xmin = elems[0]
            xmax = elems[2]
            ymin = elems[1]
            ymax = elems[3]
            
            img_path = str('%s%s.jpeg'%(img_base_path, os.path.splitext(txt_name)[0]))
            print(img_path)

            # get size of image
            im =Image.open(img_path)
            w = int(im.size[0])
            h = int(im.size[1])
            print(w, h)

            # create box
            b = (float(xmin), float(xmax), float(ymin), float(ymax))

            # upscale and convert bounding box
            bb = convert((w, h), upscale((480, 640), (w, h), b))
            print(bb)

            # write new box to converted labels
            txt_outfile.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

    """ Save those images with bb into list"""
    if(ct != 0):
        list_file.write('%s%s.jpeg\n'%(img_base_path, os.path.splitext(txt_name)[0]))
                
list_file.close()       
