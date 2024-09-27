import pymupdf
import argparse
import datetime

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

def main():
    parser = argparse.ArgumentParser(description="PDF Tools - Merge or Edit PDF files.")
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

    args = parser.parse_args()

    if args.command == "merge":
        merge_pdfs(args.input_pdf1, args.input_pdf2, args.output_pdf)
    elif args.command == "edit":
        edit_pdf(args.input_pdf, args.output_pdf, args.watermark, args.opacity, args.font_size, args.timestamp)

if __name__ == "__main__":
    main()
