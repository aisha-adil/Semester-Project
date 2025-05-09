# contains functions forencrypting and decrypting text using a columnar transposition cypher
# it takes a string and a key, either assigns a number (column numbers) to every letter of the key word to determine order or uses alphabetical order
# the  string to be encrypted is written under the keyword, transposed to be exact
# then read in order of keywords as columns


def key_sequence_generation_function(keyword):
    # takes in keywords and return list of numbers for column order

    # 1. we take in a keyword and assign a number to each letter in the keyword to form pairs of (letter, number)
    pairs = [(letter, i) for i, letter in enumerate(keyword)]

    # 2. we sort the pairs based on the letter in alphabetical order,
    # pairs.sort(key=lambda x: x[0])
    pairs.sort(key=lambda x: (x[0], x[1])) #  error3: sorting by character (alphabetically), then by original index to maintain stability

    # 3. return pairs in order they should be read in the transposition
    return [index for _, index in pairs]


def encryption_function(plaintext, keyword):
    # takes in a string and keyword and returns the encrypted text

    # 1. we generate a key sequence using the key_sequence_generation_function
    column_sequence = key_sequence_generation_function(keyword)

    # 2. we calculate the number of columns and rows (using ceiling division) needed for the transposition
    num_columns = len(keyword)
    num_rows = -(-len(plaintext) // num_columns)

    # 3. we create a matrix for the actual transposition
    matrix = [["" for _ in range(num_columns)] for _ in range(num_rows)]

    # 4. we fill the matrix with the plaintext, row by row
    text_index = 0
    for row in range(num_rows):
        for column in range(num_columns):
             if text_index < len(plaintext):
                matrix[row][column] = plaintext[text_index]
                text_index += 1

    # 5. we create the the encrypted text by reading the matrix in the order of the column sequence
    encrypted_text = ""
    for col in column_sequence:
        for row in range(num_rows):
            if matrix[row][col] != "":
                encrypted_text += matrix[row][col]
    return encrypted_text


def decryption_function(cyphertext, keyword):
    # takes in a string and keyword and returns the decrypted string

    # 1. we generate a key sequence using the key_sequence_generation_function
    key_sequence = key_sequence_generation_function(keyword)

    # 2. we calculate the number of rows and columns like in encryption function
    num_columns = len(keyword)
    num_rows = -(-len(cyphertext) // num_columns)

    # 3. we calculate number of filled positions in a transpoistion matrix
    num_filled_positions = len(cyphertext)
    num_long_cols = num_filled_positions % num_columns

    # 4. we create matrix for the transposition
    matrix = [["" for _ in range(num_columns)] for _ in range(num_rows)]

    col_length = [num_rows] * num_columns   
    for i in range(num_long_cols):
        col_length[i] += 1

    # error2: transposition was faulty in case of repititive letters and indices were calulated wrong
    # some lines of code were also removed from the encryption function to make this correct

    # # 5. we adjust for text that doesn't completely fill the transposition grid
    # remaining = num_filled_positions % num_columns
    # if remaining != 0:
    #     for i in range(remaining):
    #         col_length[i] -= 1

    # 6. we fill transposition matrix with cyphertext, column by column for reverse transposition
    text_index = 0
    for col_index in key_sequence:
        for row in range(col_length[col_index]):
            if text_index < len(cyphertext):
                matrix[row][col_index] = cyphertext[text_index]
                text_index += 1

    # 7. we create the decrypted text by reading the matrix row by row
    decrypted_text = ''
    for i in range(num_rows):
        for j in range(num_columns):
            if matrix[i][j] != '':
                decrypted_text += matrix[i][j]
    return decrypted_text


def main():
    """
    Main function to run the columnar transposition cipher example.
    """
    plaintext = "TRANSPOSITIONCIPHER"
    keyword = "SECRET"

    # Encryption
    ciphertext = encryption_function(plaintext, keyword)
    print(f"Plaintext: {plaintext}")
    print(f"Keyword: {keyword}")
    print(f"Ciphertext: {ciphertext}")

    # Decryption
    decrypted_text = decryption_function(ciphertext, keyword)
    print(f"Decrypted Text: {decrypted_text}")

    # Check if decryption works correctly
    if decrypted_text == plaintext:
        print("Decryption successful!")
    else:
        print("Decryption failed.")


if __name__ == "__main__":
    main()  # Call the main function when the script is executed
