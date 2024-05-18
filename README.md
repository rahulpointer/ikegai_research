Modify the below function to add parallel processing for function pg_data.process, chunk size should be divided based on the available no of cores and use only 40% of it. At the end processed_doc which is a dictionary should be all collected in a list and then one final dictionary should be created.   
  
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
  
              
            #process the file chunk wise  
            processed_doc=pg_data.process(page_range=f"{start}-{last}")  
              
    return file_names    
  
  
process_files_of_dir(path)



import os  
import PyPDF2  
import multiprocessing  
from functools import partial  
from typing import List  
  
def process_files_of_dir(path: str) -> List[dict]:  
    file_names = []  
    result_list = []  
    available_cores = multiprocessing.cpu_count() * 0.4  
    chunk_size = max(1, int(available_cores))  
      
    def process_chunk(chunk_start, chunk_end):  
        pg_data = DocumentProcessor(file_path, end_point=azure_doc_info.end_point, api_key=azure_doc_info.api_key)  
        processed_doc = pg_data.process(page_range=f"{chunk_start}-{chunk_end}")  
        return processed_doc  
      
    with multiprocessing.Pool() as pool:  
        for root, dirs, files in os.walk(path):  
            for file in files:  
                file_path = os.path.join(root, file)  
                file_names.append(file_path)  
                pdf_file = open(file_path, 'rb')  
                pdfReader = PyPDF2.PdfReader(file_path)  
                totalPages = len(pdfReader.pages)  
                print(f"Total Pages: {totalPages}")  
                print('Processing File ', file_path, 'in the path', file_path, 'Total Pages in the pdf', totalPages)  
  
                # divide the pages into chunks based on available cores  
                chunks = [(start, last) for start, last in zip(range(1, totalPages+1, chunk_size),   
                                                               range(chunk_size, totalPages+1, chunk_size))]  
  
                # process each chunk in parallel  
                partial_process_chunk = partial(process_chunk, file_path)  
                chunk_results = pool.starmap(partial_process_chunk, chunks)  
                result_list.extend(chunk_results)  
  
    # combining the results into a final dictionary  
    final_dict = {}  
    for result in result_list:  
        final_dict.update(result)  
  
    return [final_dict]  
process_files_of_dir(path)
