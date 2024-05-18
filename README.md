#Read all the file names from the directory
path = "C:/Users/rahulkumar60/Downloads/Tata Steel/TestFolder"
import os  
import PyPDF2  
  
def process_files_of_dir(path):  
    file_names = []  
    for root, dirs, files in os.walk(path):  
        for file in files:
            file_path = os.path.join(root, file)
            pdf_file = open(file_path, 'rb')
            #file of the directory
            file = open(file_path,'rb')
            pdfReader = PyPDF2.PdfReader(file)
            totalPages = len(pdfReader.pages)
            print(f"Total Pages: {totalPages}")
            print('Processing File ',file_path,'in the path',file_path, 'Total Pages in the pdf',totalPages)
            
            #parallel thread based on the no of cores available. let's use 40% of the cores only.  
            
            print(totalPages)
            pg_data=DocumentProcessor(file_path,end_point=azure_doc_info.end_point,api_key=azure_doc_info.api_key)

            num_cores = multiprocessing.cpu_count()
            num_workers = max(1, int(num_cores * 0.4))

            chunk_size = 100
            job_count = 0
            #to add all processed dict
            processed_docs = []

            #Running for each page range chunk size as
            for i in range(0, totalPages, chunk_size):  
                start = i + 1  
                last = min(i + chunk_size, totalPages)
                job_count += 1
                print(f"Injestion Job Page Range:{start}-{last}")    
                page_range = f"{start}-{last}"
                print(f"Running Injestion Job for Page Range:{page_range}")
                
                with ProcessPoolExecutor(max_workers=num_workers) as executor:
                    futures = {executor.submit(pg_data.process, page_range): page_range for page_range in page_ranges}
                    
                    for future in as_completed(futures):
                        file_path = futures[future]
                        try:
                            result = future.result()
                            processed_docs.append(result)
                        except Exception as e:
                            print(f"File {file_path} generated an exception: {e}")
            
                # Combine all processed docs into a single dictionary
                final_processed_doc = {i: doc for i, doc in enumerate(processed_docs)}
                
                
                #process the file chunk wise
                processed_doc=pg_data.process(page_range=f"{start}-{last}")
            
    return file_names  


process_files_of_dir(path)
