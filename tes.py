# import fitz

# def remove_all_text_from_pdf(pdf_path):
#     pdf_document = fitz.open(pdf_path)
#     for page_num in range(pdf_document.page_count):
#         page = pdf_document[page_num]
#         blocks = page.get_text("dict")["blocks"]
#         for b in blocks:
#             if b["type"] == 0:  # Text block
#                 for l in b["lines"]:
#                     for s in l["spans"]:
#                         rect = fitz.Rect(s["bbox"])
#                         page.add_redact_annot(rect)
#         page.apply_redactions()
#     pdf_document.save("modified_output.pdf")
#     pdf_document.close()

# # Example usage
# pdf_path = "0400034237962_712014486568 (1).pdf"
# remove_all_text_from_pdf(pdf_path)
# print("All text removed. Modified PDF saved as 'modified_output.pdf'.")













import pdfplumber
import fitz
import re

def extract_data_from_pdf(pdf_path):
    extracted_data = {}
    with pdfplumber.open(pdf_path) as pdf:
        first_page = pdf.pages[0]
        text = first_page.extract_text()
        
        # Extracting Customer's Name
        name_start_index = text.find("Customer's Name:") + len("Customer's Name:")
        name_end_index = text.find("\n", name_start_index)
        name = text[name_start_index:name_end_index].strip()

        # Extracting Due Date
        due_date_start_index = text.find("Dec-")
        due_date_end_index = text.find("\n", due_date_start_index)
        due_date = text[due_date_start_index:due_date_end_index].strip()

        # Extracting Amount
        amount_start_index = text.find("Rs.")
        amount_end_index = text.find("\n", amount_start_index)
        amount = text[amount_start_index:amount_end_index].strip()

        extracted_data['Customer\'s Name'] = name
        extracted_data['Due Date'] = due_date
        extracted_data['Amount'] = amount

    return extracted_data

def paste_data_to_pdf(input_pdf_path, output_pdf_path, extracted_data):
    pdf_document = fitz.open(input_pdf_path)
    for page in pdf_document:
        for key, value in extracted_data.items():
            if key == "Customer's Name":
                page.insert_text((100, 100), value, fontsize=12)  # Adjust coordinates as needed
            elif key == "Due Date":
                page.insert_text((100, 200), value, fontsize=12)  # Adjust coordinates as needed
            elif key == "Amount":
                page.insert_text((100, 300), value, fontsize=12)  # Adjust coordinates as needed

    pdf_document.save(output_pdf_path)
    pdf_document.close()

# Example usage
input_pdf_path = "0400034237962_712014486568 (1).pdf"  # Provide the path to your input PDF file
output_pdf_path = "modified_output.pdf"  # Provide the path to your output PDF file
extracted_data = extract_data_from_pdf(input_pdf_path)
paste_data_to_pdf(input_pdf_path, output_pdf_path, extracted_data)
print("Data pasted to PDF. Modified PDF saved as 'output_pdf_file.pdf'.")














