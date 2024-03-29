# Imports
import string

# Global variables
max_key_lenght = 10

english_frequences = [
    0.08167, 0.01492, 0.02782, 0.04253, 0.12702, 0.02228, 0.02015,
    0.06094, 0.06966, 0.00153, 0.00772, 0.04025, 0.02406, 0.06749,
    0.07507, 0.01929, 0.00095, 0.05987, 0.06327, 0.09056, 0.02758,
    0.00978, 0.02360, 0.00150, 0.01974, 0.00074]

# String Cleaner
def string_cleaner(string):
    clean_string = string.upper()
    # Filter only A-Z
    clean_string = ''.join(
        [char for char in clean_string if 65 <= ord(char) <= 90])
    return clean_string

# IC calculator
def ic_calculator(text):
    num_letters = [0] * 26
    text_lenght = len(text)
    for char in text:
        num_letters[ord(char) - 65] += 1
    ic = sum([entry ** 2 for entry in num_letters])
    ic /= text_lenght ** 2
    return ic

# Key lenght finder
def key_length_finder(cipher_text):

    # Creating sub collections
    sub_strings_dictionary = {}
    for i in range(1, max_key_lenght+1, 1):
        temp_list = []
        for j in range(0, i, 1):
            temp_list.append(cipher_text[j::i])
        sub_strings_dictionary[i] = temp_list

    # finding the highest coincidence
    ioc_dictionaray = {}
    for key, value in sub_strings_dictionary.items():
        temp_list = []
        for sub_string in value:
            temp_list.append(ic_calculator(sub_string))
        ioc_dictionaray[key] = temp_list

    # selecting the key length
    ave_ioc_dict = {}
    max_ioc = 0.0
    final_key_lenght = 0
    for key, value in ioc_dictionaray.items():
        ave_ioc_dict[key] = sum(value)/len(value)
        if float(ave_ioc_dict[key]) > max_ioc:
            max_ioc = ave_ioc_dict[key]
            final_key_lenght = key
    return final_key_lenght, sub_strings_dictionary[final_key_lenght], ioc_dictionaray


# Shift each character of a string
def shift_text(shift, text):
    return ''.join(chr(((ord(char) - 65 + shift) % 26) + 65) for char in text)


# Histogram matching
def mg_sum(shifted_text):
    num_letters = [0] * 26
    for char in shifted_text:
        num_letters[ord(char) - 65] += 1
    text_length = len(shifted_text)
    sub_string_letter_fre = []
    for letter in num_letters:
        sub_string_letter_fre.append(letter/text_length)
    total_mg = 0
    for index, char in enumerate(sub_string_letter_fre):
        total_mg += sub_string_letter_fre[index] * english_frequences[index]
    return total_mg


# Key Cracker
def key_solver(sub_strings):
    key_shift = {}
    mg_dict = {}
    for index, string in enumerate(sub_strings):
        max_mg = 0
        temp_list = []
        for shift in range(1, 26, 1):
            shifted = shift_text(shift, string)
            mg = mg_sum(shifted)
            temp_list.append(round(mg,3))
            if mg > max_mg:
                max_mg = mg
                key_shift[index+1] = shift
        mg_dict[index+1] = temp_list
    deciphering_key = []
    enciphering_key = []
    for key, num in key_shift.items():
        deciphering_key.append(chr(num + 65))
        enciphering_key.append(chr(26 - num + 65))
    return deciphering_key, enciphering_key, key_shift, mg_dict


# Decryptor
def vigenere_decryptor(cipher_text, deciphering_key, key_length):
    plain_text = []
    for index, char in enumerate(cipher_text):
        ciper_char_code = ord(char) - 65
        key_char_code = ord(deciphering_key[index % key_length]) - 65
        decrypted_char_code = ((ciper_char_code + key_char_code) % 26) + 65
        decrypted_char = chr(decrypted_char_code)
        plain_text.append(decrypted_char)
    return plain_text

def plain_text_formatter(cipher_text, plain_text):
    formatted_plain_text = []
    plain_counter = 0
    for char in cipher_text:
        if char not in string.ascii_letters:
            formatted_plain_text.append(char)
        elif char in string.ascii_lowercase:
            formatted_plain_text.append(plain_text[plain_counter].lower())
            plain_counter += 1
        else:
            formatted_plain_text.append(plain_text[plain_counter].upper())
            plain_counter += 1

    return formatted_plain_text


# Main function
def main():
    # getting and setting the inputs
    global max_key_lenght
    max_key_lenght = int(input("Enter the maximum key length: "))
    cipher_text = input("Enter the cipher text: ")

    # function calls
    clean_cipher = string_cleaner(cipher_text)
    key_length, sub_strings, key_ioc_dictionary = key_length_finder(clean_cipher)
    deciphering_key, enciphering_key, key_shift, mg_dict = key_solver(sub_strings)
    plain_text = vigenere_decryptor(clean_cipher, deciphering_key, key_length)
    formatted_plain_text = plain_text_formatter(cipher_text, plain_text)

    # printing the resaults
    print("The Key length is", key_length)
    print("The Enciphering key is", enciphering_key)
    print("The Deciphering key is", deciphering_key)
    print("The Plain text is \n", ''.join(plain_text))
    print("The Formatted Plain text is \n", ''.join(formatted_plain_text))


    print("The Key IOC dictionary is \n", key_ioc_dictionary)
    for key, value in key_ioc_dictionary.items():
        print("For the key length " , key, " the average is:", (sum(value)/len(value)))

    print("The Tested Shifts are \n", mg_dict)
    print("The Key shifts are \n", key_shift)
    print("The valid sub strings are \n", sub_strings)


if __name__ == '__main__':
    main()
