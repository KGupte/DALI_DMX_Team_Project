def manchester_encode(data_byte):
    """
    @brief Encode a single byte using Manchester encoding.
    @param data_byte The byte to be encoded.
    @return A string representing the Manchester encoded byte.
    """
    manchester_encoded = []
    for bit in range(8):
        if (data_byte >> (7 - bit)) & 1:
            manchester_encoded.append('10')
        else:
            manchester_encoded.append('01')
    return ''.join(manchester_encoded)
