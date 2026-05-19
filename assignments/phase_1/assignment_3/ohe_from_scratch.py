def one_hot_encoding_scratch(data):
    unique_categories = sorted(list(set(data)))
    
    category_to_index = {category: index for index, category in enumerate(unique_categories)}
    
    num_rows = len(data)
    num_cols = len(unique_categories)
    encoded_matrix = [[0] * num_cols for _ in range(num_rows)]
    
    for row_idx, item in enumerate(data):
        col_idx = category_to_index[item]
        encoded_matrix[row_idx][col_idx] = 1
        
    return encoded_matrix, unique_categories

# --- Test ---
data = ["cat", "dog", "bird", "cat", "bird"]
encoded_data, categories = one_hot_encoding_scratch(data)

print("Categories:", categories)
print("\nEncoded Matrix:")
for row in encoded_data:
    print(row)