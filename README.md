import os
import PyPDF2
from concurrent.futures import ProcessPoolExecutor, as_completed
import multiprocessing

# Assume pg_data is a module and process is the function you want to apply
import pg_data

def process_pdf_file(file_path):
    # This function will be executed in parallel for each file
    pdf_file = open(file_path, 'rb')
    pdfReader = PyPDF2.PdfReader(pdf_file)
    totalPages = len(pdfReader.pages)
    print(f"Total Pages: {totalPages}")
    print(f'Processing File {file_path} in the path {file_path}, Total Pages in the pdf {totalPages}')
    
    # Call the pg_data.process function here
    processed_doc = pg_data.process(pdf_file)
    
    pdf_file.close()
    
    return processed_doc

def process_files_of_dir(path):
    file_paths = []
    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            file_paths.append(file_path)

    # Determine the number of workers based on available cores
    num_cores = multiprocessing.cpu_count()
    num_workers = max(1, int(num_cores * 0.4))
    
    processed_docs = []

    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        futures = {executor.submit(process_pdf_file, file_path): file_path for file_path in file_paths}
        
        for future in as_completed(futures):
            file_path = futures[future]
            try:
                result = future.result()
                processed_docs.append(result)
            except Exception as e:
                print(f"File {file_path} generated an exception: {e}")

    # Combine all processed docs into a single dictionary
    final_processed_doc = {i: doc for i, doc in enumerate(processed_docs)}
    
    return final_processed_doc

# Call the function
path = "C:/Users/rahulkumar60/Downloads/Tata Steel/TestFolder"
final_result = process_files_of_dir(path)
print(final_result)
