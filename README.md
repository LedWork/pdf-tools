# pdf-tools

Small project that can do for free which you are only able to do with paid tools.


## Installation

First, make sure you have Python3 installed on your system. 

```bash
apt install python3 python3-venv
```

Then, install the required Python package by running:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```


## Usage 

This tool provides two functionalities:

1. [PDF Merger](#pdf-merger) merging two PDF files into one,
2. [PDF Editor](#pdf-editor) editing a PDF file by adding a watermark and/or timestamp.


## PDF Merger

This script merges two PDF files into one single PDF file.
To merge two PDF files, run the script from the command line by providing the paths to the two input PDF files and the desired output PDF file name

```bash
python3 pdf-tools.py merge input1.pdf input2.pdf output.pdf
```

Replace `input1.pdf` and `input2.pdf` with the filenames of your PDF files you want to merge, and `output.pdf` with the filename you want the merged PDF to be saved to.


## PDF Editor

To edit a PDF file by adding a watermark and/or timestamp, run the script with the following command:

```bash
python3 pdf-tools.py edit --watermark "WATERMARK TEXT" --opacity 20 --font_size 38 --timestamp input1.pdf output.pdf
```

Replace `input1.pdf` with the filename of your PDF file you want to edit, and `output.pdf` with the filename you want the edited PDF to be saved to. 
Adjust the watermark text, opacity, and font size as needed. 
Add `--timestamp` if you want to include a timestamp on each page.

### Known limitations

The watermark is added at the center of the page rotated anti-clockwise by 90 degrees and shifted down by a static value.
The location and font size for timestamp is not configurable.
