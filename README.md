num_workers = 3

try:
    
    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        futures = {}
        page_ranges = ['1-2','2-3']
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
            print('Executing for the page range',page_range)
            futures = {executor.submit(pg_data,page_range)}
    
        for future in as_completed(futures):
            try:
                result = future.result()
                print(result)
                processed_docs.append(result)
            except Exception as e:
                print(f"Exception occurred: {e}")
except Exception as ex:
    print(ex.message)

Exception occurred: cannot pickle 'module' object
