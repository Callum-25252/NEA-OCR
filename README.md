# NEA Program for OCR
### Prerequisites ###
* Python 3
* Pip
* OpenCV (3.4.2 or above)
* PIL
* NumPy
* scikit-image
* scikit-learn
* TensorFlow (version 2.x)
* imutils
* tqdm

### Information ###
My overall aim for this program is to create a program for Natural Scene OCR (Optical Character Recognition), wherein the user can input a photo (.jpg or .png) of a natural scene that contains synthesised text (e.g. a photo of a sign) and the program will return a text output of what the text in the image reads. Natural scene text is simply a photo of synthesised text in a completely uncontrolled environment. The text could be at an angle, within a background or have other factors making it difficult to recognise (see the later section on natural scene text and the associated difficulties).

### Fonts ###
I used the Google Fonts GitHub repository to get fonts for making training data https://github.com/google/fonts
If you use the command `FOR /R "Downloads\fonts-master\ofl\" %i IN (*.ttf) DO MOVE "%i" "Documents\NEA\charImages\Fonts\"` you can extract all the ttf files to the fonts.
You will need these fonts if you want to train the network. I personally used the fontChecker.py program to check through and remove any bad fonts by hand in an efficient manner.

### Usage ###
Import an image using the import image button and click the icon with the magnifying glass scanning a piece of paper to get text in that image displayed. The three other buttons do anticlockwise and clockwise rotation and cropping respectively.

### Installation Instructions ###
#### Pip ####
##### Windows #####
1. Download get-pip.py from https://bootstrap.pypa.io/get-pip.py
2. Open a command prompt and go to to the folder you installed get-pip.py to
3. Run the command `python get-pip.py`
4. (Optional) Verify that pip is installed by running the command `pip -V`

##### Ubuntu 18.04 #####
1. Update the package list with `sudo apt update`
2. Install pip for Python 3 with `sudo apt install python3-pip`
3. (Optional) check the installation with `pip3 --version`

#### PIL #####
1. Open a command prompt
2. Run the command `pip install Pillow`

#### NumPy ####
1. Open a a command prompt
2. Run the command `pip install numpy`

#### OpenCV ####
1. Open a command prompt
2. Run the command `pip install opencv-contrib-python`

#### scikit-image ####
1. Open a command prompt
2. Run the command `pip install scikit-image`

#### scikit-learn ####
1. Open a command prompt
2. Run the command `pip install scikit-learn`

#### TensorFlow ####
1. Open a command prompt
2. Run the command `pip install tensorflow`

#### imutils ####
1. Open a command prompt
2. Run the command `pip install imutils`

#### tqdm #####
1. Open a command prompt
2. Run the command `pip3 install tqdm`
