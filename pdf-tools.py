import pymupdf
import argparse

def merge_pdfs(input_pdf1, input_pdf2, output_pdf):
    pdf1 = pymupdf.open(input_pdf1)
    pdf2 = pymupdf.open(input_pdf2)

    pdf1.insert_pdf(pdf2)

    pdf1.save(output_pdf)
    print(f"Merged PDF saved as: {output_pdf}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Merge two PDF files.")
    parser.add_argument("input_pdf1", type=str, help="First input PDF file")
    parser.add_argument("input_pdf2", type=str, help="Second input PDF file")
    parser.add_argument("output_pdf", type=str, help="Output PDF file")

    args = parser.parse_args()

    merge_pdfs(args.input_pdf1, args.input_pdf2, args.output_pdf)

