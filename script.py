#!/usr/bin/env python3

import pathlib
import shutil
import time

from sh import cat, exiftran, tesseract, convert, scantailor_cli, mogrify, fix_perspective

def main():
    images_dir = pathlib.Path("./originals")
    output_dir = pathlib.Path("./output")

    processed_images_dir = output_dir / "images"
    scantailored_images_dir = output_dir / "scantailored"
    texts_dir = output_dir / "pages"

    output_dir.mkdir(exist_ok=True, parents=True)
    processed_images_dir.mkdir(exist_ok=True, parents=True)
    scantailored_images_dir.mkdir(exist_ok=True, parents=True)
    texts_dir.mkdir(exist_ok=True, parents=True)

    images = sorted(images_dir.glob("*"))
    for image in images:
        print(f"Processing {image} to jpeg")
        processed_image = (processed_images_dir / image.name).with_suffix(".jpeg")
        convert("-format", "jpg", str(image), str(processed_image))
        exiftran("-i", "-a", str(processed_image))
        mogrify("-units", "PixelsPerInch", "-density", "300", str(processed_image))

        print(f"Running scantailor")
        scantailor_cli(str(processed_image), str(scantailored_images_dir))
        processed_image = scantailored_images_dir / (processed_image.with_suffix(".tif")).name

        print(f"Running fix-perspective")
        fix_perspective(str(processed_image), str(processed_image))

        print(f"Running tesseract")
        processed_text = texts_dir / image.name
        #tesseract("--tessdata-dir", "tessdata_best", str(processed_image), processed_text, "-l", "eng", "--psm", "6")
        tesseract(str(processed_image), processed_text, "-l", "eng", "--psm", "3")
        #tesseract(str(processed_image), processed_text)

        print(f"Produced: {processed_text}.txt")

if __name__ == "__main__":
    main()
