import os
import PyPDF2
import multiprocessing
from concurrent.futures import ProcessPoolExecutor, as_completed

# Assuming pg_data is a module and DocumentProcessor is the class containing the process method
from pg_data import DocumentProcessor
import azure_doc_info

def process_pdf_file(file_path, page_range, pg_data):
    print(f"Processing File {file_path} for Page Range {page_range}")
    result = pg_data.process(page_range)
    return result

def process_files_of_dir(path):
    file_names = []
    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            pdf_file = open(file_path, 'rb')
            pdfReader = PyPDF2.PdfReader(pdf_file)
            totalPages = len(pdfReader.pages)
            print(f"Total Pages: {totalPages}")
            print(f'Processing File {file_path} in the path {file_path}, Total Pages in the pdf {totalPages}')

            pg_data = DocumentProcessor(file_path, end_point=azure_doc_info.end_point, api_key=azure_doc_info.api_key)

            num_cores = multiprocessing.cpu_count()
            num_workers = max(1, int(num_cores * 0.4))

            chunk_size = 100
            processed_docs = []

            page_ranges = []
            for i in range(0, totalPages, chunk_size):
                start = i + 1
                last = min(i + chunk_size, totalPages)
                page_range = f"{start}-{last}"
                page_ranges.append(page_range)

            with ProcessPoolExecutor(max_workers=num_workers) as executor:
                futures = {}
                for i, page_range in enumerate(page_ranges):
                    if len(futures) >= num_workers:
                        # Wait for the current set of futures to complete before proceeding
                        for future in as_completed(futures):
                            try:
                                result = future.result()
                                processed_docs.append(result)
                            except Exception as e:
                                print(f"Exception occurred: {e}")
                        futures = {}

                    futures[executor.submit(process_pdf_file, file_path, page_range, pg_data)] = page_range

                # Wait for any remaining futures to complete
                for future in as_completed(futures):
                    try:
                        result = future.result()
                        processed_docs.append(result)
                    except Exception as e:
                        print(f"Exception occurred: {e}")

            # Combine all processed docs into a single dictionary
            final_processed_doc = {i: doc for i, doc in enumerate(processed_docs)}

            pdf_file.close()

            # Return the final processed document (or save it as needed)
            print(f"Final Processed Document for {file_path}: {final_processed_doc}")

    return file_names

# Call the function
path = "C:/Users/rahulkumar60/Downloads/Tata Steel/TestFolder"
process_files_of_dir(path)
