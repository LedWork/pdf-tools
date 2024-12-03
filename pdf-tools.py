import pymupdf  # PyMuPDF
import argparse
import datetime
import os

def merge_pdfs(input_pdf1, input_pdf2, output_pdf):
    pdf1 = pymupdf.open(input_pdf1)
    pdf2 = pymupdf.open(input_pdf2)
    pdf1.insert_pdf(pdf2)
    pdf1.save(output_pdf)
    print(f"Merged PDF saved as: {output_pdf}")

def add_watermark_to_page(page, watermark_text, opacity, font_size):
    x_center = page.rect.width / 2
    y_center = page.rect.height / 2 + 300
    color = (0, 0, 0)
    alpha = opacity / 100.0
    page.insert_text(
        (x_center, y_center),
        text=watermark_text,
        fontsize=font_size,
        color=color,
        rotate=90,
        render_mode=0,
        fill_opacity=alpha,
        overlay=True
    )

def add_timestamp_to_page(page, font_size, timestamp):
    page.insert_text(
        (10, 10),
        text=timestamp,
        fontsize=font_size,
        color=(0, 0, 0)
    )

def edit_pdf(input_pdf, output_pdf, watermark_text, opacity, font_size, add_timestamp):
    pdf = pymupdf.open(input_pdf)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") if add_timestamp else None
    for page_number in range(len(pdf)):
        page = pdf[page_number]
        add_watermark_to_page(page, watermark_text, opacity, font_size)
        if add_timestamp:
            add_timestamp_to_page(page, 12, timestamp)
    pdf.save(output_pdf)
    print(f"Edited PDF saved as: {output_pdf}")

def split_pdf_to_images(input_pdf, output_dir, img_format, resolution=300):
    pdf = pymupdf.open(input_pdf)
    
    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Validate image format
    img_format = img_format.lower()
    if img_format not in ["jpg", "jpeg", "gif", "png"]:
        raise ValueError("Unsupported image format. Please use jpg, jpeg, gif, or png.")
    
    # Set a scaling matrix for higher resolution (default is 1.0; increase for higher DPI)
    zoom = resolution / 72  # 72 DPI is default; this increases the DPI to the desired resolution
    matrix = pymupdf.Matrix(zoom, zoom)
    
    for page_number in range(len(pdf)):
        page = pdf.load_page(page_number)  # Load individual page
        pix = page.get_pixmap(matrix=matrix)  # Get image representation of the page at higher resolution
        
        # Determine the image extension and save format
        image_filename = os.path.join(output_dir, f"page_{page_number + 1}.{img_format}")
        pix.save(image_filename)
        print(f"Saved page {page_number + 1} as {image_filename}")
    
    print(f"{len(pdf)} pages have been saved as {img_format.upper()} images in the directory: {output_dir}")

def main():
    parser = argparse.ArgumentParser(description="PDF Tools - Merge, Edit, or Split PDF files.")
    subparsers = parser.add_subparsers(dest="command")

    # Merge command
    merge_parser = subparsers.add_parser("merge", help="Merge two PDF files.")
    merge_parser.add_argument("input_pdf1", type=str, help="First input PDF file")
    merge_parser.add_argument("input_pdf2", type=str, help="Second input PDF file")
    merge_parser.add_argument("output_pdf", type=str, help="Output PDF file")

    # Edit command
    edit_parser = subparsers.add_parser("edit", help="Edit a PDF file by adding a watermark and/or timestamp.")
    edit_parser.add_argument("input_pdf", type=str, help="Input PDF file")
    edit_parser.add_argument("output_pdf", type=str, help="Output PDF file")
    edit_parser.add_argument("--watermark", type=str, default="Watermark", help="Watermark text")
    edit_parser.add_argument("--opacity", type=int, default=20, help="Opacity of the watermark (0-100)")
    edit_parser.add_argument("--font_size", type=int, default=12, help="Font size of the watermark and timestamp")
    edit_parser.add_argument("--timestamp", action="store_true", help="Add timestamp to the header of each page")

    # Split command
    split_parser = subparsers.add_parser("split", help="Split a PDF into individual images.")
    split_parser.add_argument("input_pdf", type=str, help="Input PDF file")
    split_parser.add_argument("output_dir", type=str, help="Directory to save the images")
    split_parser.add_argument("--format", type=str, default="jpg", help="Image format to save pages (jpg, jpeg, gif, png)")
    split_parser.add_argument("--resolution", type=int, default=300, help="Resolution (DPI) for the output images (default: 300)")


    args = parser.parse_args()

    if args.command == "merge":
        merge_pdfs(args.input_pdf1, args.input_pdf2, args.output_pdf)
    elif args.command == "edit":
        edit_pdf(args.input_pdf, args.output_pdf, args.watermark, args.opacity, args.font_size, args.timestamp)
    elif args.command == "split":
        split_pdf_to_images(args.input_pdf, args.output_dir, args.format, args.resolution)

if __name__ == "__main__":
    main()
