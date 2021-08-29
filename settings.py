import os
# CROP BOUNDARY SCRIPT Settings

in_NIR = "D:\\3_Sinif\Staj\\NIRalign"
in_RED = "D:\\3_Sinif\Staj\\REDalign"
out_NIR = 'D:\\3_Sinif\\Staj\\NIRCropped\\'
out_RED = 'D:\\3_Sinif\\Staj\\REDCropped\\'
dir_NIR = os.listdir(in_NIR)
dir_RED = os.listdir(in_RED)

NIR_im_paths = []
RED_im_paths = []
for f_nir, f_red in zip(dir_NIR, dir_RED):
        fp_NIR= os.path.join(in_NIR, f_nir)
        fp_RED = os.path.join(in_RED, f_red)
        NIR_im_paths.append(fp_NIR)
        NIR_im_paths.sort(key=lambda NIR_im_paths: NIR_im_paths[:-5])
        RED_im_paths.append(fp_RED)
        RED_im_paths.sort(key=lambda RED_im_paths: RED_im_paths[:-5])

# NIR_REDdifferences Settings

input_folder = "D:\\3_Sinif\Staj\\NIRCropped"
input_folder2 = "D:\\3_Sinif\Staj\\REDCropped"
dir_NIRCropped = os.listdir(out_NIR)
dir_REDCropped = os.listdir(out_RED)

NIRCropped_im_paths = []
REDCropped_im_paths = []

for f_nir_c, f_red_c in zip(dir_NIRCropped, dir_REDCropped):

    fp_NIR_c = os.path.join(out_NIR, f_nir_c)
    fp_RED_c = os.path.join(out_RED, f_red_c)
    NIRCropped_im_paths.append(fp_NIR_c)
    NIRCropped_im_paths.sort()
    REDCropped_im_paths.append(fp_RED_c)
    REDCropped_im_paths.sort()

# NIR_REDBuffer Settings


dircont = "D:\\3_Sinif\Staj\\ceylanpinar" # what is dircont? Is it possible to rename "dircont"?
directory = os.listdir(dircont)

# NIR_REDCombine Settings
out_dir = 'D:\\3_Sinif\\Staj\\Ceylanpinar_NIR_Align\\'