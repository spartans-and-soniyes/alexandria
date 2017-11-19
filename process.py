import glob, os

# Current directory
picture_dir = "/run/media/sean/SEANHDD/HackWIT/Images/"

# Directory where the data will reside, relative to 'darknet.exe'
path_data = 'data/obj/'

# Percentage of images to be used for the test set
percentage_test = 25;

# Create and/or truncate train.txt and test.txt
file_train = open('train.txt', 'w')  
file_test = open('test.txt', 'w')

# Populate train.txt and test.txt
counter = 1  
index_test = round(100 / percentage_test)  
for pathAndFilename in glob.iglob(os.path.join(picture_dir, "*.jpeg")):  
    title, ext = os.path.splitext(os.path.basename(pathAndFilename))

    if counter == index_test:
        counter = 1
        file_test.write(path_data + title + '.jpeg' + "\n")
    else:
        file_train.write(path_data + title + '.jpeg' + "\n")
        counter = counter + 1
